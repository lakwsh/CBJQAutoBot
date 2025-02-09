import re
from time import sleep

import numpy as np
import pyautogui
import win32con
import win32gui
from PIL import ImageGrab
from paddleocr import PaddleOCR


class CBJQAutoBot:
    def __init__(self) -> None:
        hwnd = win32gui.FindWindow(None, '尘白禁区')
        if not hwnd:
            raise Exception("未找到游戏窗口")
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        sleep(0.1)
        self.rect = win32gui.GetWindowRect(hwnd)
        print(self.rect)
        self.ocr = PaddleOCR(use_gpu=True, use_angle_cls=True, lang='ch', ocr_version='PP-OCRv4')
        self.screen = []
        region = np.array([(0.068, 0.25, 0.292, 0.73), (0.388, 0.25, 0.612, 0.73), (0.708, 0.25, 0.932, 0.73)])
        self.region = [self.rect[2] - self.rect[0], self.rect[3] - self.rect[1]] * 2 * region

    def capture(self) -> None:
        self.screen = self.ocr.ocr(img=np.array(ImageGrab.grab(self.rect)), det=True)[0]
        # print([i[1][0] for i in self.screen])

    def check(self, lst: list[str]) -> bool:
        lst.append('尘白禁区')
        for res in self.screen:
            for i in lst[:]:
                if re.search(i, res[1][0]):
                    lst.remove(i)
        return len(lst) == 0

    def skill(self) -> list:
        skill = []
        for i in self.region:
            lst = []
            for res in self.screen:
                # print(res[0], i)
                if i[0] <= res[0][0][0] <= i[2] and i[1] <= res[0][0][1] <= i[3]:
                    lst.append(res[1][0])
            skill.append(lst)
        return skill

    def click(self, text: str) -> bool:
        for i in self.screen:
            if i[1][0] == text:
                i[0] = np.array(i[0]) + np.array(self.rect[:2])
                # print(i[0])
                pos = i[0][2]  # 左上 右上 右下(2) 左下
                pyautogui.moveTo(pos[0], pos[1], duration=0.1)
                pyautogui.click()
                return True
        return False

    def run(self) -> None:
        while True:
            try:
                self.capture()
                if self.check(['供应站', '活动']):
                    print('首页')
                    self.click('战斗')
                elif self.check(['主线故事', '个人故事']):
                    print('战斗')
                    self.click('悖论迷宫')
                elif self.check(['限时', '验证战场']):
                    print('悖论迷宫')
                    self.click('验证战场')
                elif self.check(['积分奖励', '增益获取']):
                    print('验证战场')
                    self.click('增益试炼')
                elif self.check(['难度选择', '增益试炼·厄险']):
                    print('增益试炼')
                    self.click('增益试炼·厄险')
                elif self.check(['开始作战']):
                    print('开始作战')
                    self.click('开始作战')
                elif self.check(['第.+波', '击败来袭的敌方目标']):
                    print('战斗中')
                    pyautogui.press('q')
                    sleep(0.2)
                    pyautogui.press('e')
                    sleep(0.5)
                elif self.check(['选择增益', '确认']):
                    print('选择增益')
                    for i in self.skill():
                        if not '单体' in i:
                            self.click(i[0])
                            break
                    self.click('确认')
                elif self.check(['单体', '丢弃']):
                    print('选择增益-单体')
                    pyautogui.moveTo(self.rect[2] - 100, self.rect[3] - 100, duration=0.1)
                    pyautogui.click()
                elif self.check(['奖励列表', '退出']):
                    print('战斗结算')
                    self.click('退出')
                else:
                    sleep(1)
                    continue
                sleep(0.5)
            except KeyboardInterrupt:
                print("脚本已停止")
                break
            except Exception as e:
                print(f"错误: {str(e)}")
                sleep(1)


if __name__ == "__main__":
    bot = CBJQAutoBot()
    bot.run()
