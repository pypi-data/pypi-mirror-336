import os
import json
import xml.etree.ElementTree as ET
import random
import datetime
from tkinter import Tk, Toplevel, ttk, Button, Label, Entry, filedialog, messagebox, LEFT, END, GROOVE
from tkinter.scrolledtext import ScrolledText

# 全局变量
global version_now
global usergroup
global setting_cfg
global csdir

version_now = "3.2.1"
usergroup = "用户组=0"
setting_cfg = {}

# 获取当前脚本所在目录
csdir = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename):
    """
    获取数据文件的绝对路径。
    """
    # 获取当前包的安装目录
    package_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建数据文件的路径
    data_path = os.path.join(package_dir, 'data', filename)
    
    # 检查文件是否存在
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file '{filename}' not found at {data_path}")
    
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
    #import shutil
    import zipfile
    if extract_path=="":
        return 0
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():

            file_info.filename = file_info.filename.encode('cp437').decode('gbk')
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

def load_app(package_name):
    """加载应用程序"""
    global csdir
    package_names = os.path.join(csdir, package_name + ".py")
    return_pkg = os.path.join(csdir, 'easypv.py')
    root.destroy()
    os.system(f"python {package_names}")
    os.system(f"python {return_pkg}")

if __name__ == '__main__':
    # 检查并生成 setting.cfg 和 setting.xml 文件
    check_and_generate_files()

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
            command=lambda: load_app('adrmdr'),
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
            command=lambda: load_app('easystat'),
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
            command=lambda: load_app('pinggutools'),
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
            command=lambda: load_app('easypymanager'),
        )
        B_open_files5.pack()

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
    if input_number == sid and day_end == "未过期":
        usergroup = "用户组=1"
        text.insert(END, usergroup + "   有效期至：")
        text.insert(END, datetime.datetime.strptime(str(int(int(str(setting_cfg["sidfinal"])[6:14]) / 4)), "%Y%m%d"))
    else:
        text.insert(END, usergroup)
    text.insert(END, "\n配置文件路径：" + setting_cfg["settingdir"] + "\n")
    peizhidir = str(setting_cfg["settingdir"])
    peizhidir = os.path.join(peizhidir, 'fspsssdfpy')
    peizhidir = peizhidir.replace("fspsssdfpy", '')
    print('peizhidir:', peizhidir)

    root.mainloop()
    print("done.")
