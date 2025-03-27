import datetime
import logging
from collections import defaultdict
from dataclasses import asdict
from typing import Any

import humanize
import xnat
from rich.text import Text
from textual import work, on
from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from textual.worker import WorkerCancelled
from xnat.session import XNATSession
from xnat.exceptions import XNATResponseError
from xnat.mixin import ProjectData
from xnat.prearchive import PrearchiveSession, Prearchive

from xnat_browser.app_base import Loading
from xnat_browser.create_markdown import create_markdown
from xnat_browser.screens.prearchive_actions_screen import PrearchiveActionsScreen, PrearchiveActionResult
from xnat_browser.screens.archive_screen import ArchiveScreen
from xnat_browser.screens.confirmation_screen import ConfirmationScreen, ConfirmationResult
from xnat_browser.xnat_tree import XnatTree, Outputs, Views, PrearchiveSubject, label_from_node, enum_value_asdict_factory


def _get_subject(session: PrearchiveSession) -> str:
    subject: str = session.subject
    if len(subject) == 0:
        subject = session.label
    return subject


class DisableCaching:
    def __init__(self, session: XNATSession | Prearchive) -> None:
        self._session = session
        self._old_caching = True

    def __enter__(self) -> None:
        self._old_caching = self._session.caching
        self._session.caching = False

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._session.caching = self._old_caching


class XnatPrearchiveTree(XnatTree):  # pylint: disable=too-many-ancestors
    BINDINGS = [
        ('a', 'actions', 'Actions'),
    ]

    def __init__(self, outputs: Outputs, logger: logging.Logger, **kwargs: Any) -> None:
        super().__init__(label='xnat_prearchive_tree', outputs=outputs, logger=logger, **kwargs)
        self.logger = logger
        self.show_root = False
        self.session: xnat.XNATSession | None = None

    def set_session(self, session: xnat.XNATSession) -> None:
        self.logger.debug('Updating pre-archive tree')
        self.session = session
        with Loading(self):
            # noinspection PyArgumentList
            self._add_pre_archive_projects()
        self.root.expand()

    def _get_project(self, name: str) -> ProjectData:
        assert self.session
        project_data: list[ProjectData] = list(filter(lambda x: x.name == name, self.session.projects.values()))
        assert len(project_data) == 1
        return project_data[0]

    # @work(thread=True)
    def _add_pre_archive_projects(self) -> None:
        assert self.session
        self.logger.debug('Adding pre-archive projects')

        nodes = self._create_project_subject_nodes()

        with DisableCaching(self.session.prearchive):
            # Add the pre-archive sessions to the corresponding project/subject
            sessions = sorted(self.session.prearchive.sessions(), key=lambda x: x.name)
            for session in sessions:
                try:
                    if session.status != 'READY':
                        # Add a leaf (node without children)
                        nodes[(session.project, session.status)].add_leaf(session.name, session)
                        continue
                    nodes[(session.project, _get_subject(session))].add(session.label, session)

                except KeyError as e:
                    self.logger.error(f'Error adding {session.name}: {e}')

    def _create_project_subject_nodes(self) -> dict[tuple[str, str], TreeNode]:
        assert self.session

        with DisableCaching(self.session.prearchive):
            # First create the project and subject nodes.
            project_subjects: defaultdict[str, set] = defaultdict(set)
            for session in self.session.prearchive.sessions():
                if session.status != 'READY':
                    project_subjects[session.project].add(session.status)
                    continue

                project_subjects[session.project].add(_get_subject(session))

            project_nodes: dict[str, TreeNode] = {}
            nodes: dict[tuple[str, str], TreeNode] = {}
            for project, subjects in sorted(project_subjects.items()):
                project_node = project_nodes.get(project, None)
                if project_node is None:
                    project_node = self.root.add(project, self._get_project(project))
                    project_nodes[project] = project_node
                for subject in sorted(subjects):
                    nodes[(project, subject)] = project_node.add(subject, PrearchiveSubject(subject))

            self.root.expand()
            self.root.set_label(Text(f'[{len(project_nodes):>2}] Pre-archive'))

            return nodes

    @on(Tree.NodeExpanded)
    @on(Tree.NodeHighlighted)
    async def update_output_pane(self, event: Tree.NodeExpanded | Tree.NodeHighlighted) -> None:
        self.post_message(XnatTree.ViewChanged(Views.XNAT_INFO))

        self.outputs.clear()

        if event.node is None:
            return

        with Loading(self):
            if isinstance(event.node.data, (PrearchiveSession | PrearchiveSubject)):
                try:
                    self._process_node(event.node)
                    await self.workers.wait_for_complete()
                except XNATResponseError as e:
                    self.logger.error(e)
                except WorkerCancelled as e:
                    self.logger.debug(e)

            self.outputs.xnat.update(create_markdown(event.node.data))

    @work
    async def action_actions(self) -> None:
        if not self.cursor_node or not self.cursor_node.data or not isinstance(self.cursor_node.data, PrearchiveSession):
            return

        session = self.cursor_node.data
        result = await self.app.push_screen_wait(PrearchiveActionsScreen())
        match result:
            case PrearchiveActionResult.REBUILD:
                rebuild_result = await self.app.push_screen_wait(
                    ConfirmationScreen(f'Are you sure you want to rebuild "{session.label}"'))
                if rebuild_result != ConfirmationResult.YES:
                    return
                try:
                    session.rebuild(asynchronous=False)
                    self.notify(f'Rebuild {session.label}')
                except XNATResponseError as e:
                    self.logger.error(e)
                await self.action_refresh()

            case PrearchiveActionResult.DELETE:
                delete_result = await self.app.push_screen_wait(
                    ConfirmationScreen(f'Are you sure you want to delete "{session.label}"'))
                if delete_result != ConfirmationResult.YES:
                    return
                try:
                    session.delete(asynchronous=False)
                    self.notify(f'Deleted {session.label}')
                except XNATResponseError as e:
                    self.logger.error(e)
                await self.action_refresh()

            case PrearchiveActionResult.ARCHIVE:
                archive_result = await self.app.push_screen_wait(
                    ArchiveScreen(project=session.project, subject=session.subject, experiment=session.label)
                )
                if archive_result is None:
                    return

                # noinspection PyTypeChecker
                data = asdict(archive_result, dict_factory=enum_value_asdict_factory)
                self.logger.debug(f'Archiving: {data}')
                start = datetime.datetime.now()
                try:
                    session.archive(**data)
                    stop = datetime.datetime.now()
                    interval = humanize.precisedelta(stop - start, minimum_unit='seconds', format='%.0f')
                    self.logger.info(f'Archived {archive_result.experiment} in {interval}')
                except XNATResponseError as e:
                    self.logger.error(e)

                await self.action_refresh()

            case PrearchiveActionResult.MOVE:
                self.notify('Not implemented yet.')

            case PrearchiveActionResult.ABORT:
                self.notify('Aborted action.')

    async def action_refresh(self) -> None:
        assert self.session

        self.logger.info('Refreshing pre-archive.')

        with Loading(self):
            route = self.route(self.cursor_node)

            self.session.clearcache()  # Clear XNAT cache
            self.root.remove_children()
            self._add_pre_archive_projects()

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

    async def filter_projects(self, _: str) -> None:
        return None

    @work
    async def action_update_projects(self) -> None:
        return None
