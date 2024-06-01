from copy import deepcopy

from elements.background import Background
from elements.button import Button
from elements.header import Header
from elements.image import Image
from elements.qr_code import QRCode
from elements.text import Text
from elements.theme import Theme

from lib.llm import structure_query


class DesignController(object):
    default_n_variations = 3

    theme: Theme = Theme()
    background: Background = Background()
    image: Image = Image()
    header: Header = Header()
    texts: Text = Text()
    button: Button = Button()
    qr_code: QRCode = QRCode()

    def create(self, query, path=None):
        info = {"query": query, "path": path}

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

        self.background.process(info=info, theme=self.theme)
        self.image.process(info=info, theme=self.theme)
        self.header.process(info=info, theme=self.theme)
        self.text.process(info=info, theme=self.theme)
        self.button.process(info=info, theme=self.theme)
        # self.qr_code.process(info=info, theme=self.theme)

    def get_variations(self, n_variations=3):
        variations = []

        for index in range(n_variations):
            variation = deepcopy(self)

            variation.background.regenerate()
            variation.images.regenerate()

            variations.append(variation)

        return variations

    def render_image(self, template_index=None):
        pass

    def render_pptx(self, template_index=None):
        pass
