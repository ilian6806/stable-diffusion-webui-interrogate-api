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

        # Check if the image has an alpha channel (transparency)
        if pil_image.mode == 'RGBA':
            # Create a white background image of the same size
            background = Image.new('RGB', pil_image.size, (255, 255, 255))
            # Paste the image on the background, using the alpha channel as mask
            background.paste(pil_image, (0, 0), pil_image)
            # Replace the original image with the one having white background
            pil_image = background
        # For other possible formats with transparency
        elif pil_image.mode == 'P' and 'transparency' in pil_image.info:
            # Convert to RGBA first to handle transparency correctly
            pil_image = pil_image.convert('RGBA')
            background = Image.new('RGB', pil_image.size, (255, 255, 255))
            background.paste(pil_image, (0, 0), pil_image)
            pil_image = background

        result = interrogator.interrogate(pil_image)

        return {
            'result': result,
        }
