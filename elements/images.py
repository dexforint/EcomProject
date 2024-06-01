from lib.llm import generate_image_prompt, get_img_index, change_image_propmt
from lib.stable_diffusion import generate_image


class Image(object):
    path: str
    sd_prompt: str | None = None

    def __init__(self, path=None, query=None, theme=None):
        if not (path is not None):
            self.path = None
            return

        self.sd_prompt = generate_image_prompt(query=query, theme=theme)
        self.path = generate_image(self.sd_prompt)

    def regenerate(self):
        self.path = generate_image(self.sd_prompt)


class Images(object):
    images: list[Image] = []

    def regenerate(self):
        for image in self.images:
            image.regenerate()

    def process(self, info, theme):
        if info is None:
            return self

        action = info["action"]
        # ! НУЖНА ОБРАБОТКА LLM??

        if action == "add":
            self.images.append(
                Image(
                    path=info.get("path", None),
                    query=info.get("query", None),
                    theme=theme,
                )
            )  # !!!!!!

        elif action == "change":
            index = get_img_index(self.images, info["query"])

            img = self.images[index]

            path = info.get("path", None)
            if path is not None:
                img.path = path
            else:
                img.sd_prompt = change_image_propmt(img.sd_prompt, info["query"], theme)
                img.regenerate()

        elif action == "delete":
            index = get_img_index(self.text, info["query"])
            self.texts.pop(index)
