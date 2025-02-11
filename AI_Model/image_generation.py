# image_generation.py

import os
import torch
from PIL import Image
from diffusers import AutoPipelineForText2Image
from diffusers.image_processor import IPAdapterMaskProcessor
from diffusers.utils import load_image
from huggingface_hub import hf_hub_download
from config import DEFAULT_NEGATIVE_PROMPT, DEFAULT_NUM_INFERENCE_STEPS, DEFAULT_HEIGHT, DEFAULT_WIDTH, dtype, device

# 메인 파이프라인 로드 (일반 이미지 생성 및 캐릭터 생성에 사용)
pipeline = AutoPipelineForText2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=dtype
).to(device)

def load_unet_weights(pipeline):
    unet_weights_path = hf_hub_download(
        repo_id="lee124/sd1.5_fine_tuned",
        filename="best_model.pth"
    )
    state_dict = torch.load(unet_weights_path, map_location=device, weights_only=True)
    pipeline.unet.load_state_dict(state_dict)
    pipeline.safety_checker = None  # Safety Checker 비활성화
    return pipeline

pipeline = load_unet_weights(pipeline)

def generate_char(prompt, output_path):
    prompt += "(masterpiece, best quality,medium shot : 1.0),(upper body :1.1)"
    try:
        pipeline.to(device)
        with torch.no_grad():
            result = pipeline(
                prompt=[prompt],
                negative_prompt=[DEFAULT_NEGATIVE_PROMPT+"background"],
                num_inference_steps=DEFAULT_NUM_INFERENCE_STEPS,
                height=DEFAULT_HEIGHT,
                width=DEFAULT_WIDTH,
            ).images[0]
        result.save(output_path, format="PNG")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error generating image: {e}")

def generate_image(prompt, output_path):
    print("generate_image 사용중")
    try:
        pipeline.to(device)
        with torch.no_grad():
            result = pipeline(
                prompt=[prompt],
                negative_prompt=[DEFAULT_NEGATIVE_PROMPT],
                num_inference_steps=DEFAULT_NUM_INFERENCE_STEPS,
                height=DEFAULT_HEIGHT,
                width=DEFAULT_WIDTH,
            ).images[0]
        result.save(output_path, format="PNG")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error generating image: {e}")

def generate_image_with_reference(prompt, char_name, output_path, char_save_path):
    print('generate_image_with_reference 사용')
    try:
        reference_image_path = os.path.join(char_save_path, f"{char_name}.png")
        if not os.path.exists(reference_image_path):
            raise FileNotFoundError(f"참고 이미지가 존재하지 않습니다: {reference_image_path}")
        ref_img = Image.open(reference_image_path).convert("RGB")
        
        ref_pipeline = AutoPipelineForText2Image.from_pretrained(
            "stable-diffusion-v1-5/stable-diffusion-v1-5",
            torch_dtype=dtype
        ).to(device)
        ref_pipeline = load_unet_weights(ref_pipeline)
        
        ref_pipeline.load_ip_adapter(
            "lee124/Ip_Adapter_anyme_plus",
            subfolder="models",
            weight_name="ipAdapterPlusAnime_v10.safetensors"
        )
        ref_pipeline.set_ip_adapter_scale(0.6)
        
        with torch.no_grad():
            result = ref_pipeline(
                prompt=prompt,
                ip_adapter_image=ref_img,
                negative_prompt=DEFAULT_NEGATIVE_PROMPT,
                num_inference_steps=DEFAULT_NUM_INFERENCE_STEPS,
                guidance_scale=7.5
            ).images[0]
        
        result.save(output_path, format="PNG")
        return output_path

    except Exception as e:
        raise RuntimeError(f"Error generating image with reference: {e}")

def generate_image_with_two_reference(prompt, char_1, char_2, output_path, char_save_path):
    print('generate_image_with_two_reference 사용')
    try:
        mask1 = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/ip_mask_mask1.png")
        mask2 = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/ip_mask_mask2.png")
        processor = IPAdapterMaskProcessor()
        masks = processor.preprocess([mask1, mask2], height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH)
        masks_tensor = masks.reshape(1, masks.shape[0], masks.shape[2], masks.shape[3])
        
        reference_image_path_1 = os.path.join(char_save_path, f"{char_1}.png")
        reference_image_path_2 = os.path.join(char_save_path, f"{char_2}.png")
        if not os.path.exists(reference_image_path_1) or not os.path.exists(reference_image_path_2):
            raise FileNotFoundError(f"참고 이미지가 존재하지 않습니다: {reference_image_path_1} 또는 {reference_image_path_2}")
        
        ref_img1 = Image.open(reference_image_path_1).convert("RGB")
        ref_img2 = Image.open(reference_image_path_2).convert("RGB")
        ip_images = [[ref_img1, ref_img2]]
        
        ref_pipeline = AutoPipelineForText2Image.from_pretrained(
            "stable-diffusion-v1-5/stable-diffusion-v1-5",
            torch_dtype=dtype
        ).to(device)
        ref_pipeline = load_unet_weights(ref_pipeline)
        
        ref_pipeline.load_ip_adapter(
            "lee124/Ip_Adapter_anyme_plus",
            subfolder="models",
            weight_name="ipAdapterPlusAnime_v10.safetensors"
        )
        ref_pipeline.set_ip_adapter_scale([[0.4, 0.4]])
        
        with torch.no_grad():
            result = ref_pipeline(
                prompt=prompt,
                ip_adapter_image=ip_images,
                negative_prompt=DEFAULT_NEGATIVE_PROMPT,
                num_inference_steps=DEFAULT_NUM_INFERENCE_STEPS,
                cross_attention_kwargs={"ip_adapter_masks": [masks_tensor]},
                guidance_scale=6.5,
                height=DEFAULT_HEIGHT,
                width=DEFAULT_WIDTH,
            ).images[0]
        
        result.save(output_path, format="PNG")
        return output_path

    except Exception as e:
        raise RuntimeError(f"Error generating image with two references: {e}")
