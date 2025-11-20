from typing import List

import flet as ft

from remail.controllers.dtos.conversations import ConversationDTO
from remail.frontend.components.mail_selection.action import Action
from remail.frontend.components.mail_selection.conversationSelection import ConversationSelection
from remail.frontend.components.mail_selection.searchHeader import SearchHeader
from remail.frontend.components.mail_selection.topicSelection import TopicSelection

"""
Overall Widget to combine searchbar and selection widgets
"""
class SelectionBar(ft.Container):
    def __init__(self):
        self.base_content = []
        self.main_content = ft.AnimatedSwitcher(
            ft.Container(),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=60,
            switch_in_curve=ft.AnimationCurve.LINEAR,
            switch_out_curve = ft.AnimationCurve.LINEAR
        )

        self.conversation_selection = ConversationSelection(self.__on_conversation_or_action_selected)
        self.topic_selection = TopicSelection(self.__on_topic_selected)

        super().__init__(
            content=ft.Column(controls = [
                    SearchHeader(on_change=self.__on_search_change),
                    ft.Container(
                        content=self.main_content,
                        expand=True
                    )
                ],
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.START
            ),
            expand=True
        )
        #self.set_base_content(get_dummy_inbox_data())


    def __on_search_change(self, new_search_term):
        pass

    def __on_conversation_or_action_selected(self, selected : ConversationDTO|Action):
        if isinstance(selected, ConversationDTO):
            self.set_content_to_display([selected])
        else:
            selected.on_executed()

    def __on_topic_selected(self, selected):
        #todo
        pass

    def set_base_content(self, base_content : List[ConversationDTO]):
        print("setting new content for selection")
        self.base_content = base_content
        self.set_content_to_display(self.base_content)

    def set_content_to_display(self, content_to_display : List[ConversationDTO|Action]):
        if len(content_to_display) == 1:
            self.__show_topic_selection(content_to_display[0])
        else:
            self.__show_conversation_selection(content_to_display)

        if self.page:
            print("updating page")
            self.main_content.update()

    def __show_conversation_selection(self, content : List[ConversationDTO]):
        print("switching to conversation selection")
        self.main_content.content = None
        self.conversation_selection.set_content(content)
        self.main_content.content = self.conversation_selection

    def __show_topic_selection(self, conversation : ConversationDTO):
        print("switching to topic selection")
        self.main_content.content = None
        self.topic_selection.set_content(conversation)
        self.main_content.content = self.topic_selection
