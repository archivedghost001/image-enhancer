import requests
from api import fire_key
from tqdm import tqdm  # taqqadum = process
import sys
from datetime import datetime


def upscaling(img):
    response = requests.post(
        'https://www.cutout.pro/api/v1/photoEnhance',
        files={'file': open(img, 'rb')},
        headers={'APIKEY': fire_key},
        stream=True,  # Enable streaming response content
    )
    # get response content length in bytes
    total_length = int(response.headers.get("content-length", 0))

    # create progress bar
    progress_bar = tqdm(total=total_length, unit="iB")
    if response.status_code == requests.codes.ok:
        with open("output/result-%s.png" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'wb') as out:
            for i in response.iter_content(chunk_size=1024):
                if i:
                    # update progress bar
                    progress_bar.update(len(i))

                    out.write(i)
    else:
        print("Error:", response.status_code, response.text)

    # close progress bar after download
    progress_bar.close()


image_path = sys.argv[1]

upscaling(image_path)
