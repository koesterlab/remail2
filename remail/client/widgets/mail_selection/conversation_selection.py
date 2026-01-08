import datetime
from collections.abc import Callable
from datetime import timedelta

import flet as ft

from remail.client.state.main_app_state import MainAppState
from remail.client.widgets.mail_selection.action import Action
from remail.client.widgets.mail_selection.action_preview import ActionPreview
from remail.client.widgets.mail_selection.contact_preview import ContactPreview
from remail.client.widgets.mail_selection.group_preview import GroupPreview
from remail.controllers.dtos.conversations import ConversationDTO

"""
Subwidget of selectionBar to choose between different contacts (+groups) and actions
"""


class ConversationSelection(ft.Container):
    def __init__(self, callback: Callable[[Action | ConversationDTO], None], state: MainAppState):
        self.state = state
        self.callback = callback
        self.content = ft.Column(spacing=0)
        super().__init__(
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(  # outer: align content to top, middle: scroll, inner: enumeration of elements
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                controls=[self.content],
            ),
        )

    def set_content(self, content: list[ConversationDTO | Action]):
        # todo: make more efficient on reload
        def compute_order_value(elem: ConversationDTO | Action):
            if isinstance(elem, Action):
                return (datetime.MAXYEAR,)
            latest = max([t.last_message_datetime for t in elem.threads])
            if elem.is_favorite:
                return latest + timedelta(days=10000)
            return latest

        content.sort(key=compute_order_value, reverse=True)

        def create_list_item(elem: Action | ConversationDTO):
            def callback():
                self.callback(elem)

            if isinstance(elem, Action):
                item = ActionPreview(elem, callback)
            elif len(elem.contacts) == 1:
                item = ContactPreview(self.state, elem, callback)
            else:
                item = GroupPreview(self.state, elem, callback)

            return item

        self.content.controls = [create_list_item(elem) for elem in content]
