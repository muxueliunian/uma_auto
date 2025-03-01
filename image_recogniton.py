import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import auto_main


def find_template_in_window(window_title, template_path, threshold=0.8):
    """
    在指定窗口内进行模板匹配
    :param window_title: 窗口标题（支持模糊匹配）
    :param template_path: 模板图片路径
    :param threshold: 匹配阈值（0-1）
    :return: 成功返回中心坐标(x,y)，失败返回None并输出信息
    """
    try:
        # 获取目标窗口
        win = pyautogui.getWindowsWithTitle(window_title)
        if not win:
            print(f"未找到标题包含 '{window_title}' 的窗口")
            return None
            
        win = win[0]
        win.activate()  # 激活窗口
        pyautogui.sleep(0.5)  # 等待窗口激活
        
        # 截取窗口区域
        left, top, width, height = win.left, win.top, win.width, win.height
        screenshot = ImageGrab.grab(bbox=(left, top, left+width, top+height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # 读取模板图片
        template = cv2.imread(template_path)
        if template is None:
            print(f"无法读取模板文件: {template_path}")
            return None
            
        # 进行模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # 计算中心坐标（相对于屏幕）
            h, w = template.shape[:2]
            center_x = int(left + max_loc[0] + w/2)
            center_y = int(top + max_loc[1] + h/2)
            return (center_x, center_y)
        else:
            print(f"匹配失败，最大相似度: {max_val:.2f}")
            return None
            
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return None

def find_template_location(template_path, screenshot_path, threshold=0.8, max_scales=5):
    """在截图中查找模板匹配位置
    :param template_path: 模板图片路径
    :param screenshot_path: 截图文件路径
    :param threshold: 匹配阈值（0-1）
    :param max_scales: 最大缩放检测次数
    :return: (中心坐标(x,y), 匹配度, 是否成功)
    """
    try:
        # 读取截图和模板
        screenshot = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        
        if screenshot is None or template is None:
            print("无法读取截图或模板文件")
            return (0, 0), 0.0, False

        # 多尺度检测
        best_match = None
        scales = np.linspace(0.5, 1.2, max_scales)  # 优化缩放范围
        
        for scale in scales:
            try:
                # 调整模板尺寸
                resized = cv2.resize(template, None, fx=scale, fy=scale)
                h, w = resized.shape[:2]

                # 跳过尺寸过大的模板
                if h > screenshot.shape[0] or w > screenshot.shape[1]:
                    continue

                # 执行模板匹配
                result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                # 更新最佳匹配
                if not best_match or max_val > best_match[0]:
                    best_match = (max_val, max_loc, scale, resized.shape)

                # 提前退出条件
                if max_val > threshold + 0.1:  # 发现高质量匹配时提前退出
                    break
                    
            except Exception as e:
                print(f"缩放检测异常 (scale={scale:.2f}): {str(e)}")
                continue

        # 处理匹配结果
        if best_match and best_match[0] >= threshold:
            max_val, max_loc, scale, (h, w) = best_match
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            if show_result:
                # 绘制匹配结果
                debug_img = screenshot.copy()
                cv2.rectangle(debug_img, max_loc, (max_loc[0]+w, max_loc[1]+h), (0,255,0), 2)
                cv2.putText(debug_img, f"Conf: {max_val:.2f}", (max_loc[0], max_loc[1]-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                cv2.imshow('Match Result', debug_img)
                cv2.waitKey(2000)  # 显示2秒
                cv2.destroyAllWindows()
                
            return (center_x, center_y), max_val, True
            
        return (0, 0), best_match[0] if best_match else 0.0, False  # 总是返回最大相似度

    except Exception as e:
        print(f"模板匹配异常: {str(e)}")
        return (0, 0), 0.0, False
