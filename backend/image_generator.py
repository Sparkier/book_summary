"""Generate an image from a text prompt using Stable Diffusion."""
import torch
from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler


def generate_image_from_text(text, output_path):
    """Generate an image with the Stable Diffusion model asynchronously.

    Args:
        text (str): The text used for image generation.
        output_path (str): The file path where the image should be saved.

    Returns:
        str: The file path where the image is saved.
    """
    pipeline = AutoPipelineForText2Image.from_pretrained(
        'lykon/dreamshaper-8', torch_dtype=torch.float32, variant="fp16")
    pipeline.scheduler = DEISMultistepScheduler.from_config(
        pipeline.scheduler.config)
    prompt = [text]
    images = pipeline(prompt).images
    generated_image = images[0]
    save_image(generated_image, output_path)
    return output_path


def save_image(image, output_path):
    """Save the generated image.

    Args:
        image (PIL.Image): The image to be saved.
        output_path (str): The file path where the image should be saved.
    """
    image.save(output_path)
