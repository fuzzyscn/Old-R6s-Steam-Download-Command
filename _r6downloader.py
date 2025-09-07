import os
import re
import time
import shutil
import psutil
import datetime
import threading
import webbrowser
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

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
    "Y5S4" : ["r6_y5s4_377237", "r6_y5s4_359551", 9, 1, "霓虹黎明行动 ", "Plazas\\Y5S4", "RainbowSix.bat", "3390446325154338855", "6947060999143280245", "支持全皮肤和地图编辑器 "],
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
    "Y8S4" : ["r6_y8s4_377237", "r6_y8s4_359551", 9, 1, "极度深寒行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "7646647065987620875", "4957295777170965935", "未测试 不推荐下载"],
    "Y9S1" : ["r6_y9s1_377237", "r6_y9s1_359551", 9, 1, "绝命征兆行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "1959067516419454682", "1140469899661941149", "未测试 不推荐下载"],
    "Y9S4" : ["r6_y9s4_377237", "r6_y9s4_359551", 9, 1, "碰撞行动 ", "Plazas\\Y8SX", "RainbowSix.bat", "7684058120163063592", "2666276619654974788", "未测试 不推荐下载"],
}

def get_real_time_net_speed(interval=1):
    old = psutil.net_io_counters()
    time.sleep(interval)
    new = psutil.net_io_counters()

    down_bytes = new.bytes_recv - old.bytes_recv
    up_bytes = new.bytes_sent - old.bytes_sent

    down_speed = down_bytes / interval / (1024 * 1024)  # MB/s
    up_speed = up_bytes / interval / (1024 * 1024)      # MB/s

    return round(down_speed, 2), round(up_speed, 2)
    
def update_net_speed():
    while True:
        down, up = get_real_time_net_speed()
        speed_label.config(text=f"下载：{down:.2f} MB/s | 上传：{up:.2f} MB/s")
        root.update_idletasks()

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
    log_message("支持免登录下载Y6S1之前的赛季及Y8S2赛季，可验证完整性。", "info")
    #log_message("如出现 Trying again (#1)，请开启 Steam 社区加速器后重试。💡", "info")

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
def update_progress_from_line(line, download):
    if "Connection to Steam failed" in line:
        log_message("连接Steam网络失败，请开启302加速器或UU加速器路由模式后重试。", "error")
    if any(keyword in line for keyword in ["Encountered", "Error", "timeout"]):
        log_message("⚠️ 检测到下载错误或网络异常，如下载完后不影响运行请忽略此消息。", "warn")
        log_message(line.strip(), "error")
    if "Validating" in line:
        file_match = re.search(r'Validating\s+(.+)', line)
        if file_match:
            file_path = file_match.group(1).strip()
            log_message(f"验证文件中：{file_path}", "info")

    match = re.search(r'(\d+(\.\d+)?)%', line)
    if match:
        if download:
            log_message(f"下载文件中：{line.strip()}", "info")
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

def AddPatchGUI(version, game_path):
    start_button.config(state="normal")
    select_dir_button.config(state="normal")
    try:
        nickname = simpledialog.askstring("个性化昵称", "请输入你的英文游戏昵称（建议不要中文或空格）：")
        if not nickname:
            log_message("⚠️ 未输入昵称，使用默认名称Player", "warn")
            nickname = "Player"

        nickname += "-" + version
        patch_path = os.path.join("lib", version_map[version][5])
        patch_files = os.listdir(patch_path)
        folder_count = 0
        file_count = 0

        for file in patch_files:
            src = os.path.join(patch_path, file)
            dst = os.path.join(game_path, file)

            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                folder_count += 1
            else:
                shutil.copy(src, dst)
                file_count += 1

                if file.endswith(".ini") and file != "steam_emu.ini":
                    with open(dst, 'r') as f:
                        content = f.read()
                    content = content.replace("CHANGEGAMENAME", nickname).replace("CHANGEUSERNAME", nickname)
                    with open(dst, 'w') as f:
                        f.write(content)

                if file.endswith("HeliosLoader.json"):
                    with open(dst, 'r') as f:
                        content = f.read()
                    content = content.replace("CHANGEUSERNAME", nickname)
                    with open(dst, 'w') as f:
                        f.write(content)

        # 完整性核验
        expected_file_count = version_map[version][2]
        expected_folder_count = version_map[version][3]
        if file_count != expected_file_count:
            log_message("❌ 补丁文件数量异常，请关闭杀毒软件并重新解压下载器", "error")
        elif folder_count != expected_folder_count:
            log_message("❌ 补丁文件夹数量异常，请关闭杀毒软件并重新解压下载器", "error")
        else:
            log_message(f"✅ 补丁安装成功：{file_count}个文件，{folder_count}个文件夹", "success")

        # 提示是否启动游戏
        exe_name = version_map[version][6]
        exe_path = os.path.join(game_path, exe_name)
        if not os.path.exists(exe_path):  # 如果主启动文件不存在，试试备用名
            exe_path = os.path.join(game_path, "rainbowsix.exe")
        if os.path.exists(exe_path):
            if messagebox.askyesno("启动游戏", "补丁已安装完毕，是否启动游戏？"):
                log_message("🎮 正在启动游戏...", "info")
                os.startfile(exe_path)
            else:
                log_message("🎮 用户选择稍后启动游戏", "info")
        else:
            log_message("❌ 未找到启动文件，请验证游戏完整性", "error")

    except Exception as e:
        log_message(f"❌ 补丁安装出错：{e}", "error")

def run_command_live(cmd, download):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        update_progress_from_line(line, download)
    process.wait()
    if process.returncode != 0:
        log_message("❌ 命令执行失败", "error")
    else:
        #log_message("✅ 命令执行完成", "success")
        progress_var.set(100)  # 任务完成后设置为100%

def run_download(dir, version):
    global start_time
    start_time = time.time()
    
    install_path = dir
    manifest1 = version_map[version][7]
    manifest2 = version_map[version][8]
    log_message(f"📁 游戏的安装路径: {install_path}")
    log_message(f"🚀 开始下载赛季版本: {version}")

    mFile_1 = f"lib\\depotcache\\377237_{manifest1}.manifest"
    mFile_2 = f"lib\\depotcache\\359551_{manifest2}.manifest"
    # 🔍 如果 manifest 文件不存在，提示 Steam 登录
    if not os.path.exists(mFile_1):
        log_message("⚠️ 该版本需要登录购买了《彩虹六号：围攻》的 Steam 账号才能下载或验证！\n请使用下载器1.8命令行版本下载或验证。", "error")
    else:
        start_button.config(text="下载中...")
        start_button.config(state="disabled")
        select_dir_button.config(state="disabled")
        cmd1 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest {manifest1} -depotkeys lib\\steam.keys -manifestfile {mFile_1} -dir "{install_path}"'
        cmd2 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest {manifest2} -depotkeys lib\\steam.keys -manifestfile {mFile_2} -dir "{install_path}"'

        log_message("开始下载第一部分游戏文件（1/2）...", "info")
        run_command_live(cmd1, True)

        log_message("开始下载第二部分游戏文件（2/2）...", "info")
        run_command_live(cmd2, True)

        log_message("🎉 下载任务全部完成！", "success")
        
        # 补丁由主线程调用
        root.after(100, lambda: AddPatchGUI(version, install_path))
        start_button.config(text="开始下载")

def run_verify(dir, version):
    global start_time
    start_time = time.time()

    install_path = dir
    manifest1 = version_map[version][7]
    manifest2 = version_map[version][8]
    log_message(f"📁 游戏的安装路径: {install_path}")
    log_message(f"🚀 开始验证完整性: {version}")

    mFile_1 = f"lib\\depotcache\\377237_{manifest1}.manifest"
    mFile_2 = f"lib\\depotcache\\359551_{manifest2}.manifest"
    # 🔍 如果 manifest 文件不存在，提示 Steam 登录
    if not os.path.exists(mFile_1):
        log_message("⚠️ 该版本需要登录购买了《彩虹六号：围攻》的 Steam 账号才能下载或验证！\n请使用下载器1.8命令行版本下载或验证。", "error")
    else:
        start_button.config(text="验证中...")
        start_button.config(state="disabled")
        select_dir_button.config(state="disabled")
        cmd1 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 377237 -manifest {manifest1} -depotkeys lib\\steam.keys -manifestfile {mFile_1} -validate -dir "{install_path}"'
        cmd2 = f'lib\\net9.0\\DepotDownloaderMod.exe -app 359550 -depot 359551 -manifest {manifest2} -depotkeys lib\\steam.keys -manifestfile {mFile_2} -validate -dir "{install_path}"'

        log_message("开始验证第一部分游戏文件（1/2）...", "info")
        run_command_live(cmd1, False)

        log_message("开始验证第二部分游戏文件（2/2）...", "info")
        run_command_live(cmd2, False)

        log_message("🎉 验证完整性全部完成！", "success")
        
        # 补丁由主线程调用
        root.after(100, lambda: AddPatchGUI(version, install_path))

        start_button.config(text="验证完整性")

def download_game(folder, version):
    threading.Thread(target=run_download, args=(folder, version), daemon=True).start()
    threading.Thread(target=update_net_speed, daemon=True).start()

def verify_files(folder, version):
    threading.Thread(target=run_verify, args=(folder, version), daemon=True).start()
    threading.Thread(target=update_net_speed, daemon=True).start()

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

def ping_host_async(host_ip):
    def worker():
        try:
            result = subprocess.run(
                f"ping {host_ip} -n 8",
                shell=True,
                text=True,
                capture_output=True,
                encoding="gbk",
                errors="ignore"
            )
            output = result.stdout
            for line in output.splitlines():
                if line.strip():
                    log_message(line.strip(), "info")

            if "TTL=" in output or "TTL=" in output.upper():
                log_message("✅ 连通性测试成功，房主可达！", "success")
            else:
                log_message("⚠️ 房主不可达，请确认 VPN 是否连接正确", "warn")

        except Exception as e:
            log_message(f"❌ ping 出错：{e}", "error")

    threading.Thread(target=worker, daemon=True).start()

def is_valid_ip(ip):
    pattern = r"^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\." \
              r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\." \
              r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\." \
              r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
    return re.match(pattern, ip) is not None

def ask_ping_ip():
    top = tk.Toplevel(root)
    top.title("测试到房主延迟")
    top.geometry("300x140")
    top.resizable(False, False)

    ttk.Label(top, text="请输入房主虚拟局域网 IP：").pack(pady=(10, 5))
    ip_entry = ttk.Entry(top, width=22)
    ip_entry.pack()

    def run_test():
        ip = ip_entry.get().strip()
        if not is_valid_ip(ip):
            messagebox.showerror("格式错误", "请输入合法 IPv4 地址，例如：192.168.200.2")
            return
        log_message(f"📡 正在 ping 房主 IP {ip}，请稍候...", "info")
        ping_host_async(ip)
        top.destroy()

    ttk.Button(top, text="开始测试", command=run_test).pack(pady=10)

def run_forwarding():
    top = tk.Toplevel(root)
    top.title("启动联机转发")
    top.geometry("320x200")
    top.resizable(False, False)

    ttk.Label(top, text="请选择联机版本：").pack(pady=(10, 5))

    version_var = tk.StringVar(value="y5y8")
    ttk.Radiobutton(top, text="Y1-Y4 版本", variable=version_var, value="y1y4").pack()
    ttk.Radiobutton(top, text="Y5-Y8 版本", variable=version_var, value="y5y8").pack()

    ttk.Label(top, text="请输入房主虚拟局域网 IP：").pack(pady=(10, 5))
    ip_entry = ttk.Entry(top, width=24)
    ip_entry.pack()

    def launch_forwarding():
        host_ip = ip_entry.get().strip()

        if not is_valid_ip(host_ip):
            log_message("❌ IP 格式不合法，请输入类似 192.168.200.2 的地址", "error")
            messagebox.showerror("格式错误", "请输入合法的 IPv4 地址，例如：192.168.200.2")
            return

        selected = version_var.get()
        cmd = f'lib\\NetworkedR6.exe {host_ip}{" -p 6200" if selected == "y5y8" else ""}'
        log_message(f"🚀 正在执行联机转发命令：{cmd}", "info")

        def run_cmd_in_thread():
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="gbk", errors="ignore")
                for line in process.stdout:
                    if line.strip():
                        log_message(line.strip(), "info")
            except Exception as e:
                log_message(f"❌ 联机转发失败：{e}", "error")

        threading.Thread(target=run_cmd_in_thread, daemon=True).start()
        top.destroy()

    ttk.Button(top, text="启动", command=launch_forwarding).pack(pady=12)

def show_route_to_log():
    try:
        # 使用 gbk 编码（或 mbcs）读取结果，避免中文乱码
        result = subprocess.check_output("route print -4", shell=True, encoding="gbk", errors="ignore")
        log_message("📡 当前 IPv4 路由信息如下：", "info")
        for line in result.splitlines():
            if line.strip():
                log_message(line.strip(), "info")
    except Exception as e:
        log_message(f"❌ 获取路由信息失败：{e}", "error")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("彩虹六号旧版本下载器 By Fuzzys QQ群：439523286")
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    # 创建菜单栏
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    online_menu = tk.Menu(menu_bar, tearoff=0)
    online_menu.add_command(label="安装联机VPN", command=lambda: subprocess.Popen("lib\\openvpn-install-2.4.8-I602-Win10.exe", shell=True))
    online_menu.add_command(label="查看搜房记录", command=lambda: webbrowser.open_new("https://skin.ppkok.com/r6"))
    online_menu.add_command(label="启动联机转发", command=run_forwarding)
    online_menu.add_command(label="测试到房主延迟", command=ask_ping_ip)
    online_menu.add_command(label="查看当前路由", command=show_route_to_log)
    vpn_tishi = "安装完毕后到QQ群：439523286 中\n下载联机节点文件50120.ovpn\n导入后既可同群友联机！"
    online_menu.add_command(label="VPN使用提示", command=lambda: [messagebox.showinfo("提示", vpn_tishi),log_message(vpn_tishi)])
    menu_bar.add_cascade(label="联机工具", menu=online_menu)
    
    modifier_menu = tk.Menu(menu_bar, tearoff=0)
    modifier_menu.add_command(label="启动Y1-Y4修改器", command=lambda: subprocess.Popen("lib\\R6_Liberator_0.0.0.22.exe", shell=True))
    modifier_menu.add_command(label="启动Y5修改器", command=lambda: subprocess.Popen("lib\\Y5_xiu_gai_qi.exe", shell=True))
    xiugaiqi_tishi = "建好房间后房主展开地图模式双击最终选项即可\nY5修改器同理，选好后需要点击Send to Siege"
    modifier_menu.add_command(label="使用提示", command=lambda: [messagebox.showinfo("提示", xiugaiqi_tishi),log_message(xiugaiqi_tishi)])
    menu_bar.add_cascade(label="修改器", menu=modifier_menu)

    about_menu = tk.Menu(menu_bar, tearoff=0)
    about_menu.add_command(label="作者：Fuzzys_cn", command=lambda: [messagebox.showinfo("作者主页", "B站ID：Fuzzys_cn\nQQ群：439523286"),webbrowser.open_new("https://space.bilibili.com/22525010")])
    about_menu.add_command(label="访问官网", command=lambda: webbrowser.open_new("https://r6.002.hk/index"))
    about_menu.add_command(label="访问R6聊天室", command=lambda: webbrowser.open_new("https://chat.002.hk/R6Tools-chat/"))
    about_menu.add_separator()
    about_menu.add_command(label="捐助开发", command=lambda: os.startfile("lib\\zanzhu.png"))
    about_menu.add_command(label="程序版本：v2.01", command=lambda: messagebox.showinfo("版本信息", "当前版本：v2.01 \n获取最新信息请加入QQ群：439523286"))
    menu_bar.add_cascade(label="关于", menu=about_menu)

    ttk.Label(root, text="请选择安装文件夹：").grid(row=1, column=0)
    entry0 = ttk.Entry(root, width=37)
    entry0.grid(row=1, column=1)
    entry0.insert(0, "安装路径必须是纯英文且没有空格")

    select_dir_button = ttk.Button(root, text='选择', command=lambda: select_dir(entry0))
    select_dir_button.grid(row=1, column=2)
    select_dir_button.config(state="disabled")  # 初始禁用

    ttk.Label(root, text="请选择赛季版本：").grid(row=2, column=0)
    version_display_map = {k: f"{k} {v[4]+v[9]}" for k, v in version_map.items()}
    version_names = list(version_display_map.values())
    version_var = tk.StringVar()
    entry1 = ttk.Combobox(root, textvariable=version_var, values=version_names, state="readonly", width=35)
    entry1.grid(row=2, column=1)
    entry1.set(version_display_map["Y3S1"])  # 设置默认名称
    start_button = ttk.Button(root, text='开始下载')
    start_button.grid(row=2, column=2)
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

    progress_label = ttk.Label(root, text="进度：0% | 已用时间：--:-- ")
    progress_label.grid(row=5, columnspan=3)
    progress_var = tk.DoubleVar()
    progressbar = ttk.Progressbar(root, variable=progress_var, orient="horizontal", length=500, mode="determinate")
    progressbar.grid(row=6, columnspan=3, pady=(0, 10))
    speed_label = ttk.Label(root)
    speed_label.grid(row=7, columnspan=3)
    root.mainloop()