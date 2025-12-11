"""Dashboard view for the main application page."""

import flet as ft

from remail.client.state.app_state import AppState


def create_dashboard_view(page: ft.Page, app_state: AppState) -> ft.Container:
    """Create the main dashboard view.

    Args:
        page: The Flet page object
        app_state: The application state

    Returns:
        A Container with the dashboard view
    """
    page.title = "Remail 2.0 - Dashboard"
    page.padding = 20

    def navigate_to_chatbot(e):
        """Navigate to chatbot view."""
        # TODO: Implement navigation
        pass

    def navigate_to_settings(e):
        """Navigate to settings view."""
        # TODO: Implement navigation
        pass

    dashboard_content = ft.Column(
        controls=[
            ft.Text("Welcome to Remail 2.0", size=32, weight="bold"),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "AI Chatbot",
                        icon=ft.icons.CHAT,
                        on_click=navigate_to_chatbot,
                        width=150,
                        height=100,
                    ),
                    ft.ElevatedButton(
                        "Settings",
                        icon=ft.icons.SETTINGS,
                        on_click=navigate_to_settings,
                        width=150,
                        height=100,
                    ),
                ],
                spacing=20,
            ),
        ],
        spacing=20,
    )

    return ft.Container(
        content=dashboard_content,
        expand=True,
    )
