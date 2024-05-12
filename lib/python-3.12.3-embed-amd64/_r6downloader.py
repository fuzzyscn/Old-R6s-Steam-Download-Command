import os
import re
import time
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog

manifestList = {
    "Y1S0" : ["r6_y1s0_377237", "r6_y1s0_359551", "8358812283631269928 3893422760579204530",0, "初代 | 14.2 GB ", "Plazas\\PLAZA_BO", 7, 0, "RainbowSix.exe"],
    "Y1S1" : ["r6_y1s1_377237", "r6_y1s1_359551", "5188997148801516344 7932785808040895147",0, "墨冰行动 | 16.7 GB ", "Plazas\\PLAZA_BO", 7, 0, "RainbowSix.exe"],
    "Y1S2" : ["r6_y1s2_377237", "r6_y1s2_359551", "2303064029242396590 2206497318678061176",0, "尘土战线 | 20.9 GB ", "Plazas\\PLAZA_BO", 7, 0, "RainbowSix.exe"],
    "Y1S3" : ["r6_y1s3_377237", "r6_y1s3_359551", "5819137024728546741 5851804596427790505",1, "骷髅雨 | 25.1 GB ", "Plazas\\PLAZA_BO", 7, 0, "RainbowSix.exe"],
    "Y1S4" : ["r6_y1s4_377237", "r6_y1s4_359551", "3576607363557872807 8569920171217002292",0, "赤鸦行动 | 28.5 GB ", "Plazas\\PLAZA_BO", 7, 0, "RainbowSix.exe"],
    "Y2S1" : ["r6_y2s1_377237", "r6_y2s1_359551", "2248734317261478192 8006071763917433748",1, "丝绒壳行动 | 33.2 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y2S2" : ["r6_y2s2_377237", "r6_y2s2_359551", "5875987479498297665 708773000306432190",1, "健康行动 | 34 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y2S3" : ["r6_y2s3_377237", "r6_y2s3_359551", "6708129824495912434 1613631671988840841",0, "血兰花行动 | 34.3 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y2S4" : ["r6_y2s4_377237", "r6_y2s4_359551", "8748734086032257441 4221297486420648079",1, "白噪声行动 | 48.7 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y3S1" : ["r6_y3s1_377237", "r6_y3s1_359551", "5071357104726974256 4701787239566783972",0, "奇美拉行动 | 58.8 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y3S2" : ["r6_y3s2_377237", "r6_y3s2_359551", "6507886921175556869 8765715607275074515",1, "备战行动 | 63.3 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y3S3" : ["r6_y3s3_377237", "r6_y3s3_359551", "5562094852451837435 7781202564071310413",1, "暗空行动 | 72.6 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y3S4" : ["r6_y3s4_377237", "r6_y3s4_359551", "6502258854032233436 7659555540733025386",1, "风城行动 | 76.9 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y4S1" : ["r6_y4s1_377237", "r6_y4s1_359551", "8356277316976403078 5935578581006804383",1, "燃烧地平线 | 59.7 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y4S2" : ["r6_y4s2_377237", "r6_y4s2_359551", "693082837425613508 5408324128694463720",0, "幻镜行动 | 67.1 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y4S3" : ["r6_y4s3_377237", "r6_y4s3_359551", "3546781236735558235 7869081741739849703",1, "余烬重燃行动 | 69.6 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y4S4" : ["r6_y4s4_377237", "r6_y4s4_359551", "299124516841461614 1842268638395240106",0, "幻变潮汐行动（全皮肤）| 75.2 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y5S1" : ["r6_y5s1_377237", "r6_y5s1_359551", "4736360397583523381 6296533808765702678",1, "虚空边境行动 | 74.3 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y5S2" : ["r6_y5s2_377237", "r6_y5s2_359551", "4367817844736324940 893971391196952070",0, "钢流行动 | 81.3 GB ", "Plazas\\PLAZA_NEW", 7, 0, "RainbowSix.exe"],
    "Y5S3" : ["r6_y5s3_377237", "r6_y5s3_359551", "85893637567200342 3089981610366186823",0, "暗影传承行动 ", "Plazas\\CPlay", 12, 0, "RainbowSix.bat"],
    "Y5S4" : ["r6_y5s4_377237", "r6_y5s4_359551", "3390446325154338855 6947060999143280245",0, "霓虹黎明行动（支持联机猎恐）", "Plazas\\CPlay", 12, 0, "RainbowSix.bat"],
    "Y6S1" : ["r6_y6s1_377237", "r6_y6s1_359551", "7890853311380514304 7485515457663576274",1, "深红劫案行动 ", "Plazas\\CPlay", 12, 0, "RainbowSix.bat"],
    "Y6S2" : ["r6_y6s2_377237", "r6_y6s2_359551", "8733653062998518164 809542866761090243",1, "北极星行动 ", "Plazas\\CPlay", 12, 0, "RainbowSix.bat"],
    "Y6S3" : ["r6_y6s3_377237", "r6_y6s3_359551", "4859695099882698284 6526531850721822265",1, "晶坚守卫行动 ", "Plazas\\UPCR1", 11, 0, "RainbowSix.bat"],
    "Y6S4" : ["r6_y6s4_377237", "r6_y6s4_359551", "2637055726475611418 8627214406801860013",1, "精兵锐器行动 ", "Plazas\\UPCR2_NEW", 8, 0, "RainbowSix.bat"],
    "Y7S1" : ["r6_y7s1_377237", "r6_y7s1_359551", "8323869632165751287 2178080523228113690",1, "鬼面行动行动 ", "Plazas\\UPCR2_ORI", 8, 0, "RainbowSix.bat"],
    "Y7S2" : ["r6_y7s2_377237", "r6_y7s2_359551", "1363132201391540345 133280937611742404",1, "矢量光影行动 ", "Plazas\\UPCR2_ORI", 8, 0, "RainbowSix.bat"],
    "Y7S3" : ["r6_y7s3_377237", "r6_y7s3_359551", "6425223567680952075 5906302942203575464",1, "残蜂汹涌行动 ", "Plazas\\UPCR2_ORI", 8, 0, "RainbowSix.bat"],
    "Y7S4" : ["r6_y7s4_377237", "r6_y7s4_359551", "4466027729495813039 1819898955518120444",1, "烈日突袭行动 ", "Plazas\\UPCR2_ORI", 8, 1, "RainbowSix.bat"],
    "Y8S1" : ["r6_y8s1_377237", "r6_y8s1_359551", "3275824905781062648 5863062164463920572",1, "头号指令行动 ", "Plazas\\Y8SX", 9, 1, "RainbowSix.bat"],
    "Y8S2" : ["r6_y8s2_377237", "r6_y8s2_359551", "3050554908913191669 1575870740329742681",0, "恐惧因素行动（全干员孤狼猎恐）", "Plazas\\Y8SX", 9, 1, "RainbowSix.bat"],
    "Y8S3" : ["r6_y8s3_377237", "r6_y8s3_359551", "7845616952346988253 7492642056657673136",1, "开路先锋行动 ", "Plazas\\Y8SX", 9, 1, "RainbowSix.bat"],
}

def Help():
    print(
                '''
                ----功能 1《彩虹六号-围攻》下载器 2.0     (无需加速器，国内下载速度快，部分版本需登录Steam)
                ----功能 2《彩虹六号-围攻》下载器 1.0     (需开启UU加速器路由模式，国内下载速度中等，无需登录Steam)
                ----功能 3 打开地图模式皮肤修改器         (全皮肤最高支持到Y4S4)
                ----功能 4 安装联机工具 OpenVPN           (搜房记录查询 http://101.35.246.92/kod/r6/ )
                ----功能 5 代理转发房主IP                 (搜不到房间时使用)
                ----功能 6 显示当前网卡路由表             (搜不到房间时查看网卡优先级排错，看不懂请截图发群里)
                
                ----Made By Fuzzys QQ群：439523286
                '''
    )

def DownloadPre():
    versionList = []
    num = 0
    for id in manifestList:
        num += 1
        print("下载验证 "+id+" 请输入序号 "+str(num))
        versionList.append(id)
    id = input("\n请输入要下载或验证的《彩虹六号-围攻》赛季序号（不输默认为Y1S2）：") or 3
    return versionList[int(id)-1]

def ChoosePath():
    input("\n请回车选择保存游戏的文件夹，必须是英文路径！")
    root = tk.Tk()
    root.withdraw() #隐藏主窗口
    return filedialog.askdirectory()

def DownloadConfirm(_path, _version, _gamePath, txt):
    if _path:
        print("\n游戏文件将下载到你选择的文件夹："+_gamePath+txt)
        if os.path.exists(_gamePath):
            print("\n你选择的文件夹已安装赛季 "+_version+" "+manifestList[_version][4]+" 开始验证游戏文件完整性！")
        else:
            input("\n回车开始下载彩虹六号 "+_version+" "+manifestList[_version][4]+" 启动文件为：" + manifestList[_version][8])
    else:
        print("\n游戏文件将下载到当前文件夹！"+_gamePath)
        if os.path.exists(_gamePath):
            print("\n当前文件夹已安装赛季 "+_version+" "+manifestList[_version][4]+" 开始验证游戏文件完整性！")
        else:
            input("\n回车开始下载彩虹六号 "+_version+" "+manifestList[_version][4]+" 启动文件为：" + manifestList[_version][8])

def RunGame(filePath, cwdPath):
    try:
        subprocess.run(['start', filePath], shell=True, cwd=cwdPath)
    except Exception as e:
        print(e)
        
def DownloadPatch(_version, _gamePath):
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
                        
    if patchFolderCount != manifestList[_version][7]:
        print("\n破解补丁文件夹数量不一致！请关闭杀毒软件，或添加白名单")
    elif patchFileCount != manifestList[_version][6]:
        print("\n破解补丁文件数量不一致！请关闭杀毒软件，或添加白名单")
    elif patchFileCount > 0:
        print("\n破解补丁已安装成功！补丁文件数量："+str(patchFileCount)+" 文件夹数量："+str(patchFolderCount))
        
    startGamePath = os.path.join(_gamePath, manifestList[_version][8])
    if manifestList[_version][8] == "RainbowSix.exe":
        if os.path.exists(startGamePath):
            print("\n游戏启动路径为: "+startGamePath)
            startGame = input("\n启动游戏的 exe 文件已准备好，是否启动游戏？(y/n)：")
            startGame = startGame.lower()
            if startGame == "y":
                RunGame(startGamePath, _gamePath)
            else:
                print("\n下载已成功！即将返回主菜单！请手动启动游戏。\n")
        else:
            startGamePath = os.path.join(_gamePath, "RainbowsixGame.exe")
            if os.path.exists(startGamePath):
                print("\n游戏启动路径为: "+startGamePath)
                startGame = input("\n启动游戏的 exe 文件已准备好，是否启动游戏？(y/n)：")
                startGame = startGame.lower()
                if startGame == "y":
                    RunGame(startGamePath, _gamePath)
                else:
                    print("\n下载已成功！即将返回主菜单！请手动启动游戏。\n")
            else:
                print("\n没有启动游戏的 exe 文件！请重新下载以验证游戏完整性！")
    else:
        if os.path.exists(startGamePath):
            print("\n游戏启动路径为: "+startGamePath)
            startGame = input("\n启动游戏的 bat 文件已准备好，是否启动游戏？(y/n)：")
            startGame = startGame.lower()
            if startGame == "y":
                RunGame(startGamePath, _gamePath)
            else:
                print("\n下载已成功！即将返回主菜单！请手动启动游戏。\n")
        else:
            print("\n没有启动游戏的 bat 文件！请重新下载以验证游戏完整性！")

def Main():
    gongNeng = input("\n请输入功能编号：")
    if gongNeng == "1":
        _version = DownloadPre()
        _path = ChoosePath()
        _gamePath = os.path.join(_path, _version)
        DownloadConfirm(_path, _version, _gamePath, "")
        
        if not os.path.exists("apps.txt"):#判断是否第一次运行
            os.system("lib\\dotnet-runtime-6.0.26-win-x64.exe -q")
        if manifestList[_version][3]:
            print("\n该版本没有游戏文件的本地清单，需登录购买了《彩虹六号-围攻》的Steam账号才能下载！")
            steamUser = input("\n请输入你的steam账号：")
            steamPass = input("\n请输入你的steam密码：")
            os.system("lib\\DepotDownloader.exe -app 359550 -depot 377237 359551 -manifest "+manifestList[_version][2]+" -dir "+_gamePath+" -user "+steamUser+" -pass "+steamPass)
        else:
            os.system("lib\\DepotDownloader.exe -app 359550 -depot 377237 359551 -manifest "+manifestList[_version][2]+" -dir "+_gamePath)
        
        DownloadPatch(_version, _gamePath)
    elif gongNeng == "2":
        UUjiaoCheng = input("是否已使用UU加速器 路由模式 加速Steam商店？(y/n)：")
        UUjiaoCheng = UUjiaoCheng.lower()
        if UUjiaoCheng != "y":
            os.system('lib\\UU.png')
            
        _version = DownloadPre()
        _path = ChoosePath()
        _gamePath = os.path.join(_path, _version)  
        _txt = "\n下载前请用UU加速Steam商店，节点选路由模式！"
        DownloadConfirm(_path, _version, _gamePath, _txt)
        
        keyFile = "depot_keys.json"#复制key到LOCAL APPDATA
        path_ProgrmData = os.getenv("LOCALAPPDATA")
        steamctlPath = path_ProgrmData+"\\steamctl\\steamctl\\"
        if not os.path.exists(steamctlPath):
            os.makedirs(steamctlPath)
        shutil.copy(os.path.join("lib\\manifestFiles\\", keyFile), os.path.join(steamctlPath, keyFile))
        time.sleep(1)
        
        pythonPath = "lib\\python-3.12.3-embed-amd64\\python.exe"
        try:
            os.system(pythonPath+" -m steamctl depot download -f lib\\manifestFiles\\"+manifestList[_version][0]+" -o "+_gamePath+" --skip-licenses --skip-login")
        except Exception as e:
            print(e)
        try:
            os.system(pythonPath+" -m steamctl depot download -f lib\\manifestFiles\\"+manifestList[_version][1]+" -o "+_gamePath+" --skip-licenses --skip-login")
        except Exception as e:
            print(e)
        
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
            print("安装中... ... \n安装完毕后到QQ群：439523286 中下载联机节点文件client50120.ovpn导入既可连接群内联机服务器！")
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
    Help()    
    Main()
    
if __name__ == "__main__":
    Help()
    Main()