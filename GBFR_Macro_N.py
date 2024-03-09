import pygetwindow as gw
import pydirectinput
import time
import keyboard
import threading
import sys

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
        time.sleep(0.0001)
        pydirectinput.mouseUp()
        time.sleep(0.0001)

# 當按下f2時執行的指令（素材掛機）
def f2_commands(stop_event):
    while not stop_event.is_set():
        pydirectinput.press('w')
        time.sleep(0.1)
        pydirectinput.press('enter')
        time.sleep(0.01)
        pydirectinput.press('enter')
        time.sleep(3)

# 當按下f3時執行的指令（高階BOSS掛機）
def f3_commands(stop_event):
    def press_rg():
        while not stop_event.is_set():
            pydirectinput.press('q')
            pydirectinput.press('r')
            pydirectinput.press('g')     
            time.sleep(0.0001)
    rg_thread = threading.Thread(target=press_rg)
    rg_thread.start()    
    next_game_thread = threading.Thread(target=f2_commands, args=(stop_event,))
    next_game_thread.start()
    while not stop_event.is_set():
        pydirectinput.keyDown('v')
        time.sleep(3)
        pydirectinput.keyUp('v')
    pydirectinput.keyUp('v')

# 當按下f4時執行的指令（蘭斯洛特閃避）
def f4_commands(stop_event):
    next_game_thread = threading.Thread(target=f2_commands, args=(stop_event,))
    next_game_thread.start()
    def click_mouse_middle():
        while not stop_event.is_set():
            pydirectinput.middleClick()
            pydirectinput.keyDown('v')
            time.sleep(3)            
            pydirectinput.keyUp('v')            
        pydirectinput.keyUp('v')
    mouse_thread = threading.Thread(target=click_mouse_middle)
    mouse_thread.start()
    while not stop_event.is_set():
        pydirectinput.press('k')
        pydirectinput.press('r')
        pydirectinput.press('g')
        time.sleep(0.1)

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
        is_listening = False
        is_macro_running = False
        is_exit_listening = True
        keyboard.unhook_all()
        print("已停止所有指令")
        keyboard.hook_key('f8', on_f8_press)


pydirectinput.PAUSE = 0.0000001  # 設定按鍵間格時間
current_marco = None  # 初始化當前巨集指令的變數
is_listening = False  # 初始化鍵盤是否被監聽的變數
is_exit_listening = False  # 初始化離開程式按鍵是否被監聽的變數
is_macro_running = False  # 初始化是否有巨集指令正在執行的變數
should_exit = False  #初始化是否跳出迴圈的變數
unfocused_printed = False  # 初始化是否印出視窗未被聚焦的提示
stop_event = threading.Event()  # 初始化多線程活動變數
target_window_title = "Granblue Fantasy: Relink"  # 設定要捕捉的視窗標題

# 循環檢測視窗是否被聚焦
while True:
    if should_exit:
        break
    target_window = get_target_window()
    if target_window:
        if is_window_focused(target_window):           
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
