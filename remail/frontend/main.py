import asyncio
import random
import threading
from datetime import datetime, timedelta
from typing import List

import flet

from remail.controllers.dtos.conversations import ConversationDTO, ContactDTO, ThreadPreviewDTO
from remail.enums import ContactType
from remail.frontend.components.mail_selection.selection_bar import SelectionBar

selection = SelectionBar()

def main(page : flet.Page):
    test_container = flet.Container()
    test_container.bgcolor = flet.colors.WHITE
    test_container.width = 300
    test_container.height = 1300
    test_container.content = selection
    page.add(test_container)
    selection.set_base_content()




flet.app(main)


def create_test_data():
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Judy"]
    last_names = ["Smith", "Johnson", "Brown", "Miller", "Davis", "Wilson", "Taylor", "Anderson", "Thomas", "Jackson"]
    messages = [
        "Hey, wie geht's?", "Treffen wir uns morgen?", "Hast du die Unterlagen?",
        "Danke!", "Klingt gut!", "Ich melde mich später.", "Alles klar!", "Lass uns telefonieren."
    ]

    conversations: List[ConversationDTO] = []

    contact_id_counter = 1
    thread_id_counter = 1

    for i in range(10):
        # Zufällige Anzahl von Kontakten: 1 für Einzelchat, 2-4 für Gruppen
        if i < 5:
            num_contacts = 1
        else:
            num_contacts = random.randint(2, 4)

        contacts = []
        for _ in range(num_contacts):
            contacts.append(ContactDTO(
                id=contact_id_counter,
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f"user{contact_id_counter}@example.com",
                is_known=random.choice([True, False]),
                type=ContactType.PRIVATE
            ))
            contact_id_counter += 1

        # Threads: 2-5 pro Conversation
        threads = []
        for _ in range(random.randint(2, 5)):
            threads.append(ThreadPreviewDTO(
                thread_id=thread_id_counter,
                title=f"Thread {thread_id_counter}",
                total_count=random.randint(5, 50),
                unread_count=random.randint(0, 10),
                last_message=random.choice(messages),
                last_message_datetime=datetime.now() - timedelta(days=random.randint(0, 30))
            ))
            thread_id_counter += 1

        conversations.append(ConversationDTO(
            contacts=contacts,
            threads=threads,
            is_favorite=random.choice([True, False]),
            customName=None if num_contacts == 1 else f"Gruppe {i + 1}"
        ))

