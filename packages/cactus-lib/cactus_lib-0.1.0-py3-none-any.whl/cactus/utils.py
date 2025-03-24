import math
import os
import shutil

import random
import numpy as np

from cactus.common import DTYPE

import torch
from transformers import AutoModelForCausalLM

def generate_job_id():
    return f"job{random.randint(0, 1000)}"


def load_tensor_from_storage(weight_path, shape, dtype=DTYPE, to_ram=False):

    if isinstance(shape, tuple):
        size = math.prod(shape)
    else:
        size = shape

    data = torch.from_file(weight_path, shared=False, size=size, dtype=dtype)
    data = data.view(shape)

    if to_ram:
        data = data.clone()

    return data


def save_tensor_to_storage(weight_path, data):
    data.contiguous().detach().numpy().tofile(weight_path)


def download_weights(weight_dir, model_name):

    if os.path.exists(weight_dir):
        return
    
    os.makedirs(weight_dir, exist_ok=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=DTYPE)

    for name, param in model.named_parameters():
        file_path = f"{weight_dir}/{name}.bin"
        param.detach().numpy().tofile(file_path)

    del model



def remove_weights(weight_dir):
    if os.path.exists(weight_dir):
        if os.path.isdir(weight_dir):
            shutil.rmtree(weight_dir)
        else:
            os.remove(weight_dir)