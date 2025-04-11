import gradio as gr
from fastapi import FastAPI
from PIL import Image

from . utils import decode_base64_to_image
from . models import SingleImageRequest
from modules.shared import interrogator


class InterrogateApi():

    BASE_PATH = '/sdapi/v1/interrogate'

    def get_path(self, path):
        return f"{self.BASE_PATH}{path}"

    def add_api_route(self, path: str, endpoint, **kwargs):
        # authenticated requests can be implemented here
        return self.app.add_api_route(self.get_path(path), endpoint, **kwargs)

    def start(self, _: gr.Blocks, app: FastAPI):

        self.app = app

        self.add_api_route('/clip', self.clip, methods=['POST'])

    def clip(self, req: SingleImageRequest):
        ''' Generate mask by type '''
        pil_image = decode_base64_to_image(req.image)

        if pil_image.mode != 'RGB':
            # If image has transparency (RGBA or similar)
            if 'A' in pil_image.mode or 'transparency' in pil_image.info:
                # Create white background
                background = Image.new('RGB', pil_image.size, (255, 255, 255))
                # Handle transparency correctly by using alpha as mask if available
                if 'A' in pil_image.mode:
                    background.paste(pil_image, (0, 0), pil_image)
                else:
                    # Convert palette-based transparency to RGBA first
                    temp = pil_image.convert('RGBA')
                    background.paste(temp, (0, 0), temp)
                pil_image = background
            else:
                # For grayscale or other modes without transparency, direct conversion
                pil_image = pil_image.convert('RGB')

        result = interrogator.interrogate(pil_image)

        return {
            'result': result,
        }
