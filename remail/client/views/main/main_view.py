from dataclasses import dataclass
from typing import List

import flet as ft

from remail.client.state import AppState
from .state import MainAppState
from remail.client.widgets.mail_selection import SelectionBar
from remail.controllers.dtos.conversations import ConversationDTO, ThreadPreviewDTO
from remail.enums.email_folders import EmailFolders
from .test_data_conversations import create_test_data


def create_main_view(page: ft.Page, state: AppState):
    state = MainAppState()
    state.set_displayed(create_test_data())
    selection_bar = SelectionBar(state)
    container = ft.Row(expand=True, controls=[
        selection_bar, ft.Container(bgcolor=ft.Colors.ORANGE)
    ])

    return container
