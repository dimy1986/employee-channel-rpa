#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""表单处理模块 - 填充表单字段、输入查询条件"""

import pyautogui
import time
import logging
from datetime import datetime, timedelta


class FormHandler:
    """表单处理器"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pyautogui.FAILSAFE = False

    def fill_form(self, form_fields):
        """填充表单字段"""
        self.logger.info(f"开始填充表单，共 {len(form_fields)} 个字段")
        
        for field in form_fields:
            try:
                value = self._resolve_dynamic_value(field['value'])
                element_type = field['element_type']
                field_id = field['field_id']

                self.logger.info(f"填充字段 {field_id}: {value}")

                if element_type == "text":
                    self._fill_text(field_id, value)
                elif element_type == "date_picker":
                    self._fill_date(field_id, value)
                elif element_type == "dropdown":
                    self._select_dropdown(field_id, value)

                time.sleep(0.3)
            except Exception as e:
                self.logger.error(f"填充字段失败: {str(e)}")
                raise

    def _fill_text(self, field_id, value):
        """填充文本框"""
        self.logger.debug(f"填充文本框 {field_id} = {value}")

    def _fill_date(self, field_id, value):
        """填充日期字段"""
        self.logger.debug(f"填充日期字段 {field_id} = {value}")

    def _select_dropdown(self, field_id, value):
        """选择下拉框选项"""
        self.logger.debug(f"选择下拉框 {field_id} = {value}")

    def _resolve_dynamic_value(self, value_str):
        """解析动态参数"""
        if isinstance(value_str, str):
            if value_str == "${today}":
                result = datetime.now().strftime("%Y-%m-%d")
            elif value_str == "${current_month}":
                result = datetime.now().strftime("%Y-%m")
            elif value_str == "${first_day_of_month}":
                today = datetime.now()
                first_day = today.replace(day=1)
                result = first_day.strftime("%Y-%m-%d")
            elif value_str == "${last_month}":
                today = datetime.now()
                last_month = today.replace(day=1) - timedelta(days=1)
                result = last_month.strftime("%Y-%m")
            else:
                result = value_str
            
            return result
        
        return value_str
