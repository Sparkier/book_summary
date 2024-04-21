"""Generate an image from a text prompt using Stable Diffusion."""

import torch
from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler


def create_text_to_image_pipeline(model="lykon/dreamshaper-8"):
    """Create pipeline for generating images from text and optimize it for performance.
    Args:
        model (str): Pretrained Huggingface text-to-image model.

    Returns:
        AutoPipelineForText2Image: Text-to-image pipeline.
    """
    if torch.cuda.is_available():
        print("Using CUDA pipeline")
        # bfloat16/float16 to speed-up 2-10x compared to float32
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        pipe = AutoPipelineForText2Image.from_pretrained(
            model, torch_dtype=dtype, use_safetensors=True
        )
        pipe = pipe.to("cuda")

        # Tried performance optimizations tested on NVidia A100:
        # https://github.com/huggingface/diffusion-fast
        # They do not seem to help/work on NVidia 2080 so they 
        # are therefore commented out.
        # 
        # See also
        # https://huggingface.co/docs/diffusers/v0.27.2/en/tutorials/fast_diffusion
        # pylint: disable=protected-access
        # torch._inductor.config.conv_1x1_as_mm = True
        # torch._inductor.config.coordinate_descent_tuning = True
        # torch._inductor.config.epilogue_fusion = False
        # torch._inductor.config.coordinate_descent_check_all_directions = True
        # torch._inductor.config.force_fuse_int_mm_with_mul = True
        # torch._inductor.config.use_mixed_mm = True
        # # Change the memory layout.
        # pipe.unet.to(memory_format=torch.channels_last)
        # pipe.vae.to(memory_format=torch.channels_last)
        # Causes exception: LoweringException: ErrorFromChoice: requires Triton
        # Could be that the GPU (NVIDIA 2080) is too old...
        # pipe.unet = torch.compile(pipe.unet, mode="max-autotune", fullgraph=True)
        # pipe.vae.decode = torch.compile(pipe.vae.decode, mode="max-autotune", fullgraph=True)
        # Apply dynamic quantization
        # from torchao.quantization import swap_conv2d_1x1_to_linear
        # swap_conv2d_1x1_to_linear(pipe.unet, conv_filter_fn)
        # swap_conv2d_1x1_to_linear(pipe.vae, conv_filter_fn)

        # https://huggingface.co/docs/diffusers/v0.27.2/en/optimization/fp16#use-tensorfloat-32
        # CUDA will automatically switch to using tf32 instead of fp32 where possible,
        # assuming that the used GPU is from the Ampere series (for data centers).
        torch.backends.cuda.matmul.allow_tf32 = True
    else:
        pipe = AutoPipelineForText2Image.from_pretrained(
            model, torch_dtype=torch.float32, variant="fp16", use_safetensors=True
        )

    pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)

    return pipe


def generate_image_from_text(pipeline: AutoPipelineForText2Image, prompt):
    """Generate an image with the supplied pipeline.

    Args:
        prompt (str): The text used for image generation.
        output_path (str): The file path where the image should be saved.

    Returns:
        str: The file path where the image is saved.
    """
    images = pipeline([prompt]).images
    return images[0]
