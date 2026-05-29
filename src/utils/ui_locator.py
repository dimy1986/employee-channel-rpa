#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UI定位工具 - 自动录制和定位UI元素"""

import json
import sys
import time
from pathlib import Path
from pynput import mouse
import threading


class UILocator:
    """UI定位器 - 自动录制版"""

    def __init__(self):
        self.ui_elements_file = Path("config/ui_elements.json")
        self.ui_elements = self._load_ui_elements()
        self.element_counter = {
            'menu': 0,
            'button': 0,
            'input': 0,
            'dropdown': 0,
            'other': 0
        }
        self.is_recording = False

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

    def _auto_classify_element(self, x, y):
        """
        根据位置和环境自动分类元素类型
        简单规则：
        - 屏幕上方（y<150）通常是菜单
        - 屏幕下方（y>400）通常是按钮
        - 中间区域通常是输入框或下拉菜单
        """
        if y < 150:
            return 'menu'
        elif y > 400:
            return 'button'
        elif 150 <= y <= 400:
            return 'input'
        else:
            return 'other'

    def _save_elements(self):
        """保存UI元素到JSON文件"""
        self.ui_elements_file.parent.mkdir(exist_ok=True)
        with open(self.ui_elements_file, 'w', encoding='utf-8') as f:
            json.dump(self.ui_elements, f, indent=2, ensure_ascii=False)

    def _mouse_position_tracker(self):
        """后台线程：显示鼠标位置"""

        def on_move(x, y):
            if self.is_recording:
                # 每500ms显示一次位置
                if int(time.time() * 2) % 1 == 0:
                    print(f"\r🖱️  当前鼠标位置: ({x:4d}, {y:4d})", end="", flush=True)

        with mouse.Listener(on_move=on_move) as listener:
            listener.join()

    def record_automatic(self):
        """
        自动录制模式 - 右键点击自动记录，无需手工输入
        """
        print("\n" + "=" * 80)
        print("🎬 UI 元素自动录制工具 (智能版本)")
        print("=" * 80)
        print("\n📋 使用说明:")
        print("  1️⃣  将鼠标移动到要录制的UI元素上")
        print("  2️⃣  观察终端显示的鼠标坐标")
        print("  3️⃣  确认坐标后，按右键点击")
        print("  4️⃣  听到'嘟'声表示点击被记录")
        print("  5️⃣  重复以上步骤录制所有元素")
        print("  6️⃣  按 Ctrl+C 停止录制并自动保存")
        print("\n💡 提示:")
        print("  - 屏幕上方（y<150）会自动识别为菜单")
        print("  - 屏幕下方（y>400）会自动识别为按钮")
        print("  - 中间区域会自动识别为输入框/下拉菜单")
        print("  - 终端会实时显示鼠标坐标，帮助精确定位")
        print("\n" + "-" * 80)
        print("准备就绪！按任意键开始录制...\n")
        input()

        recorded_count = 0
        self.is_recording = True

        # 启动鼠标位置追踪线程
        tracker_thread = threading.Thread(target=self._mouse_position_tracker, daemon=True)
        tracker_thread.start()

        print("🖱️  监听中... 请移动鼠标观察坐标，然后右键点击元素\n")

        def on_click(x, y, button, pressed):
            nonlocal recorded_count

            if pressed and button == mouse.Button.right:
                # 自动分类元素类型
                element_type = self._auto_classify_element(x, y)

                # 生成自动名称
                self.element_counter[element_type] += 1
                element_name = f"{element_type}_{self.element_counter[element_type]:03d}"

                # 保存元素
                self.ui_elements[element_name] = {
                    "x": x,
                    "y": y,
                    "type": element_type
                }

                self._save_elements()
                recorded_count += 1

                # 清空鼠标位置显示，显示录制信息
                print("\r" + " " * 80 + "\r", end="", flush=True)
                print(
                    f"✅ [{recorded_count}] 成功录制 | 名称: {element_name:20s} | 坐标: ({x:4d}, {y:4d}) | 类型: {element_type}")
                print("🖱️  继续移动鼠标...\n", end="", flush=True)

                return True

        try:
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.is_recording = False
            print("\n" + "-" * 80)
            print("⏹️  录制已停止")

        if recorded_count > 0:
            print(f"\n✅ 录制完成！已保存 {recorded_count} 个元素到配置文件")
            print(f"📄 配置文件路径: {self.ui_elements_file.absolute()}")
            print(f"\n📋 已录制的元素列表:")
            print("-" * 80)
            print(f"{'元素名称':<20} | {'X坐标':<8} | {'Y坐标':<8} | {'元素类型':<10}")
            print("-" * 80)
            for name, config in self.ui_elements.items():
                print(f"{name:<20} | {config['x']:<8} | {config['y']:<8} | {config['type']:<10}")
            print("-" * 80)
            print("\n✨ 现在可以运行 RPA 测试了:")
            print("   python src/main_robot.py --report report_001\n")
        else:
            print("\n⚠️  未录制任何元素")

    def record_manual(self):
        """
        手工输入模式 - 右键点击后手工输入元素信息
        """
        print("\n" + "=" * 80)
        print("🎬 UI 元素手工录制工具")
        print("=" * 80)
        print("\n📋 使用说明:")
        print("  1. 将鼠标移动到要录制的UI元素上")
        print("  2. 右键点击来记录该位置的坐标")
        print("  3. 输入元素名称（如: menu_销售管理, button_导出 等）")
        print("  4. 选择或输入元素类型（menu/button/input/dropdown）")
        print("  5. 重复上述步骤")
        print("  6. 按 Ctrl+C 停止录制并保存配置文件")
        print("\n" + "-" * 80)
        print("准备就绪！按任意键开始录制...\n")
        input()

        recorded_elements = {}
        self.is_recording = True

        # 启动鼠标位置追踪线程
        tracker_thread = threading.Thread(target=self._mouse_position_tracker, daemon=True)
        tracker_thread.start()

        print("🖱️  监听中... 请移动鼠标观察坐标，然后右键点击元素\n")

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.right:
                print(f"\n✅ 捕获坐标: ({x}, {y})")
                element_name = input("📝 输入元素名称 (或按 Enter 跳过): ").strip()
                if element_name:
                    print("   选择元素类型:")
                    print("   1) menu (菜单)")
                    print("   2) button (按钮)")
                    print("   3) input (输入框)")
                    print("   4) dropdown (下拉菜单)")
                    type_choice = input("🏷️  输入选择 (1/2/3/4, 默认: 2): ").strip() or "2"

                    type_map = {"1": "menu", "2": "button", "3": "input", "4": "dropdown"}
                    element_type = type_map.get(type_choice, "button")

                    recorded_elements[element_name] = {
                        "x": x,
                        "y": y,
                        "type": element_type
                    }
                    print(f"📌 已保存: {element_name} = ({x}, {y}) [{element_type}]\n")
                return True

        try:
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.is_recording = False
            print("\n" + "-" * 80)
            print("⏹️  录制已停止")

        if recorded_elements:
            # 合并到现有配置
            self.ui_elements.update(recorded_elements)
            self._save_elements()
            print(f"\n✅ 录制完成！已保存 {len(recorded_elements)} 个元素")
            print(f"📄 配置文件: {self.ui_elements_file.absolute()}")
        else:
            print("\n⚠️  未录制任何元素")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python src/utils/ui_locator.py auto      # 自动录制模式（推荐）")
        print("  python src/utils/ui_locator.py manual    # 手工输入模式")
        return

    mode = sys.argv[1].lower()

    try:
        locator = UILocator()

        if mode == 'auto':
            locator.record_automatic()
        elif mode == 'manual':
            locator.record_manual()
        else:
            print(f"❌ 未知模式: {mode}")
            print("\n支持的模式:")
            print("  - auto   : 自动录制（推荐）")
            print("  - manual : 手工输入")

    except ImportError as e:
        print("❌ 缺少依赖库")
        print(f"   错误: {e}")
        print("\n请先安装:")
        print("  pip install pynput")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
