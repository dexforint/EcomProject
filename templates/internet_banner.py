import numpy as np


class InternetBannerTemplate:
    width: int = 1200
    height: int = 593
    dpi: int = 72
    canvas: np.ndarray = np.zeros((height, width, 3), dtype=np.uint8)

    padding_left: int = 60
    padding_top: int = 60
    padding_bottom: int = 190
    padding_right: int = 0

    min_x: int = padding_left
    max_x = width - padding_right

    min_y = padding_top
    max_y = height - padding_bottom

    def __init__(self, unitool):
        self.unitool = unitool
        self.elements = {
            "theme": None,  # string
            "template": None,
            "background": {
                "presence": False,
            },
            "header": {
                "presence": False,
            },
            "texts": [],
            "button": {
                "presence": False,
            },
            "qr_code": {
                "presence": False,
            },
            "images": [],
        }

    def create(self, create_info):
        """Создаём начальные элементы по обработанному запросу"""
        theme = create_info.get("theme", None)  # !

        template = self.unitool.generate_template(
            theme, create_info.get("template", None)
        )

        background = self.unitool.generate_background(
            theme, create_info.get("background", None)
        )

        # header =

    def change(self, change_info):
        pass

    def render_image(self):
        pass

    def render_pptx(self):
        pass

    def render_text(self):
        pass


create_info = {"background": {""}}

change_info = {}
