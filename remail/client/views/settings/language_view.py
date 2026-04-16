from abc import ABC

import flet as ft

from remail.client.state.app_state import AppState
from remail.client.views.settings.settings_sub_view import SettingsSubView
from remail.controllers import SettingsController
from remail.enums import Language, Timezone

class LanguageView(SettingsSubView, ABC):
    def __init__(self):
        super().__init__(route="language")

    def create_view(self) -> ft.Control:
        self.settings = self.controller.get_settings()
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Language & Region", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Choose your preferred language for the application"),
                    ft.Divider(height=2, color=ft.Colors.BLACK),
                    ft.Text("Application Language", weight=ft.FontWeight.BOLD),
                    self.create_settings_depending(lambda: ft.Dropdown(
                        value=self.settings.language.value,
                        options=[ft.dropdown.Option(lang.value) for lang in Language],
                        expand=True,
                        on_select=lambda e: self.apply_settings("language", Language(e.control.value)),
                    )),
                    ft.Text("Timezone", weight=ft.FontWeight.BOLD),
                    self.create_settings_depending(lambda: ft.Dropdown(
                        value=self.settings.timezone.value,
                        options=[ft.dropdown.Option(tz.value) for tz in Timezone],
                        expand=True,
                        on_select= lambda e: self.apply_settings("timezone", Timezone(e.control.value)),
                    )),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            border_radius=10,
            alignment=ft.Alignment.CENTER_LEFT,
            expand=True,
        )


def create_language_view(page: ft.Page, app_state: AppState) -> ft.Container:
    del app_state
    view = LanguageView()
    view.set_page(page)
    return view.create_view()
