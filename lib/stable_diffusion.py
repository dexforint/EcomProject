import torch
from rembg import new_session, remove
from diffusers import StableDiffusionXLPipeline, DPMSolverSinglestepScheduler

from lib.utils import get_random_string

pipe = StableDiffusionXLPipeline.from_pretrained(
    "sd-community/sdxl-flash", torch_dtype=torch.float16
).to(
    "cuda"
)  # , variant="fp16"

# Ensure sampler uses "trailing" timesteps.
pipe.scheduler = DPMSolverSinglestepScheduler.from_config(
    pipe.scheduler.config, timestep_spacing="trailing"
)


session = new_session("isnet-general-use")


def generate_image(sd_prompt):
    img = pipe(
        sd_prompt["prompt"],
        negative_prompt=sd_prompt["negative_prompt"],
        num_inference_steps=6,
        guidance_scale=3,
        width=512,
        height=512,
    ).images[0]

    img = remove_background(img)

    name = get_random_string(4)
    path = f"./images/{name}.png"
    img.save(path)
    return path


def remove_background(img):
    global session
    rmbg = remove(img, session=session)
    return rmbg


def stable_diffusion_create_background(sd_prompt):
    img = pipe(
        sd_prompt["prompt"],
        negative_prompt=sd_prompt["negative_prompt"],
        num_inference_steps=6,
        guidance_scale=3,
        width=1200,
        height=593,
    ).images[0]

    name = get_random_string(4)
    path = f"./images/{name}.png"
    img.save(path)
    return path
