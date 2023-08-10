# StableDiffusion-Proxy: Own your private StableDiffusion Service.

## Installation

```commandline
mkdir models & cd models
git lfs install 
git clone https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

pip install -r requirements.txt
python main.py
```

Note: If you want to generate image links that can be directly used, modify the params `{Your-server-IP}` in `main.py`, it is recommended to deploy on a cloud service and you need to start a httpd service.

```commandline
sudo yum install httpd
sudo systemctl start httpd
```


## Test
``` bash
curl -X POST -H "Content-Type: application/json" -d '{
"prompt": "a Beautiful girl ride a white horse, Gorgeous, Elegant, Graceful, Radiant, Stunning, Alluring, Enchanting, Captivating, Mesmerizing, Lovely, Exquisite, Charming, Delicate, Sophisticated, Glamorous, Dazzling, Angelic, Ethereal, Breath-taking",
"image_name": "beautiful_girl"
}' http://120.27.193.115:7860/generate_img
```


```json
{
    "success": true,
    "msg": "downloadUrl= http://120.27.193.115/beautiful_girl.png"
}
```

![beautiful_girl](assets/beautiful_girl.png)


