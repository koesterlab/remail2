import flet

from components.chatPreview import ChatPreview


def main(page : flet.Page):
    page.add(ChatPreview("Jonathan Dreisvogt", "Ich habe hunger", None, 2, None))

flet.app(main)