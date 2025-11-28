import re
from typing import List

import flet as ft

from remail.client.views.main.state import MainAppState
from remail.controllers.dtos.conversations import ConversationDTO, ThreadPreviewDTO
from remail.client.widgets.mail_selection.action import Action
from remail.client.widgets.mail_selection.conversation_selection import ConversationSelection
from remail.client.widgets.mail_selection.search_header import SearchHeader
from remail.client.widgets.mail_selection.thread_selection import ThreadSelection
from remail.client.views.main.test_data_conversations import create_test_data, create_search_result_test_data

"""
Overall Widget to combine searchbar and selection widgets
"""
class SelectionBar(ft.Container):
    def __init__(self, state: MainAppState):
        self.main_content = ft.AnimatedSwitcher(
            ft.Container(),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=130,
            switch_in_curve=ft.AnimationCurve.LINEAR,
            switch_out_curve = ft.AnimationCurve.LINEAR,
        )
        self.__state = state
        self.conversation_selection = ConversationSelection(self.__on_conversation_or_action_selected, state)
        self.topic_selection = ThreadSelection(state)

        super().__init__(
            bgcolor=ft.Colors.SURFACE,
            width=300,
            content=ft.Column(controls = [
                    SearchHeader(state),
                    ft.Container(
                        content=self.main_content,
                        expand=True
                    )
                ],
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.START
            ),
            expand=True,
            clip_behavior = ft.ClipBehavior.HARD_EDGE
        )
        state.listen_search_term(self.__on_search_change)
        state.listen_displayed(self.__set_content_to_display)
        self.__set_content_to_display(state.displayed)
        self.__on_search_change(state.search_term) #initially loading data


    def __on_search_change(self, new_search_term:str|None):
        mails = self.__load_messages(new_search_term)
        if new_search_term and re.match("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]", new_search_term): #option "mail hinzufügen
            mails.insert(0,Action(new_search_term + " zu Kontakten hinzufügen", "Als neuen Kontakt erstellen", None, ft.Colors.SECONDARY, ft.Icons.ADD))
            mails.insert(0,Action("Nachricht an " + new_search_term, "Neuer Chat", None, ft.Colors.PRIMARY, ft.Icons.MAIL))

        self.__set_content_to_display(mails)
        pass

    def __on_conversation_or_action_selected(self, selected : ConversationDTO|Action):
        if isinstance(selected, ConversationDTO):
            self.__set_content_to_display([selected])
        else:
            selected.on_executed()

    def __on_topic_selected(self, selected:ThreadPreviewDTO):
        self.__state.set_active_thread(selected)
        pass

    def __set_content_to_display(self, content_to_display : List[ConversationDTO|Action]):
        print(content_to_display)
        if len(content_to_display) == 1:
            self.__show_topic_selection(content_to_display[0])
        else:
            self.__show_conversation_selection(content_to_display)

        if self.page:
            print("updating page")
            self.main_content.update()

    def __show_conversation_selection(self, content : List[ConversationDTO]):
        print("switching to conversation selection")
        self.conversation_selection.set_content(content)
        self.main_content.content = self.conversation_selection


    def __show_topic_selection(self, conversation : ConversationDTO):
        print("switching to topic selection")
        self.topic_selection.set_content(conversation)
        self.main_content.content = self.topic_selection

    @classmethod
    def __load_messages(cls, searchterm: str|None = None):
        if searchterm:
            print("requesting search data")
            return create_search_result_test_data(searchterm)
        else:
            print("requesting standart data")
            return create_test_data()
