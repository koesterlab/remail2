import flet as ft

from remail.client.state import AppState
from remail.client.widgets.chatbot.chatbot import create_chatbot
from remail.client.widgets.mail_selection import SelectionBar
from remail.controllers import EmailController
from remail.controllers.dtos.conversations import ThreadPreviewDTO
from remail.controllers.dtos.user_dto import UserDTO
from remail.enums import MainView
from remail.interfaces.email.services.user_service import UserService
from ...scheduler import Scheduler

from ...state.main_app_state import MainAppState, MainAppStateProperties
from ...widgets.thread.thread_list import ThreadList


def create_main_view(page: ft.Page, global_state: AppState):
    main_state = MainAppState()
    # users = UserService.get_all_users()
    # if len(users) < 1:
    #     if global_state.router is not None:
    #         global_state.router.load_view(MainView.SETTINGS)
    #     return ft.Container()
    # main_state.set(MainAppStateProperties.ACTIVE_USER, users[0])
    main_state.set(
        MainAppStateProperties.DISPLAYED_MAILS,
        list(main_state.conversations_controller.get_conversations(users[0].id)),
    )  # todo
    main_state.set(MainAppStateProperties.ACTIVE_CHATBOT, False)
    main_state.set(MainAppStateProperties.ACTIVE_THREAD, None)
    main_state.set(MainAppStateProperties.ACTIVE_CONVERSATION, None)
    main_state.set(MainAppStateProperties.SEARCH_TERM, "")
    selection_bar = SelectionBar(main_state)

    # Settings button
    def navigate_to_settings(e):
        """Navigate to settings page."""
        if global_state.router:
            page.clean()
            settings_view = global_state.router.load_view(MainView.SETTINGS)
            page.add(settings_view)
            page.update()

    settings_button = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        tooltip="Settings",
        on_click=navigate_to_settings,
    )

    dashboard = ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Dashboard (vertrau ist fast fertig)", size=20),
                        settings_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10,
            ),
        ],
        expand=True,
    )
    right_view = ft.Container(dashboard, col={"xs": 6, "md": 8, "lg": 9}, expand=True)

    # Chatbot
    chatbot = create_chatbot(main_state)
    chatbot.height = 60
    chatbot.expand = False

    container = ft.ResponsiveRow(
        expand=True,
        controls=[
            ft.Column(
                [ft.Container(selection_bar, expand=1), chatbot], col={"xs": 6, "md": 4, "lg": 3}
            ),
            right_view,
        ],
    )

    def on_thread_change(new: ThreadPreviewDTO | None) -> None:
        if new:
            right_view.content = ThreadList(main_state)
        else:
            right_view.content = dashboard
        right_view.update()

    def on_chatbot_state_change(is_active: bool) -> None:
        if is_active:
            chatbot.expand = 4
        else:
            chatbot.expand = False
            chatbot.height = 60
        container.update()

    def on_emails_synced(response: dict):
        pass

    def on_email_sync_error(msg:str):
        snack_bar = ft.SnackBar(ft.Text("Error while syncing mails: " + msg, color=ft.Colors.ON_ERROR), bgcolor=ft.Colors.ERROR, duration=5000)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    scheduler: Scheduler = Scheduler(
        task = lambda:{},
        sync_interval = 30,
        on_complete = on_emails_synced,
        on_error = on_email_sync_error)

    def on_user_change(user:UserDTO) -> None:
        main_state.email_controller = EmailController.from_id(user.id)
        scheduler.stop()
        scheduler.task=
        scheduler.start()


    main_state.register_observer(MainAppStateProperties.ACTIVE_CHATBOT, on_chatbot_state_change)
    main_state.register_observer(MainAppStateProperties.ACTIVE_THREAD, on_thread_change)

    return container
