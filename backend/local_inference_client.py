"""Emulate huggingface_hub.InferenceClient executed locally"""
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from image_generator import generate_image_from_text, create_text_to_image_pipeline
from PIL import Image

class LocalInferenceClient:
    """Emulate huggingface_hub.InferenceClient executed locally"""

    def __init__(self, model="lykon/dreamshaper-8"):
        self.set_model(model)

    def text_to_image(self, prompt: str, model: Optional[str] = None) -> Image:
        """
        Generate an image based on a given text using a specified model.
        Args:
            prompt (`str`):
                The prompt to generate an image from.
            model (`str`, *optional*):
                The model to use for inference. Can be a model ID hosted on the Hugging Face Hub.
                This parameter overrides the model defined at the instance level. Defaults to None.

        Returns:
            `Image`: The generated image.

        Example:
        """
        if model and model != self.model:
            self.set_model(model)
        pipeline = self.text_to_image_pipeline_future.result()
        return generate_image_from_text(pipeline, prompt)

    def set_model(self, model: str):
        """Set the Hugging Face Hub model to use for inference.
        Args:
            model (`str`): ID of a model hosted on the Hugging Face Hub.
        """
        self.model = model
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.text_to_image_pipeline_future = executor.submit(
                create_text_to_image_pipeline, model
            )
