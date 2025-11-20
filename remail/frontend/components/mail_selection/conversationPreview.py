from typing import Callable

import flet as ft


class ConversationPreview(ft.Container):
    # component representing a single contact entry
    def __init__(self, image: ft.Control, primary_text: str, secondary_text: str, fav: bool, registered: bool,
                 on_toggle_fav: Callable[[], None], on_click: Callable[[], None]):
        print("Conversation Preview")

        # favorite button
        fav_btn = ft.IconButton(
            icon=ft.Icons.STAR if fav else ft.Icons.STAR_OUTLINE,
            tooltip="favorite",
            on_click=on_toggle_fav
        )

        # registered badge
        badge = None
        if registered:
            badge = ft.Container(
                content=ft.Text("Registered", size=11, color=ft.Colors.WHITE),
                padding=ft.padding.symmetric(horizontal=6, vertical=3),
                border_radius=6,
                bgcolor=ft.Colors.BLUE
            )

        super().__init__(
            on_click=lambda e: on_click(),
            content=ft.Row(
                [
                    ft.CircleAvatar(
                        content=image,
                        bgcolor=ft.Colors.BLUE_700,
                        radius=20
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(primary_text, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                    badge or ft.Container()
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            ft.Row(
                                [
                                    ft.Text(secondary_text, size=12, color=ft.Colors.GREY)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=6
                            )
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Row(
                        [fav_btn],
                        expand=True,
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=12
        )
