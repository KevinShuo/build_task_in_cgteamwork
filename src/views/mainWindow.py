# -*- coding: utf-8 -*-
import importlib
import sys
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from ..util import data_util, excel_util, tw_util, file_util
from .. import config
import subprocess
import threading
import json
import __future__
import glob
import cgi
import hmac
import time
import urllib
import sqlite3
import ctypes
import ctypes.wintypes
import queue
import http.cookies
import configparser
import platform

importlib.reload(config)
importlib.reload(data_util)
importlib.reload(tw_util)


class create_task_UI(QWidget):
    def __init__(self):
        super(create_task_UI, self).__init__()

    def setupUI(self):
        self.resize(config.WINDOWSIZE[0], config.WINDOWSIZE[1])
        self.setWindowTitle("{} v{}".format(config.WINDOWTITLE, config.VERSION))
        vbox_main = QVBoxLayout(self)
        # project database
        hbox_project_database = QHBoxLayout()
        label_project_database = QLabel("Project:     ")
        project_name_list = self.get_project_name()
        self.combox_project = QComboBox()
        self.combox_project.setFont(QFont("arial", 12))
        self.combox_project.addItems(project_name_list)
        self.combox_project.setMinimumWidth(600)
        hbox_project_database.addWidget(label_project_database, 0, Qt.AlignmentFlag.AlignCenter)
        hbox_project_database.addWidget(self.combox_project, 1, Qt.AlignmentFlag.AlignLeft)
        # Excel Path
        hbox_execl = QHBoxLayout()
        label_excel = QLabel("excel file:")
        label_excel.setFont(QFont("arial", 12))
        self.lineedit_excel_path = QLineEdit()
        self.lineedit_excel_path.setFont(QFont("arial", 12))
        widgetAction_open_dir = QWidgetAction(self)
        widgetAction_open_dir.setIcon(QIcon(r"./images/open_dir.png"))
        widgetAction_open_dir.triggered.connect(self.open_dir)
        self.lineedit_excel_path.addAction(widgetAction_open_dir, QLineEdit.ActionPosition.TrailingPosition)
        self.butn_Build = QPushButton("Build")
        self.butn_Build.setFont(QFont("arial", 12))
        self.butn_Build.setCheckable(False)
        self.butn_Build.clicked.connect(self.start_build_thread)
        hbox_execl.addWidget(label_excel)
        hbox_execl.addWidget(self.lineedit_excel_path, 1)
        hbox_execl.addWidget(self.butn_Build)
        # table Widget
        self.table_Widget = QTableWidget()
        self.table_Widget.setRowCount(10)
        self.table_Widget.setColumnCount(12)
        self.table_Widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_Widget.customContextMenuRequested.connect(self.add_menu)
        self.table_Widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_Widget.setSortingEnabled(True)
        self.table_Widget.setHorizontalHeaderLabels(
            ["建立状态", "关联集数", "镜头号", '3D制作内容', "Track", "Animation", "Lighting", "Lighting_Extension",
             "EFX", "CFX", "Mod", "Environment"])
        vbox_main.addLayout(hbox_project_database)
        vbox_main.addLayout(hbox_execl)
        vbox_main.addWidget(self.table_Widget, 1)
        self.show()

    def add_menu(self):
        menu = QMenu()
        delete_Shot = menu.addAction("清除当前选中的镜头")
        exec_ = menu.exec(QCursor.pos())
        if exec_ == delete_Shot:
            self.delete_shot()

    def delete_shot(self):
        row_list = []
        for select_item in self.table_Widget.selectedItems():  # type:QTableWidgetItem
            row = select_item.row()
            row_list.append(row)
        row_list1 = sorted(set(row_list), reverse=True)
        for row in row_list1:
            self.table_Widget.removeRow(row)

    def open_dir(self):
        excel_file, _ = QFileDialog.getOpenFileName(self, "请选择一个excel文件", filter="Excel文件 (*.xlsx)")
        if excel_file:
            self.lineedit_excel_path.setText(excel_file)
            shot_data_list = excel_util.get_excel_Data(excel_file)
            shot_data_len = len(shot_data_list)
            self.table_Widget.setRowCount(shot_data_len)
            row = 0
            for shot_data in shot_data_list:
                # eps number
                eps_number_item = QTableWidgetItem(shot_data.eps_number)
                eps_number_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 1, eps_number_item)
                # shot number
                shot_number_item = QTableWidgetItem(shot_data.shot_number)
                shot_number_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 2, shot_number_item)
                # product
                product_item = QTableWidgetItem(str(shot_data.product_contents))
                product_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 3, product_item)
                # track
                track_item = QTableWidgetItem(str(shot_data.track_pipeline))
                track_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 4, track_item)
                # animation
                animation_item = QTableWidgetItem(str(shot_data.animation_pipeline))
                animation_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 5, animation_item)
                # lighting
                lighting_item = QTableWidgetItem(str(shot_data.lighting_pipeline))
                lighting_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 6, lighting_item)
                # lighting extent
                lighting_extent_item = QTableWidgetItem(str(shot_data.lighting_extension_pipeline))
                lighting_extent_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 7, lighting_extent_item)
                # efx
                efx_item = QTableWidgetItem(str(shot_data.efx_pipeline))
                efx_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 8, efx_item)
                # cfx
                cfx_item = QTableWidgetItem(str(shot_data.cfx_pipeline))
                cfx_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 9, cfx_item)
                # mod
                mod_item = QTableWidgetItem(str(shot_data.mod_pipeline))
                mod_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 10, mod_item)
                # environment
                environment_item = QTableWidgetItem(str(shot_data.environment_pipeline))
                environment_item.setFont(QFont("arial", 12))
                self.table_Widget.setItem(row, 11, environment_item)
                row += 1

    def build(self):
        self.project_database = self.project_dict[self.combox_project.currentText()]
        for row in range(self.table_Widget.rowCount()):
            eps_number = self.table_Widget.item(row, 1).text()
            shot_number = self.table_Widget.item(row, 2).text()
            product = self.table_Widget.item(row, 3).text()
            track = self.table_Widget.item(row, 4).text()
            animation = self.table_Widget.item(row, 5).text()
            lighting = self.table_Widget.item(row, 6).text()
            lighting_extent = self.table_Widget.item(row, 7).text()
            efx = self.table_Widget.item(row, 8).text()
            cfx = self.table_Widget.item(row, 9).text()
            mod = self.table_Widget.item(row, 10).text()
            environment = self.table_Widget.item(row, 11).text()
            if product != "False":
                info_id_list = tw_util.build_info_task(self.project_database, eps_number, shot_number, product)
            else:
                info_id_list = tw_util.build_info_task(self.project_database, eps_number, shot_number, " ")
            if track != "False" and track != "Ready" and track != "Internal Final" and track != "Wait" and track != "Approve" and track != "Pause" and track != "omitted" and track != "Retake" and track != "0":
                self.build_cgt_task("Track", info_id_list, shot_number)
            if animation != "False" and animation != "Ready" and animation != "Internal Final" and animation != "Wait" and animation != "Approve" and animation != "Pause" and animation != "omitted" and animation != "Retake" and animation != "0":
                self.build_cgt_task("Animation", info_id_list, shot_number)
            if lighting != "False" and lighting != "Ready" and lighting != "Internal Final" and lighting != "Wait" and lighting != "Approve" and lighting != "Pause" and lighting != "omitted" and lighting != "Retake" and lighting != "0":
                self.build_cgt_task("Lighting", info_id_list, shot_number)
            if lighting_extent != "False" and lighting_extent != "Ready" and lighting_extent != "Internal Final" and lighting_extent != "Wait" and lighting_extent != "Approve" and lighting_extent != "Pause" and lighting_extent != "omitted" and lighting_extent != "Retake" and lighting_extent != "0":
                self.build_cgt_task("Lighting_Extension", info_id_list, shot_number)
            if efx != "False" and efx != "Ready" and efx != "Internal Final" and efx != "Wait" and efx != "Approve" and efx != "Pause" and efx != "omitted" and efx != "Retake" and efx != "0":
                self.build_cgt_task("EFX", info_id_list, shot_number)
            if cfx != "False" and cfx != "Ready" and cfx != "Internal Final" and cfx != "Wait" and cfx != "Approve" and cfx != "Pause" and cfx != "omitted" and cfx != "Retake" and cfx != "0":
                self.build_cgt_task("CFX", info_id_list, shot_number)
            if mod != "False" and mod != "Ready" and mod != "Internal Final" and mod != "Wait" and mod != "Approve" and mod != "Pause" and mod != "omitted" and mod != "Retake" and mod != "0":
                self.build_cgt_task("Model", info_id_list, shot_number)
            if environment != "False" and environment != "Ready" and environment != "Internal Final" and environment != "Wait" and environment != "Approve" and environment != "Pause" and environment != "omitted" and environment != "Retake" and environment != "0":
                self.build_cgt_task("Environment", info_id_list, shot_number)
            status = QTableWidgetItem("√")
            self.table_Widget.setItem(row, 0, status)

    def start_build_thread(self):
        status = QMessageBox.information(self, "提示", "是否要开始创建任务",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if status == QMessageBox.StandardButton.Yes:
            job = threading.Thread(target=self.build)
            job.start()

    def get_project_name(self) -> list:
        project_name_list = []
        self.project_dict_list = file_util.read_project_json()
        self.project_dict = {}
        for project_dict in self.project_dict_list:  # type: dict
            project_name_list.append(project_dict["project_name"])
            self.project_dict[project_dict["project_name"]] = project_dict["project_database"]
        return project_name_list

    def build_cgt_task(self, pipeline: str, info_id_list: list, shot_number: str):
        task_id = tw_util.check_task_shot_exists(self.project_database, shot_number, pipeline)
        if not task_id:
            pipeline_template = tw_util.get_pipeline_template(self.project_database, "视点工作流")
            pipeline_list = tw_util.get_pipeline_list(self.project_database, pipeline)
            flow_list = tw_util.get_flow_list(self.project_database, pipeline_list)
            tw_util.build_task(self.project_database, flow_list, info_id_list, [pipeline_template])


def build_UI():
    app = QApplication(sys.argv)
    win = create_task_UI()
    win.setupUI()
    sys.exit(app.exec())
