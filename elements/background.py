from lib.llm import (
    create_background_prompt,
    correct_background_prompt,
)
from lib.stable_diffusion import (
    stable_diffusion_create_background,
    stable_diffusion_correct_background,
    stable_diffusion_create_image,
    stable_diffusion_edit_image,
)
from lib.llm import llm


class Background(object):
    path: str | None = None
    sd_prompt: str | None = None

    def process(self, info, theme):
        if info is None:
            return

        action = info["action"]

        if action == "set" or self.path is None:
            sd_prompt = create_background_prompt(
                query=info["query"],
                theme=theme.desc,
                background_color=theme.background_color,
            )
            path = stable_diffusion_create_background(sd_prompt)

        elif action == "correct":  # !
            assert self.sd_prompt is not None

            sd_prompt = correct_background_prompt(
                query=info["query"],
                theme=theme,
                previous_background_prompt=self.sd_prompt,
                background_color=theme.background_color,
            )

            path = stable_diffusion_correct_background(sd_prompt)

        else:
            path = self.path
            sd_prompt = self.sd_prompt

        self.path = path
        self.sd_prompt = sd_prompt

    def regenerate(self):
        self.path = stable_diffusion_create_background(self.sd_prompt)
