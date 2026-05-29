#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""浏览器处理模块 - 处理浏览器弹窗"""

import pyautogui
import time
import logging


class BrowserHandler:
    """浏览器处理器"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.main_window = None

    def handle_popup(self, report_config):
        """处理浏览器弹窗"""
        try:
            self.logger.info("开始处理浏览器弹窗...")
            
            self.main_window = self._get_main_window()
            
            browser_window = self._wait_for_browser_popup(timeout=10)
            
            if not browser_window:
                raise Exception("浏览器未在规定时间内弹出")
            
            self.logger.info(f"检测到浏览器窗口")
            
            time.sleep(2)
            
        except Exception as e:
            self.logger.error(f"处理浏览器弹窗失败: {str(e)}")
            raise

    def _wait_for_browser_popup(self, timeout=10):
        """等待浏览器弹窗"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                windows = pyautogui.getAllWindows()
                
                for window in windows:
                    title = window.title.lower() if hasattr(window, 'title') else ''
                    if 'chrome' in title or 'firefox' in title or 'edge' in title:
                        return window
            except Exception:
                pass
            
            time.sleep(0.5)
        
        return None

    def _get_main_window(self):
        """获取主窗口"""
        try:
            windows = pyautogui.getAllWindows()
            return windows[0] if windows else None
        except Exception:
            return None
