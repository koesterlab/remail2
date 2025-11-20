import flet as ft

import remail.frontend.components.mail_selection.conversationPreview
from remail.frontend.dummyDataclasses import Contact
from remail.frontend.dummyDataclasses.Conversation import Conversation


class ContactPreview(remail.frontend.components.mail_selection.conversationPreview.ConversationPreview):
    # component representing a single contact entry
    def __init__(self, contact: Contact, on_click=lambda: None):
        print("Conversation Preview")

        initials = (contact.firstname[:1] + (contact.surname[:1] if contact.surname else "")).upper()
        full_name = f"{contact.firstname} {contact.surname}".strip()

        # favorite toggle handler
        def toggle_fav():
            contact.favorite = not contact.favorite

        # registered badge
        badge = None
        if contact.registered:
            badge = ft.Container(
                content=ft.Text("Registered", size=11, color=ft.Colors.WHITE),
                padding=ft.padding.symmetric(horizontal=6, vertical=3),
                border_radius=6,
                bgcolor=ft.Colors.BLUE
            )

        super().__init__(ft.Text(initials), full_name, contact.email, contact.favorite, contact.registered, toggle_fav, on_click)
