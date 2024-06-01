from lib.llm import llm


class Header(object):
    is_present: bool = False
    text_color: str | None = "#ffffff"
    text: str | None = None
    text_font: str | None = "Arial"

    def process(self, info, theme):
        if info is None:
            return self

        action = info["action"]
        # ! НУЖНА ОБРАБОТКА LLM??

        if action == "set":
            self.is_present = True
            self.text_color = info.get(
                "text_color", theme.header_text_color or self.text_color
            )
            self.text = info["text"]
            self.text_font = info.get(
                "text_font", theme.header_text_font or self.text_font
            )

        elif action == "change":
            self.is_present = info.get("is_present", self.is_present)
            self.text_color = info.get("text_color", self.text_color)
            self.text = info.get("text", self.text)
            self.text_font = info.get("text_font", self.text_font)
