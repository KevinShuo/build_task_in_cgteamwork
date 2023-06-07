#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataclasses


@dataclasses.dataclass
class shot_data:
    eps_number: str
    shot_number: str
    product_contents: str
    track_pipeline: str
    animation_pipeline: str
    lighting_pipeline: str
    lighting_extension_pipeline: str
    efx_pipeline: str
    cfx_pipeline: str
    mod_pipeline: str
    environment_pipeline: str


@dataclasses.dataclass
class cgt_task_data:
    shot_number: str
    pipeline: str
    task_id: str
