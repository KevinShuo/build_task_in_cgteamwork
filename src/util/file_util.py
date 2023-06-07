#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os


def read_project_json() -> list:
    with open(os.path.join(__file__, "../../../data/project_dict.json").replace('\\', '/'), "r+") as file:
        json_data = json.load(file)
        return json_data
