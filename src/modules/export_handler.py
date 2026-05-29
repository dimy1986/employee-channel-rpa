#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""导出模块 - 处理报表导出、文件监听和移动"""

import pyautogui
import time
import os
import shutil
import logging
from datetime import datetime
from pathlib import Path


class ExportHandler:
    """导出处理器"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.export_path = Path("D:/RPA_Exports")
        self.download_path = Path.home() / "Downloads"
        self.export_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"导出路径: {self.export_path}")

    def export(self, export_button, export_format, report_id):
        """执行导出操作"""
        try:
            self.logger.info(f"开始导出报表 {report_id}")
            
            files_before = set(os.listdir(self.download_path)) if self.download_path.exists() else set()
            
            self.logger.info("已点击导出按钮")
            
            downloaded_file = self._wait_for_download(files_before, timeout=30)
            
            if not downloaded_file:
                raise Exception(f"报表 {report_id} 导出超时")
            
            self.logger.info(f"检测到下载文件: {downloaded_file}")
            
            target_file = self._move_to_export_path(downloaded_file, report_id, export_format)
            
            self.logger.info(f"文件已移动到: {target_file}")
            return target_file
            
        except Exception as e:
            self.logger.error(f"导出失败: {str(e)}")
            raise

    def _wait_for_download(self, files_before, timeout=30):
        """等待文件下载完成"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if not self.download_path.exists():
                    time.sleep(1)
                    continue
                
                files_after = set(os.listdir(self.download_path))
                new_files = files_after - files_before
                
                if new_files:
                    new_file = list(new_files)[0]
                    if self._is_file_complete(new_file):
                        return new_file
                
                time.sleep(1)
            except Exception as e:
                time.sleep(1)
        
        return None

    def _is_file_complete(self, filename, check_interval=0.5, check_times=3):
        """检查文件是否下载完成"""
        filepath = self.download_path / filename
        
        for i in range(check_times):
            if not filepath.exists():
                return False
            
            try:
                size_before = filepath.stat().st_size
                time.sleep(check_interval)
                size_after = filepath.stat().st_size
                
                if size_before != size_after:
                    continue
                else:
                    return True
            except Exception:
                return False
        
        return True

    def _move_to_export_path(self, filename, report_id, export_format):
        """移动文件到导出目录"""
        source = self.download_path / filename
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_name = f"{report_id}_{timestamp}.{export_format}"
        target = self.export_path / target_name
        
        try:
            shutil.move(str(source), str(target))
            self.logger.info(f"文件已移动到: {target}")
            return str(target)
        except Exception as e:
            self.logger.error(f"移动文件失败: {str(e)}")
            raise
