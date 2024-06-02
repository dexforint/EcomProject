from lib.llm import generate_header, change_header


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

            header_obj = generate_header(info["query"], theme=theme.description)

            self.text_color = (
                header_obj.get("text_color", None) or theme.header_text_color
            )
            self.text = header_obj.get("text", None) or "Заголовок"

        elif action == "change":
            header_obj = change_header(
                info["query"],
                theme=theme.description,
                prev_text_color=self.text_color,
                prev_text=self.text,
            )

            self.text_color = (
                header_obj.get("text_color", None) or theme.header_text_color
            )
            self.text = header_obj.get("text", None) or "Заголовок"
