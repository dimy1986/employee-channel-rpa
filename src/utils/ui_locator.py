#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UI定位工具 - 录制和定位UI元素"""

import json
import logging
from pathlib import Path


class UILocator:
    """UI定位器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ui_elements_file = Path("config/ui_elements.json")
        self.ui_elements = self._load_ui_elements()
    
    def _load_ui_elements(self):
        """加载UI元素配置"""
        if self.ui_elements_file.exists():
            try:
                with open(self.ui_elements_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def find_element(self, element_id):
        """查找UI元素"""
        return self.ui_elements.get(element_id)
