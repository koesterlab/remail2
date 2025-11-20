from dataclasses import dataclass


@dataclass
class Contact:
    id: int
    firstname: str
    surname: str
    email: str
    registered: bool #implicite or explicite contact
    favorite: bool

    # def __eq__(self, other):
    #     return self.id == other.id or self.email == other.email
    #
    # def __lt__(self, other):
    #
    #
    #     if not self.favorite and other.favorite: return True
    #     if not self.registered and other.registered: return True
    #
    #     if self.surname != other.surname: return self.surname < other.surname
    #     if self.firstname != other.firstname: return self.firstname < other.firstname
    #
    #     return self.email < other.email