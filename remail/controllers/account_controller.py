import datetime
from typing import Callable, Iterable

from remail.controllers import EmailController
from remail.controllers.dtos.conversations import ConversationDTO, ContactDTO, ThreadPreviewDTO
from remail.controllers.dtos.threads import ThreadDTO
from remail.controllers.dtos.user_dto import UserDTO
from remail.enums import ContactType, UserAccountCategory
from remail.interfaces.email import ImapProtocol, EmailProtocol
from remail.interfaces.email.services import EmailSyncService, EmailParser, ConversationService, ThreadService
from remail.interfaces.email.services.user_service import UserService
from remail.models import User, Conversation
from remail.utils.session_management import session


class AccountController:
    """ Class for base operations for existing users"""

    @staticmethod
    def all_client_accounts() -> list["AccountController"]:
        users = UserService().get_all_users()
        return list(map(lambda dto: AccountController(dto.id), users))

    def __init__(self, account_id: int):
        self.user_id = account_id
        self.user:User = UserService.get_user_by_id(account_id)
        self.protocol: EmailProtocol = ImapProtocol(username=self.user.username, password=self.user.password,
                                                    host=self.user.host)  # todo implement exchange option
        self.sync_service = EmailSyncService(protocol=self.protocol, email_parser=EmailParser(), user=self.user)
        self.thread_service = ThreadService()
        self.user_service = UserService()
        self.conversation_service = ConversationService()
        self.callback: Callable[[Iterable[ConversationDTO]], None] = lambda _: None

    @session
    def get_conversations(self) -> Iterable[ConversationDTO]:
        """ Returns all conversations from the users inbox """
        #re-sync via imap
        self.sync_service.sync_emails(since=self.user.last_refresh)

        #notify callback if something has changed
        self._notify_callback()

        #return all conversation DTOs
        conversations_data = self.conversation_service.get_all_conversations(self.user.id)
        return [self._conversation_to_dto(e) for e in conversations_data]

    def set_callback_email_changes(self, callback: Callable[[Iterable[ConversationDTO]], None]) -> None:
        """ Registers a callback that is called every time when a Conversation is updated or new with the conversation """
        self.callback = callback

    def _notify_callback(self):
        changed = self.sync_service.check_for_changed_conversations()
        if len(changed) > 0:
            self.callback(changed)

    async def start_listening(self):
        """ Starts background task to wait for email changes in imap idle mode. Calls callback if something changes"""
        print("Starting sync service")
        self.callback(self.get_conversations())
        print("First sync over")

        async for _ in self.sync_service.wait_for_mail_changes_async():
            self._notify_callback()

    def get_email_address(self) -> str:
        return self.user.email

    def get_plain_name(self) -> str:
        return self.user.name

    def get_user(self):
        user = self.user_service.get_user_by_id(self.user_id)
        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            category=UserAccountCategory.NOT_SPECIFIED,
            protocol=user.protocol,
            unread_conversations=self.user_service.count_unread(self.user),
        )

    def get_email_controller(self) -> EmailController:
        return EmailController(self.protocol)

    @session
    def _conversation_to_dto(self, conversation: Conversation) -> ConversationDTO:
        threads = []
        for thread in conversation.threads:
            unread_count = 0
            total_count = 0
            latest_message = None
            for message in thread.messages:
                if not message.read:
                    unread_count += 1
                if not latest_message or message.sent_at > latest_message.sent_at:
                    latest_message = message
                total_count += 1
            threads.append(ThreadPreviewDTO(
                thread_id=thread.id,
                title=thread.title,
                total_count=total_count,
                unread_count=unread_count,
                last_message=latest_message.body if latest_message else "",
                last_message_datetime=latest_message.sent_at if latest_message else datetime.datetime.min,
            ))

        return ConversationDTO(
            id=conversation.id,
            is_favorite=conversation.is_favorite,
            custom_name=conversation.custom_name,
            contacts=[
                ContactDTO(
                    id=c.id,
                    first_name=c.first_name,
                    last_name=c.last_name if c.last_name else c.name,
                    email=c.email_address,
                    is_known=c.is_known,
                    type=c.contact_type,
                )
                for c in conversation.contacts
                if c.email_address != self.user.email
            ],
            threads=threads
        )

