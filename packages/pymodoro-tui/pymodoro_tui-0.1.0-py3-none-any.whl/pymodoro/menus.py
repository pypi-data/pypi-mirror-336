from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.validation import Integer
from textual.widgets import Button, Input, Label

from pymodoro.events import ValuesUpdated


class SettingsMenu(Screen):
    def compose(self) -> ComposeResult:
        focus, break_dur, _ = self.app.db.get_db_values()

        with Container(id="settings-modal"):
            with Vertical():
                yield Label("Settings", classes="modal-title")
                yield Label("Focus Duration (minutes 1-59):")
                yield Input(
                    str(focus),
                    id="focus-input",
                    type="integer",
                    max_length=2,
                    validators=[Integer(minimum=1, maximum=59)],
                )
                yield Label("Break Duration (minutes 1-59):")
                yield Input(
                    str(break_dur),
                    id="break-input",
                    type="integer",
                    max_length=2,
                    validators=[Integer(minimum=1, maximum=59)],
                )
                with Horizontal():
                    yield Button("Save", id="save-settings")
                    yield Button("Cancel", id="cancel-settings")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save-settings":
            try:
                focus_dur = int(self.query_one("#focus-input", Input).value)
                break_dur = int(self.query_one("#break-input", Input).value)
                if focus_dur not in range(1, 60) or break_dur not in range(1, 60):
                    raise ValueError
                self.post_message(ValuesUpdated(new_values=(focus_dur, break_dur)))
                self.app.pop_screen()
                self.notify("Settings saved!", severity="information")
            except ValueError:
                self.notify("Invalid values! Use positive integers", severity="error")
        else:
            self.app.pop_screen()


class StatsMenu(Screen):
    def compose(self) -> ComposeResult:
        _, _, total_time_focused = self.app.db.get_db_values()

        with Container(id="stats-modal"):
            with Vertical():
                yield Label("Statistics", classes="modal-title")
                yield Label(f"Total Focus Time: {total_time_focused} min")
                with Horizontal():
                    yield Button("Close", id="close-stats")

    def on_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()
