from __future__ import annotations

import flet as ft

from remail.client.widgets.mail_selection.profile_picture import (
    create_contact_picture,
)
from remail.controllers.dtos.conversations import ContactDTO
from remail.controllers.dtos.threads import MessageDTO
from remail.controllers.thread_controller import ThreadController


class MessageBubble(ft.Container):
    """Single chat bubble (left for others, right for me)."""

    def __init__(self, message: MessageDTO, current_user: ContactDTO) -> None:
        is_me = message.sender == current_user

        alignment = ft.Alignment.CENTER_RIGHT if is_me else ft.Alignment.CENTER_LEFT

        own_border = ft.BorderRadius.only(top_left=18, bottom_left=18, bottom_right=18)
        others_border = ft.BorderRadius.only(top_right=18, bottom_left=18, bottom_right=18)

        # --- Tag chips ---
        tag_row = ft.Row(controls=[], spacing=4, wrap=True)

        def refresh_tags(tags: list[str]) -> None:
            tag_row.controls = [
                ft.Container(
                    content=ft.Text(tag, size=11, color=ft.Colors.ON_PRIMARY_CONTAINER),
                    bgcolor=ft.Colors.PRIMARY_CONTAINER,
                    border_radius=12,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                )
                for tag in tags
            ]
            try:
                tag_row.update()
            except Exception:
                pass

        # --- Tag input field ---
        tag_input = ft.TextField(
            hint_text="Add tag...",
            height=35,
            text_size=12,
            border_radius=8,
            visible=False,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=4),
        )

        def toggle_input(e: ft.ControlEvent) -> None:
            tag_input.visible = not tag_input.visible
            tag_input.update()

        def submit_tag(e: ft.ControlEvent) -> None:
            tag = tag_input.value.strip() if tag_input.value else ""
            if not tag:
                return
            ThreadController().add_tag(message.id, tag)
            message.tags.append(tag)
            refresh_tags(message.tags)
            tag_input.value = ""
            tag_input.visible = False
            tag_input.update()

        tag_input.on_submit = submit_tag

        add_tag_btn = ft.IconButton(
            icon=ft.Icons.LABEL_OUTLINE,
            icon_size=16,
            tooltip="Add tag",
            on_click=toggle_input,
        )

        # --- Message body ---
        bubble_content = ft.Column(
            controls=[
                ft.Text(
                    message.content.body,
                    color=ft.Colors.ON_PRIMARY if is_me else ft.Colors.ON_SECONDARY,
                    size=15,
                    weight=ft.FontWeight.W_400,
                ),
                tag_row,
                tag_input,
                ft.Row(controls=[add_tag_btn], alignment=ft.MainAxisAlignment.END),
            ],
            spacing=4,
        )

        bubble = ft.Container(
            margin=ft.Margin.only(left=20) if is_me else ft.Margin.only(right=20),
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=own_border if is_me else others_border,
            bgcolor=ft.Colors.PRIMARY if is_me else ft.Colors.SECONDARY,
            expand=True,
            shadow=ft.BoxShadow(
                blur_radius=6,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            ),
            content=bubble_content,
        )

        super().__init__(
            alignment=alignment,
            padding=ft.Padding.only(left=6, right=6, top=4, bottom=4),
            content=bubble if is_me else ft.Row([create_contact_picture(message.sender), bubble]),
            expand=True,
        )