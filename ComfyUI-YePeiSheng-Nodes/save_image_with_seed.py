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
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 存储提取的seed值
        seed_values = []
        results = []
        
        # 获取计数器值
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        
        # 处理所有图像
        for index, image in enumerate(images):
            i = 255. * image.cpu().numpy().squeeze()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # 创建元数据对象
            metadata = PngInfo()
            
            # 添加ComfyUI标准元数据
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))
            
            # 从元数据中提取seed值
            seed_value = self.extract_seed_from_metadata(prompt, extra_pnginfo, index)
            seed_values.append(seed_value)
            
            # 在文件名中包含seed值
            seed_str = seed_value.replace(" ", "_").replace(",", "")[:20]  # 限制长度
            file = f"{filename}_{counter:05}_{seed_str}.png"
            counter += 1
            
            # 保存图像
            img_path = os.path.join(full_output_folder, file)
            img.save(img_path, pnginfo=metadata, compress_level=4)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
        
        # 将seed值列表转换为逗号分隔的字符串
        seeds_output = ",".join(seed_values)
        
        # 返回UI显示数据和保存结果
        return {
            "ui": {
                "images": results,
                "seed": seed_values  # 显示seed值
            },
            "result": (seeds_output,)  # 输出seed值
        }
    
    def extract_seed_from_metadata(self, prompt_data, extra_pnginfo, index=0):
        """直接从提供的元数据中提取seed值"""
        if not prompt_data:
            return "N/A"
        
        try:
            # 1. 查找包含种子的节点
            seed_nodes = []
            for node_id, node_data in prompt_data.items():
                if "inputs" in node_data and "seed" in node_data["inputs"]:
                    seed_nodes.append((int(node_id), node_data))
            
            # 2. 按节点ID排序以确保顺序一致性
            seed_nodes.sort(key=lambda x: x[0])
            
            # 3. 获取当前图像对应的种子节点
            if seed_nodes:
                # 使用索引选择种子节点（循环使用）
                seed_node = seed_nodes[index % len(seed_nodes)][1]
                return str(seed_node["inputs"]["seed"])
                
            # 4. 尝试从extra_pnginfo中提取
            if extra_pnginfo and "workflow" in extra_pnginfo:
                workflow = extra_pnginfo["workflow"]
                for node in workflow["nodes"]:
                    if "seed" in node.get("properties", {}):
                        return str(node["properties"]["seed"])
                    if "inputs" in node and any(inp.get("name") == "seed" for inp in node.get("inputs", [])):
                        seed_input = next(inp for inp in node["inputs"] if inp.get("name") == "seed")
                        return str(seed_input.get("value", "N/A"))
        
        except Exception as e:
            print(f"[YePeiSheng] Error extracting seed: {e}")
        
        return "N/A"

# 节点注册
NODE_CLASS_MAPPINGS = {
    "YePeiSheng_SaveImageWithSeed": SaveImageWithSeed
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YePeiSheng_SaveImageWithSeed": "Save Image (With Seed)"
}