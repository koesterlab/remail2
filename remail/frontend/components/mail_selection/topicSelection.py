from typing import Callable, List

import flet

from remail.frontend.components.mail_selection.Action import Action
from remail.frontend.components.mail_selection.topicPreview import TopicPreview
from remail.frontend.dummyDataclasses.Conversation import Conversation
from remail.frontend.dummyDataclasses.Contact import Contact

"""
Subwidget of selectionBar to choose between different conversations of a contact
"""
class TopicSelection(flet.Column):
    def __init__(self, callback : Callable[[Conversation], None]):
        self.callback = callback
        super().__init__()

    def set_content(self, content : Conversation):
        #todo: make more efficient on reload
        #todo: sort algorithm
        self.controls = [TopicPreview(elem) for elem in content.topics]