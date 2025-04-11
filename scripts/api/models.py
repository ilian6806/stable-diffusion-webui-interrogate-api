
from pydantic import BaseModel, Field


class SingleImageRequest(BaseModel):
    image: str = Field(default="", title="Image", description="Image to work on, must be a Base64 string containing the image's data.")
