#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

sys.path.append(r"C:\CgTeamWork_v6\bin\base")
import cgtw2

t_tw = cgtw2.tw()


def build_info_task(project_database: str, eps_number: str, shot_number: str, product: str) -> list:
    id_list = check_info_shot_exists(project_database, shot_number)
    if not id_list:
        task_ID = t_tw.info.create(db=project_database, module="shot",
                                   sign_data_dict={"shot.entity": shot_number, "shot.link_eps": eps_number,
                                                   "shot.ddd": product}, is_return_id=True)
        return [task_ID]
    else:
        return id_list


def build_task(project_database: str, flow_list: list, info_list: list, pipeline_template_list: list):
    for flow in flow_list:
        pipeline_id = flow["pipeline_id"]
        flow_id = flow["flow_id"]
        pipeline_name = flow["pipeline_name"]
        for info_id in info_list:
            t_tw.task.create(project_database, "shot", info_id, pipeline_id, pipeline_name, flow_id,
                             pipeline_template_id=pipeline_template_list[0]["#id"])


def get_pipeline_template(project_database: str, pipeline_template_name: str) -> dict:
    pipeline_list = t_tw.pipeline_template.get(project_database, "shot", ["entity"])
    sd_pipeline = [i for i in pipeline_list if i["entity"] == pipeline_template_name][0]
    return sd_pipeline


def get_pipeline_list(project_database: str, pipeline: str) -> list:
    pipeline_id_list = t_tw.pipeline.get_id(project_database,
                                            [["entity", "=", pipeline], "and", ["module", "=", "shot"]])
    return pipeline_id_list


def get_flow_list(project_database: str, pipeline_id_list: list) -> list:
    t_flow_list = t_tw.flow.get_data(project_database, pipeline_id_list)
    return t_flow_list


def check_info_shot_exists(project_database: str, shot_number: str) -> list | None:
    id_list = t_tw.info.get_id(db=project_database, module="shot", filter_list=[["shot.entity", "=", shot_number]])
    if id_list:
        return id_list
    else:
        return None


def check_task_shot_exists(project_database: str, shot_number: str, pipeline_entity: str) -> list | None:
    id_list = t_tw.task.get_id(db=project_database, module="shot",
                               filter_list=[["shot.entity", "=", shot_number], "and",
                                            ["pipeline.entity", "=", pipeline_entity]])
    if id_list:
        return id_list
    else:
        return None
