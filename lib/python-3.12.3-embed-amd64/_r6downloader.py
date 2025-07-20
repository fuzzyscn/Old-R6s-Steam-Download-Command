import os
import re
import time
import shutil
import datetime
import threading
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

version_map = {
    "Y1S0" : ["r6_y1s0_377237", "r6_y1s0_359551", 7, 0, "2015年初代 ", "Plazas\\PLAZA_BO", "RainbowSixGame.exe", "8358812283631269928", "3893422760579204530", "14.2 GB "],
    "Y1S1" : ["r6_y1s1_377237", "r6_y1s1_359551", 7, 0, "墨冰行动 ", "Plazas\\PLAZA_BO", "RainbowSixGame.exe", "5188997148801516344", "7932785808040895147", "16.7 GB "],
    "Y1S2" : ["r6_y1s2_377237", "r6_y1s2_359551", 7, 0, "尘土战线 ", "Plazas\\PLAZA_BO", "RainbowSixGame.exe", "2303064029242396590", "2206497318678061176", "20.9 GB "],
    "Y1S3" : ["r6_y1s3_377237", "r6_y1s3_359551", 7, 0, "骷髅雨行动 ", "Plazas\\PLAZA_BO", "RainbowSixGame.exe", "5819137024728546741", "5851804596427790505", "25.1 GB "],
    "Y1S4" : ["r6_y1s4_377237", "r6_y1s4_359551", 7, 0, "赤鸦行动 ", "Plazas\\PLAZA_BO", "RainbowSixGame.exe", "3576607363557872807", "8569920171217002292", "28.5 GB "],
    "Y2S1" : ["r6_y2s1_377237", "r6_y2s1_359551", 7, 0, "丝绒壳行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "2248734317261478192", "8006071763917433748", "33.2 GB "],
    "Y2S2" : ["r6_y2s2_377237", "r6_y2s2_359551", 7, 0, "健康行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "5875987479498297665", "708773000306432190", "34 GB "],
    "Y2S3" : ["r6_y2s3_377237", "r6_y2s3_359551", 7, 0, "血兰花行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "6708129824495912434", "1613631671988840841", "34.3 GB "],
    "Y2S4" : ["r6_y2s4_377237", "r6_y2s4_359551", 7, 0, "白噪声行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "8748734086032257441", "4221297486420648079", "48.7 GB "],
    "Y3S1" : ["r6_y3s1_377237", "r6_y3s1_359551", 7, 0, "奇美拉行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "5071357104726974256", "4701787239566783972", "58.8 GB "],
    "Y3S2" : ["r6_y3s2_377237", "r6_y3s2_359551", 7, 0, "备战行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "6507886921175556869", "8765715607275074515", "63.3 GB "],
    "Y3S3" : ["r6_y3s3_377237", "r6_y3s3_359551", 7, 0, "暗空行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "5562094852451837435", "7781202564071310413", "72.6 GB "],
    "Y3S4" : ["r6_y3s4_377237", "r6_y3s4_359551", 7, 0, "风城行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "6502258854032233436", "7659555540733025386", "76.9 GB "],
    "Y4S1" : ["r6_y4s1_377237", "r6_y4s1_359551", 7, 0, "燃烧地平线 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "8356277316976403078", "5935578581006804383", "59.7 GB "],
    "Y4S2" : ["r6_y4s2_377237", "r6_y4s2_359551", 7, 0, "幻镜行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "693082837425613508", "5408324128694463720", "67.1 GB "],
    "Y4S3" : ["r6_y4s3_377237", "r6_y4s3_359551", 7, 0, "余烬重燃行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "3546781236735558235", "7869081741739849703", "69.6 GB "],
    "Y4S4" : ["r6_y4s4_377237", "r6_y4s4_359551", 7, 0, "幻变潮汐行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "299124516841461614", "1842268638395240106", "75.2 GB "],
    "Y5S1" : ["r6_y5s1_377237", "r6_y5s1_359551", 7, 0, "虚空边境行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "4736360397583523381", "6296533808765702678", "74.3 GB "],
    "Y5S2" : ["r6_y5s2_377237", "r6_y5s2_359551", 7, 0, "钢流行动 ", "Plazas\\PLAZA_NEW", "RainbowSixGame.exe", "4367817844736324940", "893971391196952070", "81.3 GB "],
    "Y5S3" : ["r6_y5s3_377237", "r6_y5s3_359551", 9, 1, "暗影传承行动 ", "Plazas\\Y5S3", "RainbowSix.bat", "85893637567200342", "3089981610366186823", "支持全皮肤和地图编辑器 "],
    "Y5S4" : ["r6_y5s4_377237", "r6_y5s4_359551", 12, 0, "霓虹黎明行动", "Plazas\\CPlay", "RainbowSix.bat", "3390446325154338855", "6947060999143280245", " "],
    "Y6S1" : ["r6_y6s1_377237", "r6_y6s1_359551", 12, 0, "深红劫案行动 ", "Plazas\\CPlay", "RainbowSix.bat", "7890853311380514304", "7485515457663576274", " "],
    "Y6S2" : ["r6_y6s2_377237", "r6_y6s2_359551", 12, 0, "北极星行动 ", "Plazas\\CPlay", "RainbowSix.bat", "8733653062998518164", "809542866761090243", " "],
    "Y6S3" : ["r6_y6s3_377237", "r6_y6s3_359551", 11, 0, "晶坚守卫行动 ", "Plazas\\UPCR1", "RainbowSix.bat", "4859695099882698284", "6526531850721822265", " "],
    "Y6S4" : ["r6_y6s4_377237", "r6_y6s4_359551", 8, 0, "精兵锐器行动 ", "Plazas\\UPCR2_NEW", "RainbowSix.bat", "2637055726475611418", "8627214406801860013", " "],
    "Y7S1" : ["r6_y7s1_377237", "r6_y7s1_359551", 8, 0, "鬼面行动 ", "Plazas\\UPCR2_NEW", "RainbowSix.bat", "8323869632165751287", "2178080523228113690", " "],
    "Y7S2" : ["r6_y7s2_377237", "r6_y7s2_359551", 8, 0, "矢量光影行动 ", "Plazas\\UPCR2_NEW", "RainbowSix.bat", "1363132201391540345", "133280937611742404", " "],
    "Y7S3" : ["r6_y7s3_377237", "r6_y7s3_359551", 8, 0, "残蜂汹涌行动 ", "Plazas\\UPCR2_NEW", "RainbowSix.bat", "6425223567680952075", "5906302942203575464", " "],
    "Y7S4" : ["r6_y7s4_377237", "r6_y7s4_359551", 9, 1, "烈日突袭行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "4466027729495813039", "1819898955518120444", " "],
    "Y8S1" : ["r6_y8s1_377237", "r6_y8s1_359551", 9, 1, "头号指令行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "3275824905781062648", "5863062164463920572", " "],
    "Y8S2" : ["r6_y8s2_377237", "r6_y8s2_359551", 9, 1, "恐惧因素行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "3050554908913191669", "1575870740329742681", "全干员孤狼猎恐"],
    "Y8S3" : ["r6_y8s3_377237", "r6_y8s3_359551", 9, 1, "开路先锋行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "7845616952346988253", "7492642056657673136", "没有解锁全干员"],
}

def log_message(msg, level="info"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    tag = {"info": "💬", "error": "❌", "warn": "⚠️", "success": "✅"}
    prefix = tag.get(level, "💬")
    full_msg = f"[{now}] {prefix} {msg}\n"
    text.insert(tk.END, full_msg, level)
    text.see(tk.END)  # 自动滚动到底部

def clear_log():
    text.delete(1.0, tk.END)
    log_message("日志已清空。", "warn")

def save_log():
    log_content = text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("文本文件", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(log_content)
        log_message(f"日志已保存到：{file_path}", "success")

def show_help():
    log_message("使用说明：请选择安装位置和赛季版本，然后点击开始下载。", "info")
    log_message("Y6S1之前的赛季及Y8S2赛季免登录Steam账号，可验证完整性。", "info")

def check_dotnet_runtime():
    runtime_flag = os.path.exists("lib/net9.txt")
    if not runtime_flag:
        log_message("正在安装 .NET 9.0 运行库...", "warn")
        try:
            # 启动安装包
            subprocess.run('lib\\dotnet-runtime-9.0.3-win-x64.exe', shell=True)
            log_message("✔️ 安装完成。请继续选择安装路径。", "success")
            # 创建标记文件
            with open("lib/net9.txt", "w") as f:
                f.write("dotnet 9.0 installed")
        except Exception as e:
            log_message(f"❌ 安装失败：{e}", "error")
            return False
    else:
        log_message("✔️ 已检测到 .NET 9.0 运行库。", "success")
    # 启用路径选择按钮
    select_dir_button.config(state="normal")
    return True

start_time = time.time()  # 在下载开始时记录
def update_progress_from_line(line):
    match = re.search(r'(\d+(\.\d+)?)%', line)
    if match:
        raw_value = float(match.group(1))
        percent = round(raw_value, 2)
        progress_var.set(percent)

        # 只显示已用时间
        elapsed = time.time() - start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        time_str = f"{mins:02}:{secs:02}"

        progress_label.config(text=f"进度：{percent:.2f}% | 已用时间：{time_str}")
        root.update_idletasks()

def run_command_live(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        log_message(line.strip(), "info")
        update_progress_from_line(line)
    process.wait()
    if process.returncode != 0:
        log_message("❌ 命令执行失败", "error")
    else:
        log_message("✅ 命令执行完成", "success")
        progress_var.set(100)  # 任务完成后设置为100%

def run_download(dir, version):
    global start_time
    start_time = time.time()
    start_button.config(text="下载中...")    
    start_button.config(state="disabled")
    select_dir_button.config(state="disabled")
    
    install_path = dir
    manifest1 = version_map[version][7]
    manifest2 = version_map[version][8]
    log_message(f"📁 游戏的安装路径: {install_path}")
    log_message(f"🚀 开始下载赛季版本: {version}")

    mFile_1 = f"lib\\depotcache\\377237_{manifest1}.manifest"
    mFile_2 = f"lib\\depotcache\\359551_{manifest2}.manifest"

    cmd1 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest {manifest1} -depotkeys lib\\steam.keys -manifestfile {mFile_1} -dir "{install_path}"'
    cmd2 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest {manifest2} -depotkeys lib\\steam.keys -manifestfile {mFile_2} -dir "{install_path}"'

    log_message("开始执行第一部分下载...", "warn")
    run_command_live(cmd1)

    log_message("开始执行第二部分下载...", "warn")
    run_command_live(cmd2)
    #log_message(cmd2)

    log_message("🎉 下载任务全部完成！", "success")
    
    if messagebox.askyesno("任务完成", "下载完成，是否打开文件夹？"):
        os.startfile(install_path)
        
    start_button.config(text="开始下载")
    start_button.config(state="normal")
    select_dir_button.config(state="normal")

def run_verify(dir, version):
    global start_time
    start_time = time.time()
    start_button.config(text="验证中...")
    start_button.config(state="disabled")
    select_dir_button.config(state="disabled")

    install_path = dir
    manifest1 = version_map[version][7]
    manifest2 = version_map[version][8]
    log_message(f"📁 游戏的安装路径: {install_path}")
    log_message(f"🚀 开始验证完整性: {version}")

    mFile_1 = f"lib\\depotcache\\377237_{manifest1}.manifest"
    mFile_2 = f"lib\\depotcache\\359551_{manifest2}.manifest"

    cmd1 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest {manifest1} -depotkeys lib\\steam.keys -manifestfile {mFile_1} -validate -dir "{install_path}"'
    cmd2 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest {manifest2} -depotkeys lib\\steam.keys -manifestfile {mFile_2} -validate -dir "{install_path}"'

    log_message("开始执行第一部分验证...", "warn")
    run_command_live(cmd1)

    log_message("开始执行第二部分验证...", "warn")
    run_command_live(cmd2)
    #log_message(cmd2)

    log_message("🎉 验证完整性全部完成！", "success")
    
    if messagebox.askyesno("任务完成", "下载完成，是否打开文件夹？"):
        os.startfile(install_path)
        
    start_button.config(text="验证完整性")
    start_button.config(state="normal")
    select_dir_button.config(state="normal")

def download_game(folder, version):
    threading.Thread(target=run_download, args=(folder, version), daemon=True).start()

def verify_files(folder, version):
    threading.Thread(target=run_verify, args=(folder, version), daemon=True).start()

def has_existing_game_files(folder):
    required_files = ["defaultargs.dll", "rainbowsix.exe", "rainbowsixgame.exe"]
    for filename in required_files:
        if os.path.exists(os.path.join(folder, filename)):
            return True
    return False

def select_dir(entry):
    dir = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir)

    # 路径格式检查
    if re.search(r'[\u4e00-\u9fff]', dir) or ' ' in dir:
        messagebox.showerror("路径错误", "路径不可包含中文或空格，请重新选择英文路径。")
        log_message("路径错误：包含中文或空格", "error")
        entry.delete(0, tk.END)
        start_button.config(state="disabled")
        return

    # 检查文件夹是否为空
    if not os.listdir(dir):
        log_message(f"安装路径验证成功：准备下载到 {dir}", "success")
        start_button.config(text="开始下载")
        start_button.config(command=lambda: download_game(dir, entry1.get().split()[0]))
        start_button.config(state="normal")
    else:
        if has_existing_game_files(dir):
            log_message("检测到游戏文件：进入验证模式🔍", "info")
            start_button.config(text="验证完整性")
            start_button.config(command=lambda: verify_files(dir, entry1.get().split()[0]))
            start_button.config(state="normal")
        else:
            messagebox.showerror("安装目录无效", "请选择空文件夹或包含游戏文件的目录。")
            log_message("目录非空且无游戏文件", "error")
            entry.delete(0, tk.END)
            start_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("彩虹六号旧版本下载器 v2.0 By Fuzzys QQ群：439523286")
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(1, weight=1)

    ttk.Label(root, text='请选择安装文件夹：').grid(row=0, column=0)
    entry0 = ttk.Entry(root, width=37)
    entry0.grid(row=0, column=1)
    entry0.insert(0, "安装路径必须是纯英文且没有空格")

    select_dir_button = ttk.Button(root, text='选择', command=lambda: select_dir(entry0))
    select_dir_button.grid(row=0, column=2)
    select_dir_button.config(state="disabled")  # 初始禁用

    ttk.Label(root, text='请选择赛季版本：').grid(row=1, column=0)
    version_display_map = {k: f"{k} {v[4]+v[9]}" for k, v in version_map.items()}
    version_names = list(version_display_map.values())
    version_var = tk.StringVar()
    entry1 = ttk.Combobox(root, textvariable=version_var, values=version_names, state="readonly", width=35)
    entry1.grid(row=1, column=1)
    entry1.set(version_display_map["Y3S1"])  # 设置默认名称
    start_button = ttk.Button(root, text='开始下载')
    start_button.grid(row=1, column=2)
    start_button.config(state="disabled")  # 初始禁用

    ttk.Button(root, text="清空日志", command=clear_log).grid(row=5, column=0, pady=5)
    ttk.Button(root, text="保存日志", command=save_log).grid(row=5, column=2, pady=5)

    global text
    text = tk.Text(root, width=80, height=20)
    text.grid(row=4,columnspan=3)
    # 设置颜色标签
    text.tag_config("info", foreground="blue")
    text.tag_config("success", foreground="green")
    text.tag_config("error", foreground="red")
    text.tag_config("warn", foreground="orange")
    text.grid(row=4, columnspan=3, sticky="nsew")
    
    check_dotnet_runtime()  # 启动时检测并决定是否启用按钮
    show_help()

    progress_var = tk.DoubleVar()
    progressbar = ttk.Progressbar(root, variable=progress_var, orient="horizontal", length=500, mode="determinate")
    progressbar.grid(row=6, columnspan=3, pady=(0, 10))
    progress_label = ttk.Label(root, text="进度：0% | 已用时间：--:--")
    progress_label.grid(row=5, columnspan=3)

    root.mainloop()

def AddPatch(_version, _gamePath):
    try:
        print("如上述出现 Trying again (#10) 字样请开启Steam社区加速器重试！（302或UU路由模式）")
        name = input("\n下载验证完毕，为避免存档冲突及联机使用，请输入你的英文游戏昵称（不要直接回车！）：")
        name += '-'+_version
        patchFileCount = 0
        patchFolderCount = 0
        patchFilePath = "lib\\" + manifestList[_version][5]
        patchFileList = os.listdir(patchFilePath)
        for file in patchFileList:
            srcPath = os.path.join(patchFilePath, file)
            dstPath = os.path.join(_gamePath, file)
            if os.path.isdir(srcPath):
                if os.path.exists(dstPath):
                    shutil.rmtree(dstPath)#提前删除已存在的补丁文件夹
                shutil.copytree(srcPath, dstPath)
                patchFolderCount += 1
            else:
                shutil.copy(srcPath, dstPath)
                patchFileCount += 1
                if file.endswith('.ini') and file != "steam_emu.ini":
                    if os.path.exists(dstPath):
                        with open(dstPath, 'rt') as f:
                            content = f.read()
                            modified_content = re.sub('CHANGEGAMENAME', name, content)
                            modified_content = re.sub('CHANGEUSERNAME', name, modified_content)
                            f.close()
                        with open(dstPath, 'wt') as f:
                            f.write(modified_content)
                            f.close()
                if file.endswith('HeliosLoader.json'):#Y5S3 Heated Metal
                    if os.path.exists(dstPath):
                        with open(dstPath, 'rt') as f:
                            content = f.read()
                            modified_content = re.sub('CHANGEUSERNAME', name, content)
                            f.close()
                        with open(dstPath, 'wt') as f:
                            f.write(modified_content)
                            f.close()
                            
        if patchFolderCount != manifestList[_version][3]:
            print("\n破解补丁文件夹数量不一致！请关闭杀毒软件，重新解压下载器安装包！")
        elif patchFileCount != manifestList[_version][2]:
            print("\n破解补丁文件数量不一致！请关闭杀毒软件，重新解压下载器安装包！")
        elif patchFileCount > 0:
            print("\n破解补丁已安装成功！补丁文件数量："+str(patchFileCount)+" 文件夹数量："+str(patchFolderCount))
            
        startGamePath = os.path.join(_gamePath, manifestList[_version][6])
        if manifestList[_version][6] == "RainbowSixGame.exe":
            if os.path.exists(startGamePath):
                startGame = input("\n启动游戏的 exe 文件已准备好，是否启动游戏？(y/n)：")
                startGame = startGame.lower()
                if startGame == "y":
                    RunGame(startGamePath, _gamePath)
                print("\n即将返回主菜单！如自动启动卡BettleEye安装，请尝试手动启动游戏。")
                print("游戏启动路径为: "+startGamePath)
            else:
                startGamePath = os.path.join(_gamePath, "Rainbowsix.exe")
                if os.path.exists(startGamePath):
                    startGame = input("\n启动游戏的 exe 文件已准备好，是否启动游戏？(y/n)：")
                    startGame = startGame.lower()
                    if startGame == "y":
                        RunGame(startGamePath, _gamePath)
                    print("\n即将返回主菜单！如自动启动卡BettleEye安装，请尝试手动启动游戏。")
                    print("游戏启动路径为: "+startGamePath)
                else:
                    print("\n没有找到启动游戏的 RainbowSix.exe 文件！请验证游戏文件完整性！")
        else:
            if os.path.exists(startGamePath):
                startGame = input("\n启动游戏的 bat 文件已准备好，是否启动游戏？(y/n)：")
                startGame = startGame.lower()
                if startGame == "y":
                    RunGame(startGamePath, _gamePath)
                print("\n即将返回主菜单！如自动启动卡BettleEye安装，请尝试手动启动游戏。")
                print("游戏启动路径为: "+startGamePath)
            else:
                print("\n没有找到启动游戏的 RainbowSix.bat 文件！请重新下载以验证游戏完整性！")
    except Exception as e:
        print("\n先检查安装路径是否有空格，删除空格后开启Steam社区加速器重试！")
        print(e)

def Main():
    gongNeng = input("\n请输入功能编号：")
    if gongNeng == "1":
        _version = DownloadPre()
        print("\n提示：如需验证完整性请选择 "+_version+" 所在的文件夹上一层，即可验证补全 "+_version+"赛季 缺失的文件！")
        _path = ChoosePath(_version)
        _gamePath = os.path.join(_path, _version)
        if _gamePath.count(_version) > 1:
            print("\n你选择的文件夹为："+_gamePath)
            print("此路径下已有 "+str(_gamePath.count(_version)-1)+" 个 "+_version+" 文件夹，请重新选择首个 "+_version+" 文件夹的上一层来验证完整性！")
        else:
            _first = IsFirstDownload(_path, _version, _gamePath)
            if not os.path.exists("lib\\net9.txt"):#判断是否第一次运行
                os.system("lib\\dotnet-runtime-9.0.3-win-x64.exe -q")
                print("dotnet-9.0运行库安装成功！")
                # 将文件名和路径作为参数传递给open()函数
                file = open("lib\\net9.txt", "w")
                file.write("dotnet-9.0 has installed.")
                file.close()
                #运行后需要创建一个net9.txt文件
            mFile_1 = "lib\\depotcache\\377237_"+manifestList[_version][7]+".manifest"
            mFile_2 = "lib\\depotcache\\359551_"+manifestList[_version][8]+".manifest"
            if not os.path.exists(mFile_1):
                print("\n该版本需登录购买了《彩虹六号-围攻》的Steam账号才能下载或验证！")
                steamUser = input("\n请输入你的Steam账号：")
                print("\n 如第一次使用请按提示输入你的Steam密码：")
                if _first:
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest "+manifestList[_version][7]+" -username "+steamUser+" -remember-password -dir "+_gamePath)
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest "+manifestList[_version][8]+" -username "+steamUser+" -remember-password -dir "+_gamePath)
                else:
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest "+manifestList[_version][7]+" -username "+steamUser+" -remember-password -validate -dir "+_gamePath)
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest "+manifestList[_version][8]+" -username "+steamUser+" -remember-password -validate -dir "+_gamePath)
                    print("游戏文件完整性验证完毕！")
            else:
                if _first:
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest "+manifestList[_version][7]+" -depotkeys lib\\steam.keys -manifestfile "+mFile_1+" -dir "+_gamePath)
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest "+manifestList[_version][8]+" -depotkeys lib\\steam.keys -manifestfile "+mFile_2+" -dir "+_gamePath)
                else:
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest "+manifestList[_version][7]+" -depotkeys lib\\steam.keys -manifestfile "+mFile_1+" -validate -dir "+_gamePath)
                    os.system("lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest "+manifestList[_version][8]+" -depotkeys lib\\steam.keys -manifestfile "+mFile_2+" -validate -dir "+_gamePath)
                    print("游戏文件完整性验证完毕！")
            
            DownloadPatch(_version, _gamePath)
    elif gongNeng == "2":
        print("\n此模式仅支持中国大陆以外地区用户使用！\n国内想用请挂梯子或者UU路由模式！\n用302加速不行！")
        _version = DownloadPre()
        _path = ChoosePath(_version)
        _gamePath = os.path.join(_path, _version)
        #_txt = "\n下载前请用UU加速Steam商店，节点选路由模式！"
        if _gamePath.count(_version) > 1:
            print("\n你选择的文件夹为："+_gamePath)
            print("此路径下已有 "+str(_gamePath.count(_version)-1)+" 个 "+_version+" 文件夹，请重新选择首个 "+_version+" 文件夹的上一层！")
        else:
            _first = IsFirstDownload(_path, _version, _gamePath)
            
            keyFile = "depot_keys.json"#复制key到LOCAL APPDATA
            path_ProgrmData = os.getenv("LOCALAPPDATA")
            steamctlPath = path_ProgrmData+"\\steamctl\\steamctl\\"
            if not os.path.exists(steamctlPath):
                os.makedirs(steamctlPath)
            shutil.copy(os.path.join("lib\\manifestFiles\\", keyFile), os.path.join(steamctlPath, keyFile))
            time.sleep(1)
            
            pythonPath = "lib\\python-3.12.3-embed-amd64\\python.exe"
            os.system(pythonPath+" -m steamctl depot download -f lib\\manifestFiles\\"+manifestList[_version][0]+" -o "+_gamePath+" --skip-licenses --skip-login --cell_id 4")
            time.sleep(1)
            os.system(pythonPath+" -m steamctl depot download -f lib\\manifestFiles\\"+manifestList[_version][1]+" -o "+_gamePath+" --skip-licenses --skip-login --cell_id 4")#1 2 5
            #pythonPath = "lib\\python-3.12.3-embed-amd64\\python.exe"
            #os.system(pythonPath+" lib\\depotdownloader.py -c -o "+_gamePath+" depot -m lib\\manifestFiles\\"+manifestList[_version][0]+" -k 55e7ea1db9a23f549c35553adb88ac3f97c1fc5f649df1515f5fa1dde7f501a6")
            #time.sleep(1)
            #os.system(pythonPath+" lib\\depotdownloader.py -c -o "+_gamePath+" depot -m lib\\manifestFiles\\"+manifestList[_version][1]+" -k b13d0908374e12054e73230c57da5d674dfe45cffe6ba7e11b3f1a8b155938d0")
            
            DownloadPatch(_version, _gamePath)
    elif gongNeng == "3":
        y5 = input("\n你玩的版本是否是Y5？(y/n)：")
        y5 = y5.lower()
        if y5 == "y":
            subprocess.run(['start', "lib\\Y5_xiu_gai_qi.exe"], shell=True)
        else:
            subprocess.run(['start', "lib\\R6_Liberator_0.0.0.22.exe"], shell=True)
    elif gongNeng == "4":
        installVpn = input("\n是否安装虚拟局域网软件OpenVPN用于联机？(y/n)：")
        installVpn = installVpn.lower()
        if installVpn == "y":
            subprocess.run(['start', "lib\\openvpn-install-2.4.8-I602-Win10.exe"], shell=True)
            print("安装中... ... \n安装完毕后到QQ群：439523286 中下载联机节点文件ChengDu-50120.ovpn导入既可连接群内联机服务器！")
    elif gongNeng == "5":
        y5y8 = input("\n你联机的版本是否是Y5-Y8？(y/n)：")
        y5y8 = y5y8.lower()
        hostIP = input("\n请输入房主的虚拟局域网IP：")
        if y5y8 == "y":
            os.system("lib\\NetworkedR6.exe "+hostIP+" -p 6200")
        else:
            os.system("lib\\NetworkedR6.exe "+hostIP)
    elif gongNeng == "6":
        os.system("route print -4")
    else:
        print('\n                ----请输入提示的功能编号！！！')