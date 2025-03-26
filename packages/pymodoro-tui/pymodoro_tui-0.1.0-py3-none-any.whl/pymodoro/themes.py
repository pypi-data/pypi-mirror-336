from textual.theme import Theme

focus_theme = Theme(
    name="focus",
    primary="#EF5350",
    secondary="#E57373",
    accent="#D32F2F",
    foreground="white",
    background="#ba4949",
    surface="#A63636",
    panel="#c15c5c",
    dark=True,
    success="#66BB6A",
    warning="#FFA726",
    error="#EF5350",
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#EF5350",
        "input-selection-background": "#E57373 35%",
    },
)

break_theme = Theme(
    name="break",
    primary="#26A69A",
    secondary="#4DB6AC",
    accent="#00796B",
    foreground="white",
    background="#38858a",
    surface="#19635C",
    panel="#4c9196",
    dark=True,
    success="#66BB6A",
    warning="#FFA726",
    error="#EF5350",
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#26A69A",
        "input-selection-background": "#4DB6AC 35%",
    },
)
