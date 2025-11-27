import flet as ft
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def ChatbotWidget():
    from remail.controllers.llm_controller import LLMController
    
    # Initialize LLM controller
    llm_controller = LLMController()
    
    # Chat display area
    chat_display = ft.ListView(
        expand=True,
        auto_scroll=True,
        spacing=10,
    )

    # Message input field
    message_input = ft.TextField(
        label="Type your message...",
        expand=True,
        min_lines=1,
        max_lines=3,
    )

    def get_ai_response(user_message):
        """Get AI response using LLM controller."""
        try:
            response = llm_controller.generate_completion(
                prompt=user_message,
                max_tokens=200,
                temperature=0.7,
            )
            
            if response["status"] == "success":
                return response["completion"]
            else:
                return f"Error: {response['message']}"
        
        except Exception as e:
            # Fallback response when LLM is unavailable
            return f"(LLM Server Unavailable) I received your message: '{user_message}'. Please make sure the LLM server is running at the configured base URL."

    def send_message(e):
        user_message = message_input.value.strip()

        if user_message:
            # Clear input immediately and update
            message_input.value = ""
            message_input.update()
            
            # Add user message to chat
            chat_display.controls.append(
                ft.Text(f"You: {user_message}", color="blue")
            )
            
            # Add loading indicator
            loading_indicator = ft.ProgressRing()
            loading_container = ft.Row(
                controls=[loading_indicator, ft.Text("AI is thinking...", color="gray")],
                spacing=10,
            )
            chat_display.controls.append(loading_container)
            chat_display.update()
            
            # Get AI response
            ai_response = get_ai_response(user_message)
            
            # Remove loading indicator
            chat_display.controls.remove(loading_container)
            
            # Add AI response
            chat_display.controls.append(
                ft.Text(f"AI: {ai_response}", color="green")
            )
            
            chat_display.update()

    message_input.on_submit = send_message

    send_button = ft.IconButton(
        "send",
        on_click=send_message,
    )

    # Input row
    input_row = ft.Row(
        controls=[message_input, send_button],
        spacing=10,
    )

    return ft.Column(
        controls=[
            ft.Text("Alfred 🤖", size=24, weight="bold"),
            chat_display,
            input_row,
        ],
        expand=True,
        spacing=10,
    )
