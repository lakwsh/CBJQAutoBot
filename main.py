import ctypes
import re
from sys import exit
from time import sleep
from random import randint

import numpy as np
import pyautogui
import win32con
import win32gui
from PIL import ImageGrab
from paddleocr import PaddleOCR


class CBJQAutoBot:
    def __init__(self) -> None:
        self.hwnd = win32gui.FindWindow(None, '尘白禁区')
        if not self.hwnd:
            print("未找到游戏窗口")
            exit(1)
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)
        sleep(0.1)
        self.rect = win32gui.GetWindowRect(self.hwnd)
        print(self.rect)
        self.ocr = PaddleOCR(device='gpu', use_doc_orientation_classify=False, use_doc_unwarping=False,
                             text_detection_model_name='PP-OCRv5_mobile_det',
                             text_recognition_model_name='PP-OCRv5_mobile_rec')
        self.screen = []
        region = np.array([(0.052, 0.246, 0.312, 0.801), (0.37, 0.246, 0.63, 0.801), (0.688, 0.246, 0.948, 0.801)])
        self.region = [self.rect[2] - self.rect[0], self.rect[3] - self.rect[1]] * 2 * region

    def capture(self) -> None:
        if not win32gui.IsWindow(self.hwnd):
            print('无法找到游戏窗口')
            exit(1)
        res = self.ocr.predict(np.array(ImageGrab.grab(self.rect)))[0]
        self.screen = [[res['rec_texts'][i], res['rec_boxes'][i]] for i in range(len(res['rec_texts']))]
        # print(res['rec_texts'])

    def check(self, lst: list[str]) -> bool:
        lst.append('尘白')
        for res in self.screen:
            for i in lst[:]:
                if re.search(i, res[0]):
                    lst.remove(i)
        return len(lst) == 0

    def skill(self) -> list:
        skill = []
        for i in self.region:
            lst = []
            for res in self.screen:
                # print(res, i)
                if len(res[0]) > 2 and i[0] <= res[1][0] <= i[2] and i[1] <= res[1][1] <= i[3]:
                    lst.append(res[0])
            if not len(lst):
                raise Exception("增益获取失败")
            skill.append(lst)
        return skill

    def click(self, text: str) -> bool:
        for i in self.screen:
            if i[0].find(text) != -1:
                i[1] += np.array(self.rect[:2] * 2)
                # print(i[1])
                pyautogui.moveTo(i[1][2], i[1][3], duration=0.1)
                pyautogui.click()
                sleep(0.1)
                return True
        return False

    def run(self) -> None:
        cnt = 0
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
                elif self.check(['模式选择', '增益试炼·渊底', '增益试炼·幽馆', '增益试炼·异城']):
                    print('增益试炼')
                    rand = randint(1, 3)
                    if rand == 1:
                        self.click('增益试炼·渊底')
                    elif rand == 2:
                        self.click('增益试炼·幽馆')
                    else:
                        self.click('增益试炼·异城')
                elif self.check(['难度选择', '增益试炼·厄险']):
                    print('增益试炼')
                    self.click('增益试炼·厄险')
                elif self.check(['\s+选择', '增益试炼']):
                    print('增益试炼')
                    self.click('增益试炼')
                elif self.check(['开始作战']):
                    print('开始作战')
                    self.click('开始作战')
                elif self.check(['坚守阵地', '抵御第1波袭击']):
                    print('进入战斗')
                    pyautogui.keyDown('w')
                    sleep(0.3)
                    pyautogui.keyUp('w')
                    sleep(0.2)
                elif self.check(['第.+波', '击败来袭的敌方目标']):
                    print('战斗中')
                    if cnt < 8:
                        pyautogui.press('e')
                        cnt += 1
                    else:
                        pyautogui.press('q')
                        cnt = 0
                elif self.check(['选择增益', '确认']):
                    print('选择增益')
                    choice = [[], [], []]
                    for i in self.skill():
                        if not '单体' in i:
                            if not '该增益已获取' in i:
                                choice[0].append(i[0])
                            choice[1].append(i[0])
                        else:
                            choice[2].append(i[1])
                    if len(choice[0]):
                        self.click(choice[0][0])
                    elif len(choice[1]):
                        self.click(choice[1][0])
                    else:
                        self.click(choice[2][0])
                    self.click('确认')
                elif self.check(['单体', '(丢|丟)弃']):
                    print('选择增益-单体')
                    self.click('丟弃')
                    self.click('丢弃')
                elif self.check(['弃在试炼中选择的增益', '取消', '确定']):
                    print('丢弃增益')
                    self.click('确定')
                elif self.check(['奖励列表', '退出']):
                    print('战斗结算')
                    self.click('退出')
                elif self.check(['检测到时间节点变化', '确定']):
                    print('时间节点变化')
                    self.click('确定')
                else:
                    sleep(1)
                    continue
                sleep(0.5)
            except KeyboardInterrupt:
                print("脚本已停止")
                break
            except Exception as e:
                print(f"错误: {str(e)}")
                sleep(0.5)


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('请使用管理员权限运行脚本')
        exit(1)
    bot = CBJQAutoBot()
    bot.run()
