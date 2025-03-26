import datetime

from textual.reactive import reactive
from textual.widgets import Digits

from pymodoro.enums import Phases
from pymodoro.events import PhaseChanged


class Timer(Digits):
    val = reactive(
        datetime.datetime(year=1, month=1, day=1, minute=0, second=0, microsecond=0)
    )
    update_timer = None
    current_phase = Phases.BREAK

    def __init__(self, focus_len, break_len):
        super().__init__()
        self.focus_len = focus_len
        self.break_len = break_len

    def on_mount(self):
        self.set_phase()
        self.update_timer = self.set_interval(1, self.update_val, pause=True)

    def update_val(self):
        prev_phase = self.current_phase
        if self.val.minute == 0 and self.val.second == 0:
            self.set_phase()
            self.pause()
        else:
            self.val -= datetime.timedelta(seconds=1)
        if (
            prev_phase == Phases.FOCUS
            and self.val.second == 0
            and self.val.minute < self.focus_len
        ):
            _, _, total_time_focused = self.app.db.get_db_values()
            self.app.db.update_setting(
                key="total_time_focused_minutes", value=total_time_focused + 1
            )

    def watch_val(self):
        self.update(f"{self.val.minute:02.0f}:{self.val.second:02.0f}")

    def set_phase(self, phase: Phases = None):
        if phase:
            self.current_phase = phase
        else:
            self.current_phase = (
                Phases.FOCUS if self.current_phase == Phases.BREAK else Phases.BREAK
            )
        self.val = self.val.replace(
            minute={"FOCUS": self.focus_len, "BREAK": self.break_len}[
                self.current_phase
            ],
            second=0,
            microsecond=0,
        )
        self.post_message(PhaseChanged(self.current_phase))

    def start(self):
        self.update_timer = self.set_interval(1, self.update_val, pause=True)
        self.val = self.val.replace(microsecond=0)
        self.update_timer.resume()

    def pause(self):
        self.val = self.val.replace(microsecond=0)
        self.update_timer.pause()
