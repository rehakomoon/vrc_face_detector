#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path
import numpy as np
import cv2
from tqdm import tqdm
import itertools
from joblib import Parallel, delayed

data_path = Path.cwd() / "data"
#data_path = Path.cwd() / "data_tiny"

input_dir = Path("/mnt/D/personal/vrc_dataset/raw/")
output_dir = data_path / "collect_data"

output_dir.parent.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True)

target_dirs = [d for d in input_dir.iterdir() if d.is_dir()]
# for tiny dataset
#target_paths = [[(p, f"{d.stem}_{i:08}.png") for i, p in enumerate(list(d.glob("*.png"))[:10])] for d in target_dirs]
# for full dataset
target_paths = [[(p, f"{d.stem}_{i:08}.png") for i, p in enumerate(d.glob("*.png"))] for d in target_dirs]
target_paths = itertools.chain.from_iterable(target_paths)
target_paths = list(target_paths)


# In[ ]:


def process(params):
    load_path, save_filename = params
    load_image = cv2.imread(str(load_path), cv2.IMREAD_COLOR)
    
    if (load_image is None):
        print("Skip: ", load_path)
        return
    
    load_image = load_image[:, :, :3]
    if ((load_image.shape[0:2] != (1080, 1920)) and (load_image.shape[0:2] != (1080, 1920))):
        return
    
    output_path = output_dir / save_filename
    cv2.imwrite(str(output_path), load_image)

# for debugging
#target_paths = target_paths[:10]

#[process(params) for params in tqdm(target_paths)]
Parallel(n_jobs=-1, verbose=10)([delayed(process)(params) for params in target_paths])
None


# In[ ]:




