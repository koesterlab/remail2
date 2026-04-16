from abc import ABC

import flet as ft

from remail.client.state.app_state import AppState
from remail.client.views.settings.settings_sub_view import SettingsSubView
from remail.controllers.account_controller import AccountController
from remail.controllers.dtos import SettingsDTO
from remail.controllers.dtos.user_dto import UserDTO
from remail.controllers.email_controller import EmailController
from remail.enums import AuthMethods, ConnectionSecurity, Protocol
from remail.interfaces.email.services.user_service import UserService


class EmailAccountsView(SettingsSubView):
    def create_page(self, settings: SettingsDTO) -> ft.Container:
        smtp_user_input = ft.TextField(label="Username", hint_text="Enter SMTP username")
        smtp_pass_input = ft.TextField(
            label="Password",
            hint_text="Enter SMTP password",
            password=True,
            can_reveal_password=True,
        )
        smtp_port_input = ft.TextField(label="Port", hint_text="587")
        imap_user_input = ft.TextField(label="Username", hint_text="Enter IMAP username")
        imap_pass_input = ft.TextField(
            label="Password",
            hint_text="Enter IMAP password",
            password=True,
            can_reveal_password=True,
        )
        imap_port_input = ft.TextField(label="Port", hint_text="993")
        start_text = ft.Text("No accounts connected yet")
        accounts_counter = ft.Text(size=12)
        accounts_column = ft.Column()
        input_panel = ft.Container()
        add_button = ft.Container(
            ft.OutlinedButton("Add Email Account", icon=ft.Icons.ADD, on_click=self._show_add_form),
            alignment=ft.Alignment.CENTER,
            margin=ft.margin.only(top=20),
        )
        name_input = ft.TextField(label="Display Name", hint_text="Your Name", width=300)
        email_input = ft.TextField(
            label="Email address",
            hint_text="Enter your email address",
            width=300,
        )
        password_input = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            width=300,
        )
        imap_host_input = ft.TextField(
            label="IMAP Host",
            hint_text="Enter your IMAP host name",
            width=300,
            suffix=ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda _: _open_imap_settings()),
        )
        smtp_host_input = ft.TextField(
            label="SMTP Host",
            hint_text="Enter your SMTP host name",
            width=300,
            suffix=ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda _: _open_smtp_settings()),
        )

    def create_view(self) -> ft.Control:
        _load_connected_emails()
        _refresh_accounts()
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Email Accounts", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage your email accounts"),
                    ft.Divider(height=2, color=ft.Colors.GREY_400),
                    start_text,
                    accounts_counter,
                    accounts_column,
                    add_button,
                    input_panel,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            border_radius=10,
            alignment=ft.Alignment.CENTER_LEFT,
            expand=True,
        )

    def _load_connected_emails(self) -> None:
        app_state.connected_emails = UserService.get_all_users()

    def _show_snackbar(self, message: str, color: str) -> None:
        snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def _close_dialog(self, dialog: ft.AlertDialog) -> None:
        dialog.open = False
        page.update()

    def _open_smtp_settings(self) -> None:
        dialog = ft.AlertDialog(
            title=ft.Text("Advanced SMTP Settings"),
            content=ft.Column(
                [smtp_user_input, smtp_pass_input, smtp_port_input],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: _close_dialog(dialog)),
                ft.TextButton(
                    "Save",
                    on_click=lambda _: (_show_snackbar("SMTP settings saved!", ft.Colors.GREEN_400), _close_dialog(dialog)),
                ),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _open_imap_settings(self) -> None:
        dialog = ft.AlertDialog(
            title=ft.Text("Advanced IMAP Settings"),
            content=ft.Column(
                [imap_user_input, imap_pass_input, imap_port_input],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: _close_dialog(dialog)),
                ft.TextButton(
                    "Save",
                    on_click=lambda _: (_show_snackbar("IMAP settings saved!", ft.Colors.GREEN_400), _close_dialog(dialog)),
                ),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _show_add_form(self, _=None) -> None:
        input_panel.content = ft.Column(
            [
                ft.Text("Add Email Account", size=16, weight=ft.FontWeight.BOLD),
                name_input,
                email_input,
                password_input,
                imap_host_input,
                smtp_host_input,
                ft.Row(
                    [
                        ft.OutlinedButton("Connect", icon=ft.Icons.CHECK, on_click=lambda _: _connect_account()),
                        ft.OutlinedButton("Cancel", icon=ft.Icons.CLOSE, on_click=lambda _: _cancel_add()),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )
        add_button.visible = False
        page.update()

    def _reset_inputs(self) -> None:
        name_input.value = ""
        email_input.value = ""
        password_input.value = ""
        imap_host_input.value = ""
        smtp_host_input.value = ""

    def _cancel_add(self) -> None:
        _reset_inputs()
        input_panel.content = None
        add_button.visible = True
        page.update()

    def _connect_account(self) -> None:
        email = (email_input.value or "").strip().lower()
        password = password_input.value or ""
        imap_host = imap_host_input.value or ""
        smtp_host = smtp_host_input.value or ""

        if not email or not password or not imap_host or not smtp_host:
            _show_snackbar("Please fill in all fields", ft.Colors.RED_400)
            return

        if any(user.email.lower() == email for user in app_state.connected_emails):
            _show_snackbar("This account is already connected", ft.Colors.ORANGE_400)
            return

        if "@" not in email:
            _show_snackbar("Email must contain '@'", ft.Colors.ERROR)
            return

        local_part, default_host = email.split("@", 1)
        connection = EmailController().check_credentials(
            imap_username=imap_user_input.value or local_part,
            imap_password=imap_pass_input.value or password,
            imap_host=imap_host or default_host,
            imap_port=int(imap_port_input.value or 993),
            imap_security=ConnectionSecurity.SSL_TLS,
            imap_method=AuthMethods.PASSWORD,
            smtp_username=smtp_user_input.value or local_part,
            smtp_password=smtp_pass_input.value or password,
            smtp_host=smtp_host or default_host,
            smtp_port=int(smtp_port_input.value or 587),
            smtp_security=ConnectionSecurity.SSL_TLS,
            smtp_method=AuthMethods.PASSWORD,
        )

        if not connection:
            _show_snackbar("Connection failed", ft.Colors.ERROR)
            return

        try:
            user = AccountController.create_new_account(
                name_input.value.strip(),
                email,
                connection,
                Protocol.IMAP,
            )
            if isinstance(user, UserDTO):
                app_state.connected_emails.append(user)
            else:
                _load_connected_emails()
            _show_snackbar("Account added", ft.Colors.PRIMARY_CONTAINER)
        except ValueError as exc:
            _show_snackbar(str(exc), ft.Colors.ORANGE_400)
            _load_connected_emails()
        except Exception as exc:
            _show_snackbar(f"Error: {exc}", ft.Colors.RED_400)
            return

        _cancel_add()
        _refresh_accounts()

    def _remove_account(self, user: UserDTO) -> None:
        try:
            UserService.delete_user(user.id)
            app_state.remove_email_scheduler(user.email)
            app_state.connected_emails = [
                connected_user
                for connected_user in app_state.connected_emails
                if connected_user.id != user.id
            ]
            _show_snackbar("Account removed", ft.Colors.GREEN_400)
        except Exception as exc:
            _show_snackbar(f"Failed to remove user: {exc}", ft.Colors.ORANGE_400)
        _refresh_accounts()

    def _build_account_row(self, user: UserDTO) -> ft.Control:
        return ft.Container(
            ft.Row(
                [
                    ft.Icon(ft.Icons.EMAIL, color=ft.Colors.BLUE),
                    ft.Text(user.name or user.email, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Remove account",
                        on_click=lambda _, current_user=user: _remove_account(current_user),
                    ),
                ]
            ),
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            padding=10,
        )

    def _refresh_accounts(self) -> None:
        account_count = len(app_state.connected_emails)
        start_text.visible = account_count == 0
        accounts_counter.value = f"{account_count if account_count > 0 else 'No'} accounts connected"
        accounts_column.controls = [
            _build_account_row(user) for user in app_state.connected_emails
        ]
        for control in (start_text, accounts_counter, accounts_column):
            try:
            except RuntimeError:
                pass


def create_email_accounts_view(page: ft.Page, app_state: AppState) -> ft.Container:
    view = EmailAccountsView(app_state)
    view.set_page(page)
    return view.create_view()
