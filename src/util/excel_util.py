#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import pandas as pd
from . import data_util

importlib.reload(data_util)


def get_excel_Data(excel_path: str) -> list:
    shot_list = []
    excel = pd.read_excel(excel_path)
    excel.fillna(False, inplace=True)
    for eps, shot, product, track, animation, lighting, lighting_extent, efx, cfx, mod, environment in zip(
            excel["关联集数"], excel["镜头号"], excel["3D制作内容"], excel["Track"], excel["Animation"],
            excel["Lighting"], excel["Lighting_Extension"], excel["EFX"], excel["CFX"], excel["Mod"],
            excel["Environment"]):
        shot_data = data_util.shot_data(eps, shot, product, track, animation, lighting, lighting_extent, efx, cfx, mod,
                                        environment)
        shot_list.append(shot_data)
    return shot_list
