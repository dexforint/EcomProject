from copy import deepcopy

from elements.background import Background
from elements.button import Button
from elements.header import Header
from elements.images import Images
from elements.qr_code import QRCode
from elements.texts import Texts
from elements.theme import Theme

from templates.internet_banner import InternetBannerTemplate


class DesignController(object):
    templates = [
        InternetBannerTemplate(),
        InternetBannerTemplate(),
        InternetBannerTemplate(),
        InternetBannerTemplate(),
        InternetBannerTemplate(),
        InternetBannerTemplate(),
        InternetBannerTemplate(),
    ]
    default_template_index = 4

    default_n_variations = 3

    theme: Theme = Theme()
    background: Background = Background()
    images: Images = Images()
    header: Header = Header()
    texts: Texts = Texts()
    button: Button = Button()
    qr_code: QRCode = QRCode()

    def __init__(self):
        for template in self.templates:
            template.controller = self

    def create(self, query, path=None):
        info = {"query": query, "path": path}

        self.theme.process(query=query)
        self.background.process(info=info, theme=self.theme)
        self.images.process(info=info, theme=self.theme)
        self.header.process(info=info, theme=self.theme)
        self.texts.process(info=info, theme=self.theme)
        self.button.process(info=info, theme=self.theme)
        self.qr_code.process(info=info, theme=self.theme)

    def change(self, query, path=None):
        info = {"query": query, "path": path}

        self.theme.process(query=query)
        self.background.process(info=info, theme=self.theme)
        self.images.process(info=info, theme=self.theme)
        self.header.process(info=info, theme=self.theme)
        self.texts.process(info=info, theme=self.theme)
        self.button.process(info=info, theme=self.theme)
        self.qr_code.process(info=info, theme=self.theme)

    def get_variations(self, n_variations=3):
        variations = []

        for index in range(n_variations):
            variation = deepcopy(self)

            variation.background.regenerate()
            variation.images.regenerate()

            variations.append(variation)

        return variations

    def render_image(self, template_index=None):
        if template_index is None:
            template_index = self.default_template_index

        template_index -= 1

        template = self.templates[template_index]
        return template.render_image()

    def render_pptx(self, template_index=None):
        if template_index is None:
            template_index = self.default_template_index

        template_index -= 1

        template = self.templates[template_index]
        return template.render_pptx()

    def render_all_images(self):
        template_images = []
        for template in self.templates.items():
            template_images.append(template.render_image())
        return template_images

    def render_all_pptx(self):
        template_pptx = []
        for template in self.templates.items():
            template_pptx.append(template.render_pptx())
        return template_pptx
