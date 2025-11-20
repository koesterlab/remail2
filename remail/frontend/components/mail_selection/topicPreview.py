import flet as ft

from remail.frontend.dummyDataclasses.Conversation import Conversation, Topic


class TopicPreview(ft.Container):
    # component representing a single contact entry
    def __init__(self, topic: Topic):
        super().__init__(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(("(" + str(topic.unread_messages) + ") " if topic.unread_messages > 0 else "") + topic.name, weight=ft.FontWeight.BOLD if topic.unreadMessages > 0 else ft.FontWeight.NORMAL, color=ft.Colors.BLACK),
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            ft.Row(
                                [
                                    ft.Text(topic.lastMessage, size=12, color=ft.Colors.GREY)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=6
                            )
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Row(
                        [ft.Text("Hier noch mehr sachen anzeigen (evtl. member)", size=4)],
                        expand=True,
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=12
        )
