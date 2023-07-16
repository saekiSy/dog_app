import PySimpleGUI as sg
import os
import random
import time
import subprocess
import shutil
import sys
import threading
from logging import NullHandler

# フォルダのパス
path_current_dir = os.path.dirname(sys.argv[0])
# テスト用
vea_folder_path = "vea_dog"

# 画像のパス
# テスト用
image_paths = [
    "image/bawwow.PNG",
    "image/I'meating.PNG",
    "image/buono.PNG",
    "image/mogmog.PNG",
    "image/yumyum.PNG",
    "image/おいしい.PNG"
]

# ウィンドのレイアウト
layout = [
    [sg.Text("")],
    [sg.Text("baw wow",font=(25))],
    [sg.Text("Skinny dog processを実行します🐕",font=(20))],
    [sg.Text("")],
    [sg.Text("注意：",font=(15))],
    [sg.Text("このプロセスは非常に破壊的です。以下を守ってください",font=(15))],
    [sg.Text("1.vea_dogディレクトリ内に大事なファイルを置かないでください",font=(15))],
    [sg.Text("2.dog_appフォルダ内のファイルをdog_appフォルダ外に移動させないでください",font=(15))],
    [sg.Text("詳細はreadmeをご確認ください",font=(15))],
    [sg.Text("")],
    [sg.Button("wan(はい)", key="-WAN-",font=(20)), sg.Button("grrrr(いいえ)", key="-GRR-",font=(20))]
]
window = sg.Window("Skinny Skinny Doggy", layout, finalize=True, size=(600, 300))

# 画像ファイルに番号をつけるためのカウンタ(重複防止)
image_counter = 1
# タイマーフラグ
streamstop = False
# お腹いっぱいフラグ
dogs_are_full_of_food_flag = False

file_list = os.listdir(vea_folder_path)
# 隠しファイルは削除しない
file_list = [file_name for file_name in file_list if not file_name.startswith('.')]

# 定期でコールバックしタイマの停止フラグを確認する
def tm_callback():
    global tm
    global streamstop
    tm.cancel()
    del tm
    tm = NullHandler

    if streamstop == False:
        tm = threading.Timer(10, tm_callback)
        tm.start()
    else:
        return

# 本処理
def process_files():
    global image_counter
    global streamstop
    global dogs_are_full_of_food_flag
    global file_list

    length = len(file_list)

    for file_name in file_list:
        if streamstop:
            break
        # ファイル削除
        file_path = os.path.join(vea_folder_path, file_name)
        os.remove(file_path)
        print(file_path)

        ## 画像処理
        # ランダムで画像を選択
        image_path = random.choice(image_paths)
        file_name = os.path.basename(image_path)
        destination_path = os.path.join(vea_folder_path, file_name)
        # 画像に連番をつける
        base_name, extension = os.path.splitext(file_name)
        new_file_name = f"{base_name}_{image_counter}{extension}"
        destination_path = os.path.join(vea_folder_path, new_file_name)
        shutil.copyfile(image_path, destination_path)

        # カウンタ更新
        image_counter += 1
        length -= 1

        # lengthからファイルの犬化の進行具合を確認する
        if length == 0 or streamstop == True:
            # 全てのファイルが犬化したらループ終了
            dogs_are_full_of_food_flag = True
            streamstop = True
            tm.cancel()
            window.write_event_value("-FINISH-", "")
            break
        else:
            # range内の数字を変えると犬化にかかる時間が変わるよ
            for i in range(360):
                if streamstop:
                    break
                # クローズによる強制終了を考慮し10秒刻みでsleepする
                time.sleep(10)

def main():
    global tm
    global image_counter
    global dogs_are_full_of_food_flag
    global streamstop

    tm = threading.Timer(10,tm_callback)
    tm.start()
    while True:
        event, values = window.read()
        if event == "-WAN-":
            if len(file_list) != 0:
                sg.popup("Skinny dog processを開始します🐕")
                sg.popup("途中でやめる場合はキャンセル、またはウィンドウ右側の×を押してください")
                threading.Thread(target=process_files).start()  # 周期処理を別スレッドで実行
            else:
                tm.cancel()
                window.write_event_value("-CLOSE-", "")
                break
        elif event == "-GRR-" or event == sg.WIN_CLOSED:
            streamstop = True
            tm.cancel()
            window.write_event_value("-CLOSE-", "")
            break
        elif event == "-FINISH-":
            dogs_are_full_of_food_flag = True
            window.write_event_value("-CLOSE-", "")  # ウィンドウを閉じるイベントを通知
        if dogs_are_full_of_food_flag:
            sg.popup("woof(お腹いっぱいになりました)")
            window.close()
            break

    window.close()

if __name__ == '__main__':
    main()