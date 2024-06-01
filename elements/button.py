from lib.llm import llm


class Button(object):
    is_first: bool = True
    is_present: bool = False
    background_color: str | None = None
    text_color: str | None = "#ffffff"
    text: str | None = "Подробнее"
    border_radius: int | None = 10

    def process(self, info, theme):
        if info is None:
            return

        action = info["action"]
        # ! НУЖНА ОБРАБОТКА LLM??

        if action == "set" or self.is_first:
            self.is_present = True
            self.background_color = info.get(
                "background_color", theme.button_background_color
            )
            self.text_color = info.get("text_color", theme.button_text_color)
            self.text = info.get("text", "Подробнее")
            self.border_radius = info.get("border_radius", 10)

        elif action == "change":
            self.is_present = info.get("is_present", self.is_present)
            self.background_color = info.get("background_color", self.background_color)
            self.text_color = info.get("text_color", self.text_color)
            self.text = info.get("text", self.text)
            self.border_radius = info.get("border_radius", self.border_radius)

        self.is_first = False
