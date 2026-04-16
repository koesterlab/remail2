import flet as ft

from remail.client.state import MainAppState, MainAppStateProperties
from remail.client.views.main import MainView
from remail.client.views.settings import SettingsView


class IndexView(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(
            content=None,
            **kwargs
        )

        state = MainAppState()
        state.set(MainAppStateProperties.DISPLAYED_MAILS, [])
        state.set(MainAppStateProperties.ACTIVE_CHATBOT, False)
        state.set(MainAppStateProperties.ACTIVE_THREAD, None)
        state.set(MainAppStateProperties.ACTIVE_CONVERSATION, None)
        state.set(MainAppStateProperties.ACTIVE_THREAD_CONVERSATION, None)
        state.set(MainAppStateProperties.SEARCH_TERM, "")
        state.set(MainAppStateProperties.ACTIVE_SETTINGS, None)

        def show_content(settings: bool) -> None:
            if settings:
                self.content = SettingsView(state)
            else:
                self.content = MainView(state)
            self.update()

        state.register_observer(MainAppStateProperties.ACTIVE_SETTINGS, lambda s: )