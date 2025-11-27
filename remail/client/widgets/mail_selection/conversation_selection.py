from typing import Callable, List

import flet as ft

from remail.client.widgets.mail_selection.contact_preview import ContactPreview
from remail.client.widgets.mail_selection.group_preview import GroupPreview
from remail.client.widgets.mail_selection.action import Action
from remail.client.widgets.mail_selection.action_preview import ActionPreview
from remail.controllers.dtos.conversations import ConversationDTO

"""
Subwidget of selectionBar to choose between different contacts (+groups) and actions
"""
class ConversationSelection(ft.Column):
    def __init__(self, callback : Callable[[Action|ConversationDTO], None]):
        self.callback = callback
        super().__init__(expand=True)

    def set_content(self, content : List[ConversationDTO|Action]):
        #todo: make more efficient on reload
        #todo: sort algorithm
        print("Setting content to conversation selection")

        def create_list_item(elem : Action |ConversationDTO):
            callback = lambda: self.callback(elem)

            if isinstance(elem, Action): item = ActionPreview(elem,callback)
            elif len(elem.contacts) == 1: item = ContactPreview(elem, callback)
            else: item = GroupPreview(elem, callback)

            return item

        self.controls = [create_list_item(elem) for elem in content]