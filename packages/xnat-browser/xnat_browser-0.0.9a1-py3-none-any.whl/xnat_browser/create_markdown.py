import enum
from collections.abc import Callable
from datetime import timedelta, datetime
from typing import Any

import humanize
from rich.console import RenderableType
from rich.markdown import Markdown
from xnat.core import XNATBaseObject, CustomVariableMap, CustomVariableGroup, CustomVariableDef
from xnat.exceptions import XNATResponseError
from xnat.mixin import ProjectData, ImageScanData, SubjectData, ImageSessionData
from xnat.prearchive import PrearchiveSession, PrearchiveScan


class XnatDataType(str, enum.Enum):
    PRE_ARCHIVE_SCAN = 'pre-archive scan'
    PRE_ARCHIVE_SESSION = 'pre-archive session'
    PROJECT_DATA = 'project'
    SUBJECT_DATA = 'subject'
    IMAGE_SESSION_DATA = 'image session'
    IMAGE_SCAN_DATA = 'image scan'
    UNKNOWN = 'unknown'


class Modality(str, enum.Enum):
    CT = 'CT (Computed Tomography)'
    CR = 'CR (Computed Radiography)'
    MR = 'MR (Magnetic Resonance)'
    NM = 'NM (Nuclear Medicine)'
    US = 'US (Ultrasound)'
    XA = 'XA (X-Ray Angiography)'
    PX = 'PX (Panoramic X-Ray)'
    UNKNOWN = 'Unknown'


XSI_TYPE_MODALITY_LUT = {
    'xnat:ctScanData': Modality.CT,
    'xnat:crScanData': Modality.CR,
    'xnat:mrScanData': Modality.MR,
    'xnat:nmScanData': Modality.NM,
    'xnat:xaScanData': Modality.XA,
}


# pylint: disable=too-many-return-statements
def get_xnat_data_type(data: Any) -> XnatDataType:
    if not isinstance(data, XNATBaseObject):
        return XnatDataType.UNKNOWN

    match data:
        case PrearchiveScan():
            return XnatDataType.PRE_ARCHIVE_SCAN
        case PrearchiveSession():
            return XnatDataType.PRE_ARCHIVE_SESSION
        case ProjectData():
            return XnatDataType.PROJECT_DATA
        case SubjectData():
            return XnatDataType.SUBJECT_DATA
        case ImageSessionData():
            return XnatDataType.IMAGE_SESSION_DATA
        case ImageScanData():
            return XnatDataType.IMAGE_SCAN_DATA

    return XnatDataType.UNKNOWN
# pylint: enable=too-many-return-statements


# noinspection PyTypeChecker
def create_markdown(data: XNATBaseObject) -> RenderableType:
    _map: dict[XnatDataType, Callable[[XNATBaseObject], RenderableType]] = {
        XnatDataType.PRE_ARCHIVE_SCAN: _prearchive_scan,
        XnatDataType.PRE_ARCHIVE_SESSION: _prearchive_session,
        XnatDataType.PROJECT_DATA: _project,
        XnatDataType.SUBJECT_DATA: _subjectdata,
        XnatDataType.IMAGE_SESSION_DATA: _image_session,
        XnatDataType.IMAGE_SCAN_DATA: _scandata,
        XnatDataType.UNKNOWN: lambda x: ''
    }

    return _map[get_xnat_data_type(data)](data)


def _prearchive_scan(data: PrearchiveScan) -> RenderableType:
    try:
        num_files = str(len(data.files))
    except XNATResponseError:
        num_files = '🤷'

    markdown = [
        '# Pre-archive scan info.',
        '|Key|Value|',
        '|---|---|',
        f'|ID|{data.id}|',
        f'|Series Description|{data.series_description}|',
        f'|Number of files|{num_files}|',
    ]

    return Markdown('\n'.join(markdown))


def _prearchive_session(data: PrearchiveSession) -> RenderableType:
    markdown = [
        '# Pre-archive session info.',
        '|Key|Value|',
        '|---|---|',
        f'|Label|{data.label}|'
    ]

    if data.uploaded:
        markdown.append(f'|Uploaded|{data.uploaded:%Y-%m-%d %H:%M:%S}, {humanize.naturaltime(data.uploaded)}|')
    if data.lastmod:
        markdown.append(f'|Last modified|{data.lastmod:%Y-%m-%d %H:%M:%S}, '
                        f'{humanize.naturaltime(data.lastmod)}|')
    if data.scan_date and data.scan_time:
        scan_date = datetime.combine(data.scan_date, data.scan_time)
        markdown.append(f'|Scan date|{scan_date:%Y-%m-%d %H:%M:%S}, '
                        f'{humanize.naturaltime(scan_date)}|')

    try:
        modality = Modality.UNKNOWN
        if len(data.scans) > 0:
            modality = XSI_TYPE_MODALITY_LUT.get(data.scans[0].data['xsiType'], Modality.UNKNOWN)
        markdown.append(f'|Modality|{modality.value}|')
    except XNATResponseError:
        pass

    markdown.append(f'|Status|{data.status}|')

    return Markdown('\n'.join(markdown))


def _project(data: ProjectData) -> RenderableType:
    markdown = [
        '# Project info.',
        '_General_\n',
        '|||',
        '|---|---|',
    ]

    class PrearchiveCode(enum.IntEnum):
        PREARCHIVE = 0
        AUTO_ARCHIVED = 4
        AUTO_ARCHIVED_OVERWRITE = 5

    if data.description:  # type: ignore
        markdown.append(f'|Description|{data.description}|')  # type: ignore

    markdown.append(f'|Name|{data.name}|')  # type: ignore

    markdown.append(f'|ID|{data.id}|')
    markdown.append(f'|Secondary ID|{data.secondary_id}|')  # type: ignore

    if data.keywords:  # type: ignore
        keywords = [f'{x}' for x in data.keywords.split()]  # type: ignore
        markdown.append(f'|Keywords|{", ".join(keywords)}|')

    prearchive_code = PrearchiveCode(data.xnat_session.get_json(f'/data/projects/{data.id}/prearchive_code'))
    markdown.append(f'|Prearchive|{prearchive_code.name.lower().replace("_", " ")}|')

    try:
        markdown.extend(['\n_Primary Investigator_\n', '|||', '|---|---|', ])
        markdown.append(f'|First name|{data.pi.firstname}|')  # type: ignore
        markdown.append(f'|Last name|{data.pi.lastname}|')  # type: ignore
        markdown.append(f'|E-mail|{data.pi.email}|')  # type: ignore
        markdown.append(f'|Institution|{data.pi.institution}|')  # type: ignore
    except TypeError:
        pass

    try:
        markdown.extend(['\n_Users_\n', '|Name|Role|', '|---|---|', ])
        for _, user in sorted(data.users.data.items(), key=lambda x: x[1].access_level, reverse=True):
            markdown.append(f'|{user.first_name} {user.last_name}|{user.access_level}|')
    except TypeError:
        pass

    return Markdown('\n'.join(markdown))


def _subjectdata(data: SubjectData) -> RenderableType:
    markdown = [
        '# Subject info.',
        '|||',
        '|---|---|',
        f'|Group|{data.group}|',  # type: ignore
        f'|Label|{data.label}|',
        f'|Project|{data.project}|',  # type: ignore
        f'|ID|{data.id}|',
        f'|Shared|{"✔️" if len(data.sharing) > 0 else "❌"}|'  # type: ignore
    ]

    return Markdown('\n'.join(markdown))


def _image_session(image_session: ImageSessionData) -> RenderableType:
    ignore_list = ['ID', 'id', 'prearchivePath', 'study_id', 'subject_ID', 'UID', 'time']
    relabel = {
        'dcmAccessionNumber': 'Accession Number',
        'dcmPatientBirthDate': 'Birth Date',
        'dcmPatientId': 'Patient ID',
        'dcmPatientName': 'Patient Name',
        'dcmPatientWeight': 'Patient Weight',
        'date': 'Acquisition date',
        'scanner/manufacturer': 'Manufacturer',
        'scanner/model': 'Model',
        'session_type': 'Session Description'
    }

    new_data = {}
    for key, value in image_session.data.items():
        if key in ignore_list:
            continue

        key = relabel.get(key, key).capitalize().replace('_', ' ')
        new_data[key] = value

    try:
        age: timedelta = image_session.date - image_session.dcm_patient_birth_date  # type: ignore
        new_data['Age'] = humanize.naturaldelta(age)
    except TypeError:
        new_data['Age'] = 'Unknown'

    markdown = ['# Session info.',
                '|||',
                '|---|---|']
    for key, value in sorted(new_data.items()):
        if key in ignore_list:
            continue

        if isinstance(value, (str, list)) and len(value) == 0:
            continue

        key = relabel.get(key, key)
        markdown.append(f'|{key}|{value}|')

    custom_variable_group: CustomVariableGroup
    custom_variables: CustomVariableMap = image_session.custom_variables
    if len(custom_variables) > 0:
        for name, custom_variable_group in custom_variables.definitions.items():
            markdown.extend([f'# Custom variable "{name}".', '|||', '|---|---|'])
            custom_variable: CustomVariableDef
            for key, custom_variable in custom_variable_group.items():
                markdown.append(f'|{key}|{custom_variable}|')

    return Markdown('\n'.join(markdown))


def _scandata(data: ImageScanData) -> RenderableType:
    markdown = ['# Scan info.']

    markdown.extend(['|||', '|---|---|'])
    for key, value in sorted(data.data.items()):
        markdown.append(f'|{key}|{value}|')

    markdown.append(f'|Number of files|{len(data.files)}|')
    return Markdown('\n'.join(markdown))
