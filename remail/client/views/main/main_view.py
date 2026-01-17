import asyncio
import threading
from collections import UserDict

import flet as ft

from remail.client.state import AppState
from remail.client.widgets.chatbot.chatbot import create_chatbot
from remail.client.widgets.mail_selection import SelectionBar
from remail.controllers import EmailController
from remail.controllers.dtos.conversations import ThreadPreviewDTO
from remail.controllers.dtos.user_dto import UserDTO
from remail.enums import MainView
from remail.interfaces.email.services import EmailSyncService
from remail.interfaces.email.services.user_service import UserService
from remail.models import User
from tests.controllers.test_conversations_controller import controller
from ...scheduler import Scheduler

from ...state.main_app_state import MainAppState, MainAppStateProperties
from ...widgets.thread.thread_list import ThreadList


def create_main_view(page: ft.Page, global_state: AppState):
    main_state = MainAppState()
    main_state.set(MainAppStateProperties.DISPLAYED_MAILS, [])
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

    def on_emails_synced(acting_account: UserDTO, response: dict):
        print(response)
        if not response["synced_count"] or response["synced_count"] < 0:
            return
        if acting_account == main_state.get(MainAppStateProperties.ACTIVE_USER): #if active account: show new mails
            main_state.set(MainAppStateProperties.DISPLAYED_MAILS, main_state.conversations_controller.get_conversations(main_state.get(MainAppStateProperties.ACTIVE_USER).id))

    def on_email_sync_error(acting_account: UserDTO, msg:str):
        snack_bar = ft.SnackBar(ft.Text("[" + acting_account.email + "] Error while syncing mails: " + msg, color=ft.Colors.ON_ERROR), bgcolor=ft.Colors.ERROR, duration=50000)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    #stop old schedulers
    for k in list(global_state.email_schedulers.keys()):
        global_state.remove_email_scheduler(k)

    #start schedulers
    def start_scheduler(account: UserDTO):
        try:
            print("a")
            mail_controller = EmailController.from_id(account.id)
            print("b")
        except OSError as e:
            on_email_sync_error(account, "Could not connect to Server")
            return

        main_state.email_controllers[account.email] = mail_controller
        sync_service = EmailSyncService(
            protocol=mail_controller.protocol,
            email_parser=mail_controller.protocol.email_parser,
            user_email=account.email,
        )
        scheduler = Scheduler(
            task=sync_service.sync_emails,
            sync_interval=20,  # Sync every 60 seconds
            on_complete=lambda r: on_emails_synced(account, r),
            on_error=lambda r: on_email_sync_error(account, r),
        )
        global_state.add_email_scheduler(account.email, scheduler)
        scheduler.start()

    for account in UserService.get_all_users():
        threading.Thread(target=start_scheduler, args=(account,)).start()


    main_state.register_observer(MainAppStateProperties.ACTIVE_CHATBOT, on_chatbot_state_change)
    main_state.register_observer(MainAppStateProperties.ACTIVE_THREAD, on_thread_change)

    #test
    main_state.set(MainAppStateProperties.ACTIVE_USER, UserService.get_all_users()[0])

    return container
