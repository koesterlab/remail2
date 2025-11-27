from typing import Callable

import flet as ft

from remail.controllers.dtos.conversations import ContactDTO, ConversationDTO, ThreadPreviewDTO


class ConversationPreview(ft.Container):
    # component representing a single contact entry
    def __init__(self, image: ft.Control, primary_text: str, secondary_text: str, fav: bool, registered: bool,
                 on_toggle_fav: Callable[[], None], on_click: Callable[[], None]):
        print("Conversation Preview")

        icon_btn = ft.Row([],
                spacing=2,
                expand = True,
                alignment = ft.MainAxisAlignment.END
        )

        if not registered:
            icon_btn.controls =[
                ft.Icon(ft.Icons.ADD, color=ft.Colors.ORANGE),
                ft.Icon(ft.Icons.DRAW, color=ft.Colors.ORANGE),
            ]
        else:
            icon_btn.controls = [ft.IconButton(
                icon=ft.Icons.STAR if fav else ft.Icons.STAR_OUTLINE,
                tooltip="favorite",
                on_click=lambda e: on_toggle_fav(),

            )]

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
                    icon_btn
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=12
        )
