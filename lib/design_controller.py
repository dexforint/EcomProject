from copy import deepcopy

from elements.background import Background
from elements.button import Button
from elements.header import Header
from elements.image import Image
from elements.qr_code import QRCode
from elements.text import Text
from elements.theme import Theme

from lib.llm import structure_query
from lib.pptx_tools import convert_pptx_to_image, render_pptx


class DesignController(object):
    default_n_variations = 3

    theme: Theme = Theme()
    background: Background = Background()
    image: Image = Image()
    header: Header = Header()
    text: Text = Text()
    button: Button = Button()
    qr_code: QRCode = QRCode()

    pptx_path = None
    img_path = None

    def create(self, query, path=None):
        info = {"query": query, "path": path, "action": "set"}

        self.theme.process(query=query)
        self.background.process(info=info, theme=self.theme)
        self.image.process(info=info, theme=self.theme)
        self.header.process(info=info, theme=self.theme)
        self.text.process(info=info, theme=self.theme, header=self.header.text)
        self.button.process(info=info, theme=self.theme)
        # self.qr_code.process(info=info, theme=self.theme)

    def change(self, query, path=None):
        info = structure_query(query)
        info["query"] = query
        info["path"] = path

        # self.theme.process(query=query)

        element = info["element"]

        if element == "background":
            self.background.process(info=info, theme=self.theme)
        elif element == "image":
            self.image.process(info=info, theme=self.theme)
        elif element == "header":
            self.header.process(info=info, theme=self.theme)
        elif element == "text":
            self.text.process(info=info, theme=self.theme, header=self.header.text)
        elif element == "button":
            self.button.process(info=info, theme=self.theme)
        # self.qr_code.process(info=info, theme=self.theme)

    def get_variations(self, n_variations=3):
        variations = []

        for index in range(n_variations):
            variation = deepcopy(self)

            variation.background.regenerate()
            variation.image.regenerate()

            variations.append(variation)

        return variations

    def render_image(self):
        self.pptx_path = self.render_pptx()
        self.img_path = convert_pptx_to_image(self.pptx_path)
        return self.img_path

    def render_pptx(self):
        self.pptx_path = render_pptx(self)
        return self.pptx_path
