from lib.llm import get_theme_object


class Theme(object):
    description: str = None
    background_color: str | None = None
    button_text_color: str | None = None
    button_color: str | None = None
    header_text_color: str | None = None
    text_color: str | None = None

    header_text_font: str | None = None

    def process(self, query: str):
        theme = get_theme_object(self, query=query)

        self.description = theme["description"]
        self.background_color = theme["background_color"]

        self.button_text_color = theme["button_text_color"]
        self.button_color = theme["button_color"]

        self.header_text_color = theme.get("header_text_color", "#ffffff")
        self.text_color = theme.get("header_text_color", "#ffffff")

        self.header_text_font = theme.get("header_text_font", "Arial")
