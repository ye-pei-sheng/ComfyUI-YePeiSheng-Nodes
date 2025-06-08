from .seed_output_sampler import NODE_CLASS_MAPPINGS as sampler_mappings
from .save_image_with_seed import NODE_CLASS_MAPPINGS as saver_mappings
from .seed_output_sampler import NODE_DISPLAY_NAME_MAPPINGS as sampler_names
from .save_image_with_seed import NODE_DISPLAY_NAME_MAPPINGS as saver_names

# 合并节点映射
NODE_CLASS_MAPPINGS = {**sampler_mappings, **saver_mappings}
NODE_DISPLAY_NAME_MAPPINGS = {**sampler_names, **saver_names}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 插件元数据
__plugin_meta__ = {
    "name": "YePeiSheng Nodes",
    "description": "Custom nodes for seed management: Sampler with seed output and image saver with seed in filename",
    "author": "YePeiSheng",
    "version": (1, 1, 0),
    "install_instructions": "Install via ComfyUI Manager using URL: https://github.com/yourusername/ComfyUI-YePeiSheng-Nodes",
    "dependencies": {"comfyui": ">=1.0.0"}
}