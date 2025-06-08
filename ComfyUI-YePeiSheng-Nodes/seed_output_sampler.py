import comfy
import torch
import random
import nodes
import folder_paths

class KSamplerWithSeedOutput:
    """采样器节点，输出实际使用的Seed值"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive": ("CONDITIONING", ),
                "negative": ("CONDITIONING", ),
                "latent_image": ("LATENT", ),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LATENT", "INT")
    RETURN_NAMES = ("LATENT", "SEED")
    FUNCTION = "sample"
    CATEGORY = "YePeiSheng/sampling"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise):
        # 保存原始随机状态
        cpu_rng_state = torch.get_rng_state()
        gpu_rng_state = torch.cuda.get_rng_state() if torch.cuda.is_available() else None
        random_state = random.getstate()

        # 处理随机种子
        actual_seed = seed

        # 设置所有生成器使用指定种子
        torch.manual_seed(actual_seed)
        random.seed(actual_seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(actual_seed)

        # 调用原始采样器
        latent = nodes.KSampler().sample(model, seed, steps, cfg, sampler_name, scheduler, 
                                         positive, negative, latent_image, denoise)[0]

        # 恢复原始随机状态
        torch.set_rng_state(cpu_rng_state)
        if gpu_rng_state is not None:
            torch.cuda.set_rng_state(gpu_rng_state)
        random.setstate(random_state)

        return (latent, actual_seed)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "YePeiSheng_KSamplerWithSeed": KSamplerWithSeedOutput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YePeiSheng_KSamplerWithSeed": "KSampler with Seed Output"
}