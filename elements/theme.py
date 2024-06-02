from lib.llm import get_theme_object
from lib.utils import get_rgb


class Theme(object):
    description: str = None
    background_color: str | None = None
    button_text_color: str | None = None
    button_color: str | None = None
    header_text_color: str | None = None
    text_color: str | None = None

    header_text_font: str | None = None

    def process(self, query: str):
        theme = get_theme_object(query=query)

        self.description = theme["description"]
        self.background_color = theme["background_color"]
        self.background_color = get_rgb(self.background_color)

        self.button_text_color = theme["button_text_color"]
        self.button_text_color = get_rgb(self.button_text_color)

        self.button_color = theme["button_color"]
        self.button_color = get_rgb(self.button_color)

        self.header_text_color = theme.get("header_text_color", [255, 255, 255])
        self.header_text_color = get_rgb(self.header_text_color)

        self.text_color = theme.get("header_text_color", [255, 255, 255])
        self.text_color = get_rgb(self.text_color)

        self.header_text_font = theme.get("header_text_font", "Arial")

    def get_string(self):
        return f"""
        description: {self.description}
        background_color: RGB({self.background_color})
        button_text_color: RGB({self.button_text_color})
        button_color: RGB({self.button_color})
        header_text_color: RGB({self.header_text_color})
        text_color: RGB({self.text_color})
        header_text_font: RGB({self.header_text_font})
        """
