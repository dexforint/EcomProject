from lib.llm import generate_text, change_text
from lib.utils import get_rgb


class Text(object):
    is_present: bool = False

    text: str
    text_color: str | None = [255, 255, 255]

    text_font: str | None = "Arial"

    def process(self, info, theme, header):
        if info is None:
            return self

        action = info["action"]

        if action == "set":
            self.is_present = True
            text_info = generate_text(
                query=info["query"], theme=theme.get_string(), header=header
            )

            self.text = text_info["text"]
            self.text_color = text_info["text_color"]
            self.text_color = get_rgb(self.text_color)

        elif action == "change":
            self.is_present = True
            text_info = change_text(
                query=info["query"],
                theme=theme.get_string(),
                prev_text=self.text,
                prev_text_color=self.text_color,
                header=header,
            )

            self.text = text_info["text"]
            self.text_color = text_info["text_color"]
            self.text_color = get_rgb(self.text_color)

        elif action == "delete":
            self.is_present: bool = False
