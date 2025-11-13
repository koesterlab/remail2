"""
Shows a single Chat preview with Name, last message, unread messages, ... in chat overwiew
"""
import flet


class ChatPreview(flet.Container):
    def __init__(self, name: str, last_message: str, image_url: str = None, unread_count: int = 0, on_click=None):
        self.name = name
        self.last_message = last_message
        self.image_url = image_url
        self.unread_count = unread_count
        self.on_click = on_click
        super().__init__()

        self.content = self.build()

    def build(self):
        avatar = flet.CircleAvatar(
            content=flet.Image(src=self.image_url, fit=flet.ImageFit.COVER, width=48,
                             height=48) if self.image_url else flet.Icon(flet.Icons.PERSON, size=32),
            radius=24,
        )

        name_text = flet.Text(self.name, weight=flet.FontWeight.BOLD, size=14)
        message_text = flet.Text(self.last_message, size=12, color=flet.Colors.GREY_700, max_lines=1,
                               overflow=flet.TextOverflow.ELLIPSIS)

        text_column = flet.Column([name_text, message_text], tight=True)

        # unread badge
        badge = None
        if self.unread_count and self.unread_count > 0:
            display = str(self.unread_count) if self.unread_count < 100 else "99+"
            badge = flet.Container(
                content=flet.Text(display, size=11, weight=flet.FontWeight.BOLD, color=flet.Colors.WHITE),
                padding=flet.padding.symmetric(horizontal=8, vertical=4),
                bgcolor=flet.Colors.RED,
                border_radius=12,
                alignment=flet.alignment.center,
                animate=flet.Animation(200, flet.AnimationCurve.EASE_IN_OUT),
            )
        else:
            badge = flet.Container(width=0)

        row = flet.Container(
            content=flet.Row([
                avatar,
                flet.Container(width=12),
                text_column,
                badge,
            ], alignment=flet.MainAxisAlignment.START, vertical_alignment=flet.CrossAxisAlignment.CENTER),
            padding=flet.padding.all(8),
            on_click=self.on_click,
        )

        return row