import flet as ft

from remail.client.state.app_state import AppState


def create_email_accounts_view(page: ft.Page, app_state: AppState) -> ft.Container:
    """Create the email accounts settings view."""

    start_text = ft.Text("No accounts connected yet")
    input_panel = ft.Container()
    email_input = ft.TextField(label="Email Address", hint_text="Enter your email", width=300)
    password_input = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        password=True,
        can_reveal_password=True,
        width=300,
    )

    def add_account_click(e):
        # Hier muss man email addieren
        input_panel.content = ft.Column(
            [
                ft.Text("Add Email Account", size=16, weight=ft.FontWeight.BOLD),
                email_input,
                password_input,
                ft.Row(
                    [
                        ft.OutlinedButton("Connect", icon=ft.Icons.CHECK, on_click=connect_account),
                        ft.OutlinedButton("Cancel", icon=ft.Icons.CLOSE, on_click=cancel_add),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )

        # Versteckt die "Add Email Account" Button
        add_button.visible = False

        page.update()

    def connect_account(e):
        # Prüft, ob beide Felder ausgefüllt sind
        if email_input.value and password_input.value:
            start_text.visible = False

            # Erstellt ein neues Account-Element
            new_account = ft.Container(
                ft.Row(
                    [
                        ft.Icon(ft.Icons.EMAIL, color=ft.Colors.BLUE),
                        ft.Text(email_input.value, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, tooltip="Remove account"
                        ),
                    ]
                ),
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=5,
                padding=10,
                margin=ft.margin.only(bottom=5),
            )

            # Fügt den neuen Account vor dem input_panel ein
            create_connected_email_accounts.content.controls.insert(-2, new_account)

            # Leert die Eingabefelder
            email_input.value = ""
            password_input.value = ""
            input_panel.content = None

            # Zeigt die "Add Email Account" Button wieder an
            add_button.visible = True

            page.update()
        else:
            # Zeigt eine Fehlermeldung, wenn nicht alle Felder ausgefüllt sind
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Please fill in all fields"), bgcolor=ft.Colors.RED_400)
            )

    def cancel_add(e):
        # Leert die Eingabefelder beim Abbrechen
        email_input.value = ""
        password_input.value = ""
        input_panel.content = None

        add_button.visible = True

        page.update()

    add_button = ft.Container(
        ft.OutlinedButton(
            "Add Email Account",
            icon=ft.Icons.ADD,
            on_click=add_account_click,
        ),
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=20),
    )

    create_connected_email_accounts = ft.Container(
        ft.Column(
            [
                ft.Text("Email Accounts", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Manage your email accounts"),
                ft.Divider(height=2, color=ft.Colors.GREY_400),
                start_text,
                add_button,
                input_panel,
            ],
            spacing=15,
        ),
        padding=20,
        border_radius=10,
        alignment=ft.alignment.center_left,
    )

    return create_connected_email_accounts
