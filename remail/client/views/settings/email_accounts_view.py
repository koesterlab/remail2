from abc import ABC

import flet as ft

from remail.client.state.app_state import AppState
from remail.client.views.settings.settings_sub_view import SettingsSubView
from remail.controllers.account_controller import AccountController
from remail.controllers.dtos.user_dto import UserDTO
from remail.controllers.email_controller import EmailController
from remail.enums import AuthMethods, ConnectionSecurity, Protocol
from remail.interfaces.email.services.user_service import UserService


class EmailAccountsView(SettingsSubView, ABC):
    def __init__(self, app_state: AppState | None = None):
        super().__init__(route="email")
        self.app_state = app_state or AppState()
        self.smtp_user_input = ft.TextField(label="Username", hint_text="Enter SMTP username")
        self.smtp_pass_input = ft.TextField(
            label="Password",
            hint_text="Enter SMTP password",
            password=True,
            can_reveal_password=True,
        )
        self.smtp_port_input = ft.TextField(label="Port", hint_text="587")
        self.imap_user_input = ft.TextField(label="Username", hint_text="Enter IMAP username")
        self.imap_pass_input = ft.TextField(
            label="Password",
            hint_text="Enter IMAP password",
            password=True,
            can_reveal_password=True,
        )
        self.imap_port_input = ft.TextField(label="Port", hint_text="993")
        self.start_text = ft.Text("No accounts connected yet")
        self.accounts_counter = ft.Text(size=12)
        self.accounts_column = ft.Column()
        self.input_panel = ft.Container()
        self.add_button = ft.Container(
            ft.OutlinedButton("Add Email Account", icon=ft.Icons.ADD, on_click=self._show_add_form),
            alignment=ft.Alignment.CENTER,
            margin=ft.margin.only(top=20),
        )
        self.name_input = ft.TextField(label="Display Name", hint_text="Your Name", width=300)
        self.email_input = ft.TextField(
            label="Email address",
            hint_text="Enter your email address",
            width=300,
        )
        self.password_input = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            width=300,
        )
        self.imap_host_input = ft.TextField(
            label="IMAP Host",
            hint_text="Enter your IMAP host name",
            width=300,
            suffix=ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda _: self._open_imap_settings()),
        )
        self.smtp_host_input = ft.TextField(
            label="SMTP Host",
            hint_text="Enter your SMTP host name",
            width=300,
            suffix=ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda _: self._open_smtp_settings()),
        )

    def create_view(self) -> ft.Control:
        self._load_connected_emails()
        self._refresh_accounts()
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Email Accounts", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage your email accounts"),
                    ft.Divider(height=2, color=ft.Colors.GREY_400),
                    self.start_text,
                    self.accounts_counter,
                    self.accounts_column,
                    self.add_button,
                    self.input_panel,
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
        self.app_state.connected_emails = UserService.get_all_users()

    def _show_snackbar(self, message: str, color: str) -> None:
        snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def _close_dialog(self, dialog: ft.AlertDialog) -> None:
        dialog.open = False
        self.page.update()

    def _open_smtp_settings(self) -> None:
        dialog = ft.AlertDialog(
            title=ft.Text("Advanced SMTP Settings"),
            content=ft.Column(
                [self.smtp_user_input, self.smtp_pass_input, self.smtp_port_input],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self._close_dialog(dialog)),
                ft.TextButton(
                    "Save",
                    on_click=lambda _: (self._show_snackbar("SMTP settings saved!", ft.Colors.GREEN_400), self._close_dialog(dialog)),
                ),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _open_imap_settings(self) -> None:
        dialog = ft.AlertDialog(
            title=ft.Text("Advanced IMAP Settings"),
            content=ft.Column(
                [self.imap_user_input, self.imap_pass_input, self.imap_port_input],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self._close_dialog(dialog)),
                ft.TextButton(
                    "Save",
                    on_click=lambda _: (self._show_snackbar("IMAP settings saved!", ft.Colors.GREEN_400), self._close_dialog(dialog)),
                ),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _show_add_form(self, _=None) -> None:
        self.input_panel.content = ft.Column(
            [
                ft.Text("Add Email Account", size=16, weight=ft.FontWeight.BOLD),
                self.name_input,
                self.email_input,
                self.password_input,
                self.imap_host_input,
                self.smtp_host_input,
                ft.Row(
                    [
                        ft.OutlinedButton("Connect", icon=ft.Icons.CHECK, on_click=lambda _: self._connect_account()),
                        ft.OutlinedButton("Cancel", icon=ft.Icons.CLOSE, on_click=lambda _: self._cancel_add()),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )
        self.add_button.visible = False
        self.page.update()

    def _reset_inputs(self) -> None:
        self.name_input.value = ""
        self.email_input.value = ""
        self.password_input.value = ""
        self.imap_host_input.value = ""
        self.smtp_host_input.value = ""

    def _cancel_add(self) -> None:
        self._reset_inputs()
        self.input_panel.content = None
        self.add_button.visible = True
        self.page.update()

    def _connect_account(self) -> None:
        email = (self.email_input.value or "").strip().lower()
        password = self.password_input.value or ""
        imap_host = self.imap_host_input.value or ""
        smtp_host = self.smtp_host_input.value or ""

        if not email or not password or not imap_host or not smtp_host:
            self._show_snackbar("Please fill in all fields", ft.Colors.RED_400)
            return

        if any(user.email.lower() == email for user in self.app_state.connected_emails):
            self._show_snackbar("This account is already connected", ft.Colors.ORANGE_400)
            return

        if "@" not in email:
            self._show_snackbar("Email must contain '@'", ft.Colors.ERROR)
            return

        local_part, default_host = email.split("@", 1)
        connection = EmailController().check_credentials(
            imap_username=self.imap_user_input.value or local_part,
            imap_password=self.imap_pass_input.value or password,
            imap_host=imap_host or default_host,
            imap_port=int(self.imap_port_input.value or 993),
            imap_security=ConnectionSecurity.SSL_TLS,
            imap_method=AuthMethods.PASSWORD,
            smtp_username=self.smtp_user_input.value or local_part,
            smtp_password=self.smtp_pass_input.value or password,
            smtp_host=smtp_host or default_host,
            smtp_port=int(self.smtp_port_input.value or 587),
            smtp_security=ConnectionSecurity.SSL_TLS,
            smtp_method=AuthMethods.PASSWORD,
        )

        if not connection:
            self._show_snackbar("Connection failed", ft.Colors.ERROR)
            return

        try:
            user = AccountController.create_new_account(
                self.name_input.value.strip(),
                email,
                connection,
                Protocol.IMAP,
            )
            if isinstance(user, UserDTO):
                self.app_state.connected_emails.append(user)
            else:
                self._load_connected_emails()
            self._show_snackbar("Account added", ft.Colors.PRIMARY_CONTAINER)
        except ValueError as exc:
            self._show_snackbar(str(exc), ft.Colors.ORANGE_400)
            self._load_connected_emails()
        except Exception as exc:
            self._show_snackbar(f"Error: {exc}", ft.Colors.RED_400)
            return

        self._cancel_add()
        self._refresh_accounts()

    def _remove_account(self, user: UserDTO) -> None:
        try:
            UserService.delete_user(user.id)
            self.app_state.remove_email_scheduler(user.email)
            self.app_state.connected_emails = [
                connected_user
                for connected_user in self.app_state.connected_emails
                if connected_user.id != user.id
            ]
            self._show_snackbar("Account removed", ft.Colors.GREEN_400)
        except Exception as exc:
            self._show_snackbar(f"Failed to remove user: {exc}", ft.Colors.ORANGE_400)
        self._refresh_accounts()

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
                        on_click=lambda _, current_user=user: self._remove_account(current_user),
                    ),
                ]
            ),
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            padding=10,
        )

    def _refresh_accounts(self) -> None:
        account_count = len(self.app_state.connected_emails)
        self.start_text.visible = account_count == 0
        self.accounts_counter.value = f"{account_count if account_count > 0 else 'No'} accounts connected"
        self.accounts_column.controls = [
            self._build_account_row(user) for user in self.app_state.connected_emails
        ]
        for control in (self.start_text, self.accounts_counter, self.accounts_column):
            try:
                control.update()
            except RuntimeError:
                pass


def create_email_accounts_view(page: ft.Page, app_state: AppState) -> ft.Container:
    view = EmailAccountsView(app_state)
    view.set_page(page)
    return view.create_view()
