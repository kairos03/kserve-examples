from kserve import KServeClient

import os
import json
import requests
from PIL import Image
import numpy as np

INGRESS_HOST = os.environ["INGRESS_HOST"]
INGRESS_PORT = os.environ["INGRESS_PORT"]
HOST = f"http://{INGRESS_HOST}:{INGRESS_PORT}"

USERNAME = "user@example.com"
PASSWORD = "12341234"

NAME = "onnx-cifar10"
MODEL = "cifar"
NAMESPACE = os.environ["NAMESPACE"]


def to_numpy(im):
    im.load()
    # unpack data
    e = Image._getencoder(im.mode, "raw", im.mode)
    e.setimage(im.im)

    # NumPy buffer for the result
    shape, typestr = Image._conv_type_shape(im)
    data = np.empty(shape, dtype=np.dtype(typestr))
    mem = data.data.cast("B", (data.data.nbytes,))

    bufsize, s, offset = 65536, 0, 0
    while not s:
        l, s, d = e.encode(bufsize)
        mem[offset : offset + len(d)] = d
        offset += len(d)
    if s < 0:
        raise RuntimeError("encoder error %d in tobytes" % s)
    return data


def normalize(inputs, mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)):
    inputs = inputs.astype("float32")
    new = np.empty_like(inputs)
    for i, img in enumerate(inputs):
        new[i] = (img - mean[i]) / std[i]
    return new


def single_prediction():
    with requests.Session() as session:
        # Auth
        response = session.get(HOST)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"login": USERNAME, "password": PASSWORD}
        session.post(response.url, headers=headers, data=data)
        session_cookie = session.cookies.get_dict()["authservice_session"]

        # Prepare model info and data
        KServe = KServeClient()
        model = KServe.get(NAME, namespace=NAMESPACE)
        model_url = model["status"]["url"]

        # image transform
        img_fname = "data/cat.jpg"  # "data/horse.jpg"
        im = Image.open(img_fname).convert("RGB")
        np_img = to_numpy(im)
        np_img = np.transpose(np_img, (2, 0, 1))
        np_img = np_img / 255.0  # toTensor ([0, 255] to [0., 1.])
        np_img = normalize(np_img, (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        np_img = np.expand_dims(np_img, 0)

        print("=" * 10)
        print("image name :", img_fname)
        print("image shape:", np_img.shape)
        print("=" * 10)

        inputs = {
            "inputs": [
                {
                    "name": "input",
                    "shape": np_img.shape,
                    "datatype": "FP32",
                    "data": np_img.tolist(),
                }
            ]
        }
        url = f"{HOST}/v2/models/{MODEL}/infer"
        headers = {
            "Host": model_url.split("/")[-1],
        }
        cookies = {
            "authservice_session": session_cookie,
        }
        response = session.post(url, headers=headers, cookies=cookies, json=inputs)
        predict = response.json()["outputs"][0]["data"]

        classes = [
            "airplain",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]

        label = np.argmax(predict)
        print("=> Prediction :", classes[label])


if __name__ == "__main__":
    single_prediction()
