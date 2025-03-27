import enum
import logging
import pydicom
from pydicom.errors import InvalidDicomError
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer, Horizontal, Vertical
from textual.css.query import NoMatches
from textual.widgets import Header, Footer, Label, Input, RichLog, TabbedContent, TabPane, Tree
from textual_file_viewer.dicom_tree import DicomTree
from textual_file_viewer.image_viewer import ImageViewer
from textual_slider import Slider
from xnat.mixin import ImageScanData
from xnat.prearchive import PrearchiveScan

from xnat_browser.app_base import XnatBase, Loading
from xnat_browser.xnat_archive_tree import XnatArchiveTree
from xnat_browser.xnat_prearchive_tree import XnatPrearchiveTree
from xnat_browser.xnat_tree import XnatTree, Outputs, Views


class ProcessState(str, enum.Enum):
    PROCESS_ACTIVE = '🔴'
    PROCESS_INACTIVE = '🟢'


class Processes(enum.Enum):
    FILE_INSTANCE_MAPPING = enum.auto()


class XnatBrowser(XnatBase):
    CSS_PATH = 'browser.tcss'
    BINDINGS = [
        Binding('u', 'update_projects', 'Update projects', show=False),
        Binding('f5', 'refresh', 'Refresh'),
        Binding('ctrl+f', 'filter_project', 'Filter Project'),
        Binding('ctrl-left', 'previous_slice', 'Previous Slice', show=False),
        Binding('ctrl-right', 'next_slice', 'Next Slice', show=False),

    ]

    def __init__(self, server: str, username: str | None = None, password: str | None = None,
                 log_level: int = logging.INFO) -> None:
        super().__init__(server, username, password, log_level)
        self._dicom_instance_file_map: dict[int, int] = {}  # Mapping from InstanceNumber to XNAT file index
        self._process_state: dict[Processes, ProcessState] = {Processes.FILE_INSTANCE_MAPPING: ProcessState.PROCESS_INACTIVE}

    def compose(self) -> ComposeResult:
        logger = self._setup_logging()
        outputs = Outputs(
            xnat=Label(id='xnat_info', expand=True),
            dicom=DicomTree(id='dicom_info', expand=True),
            image=ImageViewer(id='image_info'),
        )
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical():
                widget = Input(placeholder='Project', id='project_search', classes='remove')
                widget.border_title = 'Filter projects'
                yield widget
                with TabbedContent(id='source_tabbed_content') as tabbed_content:
                    tabbed_content.border_title = 'Source'
                    with TabPane('Archive'):
                        archive = XnatArchiveTree(outputs, self.logger, id='xnat_tree')
                        archive.border_title = 'Archive'
                        yield archive
                    with TabPane('Pre-Archive'):
                        prearchive = XnatPrearchiveTree(outputs, self.logger, id='xnat_tree_pre_archive')
                        prearchive.border_title = 'Pre-Archive'
                        yield prearchive
            with TabbedContent(id='info_tabbed_content', initial='xnat_info_tab') as tabbed_content:
                tabbed_content.border_title = 'Info'
                with TabPane('XNAT', id='xnat_info_tab'):
                    with ScrollableContainer(id='xnat_info_container'):
                        yield outputs.xnat
                with TabPane('DICOM', id='dicom_info_tab'):
                    with ScrollableContainer(id='dicom_info_container'):
                        # noinspection PyTypeChecker
                        yield outputs.dicom
                with TabPane('Image', id='image_tab'):
                    with Vertical():
                        with Horizontal(id='file_id_container', classes='remove'):
                            state = self._process_state[Processes.FILE_INSTANCE_MAPPING]
                            yield Label(f'{state} Inst.', id='file_id')
                            yield Slider(min=1, max=2, step=1, id='file_slider')
                        with ScrollableContainer(id='image_container'):
                            # noinspection PyTypeChecker
                            yield outputs.image
        yield logger
        yield Footer()

    def on_mount(self) -> None:
        for tree in self.query(XnatTree):  # pylint: disable=not-an-iterable
            tree.set_session(self.session)
        self.query_one('#rich_log', RichLog).border_title = 'Log'
        self.logger.debug('Welcome')
        self._get_active_source_tree().focus()

    @on(Input.Changed, '#project_search')
    async def project_search_changed(self, message: Input.Changed) -> None:
        for xnat_tree in self.query(XnatTree):  # pylint: disable=not-an-iterable
            await xnat_tree.filter_projects(str(message.value))

    def action_filter_project(self) -> None:
        widget = self.query_one('#project_search', Input)
        widget.focus()
        widget.toggle_class('remove')

    def _get_active_source_tree(self) -> XnatTree:
        pane = self.query_one('#source_tabbed_content', TabbedContent).active_pane
        assert pane
        return pane.query_one(XnatTree)

    async def action_update_projects(self) -> None:
        async with Loading(self._get_active_source_tree()):
            self._get_active_source_tree().action_update_projects()

    async def action_refresh(self) -> None:
        await self._get_active_source_tree().action_refresh()

    @on(TabbedContent.TabActivated)
    async def tab_changed(self, event: TabbedContent.TabActivated) -> None:
        if event.tabbed_content.active in ('dicom_info_tab', 'image_tab'):
            self._get_active_source_tree().dicom_info()

    @on(XnatTree.ViewChanged)
    async def view_changed(self, event: XnatTree.ViewChanged) -> None:
        try:
            tab = self.query_one('#info_tabbed_content', TabbedContent)
        except NoMatches as e:
            self.app.notify(str(e), title='Error', severity='error')
            return

        match event.view:
            case Views.XNAT_INFO:
                tab.active = 'xnat_info_tab'
            case Views.DICOM_INFO:
                tab.active = 'dicom_info_tab'
            case Views.DICOM_IMAGE:
                tab.active = 'image_tab'

    @work
    @on(Slider.Changed, '#file_slider')
    async def file_index_changed(self, _: Slider.Changed) -> None:
        self._update_instance_slider()
        slider = self.query_one('#file_slider', Slider)
        index = self._dicom_instance_file_map.get(slider.value - 1, slider.value - 1)

        with Loading(self.query_one('#image_container', ScrollableContainer)):
            self._get_active_source_tree().load_dicom(index)

    @work(thread=True)
    def file_instance_mapping(self, data: PrearchiveScan | ImageScanData) -> None:
        self._update_instance_slider(ProcessState.PROCESS_ACTIVE)

        self._dicom_instance_file_map = {}
        if isinstance(data, ImageScanData):
            for index, file in enumerate(data.files.values()):
                try:
                    with file.open() as dicom_fh:
                        dcm = pydicom.dcmread(dicom_fh, stop_before_pixels=True, force=False)
                    self._dicom_instance_file_map[int(dcm['InstanceNumber'].value)] = index
                except InvalidDicomError:
                    continue

        # if isinstance(data, PrearchiveScan):
        #     for index, file in enumerate(data.files):
        #         value = file.dicom_dump(fields=['InstanceNumber'])
        #         self._dicom_file_instance_map[index] = value['InstanceNumber']

        self._get_active_source_tree().clear_cache()

        slider = self.query_one('#file_slider', Slider)
        index = self._dicom_instance_file_map.get(slider.value - 1, slider.value - 1)

        self._get_active_source_tree().load_dicom(index)

        self.query_one('#file_id_container', Horizontal).disabled = False
        self._update_instance_slider(ProcessState.PROCESS_INACTIVE)

    def _update_instance_slider(self, state: ProcessState = ProcessState.PROCESS_INACTIVE) -> None:
        self._process_state[Processes.FILE_INSTANCE_MAPPING] = state
        slider = self.query_one('#file_slider', Slider)
        self.query_one('#file_id', Label).update(f'{state.value} Inst.\n{slider.value:3} / {slider.max:3}')

    @on(Tree.NodeHighlighted)
    async def node_changed(self, event: Tree.NodeHighlighted) -> None:
        if not isinstance(event.node.data, (PrearchiveScan | ImageScanData)):
            return

        # Get the mapping of InstanceNumber to file name/index
        self.file_instance_mapping(event.node.data)

        slider = self.query_exactly_one('#file_slider', Slider)
        slider.min = 1
        slider.max = len(event.node.data.files)
        slider.value = len(event.node.data.files) // 2

        container = self.query_one('#file_id_container', Horizontal)
        container.set_class(slider.max <= 1, 'remove')
        container.disabled = True

    def action_next_slice(self) -> None:
        slider = self.query_one('#file_slider', Slider)
        slider.value = slider.value + 1

    def action_previous_slice(self) -> None:
        slider = self.query_one('#file_slider', Slider)
        slider.value = slider.value - 1
