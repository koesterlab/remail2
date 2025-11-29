import flet as ft

from remail.client.state import AppState
from .state import MainAppState
from remail.client.widgets.mail_selection import SelectionBar
from .test_data_conversations import create_test_data


def create_main_view(page: ft.Page, state: AppState):
    state = MainAppState()
    state.set_displayed(create_test_data())
    selection_bar = SelectionBar(state)
    thread_view = ft.Container(bgcolor=ft.Colors.ORANGE, expand=True)
    container = ft.Row(expand=True, controls=[
        selection_bar, thread_view
    ])

    print(page)

    def resize(e):
        print(container.height)


    page.on_resized = resize
    return container
