from lib.llm import (
    create_background_prompt,
    change_background_prompt,
)
from lib.stable_diffusion import (
    stable_diffusion_create_background,
)


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
                theme=theme.get_string(),
                background_color=theme.background_color,
            )
            path = stable_diffusion_create_background(sd_prompt)

        elif action == "change":  # !
            assert self.sd_prompt is not None

            sd_prompt = change_background_prompt(
                query=info["query"],
                theme=theme.get_string(),
                previous_background_prompt=self.sd_prompt,
                background_color=theme.background_color,
            )

            path = stable_diffusion_create_background(sd_prompt)

        else:
            path = self.path
            sd_prompt = self.sd_prompt

        self.path = path
        self.sd_prompt = sd_prompt

    def regenerate(self):
        self.path = stable_diffusion_create_background(self.sd_prompt)
