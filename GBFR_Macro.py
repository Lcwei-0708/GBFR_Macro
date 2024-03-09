import pygetwindow as gw
import pydirectinput
import time
import keyboard
import threading
import sys
import pyautogui
from pyautogui import ImageNotFoundException
from PIL import Image

# 縮放目標圖像大小
def scale_image(target_image, window_width, window_height):
    # 計算縮放比例
    scale_width = window_width / ORIGINAL_WIDTH
    scale_height = window_height / ORIGINAL_HEIGHT

    # 選擇較小的縮放比例以確保目標圖像完全可見
    scale_factor = min(scale_width, scale_height)

    # 縮放目標圖像
    target_width, target_height = target_image.size
    scaled_width = int(target_width * scale_factor)
    scaled_height = int(target_height * scale_factor)
    scaled_target_image = target_image.resize((scaled_width, scaled_height))

    return scaled_target_image

# 加載目標圖像
def load_target_images(target_images):
    global scaled_target_images
    for name, path in target_images.items():
        image = Image.open(path)
        scaled_image = scale_image(image, target_window_width, target_window_height)
        scaled_target_images[name] = scaled_image
    return scaled_target_images

# 偵測指定畫面是否存在
def detect_img(target_image, screenshot):
    try:
        if pyautogui.locate(target_image, screenshot, confidence=0.75, grayscale=True):
            return True
    except ImageNotFoundException:
        return False

# 獲取目標視窗
def get_target_window():
    try:
        return gw.getWindowsWithTitle(target_window_title)[0]
    except IndexError:
        return None

# 檢查視窗是否被聚焦
def is_window_focused(window):
    return window.isActive

# 當按下f1時執行的指令（左鍵連點）
def f1_commands(stop_event):
    while not stop_event.is_set():        
        pydirectinput.mouseDown()
        time.sleep(0.0000001)
        pydirectinput.mouseUp()
        time.sleep(0.0000001)

# 當按下f2時執行的指令（素材掛機）
def f2_commands(stop_event):
    global finish_counts
    while not stop_event.is_set():
        print("偵測畫面中...")
        screenshot = pyautogui.screenshot(allScreens=True)
        if detect_img(scaled_target_images['continue'], screenshot):
            pydirectinput.press('w')
            time.sleep(0.1)
            pydirectinput.press('enter')
            time.sleep(0.5)
        elif detect_img(scaled_target_images['again'], screenshot):
            pydirectinput.press('3')
            time.sleep(0.1)
            pydirectinput.press('enter')
            time.sleep(0.5)
        elif detect_img(scaled_target_images['cancel_again'], screenshot):
            pydirectinput.press('enter')
            time.sleep(0.1)
            # if detect_img(scaled_target_images['confirm'], screenshot):
            finish_counts += 1
            print(f"已完成{finish_counts}場")
            pydirectinput.press('enter')
            time.sleep(5)
        elif detect_img(scaled_target_images['exp'], screenshot):
            pydirectinput.press('enter')
            time.sleep(0.5)
        time.sleep(3)

# 當按下f3時執行的指令（高階BOSS掛機）
def f3_commands(stop_event):
    global finish_counts
    while not stop_event.is_set():
        print("偵測畫面中...")
        screenshot = pyautogui.screenshot(allScreens=True)
        if detect_img(scaled_target_images['fighting'], screenshot):
            print("偵測畫面中...")
            pydirectinput.keyDown('q')
            pydirectinput.keyDown('v')
            time.sleep(0.05)
            def Press_RG():
                while not stop_event.is_set():
                    pydirectinput.press('r')
                    pydirectinput.press('g')                    
                    time.sleep(0.05)
            RG_thread = threading.Thread(target=Press_RG)
            RG_thread.start()
            time.sleep(20)
            pydirectinput.keyUp('q')
            pydirectinput.keyUp('v')
        else:
            if detect_img(scaled_target_images['continue'], screenshot):
                pydirectinput.press('w')
                time.sleep(0.1)
                pydirectinput.press('enter')
                time.sleep(0.5)
            elif detect_img(scaled_target_images['again'], screenshot):
                pydirectinput.press('3')
                time.sleep(0.1)
                pydirectinput.press('enter')
                time.sleep(0.5)
            elif detect_img(scaled_target_images['cancel_again'], screenshot):
                pydirectinput.press('enter')
                time.sleep(1)
                # if detect_img(scaled_target_images['confirm'], screenshot):
                finish_counts += 1
                print(f"已完成{finish_counts}場")
                pydirectinput.press('enter')
                time.sleep(5)
            elif detect_img(scaled_target_images['exp'], screenshot):
                pydirectinput.press('enter')
                time.sleep(0.5)
        time.sleep(3)
    pydirectinput.keyUp('q')
    pydirectinput.keyUp('v')

# 當按下f4時執行的指令（蘭斯洛特閃避）
def f4_commands(stop_event):
    next_game_thread = threading.Thread(target=f2_commands, args=(stop_event,))
    next_game_thread.start()
    def click_mouse():
        while not stop_event.is_set():            
            time.sleep(0.0001) 
            pydirectinput.mouseDown()
            time.sleep(0.8)
            pydirectinput.mouseUp()           
        pydirectinput.mouseUp()  
    mouse_thread = threading.Thread(target=click_mouse)
    mouse_thread.start()
    while not stop_event.is_set():
        pydirectinput.keyDown('k')
        time.sleep(0.005)        
        pydirectinput.keyUp('k')
        time.sleep(0.1)     
    pydirectinput.keyUp('w')

# 當按下f8時關閉程式
def on_f8_press(event):
    global should_exit
    if event.name == 'f8':
        print("關閉程式...")
        stop_event.set()
        should_exit = True

# 按下按鍵處理任務
def on_key_press(event, stop_event):
    global current_marco
    global finish_counts
    global is_listening
    global is_macro_running
    global is_exit_listening
    if event.name == 'f1': #執行F1巨集指令
        if not is_macro_running:
            print("執行F1巨集指令（左鍵連點）")
            current_marco = 'F1'
            is_macro_running = True
            threading.Thread(target=f1_commands, args=(stop_event,)).start()
            # show_toast("執行 F1 巨集指令")
        else:
            print("已有其他巨集指令在進行")
    elif event.name == 'f2': #執行F2巨集指令
        if not is_macro_running:
            print("執行F2巨集指令（素材掛機）")
            current_marco = 'F2'
            is_macro_running = True
            threading.Thread(target=f2_commands, args=(stop_event,)).start()
        else:
            print("已有其他巨集指令在進行")
    elif event.name == 'f3': #執行F3巨集指令
        if not is_macro_running:
            current_marco = 'F3'
            print("執行F3巨集指令（高階BOSS掛機）")
            is_macro_running = True
            threading.Thread(target=f3_commands, args=(stop_event,)).start()
        else:
            print("已有其他巨集指令在進行")
    elif event.name == 'f4': #執行F4巨集指令
        if not is_macro_running:
            current_marco = 'F4'
            print("執行F4巨集指令（蘭斯洛特閃避）")
            is_macro_running = True
            threading.Thread(target=f4_commands, args=(stop_event,)).start()
        else:
            print("已有其他巨集指令在進行")
    elif event.name == 'f5': #停止所有指令
        print("正在停止所有指令...")
        stop_event.set()        
        time.sleep(1)
        current_marco = None
        finish_counts = 0
        is_listening = False
        is_macro_running = False
        is_exit_listening = True
        keyboard.unhook_all()        
        print("已停止所有指令")
        keyboard.hook_key('f8', on_f8_press)


# 目標圖像的原始大小
ORIGINAL_WIDTH = 1920
ORIGINAL_HEIGHT = 1080
# 獲取目標畫面的寬度和高度
target_window_width = 1920
target_window_height = 1080
pydirectinput.PAUSE = 0.0000001  # 設定按鍵間格時間
current_marco = None  # 初始化當前巨集指令的變數
is_listening = False  # 初始化鍵盤是否被監聽的變數
is_exit_listening = False  # 初始化離開程式按鍵是否被監聽的變數
is_macro_running = False  # 初始化是否有巨集指令正在執行的變數
should_exit = False  #初始化是否跳出迴圈的變數
unfocused_printed = False  # 初始化是否印出視窗未被聚焦的提示
stop_event = threading.Event()  # 初始化多線程活動變數
finish_counts = 0  # 初始化統計完成場數的變數
target_window_title = "Granblue Fantasy: Relink"  # 設定要捕捉的視窗標題
# 目標圖像路徑字典
target_images = {
    "continue": "./asset/continue.png",  # 設定繼續下一場的畫面路徑
    "again": "./asset/again.png",  # 設定再次挑戰的畫面路徑
    "cancel_again": "./asset/cancel_again.png",  # 設定取消繼續的畫面路徑
    "exp": "./asset/exp.png",  # 設定貢獻度的畫面路徑
    "confirm": "./asset/confirm.png",  # 設定確認挑戰的畫面路徑
    "fighting": "./asset/fighting.png"  # 設定戰鬥的畫面路徑
}
scaled_target_images = {}

# 循環檢測視窗是否被聚焦
while True:
    if should_exit:
        break
    target_window = get_target_window()
    if target_window:
        if is_window_focused(target_window):
            if target_window.width != target_window_width:
                # 獲取視窗的寬度和高度
                target_window_width = target_window.width
                target_window_height = target_window.height 
                scaled_target_images = load_target_images(target_images)
            unfocused_printed = False
            if not is_listening:                
                stop_event = threading.Event()
                keyboard.on_press(lambda event: on_key_press(event, stop_event))
                if not is_exit_listening:
                    keyboard.hook_key('f8', on_f8_press)
                    is_exit_listening = True
                is_listening = True
                if current_marco:
                    print(f"繼續執行{current_marco}指令...")
                    pydirectinput.press(current_marco)
        else:
            if not unfocused_printed:
                print("目標視窗未被聚焦...")
                unfocused_printed = True
            if is_macro_running:
                print("已暫停指令操作...")           
                stop_event.set()
            keyboard.unhook_all()
            keyboard.hook_key('f8', on_f8_press)
            is_listening = False
            is_macro_running = False
            is_exit_listening = True
    else:
        print("未找到目標視窗...")
        sys.exit()
    time.sleep(0.05)
