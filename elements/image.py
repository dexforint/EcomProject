from lib.llm import generate_image_prompt, change_image_propmt
from lib.stable_diffusion import generate_image


class Image(object):
    path: str
    sd_prompt: str | None = None

    def process(self, info, theme):
        if info is None:
            return self

        action = info["action"]

        if action == "set" or self.path is None:
            sd_prompt = generate_image_prompt(
                query=info["query"],
                theme=theme.description,
                background_color=theme.background_color,
            )
            path = generate_image(sd_prompt)

        elif action == "change":  # !
            assert self.sd_prompt is not None

            sd_prompt = change_image_propmt(
                query=info["query"],
                theme=theme,
                previous_background_prompt=self.sd_prompt,
                background_color=theme.background_color,
            )

            path = generate_image(sd_prompt)

        else:
            path = self.path
            sd_prompt = self.sd_prompt

        self.path = path
        self.sd_prompt = sd_prompt

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
