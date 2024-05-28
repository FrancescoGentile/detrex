# coding=utf-8
# Copyright 2022 The IDEA Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
from importlib import resources

import omegaconf
from detectron2.config import LazyConfig
from omegaconf import OmegaConf


def try_get_key(cfg, *keys, default=None):
    """
    Try select keys from lazy cfg until the first key that exists. Otherwise return default.
    """
    for k in keys:
        none = object()
        p = OmegaConf.select(cfg, k, default=none)
        if p is not none:
            return p
    return default


def get_config(config_path: str) -> omegaconf.DictConfig:
    """
    Returns a config object from a config_path.

    Args:
        config_path: config file name relative to detrex's "configs/"
            directory, e.g., "common/train.py"

    Returns:
        The loaded config object.
    """
    module = importlib.import_module("detrex.config")
    root = resources.files(module)
    file = root / "configs" / config_path
    if not file.exists():
        msg = f"{config_path} not available in detrex configs!"
        raise RuntimeError(msg)

    cfg = LazyConfig.load(str(file))
    return cfg
