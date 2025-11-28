from remail.controllers.dtos.conversations import ConversationDTO, ThreadPreviewDTO
from remail.enums.email_folders import EmailFolders

#State mit Listener erstellen
#Base Layout erstellen
#mit searchbar zusammen machen
#searchbar reaktiv machen

import weakref
from typing import Callable, Dict, List, Union
from uuid import uuid4

class MainAppState:
    search_term: str | None
    displayed: ThreadPreviewDTO | None
    active_folder: "EmailFolders"

    def __init__(self):
        self.__selected: List[Union["ConversationDTO", "ThreadPreviewDTO"]] = []
        self.__selection_listeners: Dict[
            Union["ConversationDTO", "ThreadPreviewDTO"], Callable[[bool], None]
        ] = {}

        self.__search_term: str | None = None
        self.__search_term_listeners: Dict[str, Union[weakref.WeakMethod, Callable]] = {}

        self.__active_folder: EmailFolders | None = None
        self.__active_folder_listeners: Dict[str, Union[weakref.WeakMethod, Callable]] = {}

        self.__displayed: List["ConversationDTO"] = []
        self.__displayed_listeners: Dict[str, Union[weakref.WeakMethod, Callable]] = {}

        self.__active_thread: ThreadPreviewDTO | None = None
        self.__active_thread_listeners: Dict[str, Union[weakref.WeakMethod, Callable]] = {}

    # ---------------- Selection ----------------

    def toggle_selection(self, item: Union["ConversationDTO", "ThreadPreviewDTO"]):
        already_selected = item in self.__selected
        if already_selected:
            self.__selected.remove(item)
        else:
            self.__selected.append(item)

        if item in self.__selection_listeners:
            self.__selection_listeners[item](not already_selected)

    def listen_selection(
        self, item: Union["ConversationDTO", "ThreadPreviewDTO"], callback: Callable[[bool], None]
    ):
        self.__selection_listeners[item] = callback

    # ---------------- Search Term ----------------

    @property
    def search_term(self):
        return self.__search_term

    def set_search_term(self, term: str):
        if self.__search_term != term:
            self.__search_term = term
            self.__cleanup_weak_listeners(self.__search_term_listeners)
            for callback_ref in self.__search_term_listeners.values():
                callback = self.__unwrap_weak(callback_ref)
                if callback:
                    callback(term)

    def listen_search_term(self, callback: Callable[[str], None]) -> str:
        token = str(uuid4())
        self.__search_term_listeners[token] = self.__wrap_weak(callback)
        return token

    def remove_search_term_listener(self, token: str):
        self.__search_term_listeners.pop(token, None)

    # ---------------- Active Folder ----------------

    @property
    def active_folder(self):
        return self.__active_folder

    def set_active_folder(self, folder: "EmailFolders"):
        if self.__active_folder != folder:
            self.__active_folder = folder
            self.__cleanup_weak_listeners(self.__active_folder_listeners)
            for callback_ref in self.__active_folder_listeners.values():
                callback = self.__unwrap_weak(callback_ref)
                if callback:
                    callback(folder)

    def listen_active_folder(self, callback: Callable[["EmailFolders"], None]) -> str:
        token = str(uuid4())
        self.__active_folder_listeners[token] = self.__wrap_weak(callback)
        return token

    def remove_active_folder_listener(self, token: str):
        self.__active_folder_listeners.pop(token, None)

    # ---------------- Displayed Conversations ----------------

    @property
    def displayed(self) -> List["ConversationDTO"]:
        return self.__displayed

    def set_displayed(self, conversations: List["ConversationDTO"]):
        self.__displayed = conversations
        self.__cleanup_weak_listeners(self.__displayed_listeners)
        for callback_ref in self.__displayed_listeners.values():
            callback = self.__unwrap_weak(callback_ref)
            if callback:
                callback(conversations)

    def listen_displayed(self, callback: Callable[[List["ConversationDTO"]], None]) -> str:
        token = str(uuid4())
        self.__displayed_listeners[token] = self.__wrap_weak(callback)
        return token

    def remove_displayed_listener(self, token: str):
        self.__displayed_listeners.pop(token, None)

    # ---------------- Active Thread ----------------

    @property
    def active_thread(self) -> ThreadPreviewDTO | None:
        return self.__active_thread

    def set_active_thread(self, thread: ThreadPreviewDTO | None):
        self.__active_thread = thread
        self.__cleanup_weak_listeners(self.__active_thread_listeners)
        for callback_ref in self.__active_thread_listeners.values():
            callback = self.__unwrap_weak(callback_ref)
            if callback:
                callback(thread)

    def listen_active_thread(self, callback: Callable[[ThreadPreviewDTO | None], None]) -> str:
        token = str(uuid4())
        self.__active_thread_listeners[token] = self.__wrap_weak(callback)
        return token

    def remove_active_thread_listener(self, token: str):
        self.__active_thread_listeners.pop(token, None)

    # ---------------- Helpers ----------------

    def __wrap_weak(self, callback):
        """Wrapped method if bound, else return callable as-is"""
        try:
            # gebundene Methode
            return weakref.WeakMethod(callback)
        except TypeError:
            # normale Funktion
            return callback

    def __unwrap_weak(self, callback_ref):
        if isinstance(callback_ref, weakref.WeakMethod):
            return callback_ref()
        return callback_ref

    def __cleanup_weak_listeners(self, listeners_dict):
        """Remove dead weakrefs"""
        dead_tokens = [t for t, ref in listeners_dict.items() if self.__unwrap_weak(ref) is None]
        for t in dead_tokens:
            listeners_dict.pop(t)
