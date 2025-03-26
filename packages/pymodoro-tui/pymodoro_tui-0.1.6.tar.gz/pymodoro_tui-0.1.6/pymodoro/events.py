from textual.events import Event


class PhaseChanged(Event):
    def __init__(self, phase: str) -> None:
        super().__init__()
        self.phase = phase


class ValuesUpdated(Event):
    def __init__(self, new_values: tuple[int, int]) -> None:
        super().__init__()
        self.focus_len, self.break_len = new_values
