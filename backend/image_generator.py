#! /usr/bin/env python3
"""Generate an image from a text prompt using Stable Diffusion."""
import argparse
import torch
from diffusers import StableDiffusionPipeline


def generate_image_from_text_and_save(text, output_path):
    """Generate an image with the Stable Diffusion model and save it.

    Args:
        text (str): The text used for image generation.
        output_path (str): The file path where the image should be saved.
    """
    pipeline = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
    prompt = [text]
    images = pipeline(prompt).images

    # Save the generated image
    image_path = f"{output_path}"
    images[0].save(image_path)

    return image_path


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

    generate_image_from_text_and_save(args.text, args.output_path)
    print(f"Image generated and saved at: {args.output_path}.png")
