from abc import ABC
from typing import Any, Callable

import flet as ft

from remail.client.views.view_router import View
from remail.controllers.dtos import SettingsDTO
from remail.controllers.settings_controller import SettingsController


class SettingsSubView(View, ABC):
    def __init__(self, route: str):
        super().__init__(f"/settings/{route}")
        self.controller = SettingsController()
        self.settings: SettingsDTO|None = None
        self._settings_change_handler: list[Callable[[], None]] = []
        self._page_ref: ft.Page | None = None

    def on_subroute_change(self, subview: View | None) -> None:
        # Settings sub-views do not have nested routes.
        return None

    def set_page(self, page: ft.Page) -> None:
        self._page_ref = page

    def create_settings_depending(self, creator: Callable[[], ft.Control]) -> ft.Control:
        """Creates a Container that re-renders the element when settings changed"""
        control = ft.Container()
        def render():
            control.content = creator()
            try:
                control.update()
            except RuntimeError:
                pass
        self._settings_change_handler.append(render)
        render()
        return control

    def apply_settings(self, key:str, value:Any):
        # Save all notification settings to database
        setattr(self.settings, key, value)
        self.controller.update_settings(self.settings)

        if self._page_ref is None:
            raise RuntimeError("SettingsSubView requires a page reference before applying settings")

        # Show success message
        snack_bar = ft.SnackBar(
            content=ft.Text("Settings saved successfully"),
            bgcolor=ft.Colors.GREEN,
        )
        self._page_ref.overlay.append(snack_bar)
        snack_bar.open = True

        #update_listeners
        for l in self._settings_change_handler:
            l()

        self._page_ref.update()
