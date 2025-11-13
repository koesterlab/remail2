import flet as ft


class Contact(ft.Container):
    def __init__(self, name: str, last_message: str, image_url: str = None, unread_count: int = 0, on_click=None):
        self.name = name
        self.last_message = last_message
        self.image_url = image_url
        self.unread_count = unread_count
        self.on_click = on_click
        super().__init__(content=self.build())

    def build(self):
        avatar = ft.CircleAvatar(
            content=ft.Image(src=self.image_url, fit=ft.ImageFit.COVER, width=48, height=48) if self.image_url else ft.Icon(ft.Icons.PERSON, size=32),
            radius=24,
        )

        name_text = ft.Text(self.name, weight=ft.FontWeight.BOLD, size=14)
        message_text = ft.Text(self.last_message, size=12, color=ft.Colors.GREY_700, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)

        text_column = ft.Column([name_text, message_text], tight=True)

        # unread badge
        badge = None
        if self.unread_count and self.unread_count > 0:
            display = str(self.unread_count) if self.unread_count < 100 else "99+"
            badge = ft.Container(
                content=ft.Text(display, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                bgcolor=ft.Colors.RED,
                border_radius=12,
                alignment=ft.alignment.center,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            )
        else:
            badge = ft.Container(width=0)

        row = ft.Container(
            content=ft.Row([
                avatar,
                ft.Container(width=12),
                text_column,
                badge,
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(8),
            on_click=self.on_click,
        )

        return row
