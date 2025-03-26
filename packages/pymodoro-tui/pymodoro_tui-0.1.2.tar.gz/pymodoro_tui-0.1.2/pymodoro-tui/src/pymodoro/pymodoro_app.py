from textual.app import App
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header

from pymodoro.db import Database
from pymodoro.enums import Phases, Themes
from pymodoro.events import PhaseChanged, ValuesUpdated
from pymodoro.menus import SettingsMenu, StatsMenu
from pymodoro.themes import break_theme, focus_theme
from pymodoro.timer import Timer


class Pymodoro(App):
    CSS_PATH = "pymodoro.tcss"
    db = Database()

    BINDINGS = [
        ("i", "show_stats", "Stats"),
        ("s", "toggle_settings", "Settings"),
        ("^q", "quit", "Quit"),
    ]

    def action_toggle_settings(self):
        """Toggle settings screen"""
        self.push_screen(SettingsMenu())

    def action_show_stats(self):
        """Show statistics screen"""
        self.push_screen(StatsMenu())

    def action_quit(self):
        """Exit the application"""
        self.exit()

    def on_mount(self):
        self.register_theme(focus_theme)
        self.register_theme(break_theme)
        self.theme = Themes.FOCUS

    def compose(self):
        yield Header()
        with Vertical() as vs:
            vs.border_title = "Pomodoro Timer"
            vs.border_subtitle = "https://github.com/alexanderchainsaw/Pymodoro"
            with Container():
                # with Horizontal(classes="mainmenu"):
                #     yield Button("Stats", id="Stats")
                #     yield Button("Settings", id="Settings")
                # TODO!
                #  menus calle with buttons (like in elia)
                with Horizontal(classes="trifecta mainmenu"):

                    yield Button("Focus", id="focus")
                    yield Button("Break", id="on_break")

                with Horizontal(classes="mainmenu"):
                    focus_duration, break_duration, _ = self.db.get_db_values()
                    yield Timer(focus_len=focus_duration, break_len=break_duration)

                with Horizontal(classes="mainmenu"):
                    yield Button("START", id="start")
                    yield Button("PAUSE", id="pause")
                    yield Button(">>", id="skip")
        yield Footer()

    def started(self):
        self.add_class("started")

    def paused(self):
        self.remove_class("started")

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id

        if button_id in ("start", "pause", "skip"):
            timer = self.query_one(Timer)
            if button_id == "start":
                self.started()
                timer.start()
            elif button_id == "pause":
                self.paused()
                timer.pause()
            elif button_id == "skip":
                self.paused()
                timer.set_phase()
                timer.pause()
        elif event.button.id == "Settings":
            self.push_screen(SettingsMenu())
        elif event.button.id == "Stats":
            self.push_screen(StatsMenu())

    def on_phase_changed(self, event: PhaseChanged) -> None:
        match event.phase:
            case Phases.FOCUS:
                self.theme = Themes.FOCUS
                self.remove_class("focused")
            case Phases.BREAK:
                self.add_class("focused")
                self.theme = Themes.BREAK

        self.paused()
        self.refresh_css()

    def on_values_updated(self, event: ValuesUpdated):
        timer = self.query_one(Timer)
        timer.focus_len, timer.break_len = event.focus_len, event.break_len
        self.db.update_setting(key="focus_duration", value=event.focus_len)
        self.db.update_setting(key="break_duration", value=event.break_len)
        timer.set_phase(phase=timer.current_phase)
