from dataclasses import dataclass
import flet as ft

from remail.client.state import AppState
from remail.client.widgets.mail_selection import SelectionBar


def create_main_view(page: ft.Page, state: AppState):
    selection_bar = SelectionBar()
    container = ft.Row(expand=True, controls=[
        selection_bar, ft.Container(bgcolor=ft.Colors.ORANGE)
    ])

    page.add(container)
