#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""错误处理 - 错误通知和异常处理"""

import logging


def notify_user(report_id, message, level="error"):
    """通知用户错误或成功信息"""
    logger = logging.getLogger(__name__)
    
    if level == "error":
        logger.error(f"【报表 {report_id}】{message}")
    elif level == "warning":
        logger.warning(f"【报表 {report_id}】{message}")
    elif level == "success":
        logger.info(f"【报表 {report_id}】✅ {message}")
    else:
        logger.info(f"【报表 {report_id}】{message}")
    
    try:
        notify_system_tray(report_id, message, level)
    except Exception as e:
        pass


def notify_system_tray(report_id, message, level):
    """系统托盘通知（Windows）"""
    try:
        from win10toast import ToastNotifier
        
        toaster = ToastNotifier()
        title = f"RPA报表导出 - {report_id}"
        
        if level == "error":
            toaster.show_toast(title, f"❌ {message}", duration=10, threaded=True)
        elif level == "success":
            toaster.show_toast(title, f"✅ {message}", duration=5, threaded=True)
        else:
            toaster.show_toast(title, message, duration=5, threaded=True)
    except Exception:
        pass
