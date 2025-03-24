#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周

# 第二部分：导入基本模块及初始化 ########################################################################
 
import tkinter as Tk
import os
import traceback
import ast
import re
import xlrd
import xlwt
import openpyxl
import pandas as pd
import numpy as np
import math
import scipy.stats as st
from tkinter import ttk,Menu,Frame,Canvas,StringVar,LEFT,RIGHT,TOP,BOTTOM,BOTH,Y,X,YES,NO,DISABLED,END,Button,LabelFrame,GROOVE, Toplevel,Label,Entry,Scrollbar,Text, filedialog, dialog, PhotoImage
import tkinter.font as tkFont
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import collections
from collections import Counter
import datetime
from datetime import datetime, timedelta
import xlsxwriter
import time
import threading
import warnings
from matplotlib.ticker import PercentFormatter
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import text as sqltext
import random
import requests
import webbrowser
# 定义一些全局变量

import shutil
import os
global version_now
global usergroup
global setting_cfg
global csdir
global peizhidir
version_now="0.0.1" 
usergroup="用户组=0"
setting_cfg=""
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")
if csdir=="":
    csdir =str (os .path .dirname (__file__ ))#
    csdir =csdir +csdir.split ("easypv")[0 ][-1 ]#
#print(csdir)

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
    def_path = get_data_path('def_fen.zip')
    #print(f"sor.zip path: {sor_path}")
except FileNotFoundError as e:
    print(e)



title_all="分样工具 V"+version_now
title_all2="分样工具 V"+version_now
# 第二部分：函数模块 ##################################################################

    
#序列号与用户组验证模块。
def EasyInf():
    inf={
    '软件名称':'分样工具',
    '版本号':'1.0.1',
    '功能介绍':'快速启动一些小工具。',
    'PID':'MDRdsfsGTLF006',
    '分组':'药物警戒',
    '依赖':'pandas,numpy,scipy,matplotlib,sqlalchemy'
        }
    return inf
def extract_zip_file(zip_file_path, extract_path):
    #import shutil
    import zipfile
    if extract_path=="":
        return 0
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():

            file_info.filename = file_info.filename.encode('cp437').decode('gbk')
            zip_ref.extract(file_info, extract_path)


def get_directory_path(directory_path):
    global csdir  # 假设 csdir 是之前定义好的包含 zip 文件的目录
    
    # 检查目录是否存在指定的文件
    file_path = os.path.join(directory_path, '（分样）任务分配.xls')
    if not os.path.isfile(file_path):
        # 创建一个 Tkinter 根窗口（隐藏主窗口）
        root = Toplevel()
        root.withdraw()  # 隐藏主窗口
        from tkinter import messagebox
        # 弹出确认框
        message = "程序将在该目录内生成相关配置文件。这个目录内的同名文件将会被取代，建议做好备份，请问是否继续？"
        user_response = messagebox.askyesno("确认解压", message)
        
        # 根据用户响应决定是否解压
        if user_response:
            # 假设 csdir + "def.zip" 是正确的 zip 文件路径
            #zip_file_path = os.path.join(csdir, "def_fen.py")  # 修改为正确的 zip 文件名
            extract_zip_file(def_path, directory_path)
        else:
            # 用户选择否，退出程序
            root.destroy()  # 销毁隐藏的 Tkinter 窗口
            quit()
    
    # 检查目录路径是否为空，如果为空则退出程序
    if directory_path == "":
        quit()
    
    # 返回目录路径
    return directory_path
    
    


def convert_and_compare_dates(date_str):
    import datetime
    current_date = datetime.datetime.now()

    try:
       date_obj = datetime.datetime.strptime(str(int(int(date_str)/4)), "%Y%m%d") 
    except:
        text.insert(END,"fail")
        return  "已过期"
  
    if date_obj > current_date:
        
        return "未过期"
    else:
        return "已过期"
    
def read_setting_cfg():
    global csdir
    # 读取 setting_fen.cfg 文件
    if os.path.exists(csdir+'setting_fen.cfg'):
        text.insert(END,"已完成初始化\n")
        with open(csdir+'setting_fen.cfg', 'r') as f:
            setting_cfg = eval(f.read())
    else:
        # 创建 setting_fen.cfg 文件，如果文件已存在则覆盖
        setting_cfg_path =csdir+ 'setting_fen.cfg'
        with open(setting_cfg_path, 'w') as f:
            f.write('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')
        text.insert(END,"未初始化，正在初始化...\n")
        setting_cfg = read_setting_cfg()
    return setting_cfg
    

def open_setting_cfg():
    global csdir
    # 打开 setting_fen.cfg 文件
    with open(csdir+"setting_fen.cfg", 'r') as f:
        # 将文件内容转换为字典
        setting_cfg = eval(f.read())
    return setting_cfg

def update_setting_cfg(keys,values):
    global csdir
    # 打开 setting_fen.cfg 文件
    with open(csdir+"setting_fen.cfg", 'r') as f:
        # 将文件内容转换为字典
        setting_cfg = eval(f.read())
    
    if setting_cfg[keys]==0 or setting_cfg[keys]=="11111180000808" :
        setting_cfg[keys]=values
        # 保存字典覆盖源文件
        with open(csdir+"setting_fen.cfg", "w") as f:
            f.write(str(setting_cfg))


def generate_random_file():
    # 生成一个六位数的随机数
    random_number = random.randint(200000, 299999)
    # 将随机数保存到文本文件中
    update_setting_cfg("sidori",random_number)

def display_random_number():
    global csdir
    mroot = Toplevel()
    mroot.title("ID")
    
    sw = mroot.winfo_screenwidth()
    sh = mroot.winfo_screenheight()
    # 得到屏幕高度
    ww = 80
    wh = 70
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    mroot.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    
    # 打开 setting_fen.cfg 文件
    with open(csdir+"setting_fen.cfg", "r") as f:
        # 将文件内容转换为字典
        setting_cfg = eval(f.read())
    random_number=int(setting_cfg["sidori"])
    sid=random_number*2+183576

    print(sid)
    # 创建标签和输入框
    label = ttk.Label(mroot, text=f"机器码: {random_number}")
    entry = ttk.Entry(mroot)

    # 将标签和输入框添加到窗口中
    label.pack()
    entry.pack()

    # 监听输入框的回车键事件
    #entry.bind("<Return>", check_input)
    ttk.Button(mroot, text="验证", command=lambda:check_input(entry.get(),sid)).pack()
    
def check_input(input_numbers,sid):

    # 将输入的数字转换为整数'

    try:
        input_number = int(str(input_numbers)[0:6])
        day_end=convert_and_compare_dates(str(input_numbers)[6:14])
    except:
        showinfo(title="提示", message="不匹配，注册失败。")
        return 0
    # 核对输入的数字是否等于随机数字
    if input_number == sid and day_end=="未过期":
        update_setting_cfg("sidfinal",input_numbers)
        showinfo(title="提示", message="注册成功,请重新启动程序。")
        quit()
    else:
        showinfo(title="提示", message="不匹配，注册失败。")

###############################


def update_software(package_name):
    # 检查当前安装的版本
    global version_now   
    text.insert(END,"当前版本为："+version_now+",正在检查更新...(您可以同时执行分析任务)") 
    try: 
        latest_version = requests.get(f"https://pypi.org/pypi/{package_name}/json",timeout=2).json()["info"]["version"]
    except:
        return "...更新失败。"
    if latest_version > version_now:
        text.insert(END,"\n最新版本为："+latest_version+",正在尝试自动更新....")        
        # 如果 PyPI 中有更高版本的软件，则使用 `pip install --upgrade` 进行更新
        pip.main(['install', package_name, '--upgrade'])
        text.insert(END,"\n您可以开展工作。")
        return "...更新成功。"







      
#####第四部分：主界面 ########################################################################
def copy_file_as_backup(source_file, backup_file):
    """
    复制源文件并创建一个备份文件。
 
    :param source_file: 源文件路径
    :param backup_file: 备份文件路径
    """
    try:
        # 检查源文件是否存在
        if not os.path.isfile(source_file):
            print(f"源文件 {source_file} 不存在")
            return
        
        # 使用 shutil.copy2() 方法复制文件，同时保留元数据（如修改时间）
        shutil.copy2(source_file, backup_file)
        text.insert(END,f"文件已成功复制到备份路径: {backup_file}\n\n ")
    
    except Exception as e:
        text.insert(END,f"复制文件时出错: {e}\n\n ")

def aaa(methon):
	all_list = pd.read_excel(peizhidir+"（分样）所有分过的表格.xls", header=0, sheet_name=0,converters={"报告编码": str})
	fenbiao= pd.read_excel(peizhidir+"（分样）任务分配.xls", header=0, sheet_name=0)
	qingdan= pd.read_excel(peizhidir+"（分样）地市清单.xlsx", header=0, sheet_name=0)
	all_now = pd.read_excel(peizhidir+"（分样）报告审核任务分配表.xls", header=0, sheet_name=0,converters={"报告编码": str})
	#now = datetime.now()
	#formatted_datetime = now.strftime("%Y-%m-%d")
	copy_file_as_backup(peizhidir+"所有分过的表格.xls",peizhidir+"backup_所有分过的表格.xls")

	all_list["报告编码"]=all_list["报告编码"].astype(str)
	all_now["报告编码"]=all_now["报告编码"].astype(str)
	all_now["分样序号"]=all_now.index.copy()
	#print(all_now.head(10))

	#打乱分样清单地市的顺序
	text.insert(END,"打乱分样地市顺序中...打乱后的排序：\n\n ")
	fenbiao=fenbiao.sample(frac=1).reset_index(drop=True)
	listdishi=[k for k in fenbiao["承接评价任务的地市"]]
	text.insert(END,listdishi,'\n\n')
	#将之前已经分过的在当前任务中标记好
	a = methon#input("1-随机分样；2-顺序分样。请输入分样模式（1或2）:")
	try:
		a=int(a)
		if a not in (1,2):
			a=a/0

	except:
		a = input("输入错误或未输入，程序结束。")	
		exit()	

	for ids, cols in all_list.iterrows():
		all_now.loc[(all_now["报告编码"] ==cols["报告编码"]), "承接评价任务的地市"] = cols["承接评价任务的地市"]
		all_now.loc[(all_now["报告编码"] ==cols["报告编码"]), "分配日期"] = cols["分配日期"]
		all_now.loc[(all_now["报告编码"] ==cols["报告编码"]), "是否曾分过"] = "是"
	all_now2 = all_now[(all_now["是否曾分过"] != "是")].copy()

	#对没有分过的，按照任务分配清单进行分样
	text.insert(END,"\n\n 未分样报告数量："+str(len(all_now2)))
	text.insert(END,"\n\n 准备分表总数量："+str((fenbiao["数量"].sum())))
	if fenbiao["数量"].sum()>len(all_now2):
		text.insert(END,"\n\n 准备分表总数量大于未分样报告数量，无法分配，任务结束。")
		cc = input("按任意键结束。")	

		#.sample(frac=float(fracn),replace=False)
	else:
		text.insert(END,"正在分样中，请稍后...")
		for ids, cols in fenbiao.iterrows():
			if a==1:
				datax23 = all_now2.sample(cols["数量"], replace=False)
			elif a==2:
				datax23 = all_now2.head(cols["数量"]).sample(cols["数量"], replace=False)
			all_now2 = pd.concat([all_now2, datax23], axis=0).copy()
			all_now2.drop_duplicates(subset=["报告编码"], keep=False, inplace=True)
			text.insert(END,"\n\n 当前剩余数量："+str(len(all_now2)))
			for ids2, cols2 in datax23.iterrows():
				all_now.loc[(all_now["报告编码"] ==cols2["报告编码"]), "承接评价任务的地市"] = cols["承接评价任务的地市"]
				all_now.loc[(all_now["报告编码"] ==cols2["报告编码"]), "分配日期"] = cols["分配日期"]
				all_now.loc[(all_now["报告编码"] ==cols2["报告编码"]), "是否曾分过"] = "是"

				all_list = pd.concat([all_list, all_now[(all_now["是否曾分过"] == "是")]], axis=0).copy()
				all_list.drop_duplicates(subset=["报告编码"], inplace=True)
		all_list = all_list.sort_values(by="承接评价任务的地市", ascending=[True], na_position="last").reset_index(drop=True)
		all_now = all_now.sort_values(by="承接评价任务的地市", ascending=[True], na_position="last").reset_index(drop=True)
		writer = pd.ExcelWriter(peizhidir+"所有分过的表格.xls",engine="xlsxwriter")  # 
		all_list[["报告编码","承接评价任务的地市","分配日期","是否曾分过"]].to_excel(writer, sheet_name="器械")
		writer.close()
		writer2 = pd.ExcelWriter(peizhidir+"报告审核任务分配表.xls",engine="xlsxwriter")  # 
		all_now[["报告编码","承接评价任务的地市","分配日期","是否曾分过"]].to_excel(writer2, sheet_name="器械")
		writer2.close()

		text.insert(END,"\n\n 正在生成分配表...")
		all_now_t = all_now.groupby(["承接评价任务的地市"]).aggregate( {"报告编码": "count"}).sort_values(by=["报告编码"], ascending=False, na_position="last")
		all_now_t = all_now_t.rename(columns={"报告编码": "所有待评价报告总数量"})
		all_list_t = all_list.groupby(["承接评价任务的地市"]).aggregate( {"报告编码": "count"}).sort_values(by=["报告编码"], ascending=False, na_position="last")
		all_list_t = all_list_t.rename(columns={"报告编码": "所有分过的报告总数量"})
		
		#对不幸分到第一个的地市进行提醒
		
		
		writer11 = pd.ExcelWriter(peizhidir+"●报告审核任务分配表(发布版).xls",engine="xlsxwriter")  #
		writer22 = pd.ExcelWriter(peizhidir+"●所有分过的表格(发布版).xls",engine="xlsxwriter")  #	
		all_now_t.to_excel(writer11, sheet_name="总体概况")
		all_list_t.to_excel(writer22, sheet_name="总体概况")
		for ids3, cols3 in qingdan.iterrows():
			u1= all_now[ (all_now["承接评价任务的地市"] == cols3["承接评价任务的地市"])].copy().reset_index()
			u1=u1.sort_values(by="分样序号", ascending=[False], na_position="last").reset_index(drop=True)
			u2= all_list[ (all_list["承接评价任务的地市"] == cols3["承接评价任务的地市"])].copy().reset_index()	

			if len(u1)>0:
				u1[["分样序号","报告编码","承接评价任务的地市","分配日期","是否曾分过"]].to_excel(writer11, sheet_name=cols3["承接评价任务的地市"])
			if len(u2)>0:
				u2[["报告编码","承接评价任务的地市","分配日期","是否曾分过"]].to_excel(writer22, sheet_name=cols3["承接评价任务的地市"])	
		writer11.close()
		writer22.close()


		text.insert(END, "\n\n任务完成。")


def A0000_Main():
	print("")

if __name__ == '__main__':
	

	root = Tk.Tk()
	root.title(title_all)

	sw_root = root.winfo_screenwidth()
	# 得到屏幕宽度
	sh_root = root.winfo_screenheight()
	# 得到屏幕高度
	ww_root = 700
	wh_root = 620
	# 窗口宽高为100
	x_root = (sw_root - ww_root) / 2
	y_root = (sh_root - wh_root) / 2
	root.geometry("%dx%d+%d+%d" % (ww_root, wh_root, x_root, y_root))
	#root.configure(bg="steelblue")#royalblue

	


	#sysu = ttk.Style()
	##############窗口按钮########################
	try:
		frame0 = ttk.Frame(root, width=90, height=20)
		frame0.pack(side=LEFT)
		B_open_files1 = Button(
			frame0,
			text="随机分样",
			bg="white",
			height=2,
			width=12,
			font=("微软雅黑", 10),
			relief=GROOVE,
			activebackground="green",
			command=lambda:aaa(1),
		)
		B_open_files1.pack()
			

		B_open_files44 = Button(
			frame0,
			text="顺序分样",
			bg="white",
			height=2,
			width=12,
			font=("微软雅黑", 10),
			relief=GROOVE,
			activebackground="green",
			command=lambda:aaa(2),
		)
		B_open_files44.pack()		
		


		

	except KEY:
		pass


	##############提示框########################
	text = ScrolledText(root, height=400, width=400, bg="#FFFFFF")
	text.pack(padx=5, pady=5)
	text.insert(END, "\n 本程序适用于报告分样。\n\n "
	)
	text.insert(END, "\n\n")

	#序列好验证、配置表生成与自动更新。
	setting_cfg=read_setting_cfg()
	generate_random_file()
	setting_cfg=open_setting_cfg()
	if setting_cfg["settingdir"]==0:
		showinfo(title="提示", message="未发现默认工作文件夹，请选择一个。如该工作文件夹中并无配置文件，将生成默认配置文件。")
		filepathu=filedialog.askdirectory()
		filepathu=os.path.normpath(filepathu)
		path=get_directory_path(filepathu)
		update_setting_cfg("settingdir",path)    	
	setting_cfg=open_setting_cfg()
	random_number=int(setting_cfg["sidori"])
	input_number=int(str(setting_cfg["sidfinal"])[0:6])
	day_end=convert_and_compare_dates(str(setting_cfg["sidfinal"])[6:14])
	sid=random_number*2+183576
	if input_number == sid  and day_end=="未过期":
		usergroup="用户组=1" 
		text.insert(END,usergroup+"   有效期至：\n\n ")
		text.insert(END,datetime.strptime(str(int(int(str(setting_cfg["sidfinal"])[6:14])/4)), "%Y%m%d") )
	else:
		text.insert(END,usergroup)	
	text.insert(END,"\n配置文件路径："+setting_cfg["settingdir"]+"\n")
	peizhidir=str(setting_cfg["settingdir"])
	peizhidir=os.path.join(peizhidir, 'fspsssdfpy')
	peizhidir=peizhidir.replace("fspsssdfpy",'')





	#root.deiconify() # show lab window
	root.mainloop()
	print("done.")

	

