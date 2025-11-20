import flet as ft

from remail.controllers.dtos.conversations import ThreadPreviewDTO


class ThreadPreview(ft.Container):
    # component representing a single contact entry
    def __init__(self, topic: ThreadPreviewDTO):
        super().__init__(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(("(" + str(topic.unread_count) + ") " if topic.unread_count > 0 else "") + topic.title, weight=ft.FontWeight.BOLD if topic.unread_count > 0 else ft.FontWeight.NORMAL, color=ft.Colors.BLACK),
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            ft.Row(
                                [
                                    ft.Text(topic.last_message, size=12, color=ft.Colors.GREY)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=6
                            )
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START
                    ),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=12
        )
