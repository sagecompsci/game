from dataclasses import dataclass

@dataclass
class Dialog:
    """
    text: str - What text should display in the text box

    options: dict[str, int] - what text should display in answer box, what dialog code clicking should go to
    """
    text: str
    options: dict[str, int]
