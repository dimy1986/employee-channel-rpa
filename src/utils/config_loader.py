#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""配置加载器 - 加载和管理配置文件"""

import yaml
import logging
from pathlib import Path


class ConfigLoader:
    """配置加载器"""
    
    logger = logging.getLogger(__name__)
    _cache = {}
    
    @classmethod
    def load(cls, config_path):
        """加载配置文件"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        if str(config_path) in cls._cache:
            cls.logger.debug(f"从缓存加载配置: {config_path}")
            return cls._cache[str(config_path)]
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            cls._cache[str(config_path)] = config
            cls.logger.info(f"配置文件加载成功: {config_path}")
            
            return config
        except Exception as e:
            cls.logger.error(f"加载配置文件失败: {str(e)}")
            raise
