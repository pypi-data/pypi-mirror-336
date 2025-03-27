import enum
import http
import logging
from typing import Any
import re
from dataclasses import dataclass
from functools import cache

import numpy as np
import pydicom
import xnat

from pydicom import Dataset
from pydicom.multival import MultiValue
from pydicom.pixel_data_handlers import util
from rich.text import Text
from textual import work
from textual.binding import Binding
from textual.message import Message
from textual.widgets import Tree, Label
from textual.widgets.tree import TreeNode
from textual_file_viewer.dicom_tree import DicomTree
from textual_file_viewer.image_viewer import ImageViewer
from xnat.core import XNATListing
from xnat.exceptions import XNATResponseError
from xnat.mixin import ImageScanData, ProjectData, SubjectData, ImageSessionData
from xnat.prearchive import PrearchiveScan, PrearchiveSession

from xnat_browser.app_base import Loading

MAX_NAME_LENGTH = 25


# XNAT does not have a PrearchiveSubject, so define it here.
@dataclass
class PrearchiveSubject:
    # Used as a placeholder incase the subject does not (yet) exist.
    name: str


class Views(enum.Enum):
    XNAT_INFO = enum.auto()
    DICOM_INFO = enum.auto()
    DICOM_IMAGE = enum.auto()


@dataclass
class Outputs:
    xnat: Label
    dicom: DicomTree
    image: ImageViewer

    def clear(self) -> None:
        self.xnat.update('')
        self.dicom.update('')
        self.image.clear()


def enum_value_asdict_factory(data: list[tuple[str, Any]]) -> dict[Any, Any]:
    def convert_value(obj: Any) -> Any:
        if isinstance(obj, enum.Enum):
            return obj.value
        return obj

    return dict((k, convert_value(v)) for k, v in data)


def get_window_center_width(data: Dataset) -> tuple[int, int]:
    center, width = data.WindowCenter, data.WindowWidth

    if isinstance(center, MultiValue):
        center = center[0]

    if isinstance(width, MultiValue):
        width = width[0]

    return center, width


class XnatTree(Tree):
    class ViewChanged(Message):
        def __init__(self, view: Views):
            super().__init__()
            self.view = view

    BINDINGS = [
        Binding('left', 'goto_parent', 'Goto Parent', show=False),
    ]

    def __init__(self, outputs: Outputs, logger: logging.Logger, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.outputs = outputs
        self.logger = logger
        self.show_root = False
        self.session: xnat.XNATSession | None = None
        self._last_processed_dicom: TreeNode | None = None

    def set_session(self, session: xnat.XNATSession) -> None:
        raise NotImplementedError()

    @staticmethod
    def clear_cache() -> None:
        _get_dicom_from_xnat.cache_clear()

    def access_level(self) -> dict:
        # copied from https://gitlab.com/radiology/infrastructure/xnatpy/-/commit/d0e32c669a0cb2bda0f2c8b828d80470510f1c7b
        assert self.session
        data: list[dict[str, Any]] = self.session.get_json('/xapi/access/projects')
        result = {}
        for x in data:
            if 'ID' not in x or 'role' not in x:
                continue
            result[x['ID']] = x['role']
        return result

    def action_goto_parent(self) -> None:
        node = self.cursor_node
        if node is None or node.parent is None:
            return

        self.select_node(node.parent)
        self.scroll_to_node(node.parent)

    async def filter_projects(self, _: str) -> None:
        raise NotImplementedError()

    async def action_refresh(self) -> None:
        raise NotImplementedError()

    @work
    async def action_update_projects(self) -> None:
        raise NotImplementedError()

    def dicom_info(self) -> None:
        node = self.cursor_node
        if node is None or node == self._last_processed_dicom:
            return

        with Loading(self.outputs.xnat):
            self.logger.debug('DICOM action')
            self._last_processed_dicom = node
            if isinstance(node.data, (ImageScanData, PrearchiveScan)):
                self.load_dicom(index=len(node.data.files) // 2)

    @staticmethod
    def _process_node(node: TreeNode) -> None:
        match node.data:
            case ProjectData():
                if len(node.children) > 0:
                    return
                node.data.subjects.clearcache()
                _add(node, node.data.subjects, ' SUB')

            case SubjectData():
                if len(node.children) > 0:
                    return
                node.data.experiments.clearcache()
                _add(node, node.data.experiments, ' EXP')  # type: ignore

            case ImageSessionData():
                if len(node.children) > 0:
                    return
                scans = node.data.scans  # type: ignore
                scans.clearcache()
                node.set_label(Text(f'[{len(scans):>3} SCN] {label_from_node(node)}'))
                for scan in scans.values():  # type: ignore
                    node.add_leaf(Text.assemble((f'{scan.id:>7}', 'reverse'), f' {scan.type}'), scan)

            case PrearchiveSession():
                if len(node.children) > 0:
                    return
                if node.data.status != 'READY':
                    return
                scans = node.data.scans  # type: ignore
                node.set_label(Text(f'[{len(scans):>3} SCN] {label_from_node(node)}'))
                for scan in scans:  # type: ignore
                    label = scan.series_description if len(scan.series_description) > 0 else scan.id
                    node.add_leaf(label, scan)

            case PrearchiveSubject():
                # See if the subject already exists in this project. If so, add the SubjectData to the node
                assert node.parent
                project_data = node.parent.data
                assert isinstance(project_data, ProjectData)

                xnat_subject = _get_subject(project_data, label_from_node(node))
                if xnat_subject:
                    node.data = xnat_subject

    def load_dicom(self, index: int = 0) -> None:
        if not self._last_processed_dicom:
            return

        xnat_data = self._last_processed_dicom.data
        assert xnat_data
        index = max(0, min(index, len(xnat_data.files) - 1))

        try:
            dicom_data = _get_dicom_from_xnat(xnat_data, index)
            self.outputs.dicom.set_dataset(dicom_data)

            np_array = dicom_data.pixel_array

            match dicom_data.PhotometricInterpretation:
                case 'MONOCHROME1':
                    # minimum is white, maximum is black
                    # (https://dicom.innolitics.com/ciods/ct-image/image-pixel/00280004)
                    np_array = pydicom.pixel_data_handlers.apply_voi_lut(np_array, dicom_data)
                    minimum, maximum = np.amin(np_array), np.amax(np_array)
                    np_array = (maximum - np_array) * 255.0 / (maximum - minimum)
                case 'MONOCHROME2':
                    center, width = get_window_center_width(dicom_data)
                    minimum, maximum = center - width / 2, center + width / 2
                    np_array[np_array < minimum] = minimum
                    np_array[np_array > maximum] = maximum
                    np_array = (np_array - minimum) * 255.0 / (maximum - minimum)
                case 'YBR_FULL_422':
                    np_array = util.convert_color_space(np_array, 'YBR_FULL', 'RGB')
                case _:
                    pass

            try:
                text = [
                    str(dicom_data.PatientName),
                    str(dicom_data.PatientID),
                    str(dicom_data.PatientBirthDate),
                    str(dicom_data.StudyDescription),
                    str(dicom_data.SeriesDescription),
                ]
                self.outputs.image.text_top_left = '\n'.join(text)
            except (ValueError, AttributeError):
                pass

            try:
                text = [
                    str(dicom_data.InstitutionName),
                    str(dicom_data.ManufacturerModelName),
                    f'{dicom_data.StudyDate} {dicom_data.StudyTime}']
                self.outputs.image.text_top_right = '\n'.join(text)
            except (ValueError, AttributeError):
                pass

            try:
                text = [
                    f'ST: {dicom_data.SliceThickness} mm, SL: {dicom_data.SliceLocation:.3f}',
                    str(dicom_data.Modality),
                    f'Images: {dicom_data.InstanceNumber + 1} / {len(xnat_data.files)}',
                    f'Series: {dicom_data.SeriesNumber}',
                ]
                self.outputs.image.text_bottom_left = '\n'.join(text)
            except (ValueError, AttributeError):
                pass

            try:
                text = [f'{dicom_data.Rows} x {dicom_data.Columns}',
                        f'{dicom_data.PixelSpacing[0]:.3f} mm x {dicom_data.PixelSpacing[1]:.3f} mm',]
                self.outputs.image.text_bottom_right = '\n'.join(text)
            except (ValueError, AttributeError):
                pass

            self.outputs.image.set_array(np_array)
        except XNATResponseError as e:
            match _get_http_status_code(e):
                case http.HTTPStatus.FORBIDDEN:
                    self.logger.error("you don't have permission to access this resource.")
                case _:
                    self.logger.error(f'Error downloading dicom file. {e}')
        except (TypeError, ValueError, AttributeError) as e:
            self.logger.error(f'Error {e}')

    def route(self, node: TreeNode | None) -> list[str]:
        output = []
        while node is not None and node is not self.root:
            output.append(label_from_node(node))
            node = node.parent
        return list(reversed(output))


@cache
def _get_dicom_from_xnat(xnat_data: PrearchiveSession | ImageSessionData, index: int) -> pydicom.Dataset:
    with xnat_data.files[index].open() as dicom_fh:
        return pydicom.dcmread(dicom_fh, stop_before_pixels=False, force=False)


def _get_subject(project: ProjectData, name: str) -> SubjectData | None:
    subjects: list[SubjectData] = list(filter(lambda x: label_from_node(x) == name, project.subjects.values()))
    return subjects[0] if len(subjects) > 0 else None


def label_from_node(node: TreeNode) -> str:
    label_re = r'.*\] (?P<label>.*)$'

    label = str(node.label)
    m = re.search(label_re, label)
    if m:
        return m.group('label')
    return label


def _add(node: TreeNode, data: XNATListing, suffix: str = "") -> None:
    label_re = r'.*\] (?P<label>.*)$'

    label = label_from_node(node)
    m = re.search(label_re, str(label))
    if m:
        label = m.group('label')
    node.set_label(Text(f'[{len(data):>4}{suffix}] {label}'))

    for key in sorted(label_from_node(x) for x in data.values()):
        value = data[key]
        node.add(label_from_node(value), value)


def _get_http_status_code(e: Exception) -> int:
    match = re.search(r'status (?P<status_code>\d{3})', str(e), flags=re.S)
    if not match:
        return -1

    return int(match.group("status_code"))
