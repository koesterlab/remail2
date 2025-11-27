from typing import Callable, List

import flet

from remail.controllers.dtos.conversations import ConversationDTO
from remail.frontend.components.mail_selection.thread_preview import ThreadPreview

"""
Subwidget of selectionBar to choose between different conversations of a contact
"""
class ThreadSelection(flet.Column):
    def __init__(self, callback : Callable[[ConversationDTO], None]):
        self.callback = callback
        super().__init__(scroll=flet.ScrollMode.AUTO)

    def set_content(self, content : ConversationDTO):
        #todo: make more efficient on reload
        #todo: sort algorithm
        self.controls = [ThreadPreview(elem) for elem in content.threads]