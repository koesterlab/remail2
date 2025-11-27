import flet as ft


class SearchHeader(ft.Container):
    def __init__(self, on_change, on_home_click=None, on_archiv=None, on_spam=None):
        self.on_change = on_change
        self.on_home_click = on_home_click
        self.on_archiv = on_archiv
        self.on_spam = on_spam

        # ----- Search Input -----
        def handle_change(e):
            self.on_change(e.control.value)

        self.input = ft.TextField(
            hint_text="Search...",
            on_change=handle_change,
            expand=True,
            color=ft.Colors.BLACK,
            border_color="transparent",     # kein Outline
            bgcolor="#e0e0e0",
            border_radius=ft.border_radius.all(30),
            content_padding=ft.padding.symmetric(vertical=6, horizontal=8),
            dense=True,
        )

        # ----- Home Icon -----
        home_icon = ft.IconButton(
            icon=ft.Icons.HOME,
            icon_color=ft.Colors.BLACK,
            on_click=lambda e: self.on_home_click and self.on_home_click(),
            icon_size=30,
            style=ft.ButtonStyle(
                padding=0,
                bgcolor="transparent"
            ),
        )

        # ----- Links unterhalb -----
        archiv_link = ft.Container(ft.Text(
            "Archiv",
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
            color=ft.Colors.BLACK,

        ),on_click=lambda _: self.on_archiv and self.on_archiv())

        spam_link = ft.Container(content=ft.Text(
            "Spam",
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
            color=ft.Colors.BLACK,

        ), on_click=lambda _: self.on_spam and self.on_spam())

        # ----- Layout -----
        content = ft.Column(
            controls=[
                ft.Row(
                    [self.input, home_icon],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row([archiv_link, spam_link], spacing=20),
                ft.Divider(height=3, thickness=2)
            ],
            spacing=5
        )

        super().__init__(
            content=content,
            padding=2,
            margin=1,
        )