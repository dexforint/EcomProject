from fastapi import background
from lib.llm import generate_button, change_button


class Button(object):
    is_first: bool = True
    is_present: bool = False

    background_color: list = [255, 0, 50]
    text_color: list = [255, 255, 255]
    text: str | None = "Подробнее"

    border_radius: int | None = 10

    def process(self, info, theme):
        if info is None:
            return

        action = info["action"]
        # ! НУЖНА ОБРАБОТКА LLM??

        if action == "set" or self.is_first:
            self.is_present = True

            button_obj = generate_button(info["query"], theme=theme.description)

            self.background_color = (
                button_obj.get("background_color", None)
                or theme.button_background_color
            )
            self.text_color = (
                button_obj.get("text_color", None) or theme.button_text_color
            )
            self.text = button_obj.get("text", None) or "Подробнее"
            self.border_radius = button_obj.get("border_radius", None) or 10

        elif action == "change":
            button_obj = change_button(
                info["query"],
                theme=theme.description,
                prev_background_color=self.background_color,
                prev_text_color=self.text_color,
                prev_text=self.text,
            )

            self.background_color = (
                button_obj.get("background_color", None)
                or theme.button_background_color
            )
            self.text_color = (
                button_obj.get("text_color", None) or theme.button_text_color
            )
            self.text = button_obj.get("text", None) or "Подробнее"
            self.border_radius = button_obj.get("border_radius", None) or 10

        self.is_first = False
