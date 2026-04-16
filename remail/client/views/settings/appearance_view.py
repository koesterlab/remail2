"""Appearance settings view."""
from abc import ABC

import flet as ft

from remail.client.state.app_state import AppState
from remail.client.views.settings.settings_sub_view import SettingsSubView
from remail.controllers import SettingsController
from remail.enums import FontFamily, FontSize, ThemeMode


class AppearanceView(SettingsSubView, ABC):
    def __init__(self, app_state: AppState | None = None):
        super().__init__(route="appearance")
        self.app_state = app_state or AppState()

    def _apply_theme_mode(self, value: str) -> None:
        theme_mode = ThemeMode(value)
        self.app_state.theme_mode = theme_mode
        if self._page_ref is not None:
            self._page_ref.theme_mode = theme_mode
        self.apply_settings("theme_mode", theme_mode)

    def _apply_font_size(self, value: str) -> None:
        font_size = FontSize(value)
        self.app_state.font_size = font_size
        self.apply_settings("font_size", font_size)

    def _apply_font_family(self, value: str) -> None:
        font_family = FontFamily(value)
        self.app_state.font_family = font_family
        self.apply_settings("font_family", font_family)

    def create_view(self) -> ft.Control:
        self.settings = self.controller.get_settings()
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Appearance", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Customize how the app looks and feels"),
                    ft.Divider(height=2, color=ft.Colors.BLACK),
                    ft.Text("Theme", weight=ft.FontWeight.BOLD),
                    self.create_settings_depending(
                        lambda: ft.RadioGroup(
                            content=ft.Row(
                                [
                                    ft.Radio(value=ThemeMode.LIGHT.value, label="Light"),
                                    ft.Radio(value=ThemeMode.DARK.value, label="Dark"),
                                    ft.Radio(value=ThemeMode.SYSTEM.value, label="System"),
                                ]
                            ),
                            value=self.settings.theme_mode.value,
                            on_change=lambda e: self._apply_theme_mode(e.control.value),
                        )
                    ),
                    ft.Text("Font size", weight=ft.FontWeight.BOLD),
                    self.create_settings_depending(
                        lambda: ft.Dropdown(
                            value=self.settings.font_size.value,
                            options=[ft.dropdown.Option(size.value) for size in FontSize],
                            width=200,
                            on_select=lambda e: self._apply_font_size(e.control.value),
                        )
                    ),
                    ft.Text("Font family", weight=ft.FontWeight.BOLD),
                    self.create_settings_depending(
                        lambda: ft.Dropdown(
                            value=self.settings.font_family.value,
                            options=[ft.dropdown.Option(family.value) for family in FontFamily],
                            width=200,
                            on_select=lambda e: self._apply_font_family(e.control.value),
                        )
                    ),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            border_radius=10,
            alignment=ft.Alignment.CENTER_LEFT,
            expand=True,
        )


def create_appearance_view(page: ft.Page, app_state: AppState) -> ft.Container:
    view = AppearanceView(app_state)
    view.set_page(page)
    return view.create_view()
