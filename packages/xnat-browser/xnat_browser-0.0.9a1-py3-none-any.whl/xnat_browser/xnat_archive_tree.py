import logging
import math
from typing import Any, cast, Final

import xnat
import xnat.core
from rich.text import Text
from textual import work, on
from textual.widgets import Tree
from textual.worker import WorkerCancelled
from xnat.mixin import ProjectData, ImageSessionData, SubjectData, ImageScanData

from xnat_browser.app_base import Loading
from xnat_browser.create_markdown import create_markdown, get_xnat_data_type
from xnat_browser.screens.archive_action_screen import ArchiveActionsScreen, ArchiveActionResult
from xnat_browser.screens.confirmation_screen import ConfirmationScreen, ConfirmationResult
from xnat_browser.xnat_tree import XnatTree, MAX_NAME_LENGTH, Outputs, Views, label_from_node

ARCHIVE_NODE_ID: Final[str] = 'archive'


class XnatArchiveTree(XnatTree):  # pylint: disable=too-many-ancestors
    BINDINGS = [
        ('a', 'actions', 'Actions'),
    ]

    def __init__(self, outputs: Outputs, logger: logging.Logger, **kwargs: Any) -> None:
        super().__init__(label='xnat_archive_tree', outputs=outputs, logger=logger, **kwargs)
        self.outputs = outputs
        self.logger = logger
        self.show_root = False
        self.session: xnat.XNATSession | None = None

    def set_session(self, session: xnat.XNATSession) -> None:
        self.logger.debug('Updating archive tree')
        self.session = session
        with Loading(self):
            # noinspection PyArgumentList
            self._add_projects()
        self.root.expand()

    @work(thread=True)
    def _add_projects(self) -> None:
        assert self.session
        self.logger.debug('Adding archive projects')

        allowed_projects = self.access_level().keys()

        # sort the projects using case-insensitive sorting.
        for project in sorted(self.session.projects.values(), key=lambda x: x.name.casefold()):  # type: ignore
            if project.id not in allowed_projects:
                continue

            name = project.name
            if len(name) > MAX_NAME_LENGTH:
                name = name[:MAX_NAME_LENGTH - 3] + '...'
            self.root.add(name, project)
        self.root.expand()
        self.root.set_label(Text(f'[{len(self.root.children):>2}] Archive'))

    async def action_refresh(self) -> None:
        assert self.session

        with Loading(self):
            self.session.clearcache()  # Clear XNAT cache

            route = self.route(self.cursor_node)

            node = self.cursor_node
            if node is not None and node.data is not None and isinstance(node.data, xnat.core.XNATBaseListing):
                node.data.clearcache()

            if node is None or node == self.root:
                self.root.remove_children()
                self.logger.debug('Refreshing archive root')
                # noinspection PyArgumentList
                self._add_projects()
                return

            self.logger.debug(f'Refreshing {get_xnat_data_type(node.data).value} "{label_from_node(node)}"')
            node.remove_children()
            self._process_node(node)

            active_node = self.root
            for value in route:
                for child in active_node.children:
                    if label_from_node(child) != value:
                        continue
                    child.expand()
                    active_node = child
                    break

            self.select_node(active_node)
            self.scroll_to_node(active_node)

            return

    @work
    async def action_update_projects(self) -> None:
        with Loading(self):
            self.logger.debug('Updating projects')
            proj_dict = {}

            # make a copy of the children because the iterator becomes invalid on node removal.
            for project_node in list(self.root.children):
                num_subjects = len(cast(ProjectData, project_node.data).subjects)
                if num_subjects == 0:
                    project_node.remove()
                    continue
                proj_dict[project_node] = num_subjects

            max_subjects = max(proj_dict.values())
            num_digits = int(math.log10(max_subjects)) + 1

            for project_node, num_subjects in proj_dict.items():
                project_node.set_label(
                    Text(f'[{num_subjects:>{num_digits}} SUB] {cast(ProjectData, project_node.data).project}'))

            self.root.set_label(Text(f'[{len(self.root.children):>2}] Archive'))

    @work
    async def action_actions(self) -> None:
        if (not self.cursor_node or not self.cursor_node.data or
                not isinstance(self.cursor_node.data, (ImageSessionData, SubjectData, ImageScanData))):
            return

        session: ImageSessionData | SubjectData | ImageScanData = self.cursor_node.data

        result = await self.app.push_screen_wait(ArchiveActionsScreen())
        match result:
            case ArchiveActionResult.DELETE:
                delete_result = await self.app.push_screen_wait(
                    ConfirmationScreen(f'Are you sure you want to delete "{session.id}"'))
                if delete_result == ConfirmationResult.YES:
                    session_id = session.id  # store it, because the session is not valid after removing it.
                    session.delete(remove_files=True)
                    self.cursor_node.data.clearcache()
                    self.notify(f'Deleted {session_id}')
                    await self.action_refresh()

            case ArchiveActionResult.SHARE:
                self.notify('Not implemented yet.')

            case ArchiveActionResult.ABORT:
                self.notify('Aborted action.')

    @on(Tree.NodeExpanded)
    @on(Tree.NodeHighlighted)
    async def update_output_pane(self, event: Tree.NodeExpanded | Tree.NodeHighlighted) -> None:
        self.post_message(XnatTree.ViewChanged(Views.XNAT_INFO))

        self.outputs.clear()

        if event.node is None:
            return

        with Loading(self):
            self.outputs.xnat.update(create_markdown(event.node.data))
            self._process_node(event.node)
            try:
                await self.workers.wait_for_complete()
            except WorkerCancelled as e:
                self.logger.debug(e)

    async def filter_projects(self, value: str) -> None:
        self.root.remove_children()

        for project in sorted(self.session.projects.values(), key=lambda x: x.name.casefold()):  # type: ignore
            if not str(project.name).casefold().startswith(value.casefold()):
                continue
            self.root.add(project.name, project)

        self.root.expand()
        self.root.set_label(Text(f'[{len(self.root.children):>2}] Archive'))
