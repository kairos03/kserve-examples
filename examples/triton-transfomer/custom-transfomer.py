import base64
import io

from typing import Dict

import torchvision.transforms as transforms
from PIL import Image


def image_transform(instance):
    """converts the input image of Bytes Array into Tensor
    Args:
        instance (dict): The request input for image bytes.
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
    instance["data"] = image_processing(image).tolist()

    return instance


from kserve import Model, ModelServer, model_server


class ImageTransformer(Model):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host

    def preprocess(self, inputs: Dict) -> Dict:
        return {
            "inputs": [
                {
                    "name": instance["name"],
                    "shape": instance["shape"],
                    "datatype": instance["datatype"],
                    "data": image_transform(instance),
                }
                for instance in inputs["inputs"]
            ]
        }

    def postprocess(self, inputs: Dict) -> Dict:
        return inputs
