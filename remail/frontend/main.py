import asyncio
import threading

import flet

from remail.frontend.components.mail_selection.selectionBar import SelectionBar
from remail.frontend.dummyDataclasses.Contact import Contact
from remail.frontend.dummyDataclasses.Conversation import Topic, Conversation, get_dummy_inbox_data

selection = SelectionBar()

def main(page : flet.Page):
    test_container = flet.Container()
    test_container.bgcolor = flet.Colors.WHITE
    test_container.width = 300
    test_container.height = 1300
    test_container.content = selection
    page.add(test_container)



flet.app(main)


