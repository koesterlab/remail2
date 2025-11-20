import flet as ft


class SearchHeader(ft.Container):
    def __init__(self, on_change):
        self.on_change = on_change

        def handle_change(e):
            self.on_change(e.control.value)

        self.input = ft.TextField(
            hint_text="Search...",
            on_change=handle_change,
            expand=True,
        )

        super().__init__(
            content=ft.Row(
                [self.input],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=10
        )