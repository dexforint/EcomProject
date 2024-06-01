from lib.llm import get_text_index
from dataclasses import dataclass


@dataclass
class Text(object):
    text: str
    text_color: str | None = "#ffffff"
    text_font: str | None = "Arial"


class Texts(object):
    texts = []

    def process(self, info, theme):
        if info is None:
            return self

        action = info["action"]
        # ! НУЖНА ОБРАБОТКА LLM??

        if action == "add":
            self.texts.append(Text(**info))  # !!!!!!

        elif action == "change":
            index = get_text_index(self.texts, info["query"])

            self.texts[index].text = info.get("text", self.texts[index].text)
            self.texts[index].text_color = info.get(
                "text_color", self.texts[index].text_color
            )
            self.texts[index].text_font = info.get(
                "text_font", self.texts[index].text_font
            )

        elif action == "delete":
            index = get_text_index(self.text, info["query"])
            self.texts.pop(index)
