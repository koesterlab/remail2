from asyncio import Future
from collections.abc import Callable
from enum import Enum
from typing import Union

from flet.core.page import Page

from remail.client.state.observable_state import ObservableState
from remail.client.views.view_router import ViewRouter
from remail.controllers.account_controller import AccountController
from remail.controllers.account_controller import AccountController
from remail.controllers.dtos.conversations import ConversationDTO, ThreadPreviewDTO
from remail.controllers.dtos.user_dto import UserDTO
from remail.controllers.thread_controller import ThreadController
from remail.enums import MainView, SettingsSubView


class MainAppStateProperties(Enum):
    DRAFT = "draft"
    ACTIVE_USER = "active_user"
    ACTIVE_THREAD = "active_thread"
    ACTIVE_CONVERSATION = "active_conversation"
    ACTIVE_CHATBOT = "active_chatbot"
    SEARCH_TERM = "search_term"
    DISPLAYED_MAILS = "displayed_mails"


class MainAppState(ObservableState[MainAppStateProperties]):
    def __init__(self):
        super().__init__()
        self.__selected: list[ConversationDTO | ThreadPreviewDTO] = []
        self.__selection_listeners: dict[
            ConversationDTO | ThreadPreviewDTO | None, Callable[[bool], None]
        ] = {}

        self.thread_controller = ThreadController()
        self.account_controllers: dict[str, AccountController] = {}
        self.sync_threads: list[Future] = []

    def get_active_email_account(self) -> AccountController:
        mail: UserDTO | None = self.get(MainAppStateProperties.ACTIVE_USER)
        if mail is None:
            raise Exception("Account Controller was requested without active email account")
        controller = self.account_controllers.get(mail.email)
        if controller is None:
            raise Exception("Account Controller was requested but not found for mail " + mail.email)
        return controller
        self.account_controllers: dict[str, AccountController] = {}
        self.sync_threads: list[Future] = []

    def set_router(self, router: ViewRouter, page: Page):
        self._router = router
        self._page = page

    def go_to_settings(self, view:SettingsSubView):
        if self._page and self._router:
            self._page.clean()
            settings_view = self._router.load_view(MainView.SETTINGS)
            self._page.add(settings_view)
            self._page.update()

    def get_active_email_account(self) -> AccountController:
        mail: UserDTO | None = self.get(MainAppStateProperties.ACTIVE_USER)
        if mail is None:
            raise Exception("Account Controller was requested without active email account")
        controller = self.account_controllers.get(mail.email)
        if controller is None:
            raise Exception("Account Controller was requested but not found for mail " + mail.email)
        return controller

    def toggle_selection(self, item: Union["ConversationDTO", "ThreadPreviewDTO"]) -> None:
        already_selected = item in self.__selected
        if already_selected:
            self.__selected.remove(item)
        else:
            self.__selected.append(item)

        if item in self.__selection_listeners:
            self.__selection_listeners[item](not already_selected)
        if None in self.__selection_listeners:
            self.__selection_listeners[None](False)

    def listen_selection(
        self,
        item: Union["ConversationDTO", "ThreadPreviewDTO", None],
        callback: Callable[[bool], None],
    ) -> None:
        self.__selection_listeners[item] = callback

    def get_selected(self):
        return self.__selected

    def clear_selected(self):
        selected = self.__selected
        self.__selected = []
        for s in selected:
            if s in self.__selection_listeners:
                self.__selection_listeners[s](False)

        if None in self.__selection_listeners:
            self.__selection_listeners[None](False)
