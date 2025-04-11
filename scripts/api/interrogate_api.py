import gradio as gr
from fastapi import FastAPI

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
        result = interrogator.interrogate(pil_image)
        return {
            'result': result,
        }
