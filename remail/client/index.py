"""Main entry point for the Remail client application."""

import flet as ft

from remail.client.state import AppState
from remail.client.state.settings_loader import load_settings_into_state
from remail.client.views.main import MainView
from remail.client.views.settings import AppearanceView, LanguageView, NotificationsView, EmailAccountsView
from remail.client.views.settings.settings_view import SettingsView
from remail.client.views.view_router import ViewRouter
from remail.interfaces.email.services.user_service import UserService


def main(page: ft.Page):
    """Initialize and run the Remail application.

    Args:
        page: The Flet page object
    """

    page.title = "Remail 2.0"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    app_state = AppState()
    load_settings_into_state(app_state, page)

    saved_users = UserService.get_all_users()
    app_state.connected_emails = saved_users

    # Create router and register views
    router = ViewRouter(page)
    app_state.router = router
    router.register_view(SettingsView())
    router.register_view(MainView())
    router.register_view(AppearanceView())
    router.register_view(EmailAccountsView())
    router.register_view(LanguageView())
    router.register_view(NotificationsView())

    page.go("/start")

if __name__ == "__main__":
    ft.context.disable_auto_update()
    ft.run(main)
