# -*- coding: utf-8 -*-

import os

import tkinter
from tkinter import *
from tkinter.filedialog import askdirectory

import Decrypt
import string
import base64
from icon import img

titleConfig = "玩男人解密工具"

class logUI:
    def __init__(self):
        return 

class DecryptUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title(titleConfig)
        self.root.geometry("260x100")


        ico = base64.b64decode(img)
        with open("tmp.ico", 'wb+') as tmp:
            tmp.write(ico)
            tmp.close()

        self.root.iconbitmap("tmp.ico")
        os.remove("tmp.ico")

        # 子元素
        self.getDirPath()
        self.getFilePath()
        self.fullDecrypt()

# UI 函数
    def loop(self):
        self.root.mainloop()
    
    def getDirPath(self):
        self.dirPath = StringVar()
        thisRow = 3
        thisColumn = 3

        Label(self.root,text = "目录路径:").grid(row = thisRow, column = thisColumn)
        Entry(self.root, textvariable = self.dirPath).grid(row = thisRow, column = thisColumn + 1)
        Button(self.root, text = "目录解密", command = self.selectDirPath).grid(row = thisRow, column = thisColumn + 2)
        return 


    def getFilePath(self):
        self.filePath = StringVar()
        thisRow = 4
        thisColumn = 3

        Label(self.root,text = "文件路径:").grid(row = thisRow, column = thisColumn)
        Entry(self.root, textvariable = self.filePath).grid(row = thisRow, column = thisColumn + 1)
        Button(self.root, text = "文件解密", command = self.selectFilePath).grid(row = thisRow, column = thisColumn + 2)
        return 

    def fullDecrypt(self):
        thisRow = 5
        thisColumn = 3

        Button(self.root, text = "全盘解密", command = self.do_FullDecrypt).grid(row = thisRow, column = thisColumn + 1)
        return 

# UI 功能函数
    def selectFilePath(self):
        path = tkinter.filedialog.askopenfilename()
        self.filePath.set(path)
        self.decrypt(path)
        tkinter.messagebox.showinfo(title="a", message="解密完成")
        return 
    def selectDirPath(self):
        path = tkinter.filedialog.askdirectory()
        self.dirPath.set(path)
        self.decrypt(path)
        tkinter.messagebox.showinfo(title="a", message="解密完成")
        return 

    def do_FullDecrypt(self):
        disk = self.get_disklist()
        for x in disk:
            y = x + "\\\\"
            self.decrypt(y)
        return

# 其他功能函数
    def get_disklist(self):
        disk_list = []
        for c in string.ascii_uppercase:
            disk = c+':'
            if os.path.isdir(disk):
                disk_list.append(disk)
        return disk_list
# 解密接口函数
    def decrypt(self, path):

        if False == os.path.exists(path):
            tkinter.messagebox.showerror(title="ERROR", message="Wrong path")

        try:
            if os.path.isdir(path):
                Decrypt.DecryptDir(path)
            else:
                Decrypt.DecryptFile(path)
        except Exception as string:
            tkinter.messagebox.showerror(title="ERROR", message=string)

        return

if __name__ == "__main__":
    
    a = DecryptUI()
    a.loop()