import os
import time

import torch
import uvicorn
from diffusers import DiffusionPipeline
from fastapi import FastAPI
from pydantic import BaseModel

OUT_IP = "127.0.0.1"
# OUT_IP = "{Your-server-IP}"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = ROOT_DIR + "/models/stable-diffusion-xl-base-1.0"

# the image generated path, default in /var/www/html, if you start a httpd service, you can access by {OUT_IP/image.png}
GENERATED_IMAGES_PATH = "/var/www/html"

pipe = DiffusionPipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.float16,
                                         use_safetensors=True, variant="fp16")
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)

app = FastAPI()


class SDPrompt(BaseModel):
    prompt: str = None
    image_name: str = None
    image_type: str = "png"


@app.post("/generate_img")
def generate_image(sd_prompt: SDPrompt):
    try:
        prompt = sd_prompt.prompt
        image_name = sd_prompt.image_name
        image_type = sd_prompt.image_type

        if image_name is None:
            raise Exception("input param 'image_name' should not be empty!")

        image = pipe(prompt=prompt).images[0]
        tmp_dir = create_tmp_folder()
        img_name = f"{image_name}.{image_type}"
        ret_dir = os.path.join(tmp_dir, img_name)
        image.save(ret_dir)

        ret_dir = ret_dir.replace(GENERATED_IMAGES_PATH + '/', '')
        return {"success": True, "msg": f"downloadUrl= http://{OUT_IP}/{ret_dir}"}
    except Exception as e:
        return {"success": False, "msg": f"generate image error: {str(e)}"}


def create_tmp_folder():
    timestamp = int(time.time())
    folder_name = os.path.join(GENERATED_IMAGES_PATH, str(timestamp))
    if os.path.exists(folder_name):
        raise Exception(f"folder {folder_name} was existed!")
    else:
        os.mkdir(folder_name)
    return folder_name


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info")