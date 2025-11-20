from typing import Callable, List

import flet as ft

import remail.frontend.components.mail_selection.conversationPreview
from remail.frontend.components.mail_selection.contactPreview import ContactPreview
from remail.frontend.components.mail_selection.groupPreview import GroupPreview
from remail.frontend.dummyDataclasses.Conversation import Conversation
from remail.frontend.components.mail_selection.Action import Action
from remail.frontend.components.mail_selection.ActionPreview import ActionPreview
from remail.frontend.dummyDataclasses.Contact import Contact

"""
Subwidget of selectionBar to choose between different contacts (+groups) and actions
"""
class ConversationSelection(ft.Column):
    def __init__(self, callback : Callable[[Action|Conversation], None]):
        self.callback = callback
        super().__init__()

    def set_content(self, content : List[Conversation|Action]):
        #todo: make more efficient on reload
        #todo: sort algorithm
        print("Setting content to conversation selection")

        def create_list_item(elem : Action |Conversation):
            callback = lambda: self.callback(elem)

            if isinstance(elem, Action): item = ActionPreview(elem,callback)
            elif len(elem.members) == 1: item = ContactPreview(elem.members[0], callback)
            else: item = GroupPreview(elem, callback)

            return item

        self.controls = [create_list_item(elem) for elem in content]