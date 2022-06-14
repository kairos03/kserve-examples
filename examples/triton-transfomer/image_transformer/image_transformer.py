import base64
import io
import logging
from typing import Dict

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
    image_processing = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )
    byte_array = base64.b64decode(instance["data"])
    image = Image.open(io.BytesIO(byte_array))

    instance["name"] = "input"
    instance["datatype"] = "FP32"
    instance["data"] = image_processing(image).tolist()
    instance["shape"] = image.size

    return instance


class ImageTransformer(kserve.Model):
    def __init__(self, name: str, predictor_host: str, protocol: str):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.protocol = protocol
        logging.info(f"Start: {name}, {predictor_host}, {protocol}")

    def preprocess(self, inputs: Dict) -> Dict:
        result = {"inputs": []}
        for instance in inputs["inputs"]:
            transformed = image_transform(instance)
            result["inputs"].append(transformed)

        return result

    def postprocess(self, inputs: Dict) -> Dict:
        return inputs