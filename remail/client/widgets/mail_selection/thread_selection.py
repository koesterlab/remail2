from typing import List

import flet

from remail.client.views.main.state import MainAppState
from remail.controllers.dtos.conversations import ConversationDTO
from remail.client.widgets.mail_selection.thread_preview import ThreadPreview

"""
Subwidget of selectionBar to choose between different conversations of a contact
"""
class ThreadSelection(flet.Column):
    def __init__(self, state:MainAppState):
        self.slided_in = False
        self.__state = state
        super().__init__(scroll=flet.ScrollMode.AUTO)

    def __on_conversations_change(self, conversations: List[ConversationDTO]):
        if len(conversations) == 1:
            if not self.slided_in: self.__slide_in()
            self.set_content(conversations[0])
        else:
            if self.slided_in: self.__slide_out()

    def __slide_out(self):
        pass #todo

    def __slide_in(self):
        pass #todo

    def set_content(self, content : ConversationDTO):
        #todo: make more efficient on reload
        #todo: sort algorithm
        self.controls = [ThreadPreview(elem) for elem in content.threads]