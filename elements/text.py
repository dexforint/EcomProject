from lib.llm import generate_text, change_text
from dataclasses import dataclass


@dataclass
class Text(object):
    is_present: bool = False

    text: str
    text_color: str | None = "#ffffff"

    text_font: str | None = "Arial"

    def process(self, info, theme, header):
        if info is None:
            return self

        action = info["action"]

        if action == "add":
            self.is_present = True
            text_info = generate_text(
                query=info["query"], theme=theme.desc, header=header
            )

            self.text = text_info["text"]
            self.text_color = text_info["text_color"]

        elif action == "change":
            self.is_present = True
            text_info = change_text(
                query=info["query"],
                theme=theme.desc,
                prev_text=self.text,
                prev_text_color=self.text_color,
                header=header,
            )

            self.text = text_info["text"]
            self.text_color = text_info["text_color"]

        elif action == "delete":
            self.is_present: bool = False
