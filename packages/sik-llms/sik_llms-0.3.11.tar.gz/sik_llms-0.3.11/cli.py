from copy import deepcopy
import os
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container
from textual.widgets import TextArea, Static
import subprocess
import json
from sik_llms import OpenAI, create_client, user_message, TextChunkEvent
from sik_llms.models_base import (
    assistant_message, system_message, ThinkingEvent,
    ToolPredictionEvent, ToolResultEvent, ErrorEvent,
    TextResponse,
)
from sik_llms.reasoning_agent import ReasoningAgent
from rich.syntax import Syntax
from rich.text import Text
from rich.console import Console
from sik_llms.mcp_manager import MCPClientManager

DEFAULT_MESSAGES = [system_message("You are a CLI conda assistant. Give helpful and detailed but concise replies. Prefer conda over pip when possible.")]  # noqa: E501

class CustomTextArea(TextArea):
    async def _on_key(self, event) -> None:
        if event.key == "enter" and self.app.multiline_mode:
            await super()._on_key(event)
        elif event.key == "enter":
            event.prevent_default()
            event.stop()
            await self.app.handle_submission(self.text)
        else:
            await super()._on_key(event)

def escape_markup(text: str) -> str:
    """Escapes only characters that would interfere with Textual's markup syntax"""
    return text.replace('[', r'\[') \
              .replace(']', r'\]') \
              .replace('\\[', r'\\[') \
              .replace('\\]', r'\\]')

class ChatTerminalApp(App):
    CSS = """
    Screen {
        layers: base overlay;
        background: white;
        color: black;
    }
    
    .output-container {
        height: 80%;
        border: solid green;
        margin: 0;
        padding: 1;
        overflow-y: auto;
        scrollbar-gutter: stable;
        overflow-x: hidden;
    }
    
    .status-container {
        height: 3;
        margin: 0;
        padding-left: 1;
        padding-top: 2;
    }
    
    .input-container {
        height: 15%;
        margin: 0;
        padding: 0;
    }

    TextArea {
        background: white;
        color: black;
        border: solid blue;
    }

    TextArea.terminal-mode {
        border: solid red;
        background: #2b2b2b;
        color: #ffffff;
    }

    TextArea.agent-mode {
        border: solid purple;
        background: white;
        color: black;
    }

    #output {
        width: 100%;
        background: white;
        color: black;
        border: none;
    }

    #status {
        text-align: left;
    }
    """

    def __init__(self):
        super().__init__()
        self.mode = "chat"
        self.multiline_mode = False
        self.raw_content = ""
        self.messages = deepcopy(DEFAULT_MESSAGES)  # noqa: E501
        if os.path.exists("mcp_servers.json"):
            self.mcp_manager = MCPClientManager(configs="./mcp_servers.json")
        else:
            self.mcp_manager = None


    def compose(self) -> ComposeResult:
        with ScrollableContainer(classes="output-container") as output_container:
            yield Static(id="output")
        with Container(classes="status-container"):
            yield Static("MODE: chat | ENTER: submit", id="status")
        with Container(classes="input-container"):
            yield CustomTextArea(id="input")

    def update_status(self) -> None:
        mode_text = "terminal" if self.mode == "terminal" else ("agent" if self.mode == "agent" else "chat")
        input_text = "new-line" if self.multiline_mode else "submit"
        self.query_one("#status").update(f"MODE: {mode_text} | ENTER: {input_text}")
        
        # Add or remove mode classes based on mode
        input_area = self.query_one("#input")
        input_area.remove_class("terminal-mode")
        input_area.remove_class("agent-mode")
        
        if self.mode == "terminal":
            input_area.add_class("terminal-mode")
            input_area.placeholder = "$ "
        elif self.mode == "agent":
            input_area.add_class("agent-mode")
            input_area.placeholder = "Ask the agent..."
        else:
            input_area.placeholder = ""

    async def on_key(self, event) -> None:
        if event.key == "ctrl+c":
            self.exit()
        elif event.key == "ctrl+t":
            # Cycle through modes: chat -> terminal -> agent -> chat
            if self.mode == "chat":
                self.mode = "terminal"
            elif self.mode == "terminal":
                self.mode = "agent"
            else:
                self.mode = "chat"
            self.update_status()
        elif event.key == "ctrl+l":
            self.multiline_mode = not self.multiline_mode
            self.update_status()

    async def handle_submission(self, text: str) -> None:
        if not text.strip():
            return
            
        output = self.query_one("#output", Static)
        input_area = self.query_one("#input", TextArea)
        input_area.clear()
        scroll_container = self.query_one(ScrollableContainer)
        
        if self.mode == "chat":
            # Add user message
            self.messages.append(user_message(text))
            if self.raw_content:
                self.raw_content += "\n"
            self.raw_content += f"[blue]USER:[/blue]\n{text}\n\n[green]ASSISTANT:[/green]\n"
            output.update(self.raw_content)

            # Create client and message
            client = create_client(
                model_name='gpt-4o-mini',
                temperature=0.1,
            )
            # Stream the response
            response = ""
            async for event in client.stream(messages=self.messages):
                if isinstance(event, TextChunkEvent):
                    self.raw_content += event.content
                    response += event.content
                    output.update(self.raw_content)
                    scroll_container.scroll_end(animate=False)
            self.raw_content += "\n"
            self.messages.append(assistant_message(response))

        elif self.mode == "agent":
            # Add user message
            if self.raw_content:
                self.raw_content += "\n"
            self.raw_content += f"[blue]USER:[/blue]\n{text}\n\n"
            output.update(self.raw_content)

            tools = []
            if self.mcp_manager:
                await self.mcp_manager.connect_servers()
                tools = self.mcp_manager.get_tools()
            try:
                # Stream the agent's response
                agent = ReasoningAgent(
                    model_name='gpt-4o-mini',
                    tools=tools,
                    max_iterations=10,
                    temperature=0.1,
                )

                current_iteration = 0
                async for event in agent.stream(messages=[user_message(text)]):
                    if isinstance(event, ThinkingEvent):
                        if hasattr(event, 'iteration') and event.iteration != current_iteration:
                            current_iteration = event.iteration
                            # self.raw_content += f"\n[magenta]--- Iteration {current_iteration} ---[/magenta]\n"
                        if event.content:
                            self.raw_content += f"\n[orange]THINKING:[/orange]\n{event.content}\n"

                    elif isinstance(event, ToolPredictionEvent):
                        self.raw_content += f"\n[purple]TOOL PREDICTION:[/purple]\n"
                        self.raw_content += f"Tool: `{event.name}`\n"
                        self.raw_content += f"Parameters:\n```json\n{json.dumps(event.arguments, indent=2)}\n```\n"

                    elif isinstance(event, ToolResultEvent):
                        self.raw_content += f"\n[purple]TOOL RESULT:[/purple]\n"
                        self.raw_content += f"Tool: `{event.name}`\n"
                        self.raw_content += f"Result: {event.result}\n"

                    elif isinstance(event, ErrorEvent):
                        self.raw_content += f"\n[red]ERROR:[/red]\n"
                        self.raw_content += f"Error: {event.content}\n"

                    elif isinstance(event, TextChunkEvent):
                        if current_iteration >= 0:  # Only print header once
                            self.raw_content += f"\n[green]FINAL RESPONSE:[/green]\n"
                            current_iteration = -1  # Prevent header from showing again
                        self.raw_content += event.content

                    output.update(self.raw_content)
                    scroll_container.scroll_end(animate=False)

            finally:
                if self.mcp_manager:
                    await self.mcp_manager.cleanup()
            self.raw_content += "\n\n[magenta]---[/magenta]\n"

        else:
            try:
                if text.strip() == "clear":
                    output.update("")
                    self.raw_content = ""
                    self.messages = deepcopy(DEFAULT_MESSAGES)
                    return
                result = subprocess.run(
                    text,
                    capture_output=True,
                    text=True,
                    shell=True
                )
                output_text = result.stdout if result.stdout else result.stderr
                if self.raw_content:
                    self.raw_content += "\n"
                # Escape special characters and use Textual's markup for terminal output
                escaped_output = escape_markup(output_text)
                content = f"$ {text}\n[monospace]{escaped_output}[/monospace]"
                self.raw_content += content
                self.messages.append(user_message("[PREVIOUS COMMAND]\n\n" + content))
                output.update(self.raw_content)
            except Exception as e:
                if self.raw_content:
                    self.raw_content += "\n"
                self.raw_content += f"Error: {str(e)}"
                output.update(self.raw_content)
        scroll_container.scroll_end(animate=False)

if __name__ == "__main__":
    app = ChatTerminalApp()
    app.run()