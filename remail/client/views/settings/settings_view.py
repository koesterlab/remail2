"""Settings view with navigation and sub-views."""
from abc import ABC

import flet as ft

from remail.client.views.view_router import View


class SettingsView(View):
    def __init__(self):
        super().__init__("/settings")
        self.sub_view = ft.Container()

    def create_view(self) -> ft.Control:
        self.page.title = "Settings"

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Back to Dashboard",
            on_click=lambda: self.page.go("/start/dashboard"),
        )

        # Create header with back button
        header = ft.Container(
            content=ft.Row(
                [
                    back_button,
                    ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD),
                ],
            ),
            padding=ft.padding.only(left=10, top=10, bottom=10),
        )

        # Create main layout
        main_row = ft.Row(
            controls=[
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.TextButton(
                                content=label,
                                on_click=lambda: self.page.go(f"/settings/{link_name}"),
                                style=ft.ButtonStyle(
                                    color= ft.Colors.ON_SURFACE,
                                ),
                            ) for label, link_name in [("Appearance", "appearance"), ("Email Accounts", "email"), ("Language", "language"), ("Notification", "notifications")]
                        ],
                        spacing=16,
                    ),
                    width=200,
                    padding=10,
                ),

                ft.VerticalDivider(width=1),
                self.sub_view,
            ],
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Divider(height=1),
                    ft.Container(content=main_row, expand=True),
                ],
                expand=True,
            ),
            expand=True,
        )

    def on_subroute_change(self, subview: "View|None") -> None:
        """
        Called when the sub-view (the specific settings page) changes.
        """
        self.sub_view = subview.get_view() if subview else ft.Container()
