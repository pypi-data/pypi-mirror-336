import os
import json
import xml.etree.ElementTree as ET
import random
import datetime
import time
from tkinter import Tk, Toplevel, ttk, Button, Label, Entry, filedialog, messagebox, LEFT, END, GROOVE
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog  # 导入 simpledialog
import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import xml.etree.ElementTree as ET
import os
import tempfile

# 全局变量
global version_now
global usergroup
global setting_cfg
global csdir
import webbrowser

version_now = "3.2.5"
usergroup = "用户组=0"
setting_cfg = {}

# 获取当前脚本所在目录
csdir = os.path.dirname(os.path.abspath(__file__))

def run_apps():
    print('done.')

def run_encrypted_client_app():
    global aaaa
    # Default values for failed login
    aaaa = {'group': '用户未登录', 'username': '用户未登录'}
    
    # AES 加密密钥（必须是 16, 24 或 32 字节）
    AES_KEY = b'your_aes_key_32bytes_1234567890abcdef'[:32]  # 确保密钥长度为 32 字节

    # AES 加密函数
    def aes_encrypt(data):
        cipher = AES.new(AES_KEY, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    # AES 解密函数
    def aes_decrypt(iv, ct):
        try:
            iv = base64.b64decode(iv)
            ct = base64.b64decode(ct)
            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except:
            return None

    # 获取CSRF令牌的函数
    def get_csrf_token():
        try:
            response = requests.get("http://159.75.253.250:5000/", timeout=5)
            return response.cookies.get('csrf_token')
        except Exception as e:
            print("获取CSRF令牌失败:", str(e))
            return ""

    # 调用 API 接口的函数
    def call_api(username_iv, username_ct, password_iv, password_ct):
        url = "http://159.75.253.250:5000/api/get_user_group"
        payload = {
            "username_iv": username_iv,
            "username_ct": username_ct,
            "password_iv": password_iv,
            "password_ct": password_ct
        }
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": get_csrf_token()  # 添加CSRF令牌
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                global aaaa
                aaaa = response.json()
                print("登录成功。")
                return True
            else:
                print("登录失败，可能用户未注册。")
                return False
        except Exception as e:
            print("API 调用异常:", str(e))
            return False

    # 将加密的用户名和密码写入 user.xml
    def save_to_xml(username_iv, username_ct, password_iv, password_ct, success=False):
        root = ET.Element("user")
        ET.SubElement(root, "username_iv").text = username_iv
        ET.SubElement(root, "username_ct").text = username_ct
        ET.SubElement(root, "password_iv").text = password_iv
        ET.SubElement(root, "password_ct").text = password_ct
        ET.SubElement(root, "success").text = str(success).lower()
        tree = ET.ElementTree(root)
        tree.write(os.path.join(os.path.dirname(__file__), 'user.xml'), encoding="utf-8", xml_declaration=True)

    # 从 XML 文件中读取加密的用户名和密码
    def read_from_xml():
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'user.xml')):
            return None, None, None, None, None

        try:
            tree = ET.parse(os.path.join(os.path.dirname(__file__), 'user.xml'))
            root = tree.getroot()
            username_iv = root.find("username_iv").text
            username_ct = root.find("username_ct").text
            password_iv = root.find("password_iv").text
            password_ct = root.find("password_ct").text
            success = root.find("success")
            success = success.text.lower() == 'true' if success is not None else False
            return username_iv, username_ct, password_iv, password_ct, success
        except:
            return None, None, None, None, None

    # 注册函数
    def open_register_page():
        webbrowser.open("http://159.75.253.250:5000/register")

    # 创建登录窗口
    def create_login_window():
        root = tk.Tk()
        root.title("用户登录")
        root.configure(bg='steelblue')

        # 设置窗口样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='steelblue')
        style.configure('TLabel', background='steelblue', foreground='white', font=('微软雅黑', 10))
        style.configure('TButton', font=('微软雅黑', 10), padding=5)
        style.map('TButton', 
                 background=[('active', 'dodgerblue'), ('!active', 'lightsteelblue')],
                 foreground=[('active', 'white'), ('!active', 'black')])

        # 窗口居中显示
        window_width = 450
        window_height = 350
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill='both')
        main_frame.grid_columnconfigure(0, weight=1)

        # 标题
        title_label = ttk.Label(main_frame, text="用户登录", font=('微软雅黑', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky='n')

        # 输入框框架
        entry_frame = ttk.Frame(main_frame)
        entry_frame.grid(row=1, column=0, pady=10, sticky='ew')
        entry_frame.grid_columnconfigure(1, weight=1)

        # 用户名输入框
        label_username = ttk.Label(entry_frame, text="用户名:")
        label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_username = ttk.Entry(entry_frame, width=25)
        entry_username.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # 密码输入框
        label_password = ttk.Label(entry_frame, text="密码:")
        label_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_password = ttk.Entry(entry_frame, show="*", width=25)
        entry_password.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # 读取 XML 文件中的加密数据并填充到输入框
        username_iv, username_ct, password_iv, password_ct, _ = read_from_xml()
        if username_iv and username_ct:
            decrypted_username = aes_decrypt(username_iv, username_ct)
            if decrypted_username:
                entry_username.insert(0, decrypted_username)

        if password_iv and password_ct:
            decrypted_password = aes_decrypt(password_iv, password_ct)
            if decrypted_password:
                entry_password.insert(0, decrypted_password)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10, sticky='ew')

        # 提交按钮
        def on_submit():
            username = entry_username.get()
            password = entry_password.get()

            if not username or not password:
                messagebox.showerror("错误", "用户名和密码不能为空")
                return

            # 加密用户名和密码
            username_iv, username_ct = aes_encrypt(username)
            password_iv, password_ct = aes_encrypt(password)

            # 调用 API
            if call_api(username_iv, username_ct, password_iv, password_ct):
                # 只有登录成功才保存到XML
                save_to_xml(username_iv, username_ct, password_iv, password_ct, True)
            # 无论成功失败都继续执行
            root.destroy()
            load_ui(aaaa)

        button_submit = ttk.Button(button_frame, text="登录", command=on_submit)
        button_submit.pack(side='left', expand=True, fill='x', padx=5)

        # 注册按钮
        button_register = ttk.Button(button_frame, text="注册", command=open_register_page)
        button_register.pack(side='left', expand=True, fill='x', padx=5)

        # 添加登录说明标签
        login_info_label = ttk.Label(
            main_frame, 
            text="您需要使用账号登录，以进行用户登记和自动获取对应的更新。\n如无账号请点击注册，之后使用注册的账号和密码登录。",
            wraplength=400,
            justify='center'
        )
        login_info_label.grid(row=3, column=0, pady=(20, 0), sticky='nsew')

        root.mainloop()

    # 主逻辑
    username_iv, username_ct, password_iv, password_ct, success = read_from_xml()
    
    if all([username_iv, username_ct, password_iv, password_ct]):
        # 尝试自动登录
        login_success = call_api(username_iv, username_ct, password_iv, password_ct)
        if login_success:
            # 自动登录成功，更新success字段为True
            save_to_xml(username_iv, username_ct, password_iv, password_ct, True)
        elif success:
            # 自动登录失败但上次成功，使用缓存状态继续
            print("网络不畅，使用上次成功登录状态继续")
            aaaa = {'group': '网络不畅无法获取', 'username': '网络不畅无法获取'}
        
        # 无论自动登录成功与否都继续执行
        load_ui(aaaa)
    else:
        # 没有保存的登录信息，显示登录窗口
        create_login_window()
        
def update_database(filename):
    import zipfile
    import shutil
    import requests
    import tempfile
    import os
    from tkinter import messagebox
    import xml.etree.ElementTree as ET
    import random
    from datetime import datetime
    
    # 获取工作目录从setting.xml
    def get_work_dir():
        try:
            setting_file = os.path.join(os.path.dirname(__file__), 'setting.xml')
            if os.path.exists(setting_file):
                tree = ET.parse(setting_file)
                root = tree.getroot()
                work_dir = root.find('work_dir').text
                return work_dir
            return os.path.dirname(__file__)  # 默认返回程序目录
        except Exception as e:
            print(f"读取setting.xml失败: {str(e)}")
            return os.path.dirname(__file__)
    
    # 创建备份函数
    def create_backup(work_dir):
        try:
            # 创建backup目录
            backup_dir = os.path.join(work_dir, 'backup')
            os.makedirs(backup_dir, exist_ok=True)
            
            # 生成备份文件名: 日期+两位随机数
            now = datetime.now()
            random_num = random.randint(10, 99)
            backup_filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{random_num}.zip"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 创建ZIP文件
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(work_dir):
                    # 跳过backup目录
                    if 'backup' in dirs:
                        dirs.remove('backup')
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 跳过备份文件本身（如果存在）
                        if file_path == backup_path:
                            continue
                        # 计算相对路径
                        arcname = os.path.relpath(file_path, work_dir)
                        try:
                            zipf.write(file_path, arcname)
                        except Exception as e:
                            print(f"无法备份文件 {file_path}: {str(e)}")
                            continue
            
            return backup_path
        except Exception as e:
            print(f"创建备份失败: {str(e)}")
            return None

    # 获取本地版本号（从work_dir/version.txt读取）
    def get_local_version():
        work_dir = get_work_dir()
        version_file = os.path.join(work_dir, 'version.txt')
        try:
            if os.path.exists(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            return "0.0.0"  # 默认版本号
        except Exception as e:
            print(f"读取版本文件失败: {str(e)}")
            return "0.0.0"

    # 首先检查服务器版本
    version_url = "http://159.75.253.250:5000/api/download_file"
    version_payload = {
        "username_iv": 'NheVgRrBk8hl0qe0/bf6AA==',
        "username_ct": 't7TaVtUIUHWACMhphF3cZg==',
        "password_iv": 'wl0nvIIYwto+aC/lH8fUwg==',
        "password_ct": 'rTJ8uG9iMUYgtJotz83clQ==',
        "filename": "easypvver.txt",
    }
    
    try:
        # 获取本地版本
        local_version = get_local_version()
        
        # 获取服务器版本
        response = requests.post(version_url, json=version_payload)
        if response.status_code != 200:
            messagebox.showerror("错误", f"无法获取服务器版本: {response.text}")
            return
            
        server_version = response.text.strip()
        if not server_version:
            messagebox.showerror("错误", "服务器版本号无效")
            return
            
        # 比较版本
        from packaging import version
        if version.parse(server_version) <= version.parse(local_version):
            print( f"当前资源库版本 {local_version} 已经是最新版本，无需更新。")
            return
            
        # 如果服务器版本较新，则进行更新
        # 首先创建备份
        work_dir = get_work_dir()
        backup_path = create_backup(work_dir)
        if backup_path:
            print("检测到资源库有更新版本,正在更新资源库。\n正在创建原来的资源库备份...", f"已创建备份文件: {os.path.basename(backup_path)}")
        else:
            if messagebox.askyesno("备份失败", "检测到资源库有更新版本,正在更新资源库。但原来的资源库创建备份失败，是否继续更新？") == False:
                return
        
        url = "http://159.75.253.250:5000/api/download_file"
        payload = {
            "username_iv": 'NheVgRrBk8hl0qe0/bf6AA==',
            "username_ct": 't7TaVtUIUHWACMhphF3cZg==',
            "password_iv": 'wl0nvIIYwto+aC/lH8fUwg==',
            "password_ct": 'rTJ8uG9iMUYgtJotz83clQ==',
            "filename": filename,
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # 保存ZIP到临时文件
            with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_zip:
                temp_zip.write(response.content)
                zip_path = temp_zip.name
            
            # 创建目标目录（如果不存在）
            os.makedirs(work_dir, exist_ok=True)
            
            # 解压ZIP文件到工作目录（支持中文文件名）
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 先获取所有文件列表
                for file_info in zip_ref.infolist():
                    try:
                        # 正确解码文件名（支持中文）
                        original_filename = file_info.filename
                        try:
                            # 尝试UTF-8解码
                            file_info.filename = original_filename.encode('cp437').decode('gbk')
                        except:
                            try:
                                # 尝试其他编码方式
                                file_info.filename = original_filename.encode('cp437').decode('utf-8')
                            except:
                                # 如果还是失败，保持原样
                                file_info.filename = original_filename
                        
                        # 解压文件
                        zip_ref.extract(file_info, work_dir)
                        print(f"已解压文件: {file_info.filename} 到 {work_dir}")
                    except Exception as e:
                        messagebox.showwarning("警告", f"解压文件 {file_info.filename} 时出错: {str(e)}")
                        continue
            
            messagebox.showinfo("资源库更新成功", f"检测到资源库有更新版本。成功从版本 {local_version} 更新到 {server_version}！")
        else:
            messagebox.showerror("错误", f"文件下载失败: {response.text}")
    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出现异常: {str(e)}")
    finally:
        # 确保删除临时ZIP文件
        if 'zip_path' in locals() and os.path.exists(zip_path):
            os.unlink(zip_path)

def get_data_path(filename):
    """
    获取数据文件的绝对路径。
    """
    # 获取当前包的安装目录
    package_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建数据文件的路径
    data_path = os.path.join(package_dir, 'data', filename)
    
    # 检查文件是否存在
    #if not os.path.exists(data_path):
    #    raise FileNotFoundError(f"Data file '{filename}' not found at {data_path}")
    
    return data_path

# 示例：获取 sor.zip 的路径
try:
    def_path = get_data_path('def.zip')
    #print(f"sor.zip path: {sor_path}")
except FileNotFoundError as e:
    print(e)

def load_setting_cfg(file_path):
    """加载 setting.cfg 文件"""
    with open(file_path, 'r', encoding='gb18030') as file:
        content = file.read()
        setting_dict = eval(content)
        return setting_dict

def generate_setting_xml(setting_dict, output_path):
    """生成 setting.xml 文件"""
    settings = ET.Element("settings")
    python_command = ET.SubElement(settings, "python_command")
    python_command.text = "python"
    work_dir = ET.SubElement(settings, "work_dir")
    work_dir.text = setting_dict['settingdir']
    check_interval = ET.SubElement(settings, "check_interval")
    check_interval.text = "60000"
    tree = ET.ElementTree(settings)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
def extract_zip_file(zip_file_path, extract_path):
    import zipfile
    import sys
    
    if not extract_path:
        return 0
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            try:
                # 尝试UTF-8解码（Python 3.11+默认使用UTF-8）
                filename = file_info.filename.encode('cp437').decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # 尝试GBK解码（常见于中文Windows创建的zip文件）
                    filename = file_info.filename.encode('cp437').decode('gbk')
                except UnicodeDecodeError:
                    # 如果都失败，使用原始文件名
                    filename = file_info.filename
            
            # 确保路径分隔符是当前系统的正确格式
            filename = filename.replace('/', '\\') if '\\' in sys.path[0] else filename.replace('\\', '/')
            
            # 更新文件名并解压
            file_info.filename = filename
            zip_ref.extract(file_info, extract_path)
def check_and_generate_files():
    """检查并生成 setting.cfg 和 setting.xml 文件"""
    cfg_file_path = os.path.join(csdir, 'setting.cfg')
    xml_file_path = os.path.join(csdir, 'setting.xml')
    
    # 检查并生成 setting.cfg
    if not os.path.exists(cfg_file_path):
        default_setting_dir = os.path.join(os.path.expanduser('~'), 'easypv')
        if not os.path.exists(default_setting_dir):
            os.makedirs(default_setting_dir)
            extract_zip_file(def_path, default_setting_dir)
        setting_cfg_content = {'settingdir': default_setting_dir, 'sidori': random.randint(200000, 299999), 'sidfinal': '11111180000808'}
        with open(cfg_file_path, 'w', encoding='gb18030') as f:
            f.write(str(setting_cfg_content))
    
    # 检查并生成 setting.xml
    if not os.path.exists(xml_file_path):
        setting_dict = load_setting_cfg(cfg_file_path)
        generate_setting_xml(setting_dict, xml_file_path)

def read_setting_cfg():
    """读取 setting.cfg 文件"""
    global csdir
    cfg_file_path = os.path.join(csdir, 'setting.cfg')
    if os.path.exists(cfg_file_path):
        with open(cfg_file_path, 'r', encoding='gb18030') as f:
            setting_cfg = eval(f.read())
    else:
        setting_cfg = {'settingdir': 0, 'sidori': 0, 'sidfinal': '11111180000808'}
        with open(cfg_file_path, 'w', encoding='gb18030') as f:
            f.write(str(setting_cfg))
    return setting_cfg

def open_setting_cfg():
    """打开 setting.cfg 文件"""
    global csdir
    cfg_file_path = os.path.join(csdir, 'setting.cfg')
    with open(cfg_file_path, 'r', encoding='gb18030') as f:
        setting_cfg = eval(f.read())
    return setting_cfg

def update_setting_cfg(keys, values):
    """更新 setting.cfg 文件"""
    global csdir
    cfg_file_path = os.path.join(csdir, 'setting.cfg')
    with open(cfg_file_path, 'r', encoding='gb18030') as f:
        setting_cfg = eval(f.read())
    setting_cfg[keys] = values
    with open(cfg_file_path, 'w', encoding='gb18030') as f:
        f.write(str(setting_cfg))

def generate_random_file():
    """生成随机数并更新 setting.cfg"""
    global csdir
    random_number = random.randint(200000, 299999)
    update_setting_cfg("sidori", random_number)

def convert_and_compare_dates(date_str):
    """转换并比较日期"""
    current_date = datetime.datetime.now()
    try:
        date_obj = datetime.datetime.strptime(str(int(int(date_str) / 4)), "%Y%m%d")
    except:
        return "已过期"
    if date_obj > current_date:
        return "未过期"
    else:
        return "已过期"

def display_random_number():
    """显示随机数"""
    global csdir
    mroot = Toplevel()
    mroot.title("ID")
    sw = mroot.winfo_screenwidth()
    sh = mroot.winfo_screenheight()
    ww = 80
    wh = 70
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    mroot.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    with open(os.path.join(csdir, 'setting.cfg'), 'r', encoding='gb18030') as f:
        setting_cfg = eval(f.read())
    random_number = int(setting_cfg["sidori"])
    sid = random_number * 2 + 183576
    label = ttk.Label(mroot, text=f"机器码: {random_number}")
    entry = ttk.Entry(mroot)
    label.pack()
    entry.pack()
    ttk.Button(mroot, text="验证", command=lambda: check_input(entry.get(), sid)).pack()

def check_input(input_numbers, sid):
    """检查输入"""
    try:
        input_number = int(str(input_numbers)[0:6])
        day_end = convert_and_compare_dates(str(input_numbers)[6:14])
    except:
        messagebox.showinfo(title="提示", message="不匹配，注册失败。")
        return 0
    if input_number == sid and day_end == "未过期":
        update_setting_cfg("sidfinal", input_numbers)
        messagebox.showinfo(title="提示", message="注册成功,请重新启动程序。")
        quit()
    else:
        messagebox.showinfo(title="提示", message="不匹配，注册失败。")

def load_app(root,package_name):
    """加载应用程序"""
    global csdir
    package_names = os.path.join(csdir, package_name + ".py")
    return_pkg = os.path.join(csdir, 'easypv.py')
    root.destroy()
    os.system(f"python {package_names}")
    os.system(f"python {return_pkg}")


def load_ui(aaaa):
    root = Tk()
    root.title("药物警戒数据分析工作平台 EasyPV" + " " + version_now)
    sw_root = root.winfo_screenwidth()
    sh_root = root.winfo_screenheight()
    ww_root = 700
    wh_root = 620
    x_root = (sw_root - ww_root) / 2
    y_root = (sh_root - wh_root) / 2
    root.geometry("%dx%d+%d+%d" % (ww_root, wh_root, x_root, y_root))
    root.configure(bg="steelblue")

    try:
        frame0 = ttk.Frame(root, width=90, height=20)
        frame0.pack(side=LEFT)

        B_open_files1 = Button(
            frame0,
            text="基础统计分析\n（适用于药械妆全字段标准数据和固化统计）",
            bg="steelblue",
            fg="snow",
            height=2,
            width=30,
            font=("微软雅黑", 12),
            relief=GROOVE,
            activebackground="lightsteelblue",
            command=lambda: load_app(root,'adrmdr'),
        )
        B_open_files1.pack()

        B_open_files2 = Button(
            frame0,
            text="进阶统计分析\n（适用于所有表格数据和自定义分析）",
            bg="steelblue",
            fg="snow",
            height=2,
            width=30,
            font=("微软雅黑", 12),
            relief=GROOVE,
            activebackground="lightsteelblue",
            command=lambda: load_app(root,'easystat'),
        )
        B_open_files2.pack()

        B_open_files3 = Button(
            frame0,
            text="报告表质量评估\n（适用于药械全字段标准数据）",
            bg="steelblue",
            fg="snow",
            height=2,
            width=30,
            font=("微软雅黑", 12),
            relief=GROOVE,
            activebackground="lightsteelblue",
            command=lambda: load_app(root,'pinggutools'),
        )
        B_open_files3.pack()


        B_open_files5 = Button(
            frame0,
            text="工具箱\n（其他定制的小工具）",
            bg="steelblue",
            fg="snow",
            height=2,
            width=30,
            font=("微软雅黑", 12),
            relief=GROOVE,
            activebackground="lightsteelblue",
            command=lambda: load_app(root,'easypymanager'),
        )
        B_open_files5.pack()

        B_open_files6 = Button(
            frame0,
            text="资源库更新",
            bg="steelblue",
            fg="snow",
            height=2,
            width=30,
            font=("微软雅黑", 12),
            relief=GROOVE,
            activebackground="lightsteelblue",
            command=lambda: update_database('epv.zip'),
        )
        B_open_files6.pack()




        B_open_files6 = Button(
            frame0,
            text="意见反馈",
            bg="steelblue",
            fg="snow",
            height=2,
            width=30,
            font=("微软雅黑", 12),
            relief=GROOVE,
            activebackground="lightsteelblue",
            command=lambda: messagebox.showinfo(title="联系我们", message="如有任何问题或建议，请联系蔡老师，411703730（微信或QQ）。"),
        )
        B_open_files6.pack()

    except Exception as e:
        print(f"Error: {e}")

    text = ScrolledText(root, height=400, width=400, bg="#FFFFFF")
    text.pack(padx=5, pady=5)
    text.insert(
        END, "\n\n\n\n\n\n\n\n\n\n\n本工作站适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。\n\n"
    )
    text.insert(END, "\n\n")
    text.insert(END,'用户信息：'+str(aaaa['username'])+'\n用户分组：'+str(aaaa['group'])+'\n\n')

    setting_cfg = read_setting_cfg()
    generate_random_file()
    setting_cfg = open_setting_cfg()
    if setting_cfg["settingdir"] == 0:
        messagebox.showinfo(title="提示", message="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")
        filepathu = filedialog.askdirectory()
        filepathu = os.path.normpath(filepathu)
        path = get_directory_path(filepathu)
        update_setting_cfg("settingdir", path)
    setting_cfg = open_setting_cfg()
    random_number = int(setting_cfg["sidori"])
    input_number = int(str(setting_cfg["sidfinal"])[0:6])
    day_end = convert_and_compare_dates(str(setting_cfg["sidfinal"])[6:14])
    sid = random_number * 2 + 183576
    #if input_number == sid and day_end == "未过期":
    #    usergroup = "用户组=1"
    #    text.insert(END, usergroup + "   有效期至：")
    #    text.insert(END, datetime.datetime.strptime(str(int(int(str(setting_cfg["sidfinal"])[6:14]) / 4)), "%Y%m%d"))
    #else:
    #    text.insert(END, usergroup)
    text.insert(END, "\n配置文件路径：" + setting_cfg["settingdir"] + "\n")
    peizhidir = str(setting_cfg["settingdir"])
    peizhidir = os.path.join(peizhidir, 'fspsssdfpy')
    peizhidir = peizhidir.replace("fspsssdfpy", '')
    print('peizhidir:', peizhidir)
    try:
        update_database('epv.zip')
    except:
        print('资源库获取更新不成功。')
    root.mainloop()
    print("done.")
       
if __name__ == '__main__':
    # 检查并生成 setting.cfg 和 setting.xml 文件
    check_and_generate_files()
    run_encrypted_client_app()

