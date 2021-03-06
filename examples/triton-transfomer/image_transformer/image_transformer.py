import base64
import io
import logging
from typing import Dict
import time

import torch
import torchvision.transforms as transforms
from PIL import Image
import kserve

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)


def image_transform(instance):
    """converts the input image of Bytes Array into Tensor
    Args:
        image (str): The request input for image bytes.
    Returns:
        list: Returns converted tensor as input for predict handler with v1/v2 inference protocol.
    """
    # image_processing = transforms.Compose(
    #     [
    #         transforms.ToTensor(),
    #         transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    #     ]
    # )
    # byte_array = base64.b64decode(instance["data"])
    # image = Image.open(io.BytesIO(byte_array))

    # processed_image = image_processing(image)

    instance["name"] = "input"
    instance["datatype"] = "FP32"
    instance["data"] = torch.ones((1, 3, 32, 32)).tolist()
    # instance["data"] = processed_image.tolist()
    # instance["shape"] = [1] + list(processed_image.shape)
    instance["shape"] = [1, 3, 32, 32]

    return instance


class ImageTransformer(kserve.Model):
    def __init__(self, name: str, predictor_host: str, protocol: str="v2"):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.protocol = protocol
        logging.info("MODEL NAME %s", name)
        logging.info("PREDICTOR URL %s", self.predictor_host)
        logging.info("PROTOCOL %s", self.protocol)
        self.timeout = 100

    def preprocess(self, inputs: Dict) -> Dict:
        return inputs
        logging.info("[PREPROCESS]")
        st = time.time()
        result = {"inputs": []}
        for instance in inputs["inputs"]:
            transformed = image_transform(instance)
            result["inputs"].append(transformed)
        logging.info(f"[RESULT]: {result}")
        logging.info(f"[PREPROCESS] Done: {time.time() - st:.4f} s")
        return result

    def postprocess(self, inputs: Dict) -> Dict:
        return inputs


if __name__ == "__main__":
    inputs = {
        "inputs": [
            {
                # "name": "input",
                # "shape": "",
                # "datatype": "FP32",
                "data": None,
            }
        ]
    }

    tf = ImageTransformer(None, None)

    result = tf.preprocess(inputs)

    print(result)