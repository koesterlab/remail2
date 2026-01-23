from sqlmodel import Session, select

from remail.database import engine
from remail.models import Contact, User
from remail.utils.session_management import session

class ContactService:
    def __init__(self):
        """
        Initialize conversation service.
        """

        self.engine = engine

    def get_contact_by_id(self, contact_id: int) -> Contact | None:
        """
        Fetch a contact by its ID.

        Args:
            contact_id: Contact ID to fetch

        Returns:
            Contact object if found, else None
        """
        with Session(self.engine) as session:
            contact = session.get(Contact, contact_id)

            return contact

    @session
    def create_contact(self, name: str, email: str, session:Session|None) -> Contact:
        new_contact = Contact(
            name=name,
            email_address=email,
        )

        session.add(new_contact)
        return new_contact

    @session
    def get_or_create_contact(self, email: str, name:str = None, session:Session = None) -> Contact:
        contact = session.exec( select(Contact).where(Contact.email_address == email)).first()
        if contact:
            return contact
        contact = Contact(name=name, email_address=email, is_known=False)
        session.add(contact)
        return contact

    def get_user_contact(self, user: User) -> Contact:
        return self.get_or_create_contact(user.email, user.name)
