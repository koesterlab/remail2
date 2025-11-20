from remail.frontend.components.mail_selection.conversation_preview import ConversationPreview
import flet as ft

from remail.controllers.dtos.conversations import ContactDTO, ConversationDTO, ThreadPreviewDTO


class GroupPreview(ConversationPreview):
    # component representing a single contact entry
    def __init__(self, group: ConversationDTO, on_click=lambda: None):
        print("Conversation Preview")

        primary = group.customName if group.customName else ", ".join(map(lambda contact : contact.first_name[0] + ". " + contact.last_name, group.contacts))
        secondary = str(len(group.contacts)) + " Members"
        # favorite toggle handler
        def toggle_fav():
            group.favorite = not group.favorite

        super().__init__(ft.Icon(ft.Icons.GROUP), primary, secondary, group.is_favorite, bool(group.customName), toggle_fav, on_click)
