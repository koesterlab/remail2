import flet as ft

from remail.frontend.client.components.inbox.contact import Contact

class SimpleText(ft.Container):
    def __init__(self):
        super().__init__(content=self.build(), border_radius=2)
    def build(self):
        return ft.Text("Hallo, ich bin eine einfache Component!", size=16)

def main(page : ft.Page):

    page.add(Contact("Jonathan Dreisvogt", "Ich hab Hunger", None, 1))

ft.app(main)