

![image](https://github.com/user-attachments/assets/2c170d9e-0ba1-4310-832c-ed398a72512f)

Two custom ComfyUI nodes developed using DeepSeek Auto-Create:

A KSampler node that outputs the currently used Seed value (seed_output_sampler.py)

An image-saving node that outputs the Seed value used for the first sampling (save_image_with_seed.py)

These nodes can be used either individually or in combination. Their primary purpose is to visually and clearly display the Seed value of generated images without needing to reload the workflow.

It is hoped that such functionality will eventually be merged into the official default nodes.

Note: save_image_with_seed.py can only output the Seed value of the first sampled image, which also serves as the default Seed value for the entire workflow.

=================

使用 DeepSeek 自动创建的两个ComfyUI自定义节点。

一个是可以输出当前所用Seed值的K采样器节点；（seed_output_sampler.py）；

一个是可以输出首采样所用Seed值的保存图像节点；（save_image_with_seed.py）；

﻿
这两个节点可以组合使用，也可以单独使用，主要的目的就在于可以更直观，更清晰地显示当前已生成图片的Seed值，而无需重新载入工作流。
希望这样的功能，最终能合并到官方的默认节点中。

﻿
注：save_image_with_seed.py 只能输出首采样图像的Seed值，这个Seed值也是整个工作流的默认Seed值。



=================



[Uploading ComfyUI_YePeiSheng_Nodes.json…]()
