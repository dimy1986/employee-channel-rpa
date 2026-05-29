#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""导航模块 - 菜单导航和UI元素定位"""

import pyautogui
import time
import logging
from pathlib import Path


class Navigator:
    """菜单导航器"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        self.retry_max = 3
        pyautogui.FAILSAFE = False

    def navigate_to_menu(self, menu_path):
        """导航到指定菜单"""
        self.logger.info(f"开始导航: {' -> '.join(menu_path)}")
        
        for i, menu_name in enumerate(menu_path):
            try:
                self._click_menu(menu_name, level=i)
                time.sleep(0.5)
            except Exception as e:
                self.logger.error(f"导航到菜单 {menu_name} 失败: {str(e)}")
                raise

    def _click_menu(self, menu_name, level=0):
        """点击菜单项"""
        for attempt in range(self.retry_max):
            try:
                self.logger.debug(f"尝试点击菜单: {menu_name}")
                self.logger.warning(f"菜单 {menu_name} 的UI定位逻辑需要配置")
                return
                
            except Exception as e:
                if attempt == self.retry_max - 1:
                    raise Exception(f"无法找到菜单: {menu_name}")
                time.sleep(1)
