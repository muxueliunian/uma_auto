import cv2
import numpy as np
import os
from pathlib import Path
import image_recogniton
import pyautogui
import auto_main




def fuck_jjc():
    # 点击竞技场入口
    
    result_path = os.path.join("database", "main_interface", "compettion.png")
    if pos := image_recogniton.find_template_in_window("MuMu", result_path, threshold=0.7):
        pyautogui.click(pos)
        for a in range(3):
            print("等待"+ str(a + 1) + "秒")
            pyautogui.sleep(1)  # 等待结算界面
        
    # 检测战斗结果
    start_path = os.path.join("database", "main_interface", "jjc_start.png")
    if pos := image_recogniton.find_template_in_window("MuMu", start_path, threshold=0.8):
        pyautogui.click(pos)
        for a in range(3):
            print("等待"+ str(a + 1) + "秒")
            pyautogui.sleep(1)  # 等待结算界面
        
    # 点击匹配按钮
    pipei_path = os.path.join("database", "main_interface", "jjc_pipei.png") 
    if pos := image_recogniton.find_template_in_window("MuMu", pipei_path, threshold=0.7):
        pyautogui.click(pos)
        for a in range(3):
            print("等待"+ str(a + 1) + "秒")
            pyautogui.sleep(1)  # 等待结算界面
    
        
    
