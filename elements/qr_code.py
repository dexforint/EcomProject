from lib.utils import get_random_string
import qrcode


class QRCode(object):
    is_present: bool = False
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

                self.is_generated = False
                img = qrcode.make(url)
                name = get_random_string(4)
                path = f"./images/{name}.png"  # !!!
                img.save(path)

                self.url = info["url"]
                self.path = path

        elif action == "delete":
            self.is_present = False
