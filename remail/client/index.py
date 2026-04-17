"""Main entry point for the Remail client application."""

import flet as ft
from remail.client.views.index_view import IndexView


def main(page: ft.Page):
    """Initialize and run the Remail application.

    Args:
        page: The Flet page object
    """

    page.title = "Remail 2.0"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    view = IndexView()
    page.add(view)
    view.start()

if __name__ == "__main__":
    ft.context.disable_auto_update()
    ft.run(main)
