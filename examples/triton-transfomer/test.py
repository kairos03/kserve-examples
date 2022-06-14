import os

import numpy as np
import requests
from kserve import KServeClient
from PIL import Image
from base64 import b64encode


# INGRESS_HOST = os.environ["INGRESS_HOST"]
# INGRESS_PORT = os.environ["INGRESS_PORT"]
# HOST = f"http://{INGRESS_HOST}:{INGRESS_PORT}"

USERNAME = "user@example.com"
PASSWORD = "12341234"

NAME = "onnx-cifar10"
MODEL = "cifar10"
# NAMESPACE = os.environ["NAMESPACE"]


def single_prediction():
    with requests.Session() as session:
        # Auth
        img_fname = "data/cat.jpg"  # "data/horse.jpg"

        print("=" * 10)
        print("image name :", img_fname)
        print("=" * 10)

        with open(img_fname, 'rb') as f:
            data = b64encode(f.read())

        inputs = {
            "inputs": [
                {
                    # "name": "input",
                    # "shape": "",
                    # "datatype": "FP32",
                    "data": data.decode('utf-8'),
                }
            ]
        }
        # url = f"{HOST}/v2/models/{MODEL}/infer"
        # headers = {
        #     "Host": model_url.split("/")[-1],
        # }
        # cookies = {
        #     "authservice_session": session_cookie,
        # }
        url="http://localhost:8080"
        # response = session.post(url, headers=headers, cookies=cookies, json=inputs)
        response = session.post(url, json=inputs)
        # print(response.json())
        print(response.content)
        # predict = response.json()["outputs"][0]["data"]

        # classes = [
        #     "airplain",
        #     "automobile",
        #     "bird",
        #     "cat",
        #     "deer",
        #     "dog",
        #     "frog",
        #     "horse",
        #     "ship",
        #     "truck",
        # ]

        # label = np.argmax(predict)
        # print("=> Prediction :", classes[label])


if __name__ == "__main__":
    single_prediction()
