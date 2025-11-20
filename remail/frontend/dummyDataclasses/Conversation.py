from dataclasses import dataclass
from typing import List

from remail.frontend.dummyDataclasses.Contact import Contact

@dataclass
class Topic:
    id: int
    name: str
    unreadMessages: int
    messages: int
    lastMessage: str
    unread_messages: int


@dataclass
class Conversation:
    id: int
    customName: str|None
    members: List[Contact]
    topics: List[Topic]
    favorite: bool



def get_dummy_inbox_data():
    # Testdaten (chatGpt)
    alice = Contact(1, "Alice", "Meyer", "alice@example.com", True, False)
    bob = Contact(2, "Bob", "Schulz", "bob@example.com", True, True)
    carla = Contact(3, "Carla", "Fischer", "carla@example.com", False, False)
    daniel = Contact(4, "Daniel", "Klein", "daniel@example.com", True, True)
    eva = Contact(5, "Eva", "Neumann", "eva@example.com", False, False)
    frank = Contact(6, "Frank", "Becker", "frank@example.com", True, False)
    gina = Contact(7, "Gina", "Wolf", "gina@example.com", True, True)

    conversations = [
        Conversation(1, None, [alice, bob], [
            Topic(1, "Projekt A", 2, 10, "Bob: Update morgen?", 0),
            Topic(2, "Allgemein", 0, 5, "Alice: Hallo zusammen!", 0)
        ], True),
        Conversation(2, "Team Chat", [bob], [
            Topic(3, "Sprint Planung", 1, 8, "Daniel: Sprint Review am Freitag", 0),
            Topic(4, "Ideen", 0, 3, "Carla: Vorschläge?", 0),
            Topic(5, "Fehlerbehebung", 2, 6, "Bob: Bugfix deployed", 0)
        ], True),
        Conversation(3, None, [alice, eva], [
            Topic(6, "Urlaubsplanung", 0, 2, "Eva: Ich bin nächste Woche weg", 0)
        ], True),
        Conversation(4, "Freunde", [frank], [
            Topic(7, "Party", 3, 15, "Gina: Wer bringt Snacks?", 0),
            Topic(8, "Filmabend", 0, 4, "Frank: Welche Filme?", 0)
        ], False),
        Conversation(5, "Projekt B", [daniel, eva, carla, gina], [
            Topic(9, "Meeting Notizen", 0, 7, "Daniel: Protokoll angehängt", 0),
            Topic(10, "Aufgaben", 1, 9, "Eva: Task 5 erledigt", 0),
            Topic(11, "Feedback", 2, 5, "Gina: Sieht gut aus", 0)
        ], False),
    ]
    return conversations