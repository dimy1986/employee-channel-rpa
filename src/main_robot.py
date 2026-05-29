#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""员工渠道RPA机器人 - 主程序入口"""

import sys
import argparse
import logging
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger
from src.modules.navigator import Navigator
from src.modules.form_handler import FormHandler
from src.modules.export_handler import ExportHandler
from src.modules.browser_handler import BrowserHandler
from src.utils.error_handler import notify_user


class EmployeeChannelRPA:
    """员工渠道RPA机器人主类"""

    def __init__(self):
        """初始化RPA机器人"""
        self.config = ConfigLoader.load('config/reports_config.yaml')
        self.logger = setup_logger('EmployeeChannelRPA')
        self.navigator = Navigator()
        self.form_handler = FormHandler()
        self.export_handler = ExportHandler()
        self.browser_handler = BrowserHandler()
        self.logger.info("RPA机器人已初始化")

    def execute_report(self, report_id):
        """执行单个报表"""
        try:
            if report_id not in self.config['reports']:
                raise ValueError(f"报表 {report_id} 不存在")

            report_config = self.config['reports'][report_id]
            self.logger.info(f"开始执行报表: {report_config['name']} (ID: {report_id})")

            self.navigator.navigate_to_menu(report_config['menu_path'])

            if report_config.get('form_fields'):
                self.form_handler.fill_form(report_config['form_fields'])

            if report_config.get('is_browser_popup', False):
                self.logger.info("检测到浏览器弹窗，正在处理...")
                self.browser_handler.handle_popup(report_config)

            self.export_handler.export(
                report_config['action_button'],
                report_config['export_format'],
                report_id
            )

            self.logger.info(f"✅ 报表 {report_config['name']} 导出成功")
            notify_user(report_id, f"报表 {report_config['name']} 导出成功", level="success")

        except Exception as e:
            error_msg = f"报表 {report_id} 执行失败: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            notify_user(report_id, error_msg, level="error")

    def execute_all(self):
        """执行所有配置的报表"""
        self.logger.info("="*50)
        self.logger.info("开始执行所有报表...")
        self.logger.info("="*50)

        report_ids = list(self.config['reports'].keys())
        total = len(report_ids)
        success_count = 0

        for idx, report_id in enumerate(report_ids, 1):
            self.logger.info(f"[{idx}/{total}] 执行报表: {report_id}")
            try:
                self.execute_report(report_id)
                success_count += 1
            except Exception as e:
                self.logger.error(f"执行报表 {report_id} 时出错: {str(e)}")

        self.logger.info("="*50)
        self.logger.info(f"执行完成: 成功 {success_count}/{total}")
        self.logger.info("="*50)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='员工渠道RPA自动化机器人')
    parser.add_argument('--report', help='执行指定的报表ID')
    parser.add_argument('--all', action='store_true', help='执行所有报表')

    args = parser.parse_args()

    robot = EmployeeChannelRPA()

    if args.report:
        robot.execute_report(args.report)
    elif args.all:
        robot.execute_all()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
