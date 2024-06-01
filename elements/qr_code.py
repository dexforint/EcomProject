from lib.llm import llm
from lib.prompt_templates import qr_code_prompt
from lib.stable_diffusion import generate_qr_code
from lib.utils import get_random_string
import qrcode


class QRCode(object):
    is_present: bool = False
    is_generated: bool = False
    url: str | None = None
    path: str | None = None

    def process(self, info, theme):
        if info is None:
            return self

        action = info["action"]
        # ! НУЖНА ОБРАБОТКА LLM??

        if action in ("set", "change"):
            self.is_present = True
            if info["path"]:
                self.path = info["path"]
            else:
                url = info.get("url", self.url)
                if info.get("is_generated", False):
                    self.is_generated = True
                    llm_prompt = qr_code_prompt(theme.description)
                    sd_prompt = llm(llm_prompt)
                    path = generate_qr_code(url, sd_prompt)
                else:
                    self.is_generated = False
                    img = qrcode.make(url)
                    name = get_random_string(4)
                    path = f"./images/{name}.png"  # !!!
                    img.save(path)

                self.url = info["url"]
                self.path = path

        elif action == "delete":
            self.is_present = False
