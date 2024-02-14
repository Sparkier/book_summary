#! /usr/bin/env python3
"""Generate an image from a text prompt using Stable Diffusion."""
import argparse
import torch
from diffusers import StableDiffusionPipeline


def generate_image_from_text(text):
    """Generate an image with the Stable Diffusion model.

    Args:
        text (str): The text used for image generation.

    Returns:
        PIL.Image: The generated image.
    """
    pipeline = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
    prompt = [text]
    images = pipeline(prompt).images
    return images[0]


def save_image(image, output_path):
    """Save the generated image.

    Args:
        image (PIL.Image): The image to be saved.
        output_path (str): The file path where the image should be saved.
    """
    image.save(output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate image from text using Stable Diffusion.')
    parser.add_argument('--text', type=str,
                        help='text prompt for image generation')
    parser.add_argument('--output_path', type=str,
                        help='output path for the generated image')

    args = parser.parse_args()

    if not args.text or not args.output_path:
        print("Please provide both --text and --output_path arguments.")
    else:
        generated_image = generate_image_from_text(args.text)
        save_image(generated_image, args.output_path)
        print(f"Image generated and saved at: {args.output_path}")
