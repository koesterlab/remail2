import flet

from remail.client.widgets.mail_selection import SelectionBar

selection = SelectionBar()

def main(page : flet.Page):
    test_container = flet.Container()
    test_container.bgcolor = flet.Colors.WHITE
    test_container.width = 300
    test_container.height = 1300
    test_container.content = selection
    page.add(test_container)




flet.app(main)