from remail.frontend.components.mail_selection.conversationPreview import ConversationPreview
import flet as ft

from remail.frontend.dummyDataclasses.Conversation import Conversation


class GroupPreview(ConversationPreview):
    # component representing a single contact entry
    def __init__(self, group: Conversation, on_click=lambda: None):
        print("Conversation Preview")

        primary = group.customName if group.customName else ", ".join(map(lambda contact : contact.firstname[0] + ". " + contact.surname, group.members))
        secondary = str(len(group.members)) + " Members"
        # favorite toggle handler
        def toggle_fav():
            group.favorite = not group.favorite

        super().__init__(ft.Icon(ft.Icons.GROUP), primary, secondary, group.favorite, bool(group.customName), toggle_fav, on_click)
