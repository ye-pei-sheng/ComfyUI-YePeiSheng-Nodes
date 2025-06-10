import os
import numpy as np
import folder_paths
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import comfy.utils
import json
import re

class SaveImageWithSeed:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("seeds",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "YePeiSheng/image"

    def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        os.makedirs(self.output_dir, exist_ok=True)
        seed_values = []
        results = []
        
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        
        for index, image in enumerate(images):
            i = 255. * image.cpu().numpy().squeeze()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            metadata = PngInfo()
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))
            
            seed_value = self.extract_seed_from_metadata(prompt, extra_pnginfo, index)
            seed_values.append(seed_value)
            
            seed_str = seed_value.replace(" ", "_").replace(",", "")[:20]
            file = f"{filename}_{counter:05}_{seed_str}.png"
            counter += 1
            
            img_path = os.path.join(full_output_folder, file)
            img.save(img_path, pnginfo=metadata, compress_level=4)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
        
        seeds_output = ",".join(seed_values)
        
        return {
            "ui": {
                "images": results,
                "seed": seed_values
            },
            "result": (seeds_output,)
        }
    
    def extract_seed_from_metadata(self, prompt_data, extra_pnginfo, index=0):
        if not prompt_data and not extra_pnginfo:
            return "Unknown"
        
        seed_candidates = []
        
        # 1. 搜索 prompt 中的节点
        if prompt_data:
            for node_id, node_data in prompt_data.items():
                try:
                    # 检查 inputs 中的 seed/noise_seed
                    inputs = node_data.get("inputs", {})
                    for key in ["seed", "noise_seed"]:
                        if key in inputs:
                            seed_candidates.append(str(inputs[key]))
                    
                    # 检查 class_type 是否包含 sampler
                    if "sampler" in node_data.get("class_type", "").lower():
                        properties = node_data.get("properties", {})
                        if "Seed" in properties:
                            seed_candidates.append(str(properties["Seed"]))
                except:
                    continue
        
        # 2. 搜索 extra_pnginfo 中的 workflow 节点
        if extra_pnginfo and "workflow" in extra_pnginfo:
            workflow = extra_pnginfo["workflow"]
            for node in workflow.get("nodes", []):
                try:
                    # 检查 properties 中的 seed
                    properties = node.get("properties", {})
                    if "Seed" in properties:
                        seed_candidates.append(str(properties["Seed"]))
                    elif "seed" in properties:
                        seed_candidates.append(str(properties["seed"]))
                    
                    # 检查 widgets_values 中的 seed
                    widgets = node.get("widgets_values", [])
                    if widgets and isinstance(widgets, list):
                        # 假设seed是widgets列表中的第一个数字
                        for val in widgets:
                            if isinstance(val, (int, float)):
                                seed_candidates.append(str(int(val)))
                                break
                except:
                    continue
        
        # 3. 返回找到的seed值（按索引选择）
        if seed_candidates:
            return seed_candidates[index % len(seed_candidates)]
        
        return "Unknown"

NODE_CLASS_MAPPINGS = {
    "YePeiSheng_SaveImageWithSeed": SaveImageWithSeed
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YePeiSheng_SaveImageWithSeed": "Save Image (With Seed)"
}