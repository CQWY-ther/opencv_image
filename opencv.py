import shutil

import cv2
import os
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from PIL import Image, ImageTk
import numpy as np

root = Tk()
root.geometry("1500x700")
root.configure(bg="seagreen")
root.title("JiaFeng CV 1.0")


def selectPath():
    global path_
    path_ = askdirectory()  # 使用askdirectory()方法返回文件夹的路径
    global dirs
    dirs = os.listdir(path_)
    if path_ == "":
        path.get()  # 当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    else:
        path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
        path.set(path_)


def openPath():
    dir = os.path.dirname(path.get() + "\\")
    os.system('start ' + dir)


def help():
    tkinter.messagebox.showinfo("帮助", "①翻转操作：输入0绕x轴翻转，输入正数绕y轴翻转，输入负数x,y轴同时翻转"
                                        "②旋转操作：输入旋转角度（正数为逆时针旋转），输入缩放倍数                  "
                                        "③阈值处理：输入处理方式（二值化阈值处理、反二值化阈值处理、截断阈值"
                                        "化处理、超阈值零处理、低阈值零处理），输入阈值（0-255）                        "
                                        "④滤波操作：输入处理方式（均值滤波、方块滤波、高斯滤波、中值滤波、双"
                                        "边滤波），输入滤波核大小                                                                                   "
                                        "⑤形态学操作：输入操作类型（腐蚀、膨胀、开运算、闭运算、形态学梯度运"
                                        "算、礼帽运算、黑帽运算），输入滤波核大小                                                     "
                                        "⑥canny边缘检测：输入阈值区间                                                                      "
                                        "⑦直方图均衡化处理                                                                                             "
                                        "⑧分水岭算法图像分割：输入滤波核大小                                                           "
                                        "⑨Hough直线检测：输入直线最短长度、一条线中两点最大间隔                      "
                                        "⑩Hough圆检测：输入圆的最小和最大半径                                                      "
                                        "关于文件保存：可以点击左上角文件进行保存，也可以鼠标右键进行选择保存"
                                        "点击左上角文件按钮进行打开要编辑的文件夹的位置，编辑按钮进行界面清空"
                                )


def concern():
    tkinter.messagebox.showinfo("版权", "Copyright 2023 李婷.All rights reserved.")


def show_yuantu(dst, label):
    a = ImageTk.PhotoImage(dst)
    label.config(image=a)
    label.image = a


def show_xiantu(rst, label):
    a = ImageTk.PhotoImage(rst)
    label.config(image=a)
    label.image = a


def clear():
    for i in range(10):
        result = eval("result" + str(i + 1))
        result.delete("1.0", "end")
        sign = eval("label" + str(i + 3))
        sign.config(image="")


def fanzhuan():
    global code  # 0绕x轴，正数绕y轴，负数绕x,y轴
    code = eval(Code.get("1.0", "end-1c"))
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        dst = cv2.imread(path_ + "/" + dirs[i])
        rst = cv2.flip(dst, code)
        dst = Image.open(path_ + "/" + dirs[i])
        dst = dst.resize((150, 150))
        show_yuantu(dst, sign1)
        cv2.imwrite(dirs[i], rst)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result1.insert("1.0", "图片翻转已完成！")


def save_fanzhaun():
    wj_name = "fanzhuan"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        dst = cv2.imread(old_path)
        rst = cv2.flip(dst, code)
        cv2.imwrite(wj_name + "/" + file, rst)


btn1 = Button(root, text="翻转图片", bg="steelblue", relief=tkinter.FLAT, command=fanzhuan)
btn1.place(x=20, y=420, width=120, height=40)
label1 = Label(root, text="code=", bg="wheat")
label1.place(x=160, y=420, width=150, height=40)
Code = Text(root)
Code.place(x=330, y=420, width=80, height=40)
Code.insert("1.0", "0")
result1 = Text(root)  # 图片翻转已完成！
result1.place(x=700, y=420, width=150, height=40)


def xuanzhuan():
    global angle  # 正数逆时针，负数顺时针
    angle = eval(Angle.get("1.0", "end-1c"))
    global scale  # 缩放倍数
    scale = eval(Scale.get("1.0", "end-1c"))
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i])
        height, width = img.shape[:2]
        M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
        rotate = cv2.warpAffine(img, M, (width, height))
        dst = Image.open(path_ + "/" + dirs[i])
        show_yuantu(dst, sign1)
        cv2.imwrite(dirs[i], rotate)
        rst = Image.open(dirs[i])
        show_xiantu(rst, sign2)
    result2.insert("1.0", "图片旋转已完成！")


def save_xuanzhaun():
    wj_name = "xuanzhuan"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path)
        height, width = img.shape[:2]
        M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
        rotate = cv2.warpAffine(img, M, (width, height))
        cv2.imwrite(wj_name + "/" + file, rotate)


btn2 = Button(root, text="旋转图片", bg="steelblue", relief=tkinter.FLAT, command=xuanzhuan)
btn2.place(x=20, y=120, width=120, height=40)
label2 = Label(root, text="angle=", bg="wheat")
label2.place(x=160, y=120, width=150, height=40)
Angle = Text(root, width=20, height=2)
Angle.place(x=330, y=120, width=80, height=40)
Angle.insert("1.0", "45")
label13 = Label(root, text="scale=", bg="wheat")
label13.place(x=430, y=120, width=150, height=40)
Scale = Text(root, width=20, height=2)
Scale.place(x=600, y=120, width=80, height=40)
Scale.insert("1.0", "0.6")
result2 = Text(root, width=20, height=2)  # 图片旋转已完成！
result2.place(x=700, y=120, width=150, height=40)


def yuzhi_chuli():
    global thresh  # 阈值
    thresh = eval(Thresh.get("1.0", "end-1c"))
    global type  # 阈值处理类型
    type = Type.get("1.0", "end-1c")
    if type == "二值化阈值处理":
        type = eval("cv2.THRESH_BINARY")
    elif type == "反二值化阈值处理":
        type = eval("cv2.THRESH_BINARY_INV")
    elif type == "截断阈值化处理":
        type = eval("cv2.THRESH_TRUNC")
    elif type == "超阈值零处理":
        type = eval("cv2.THRESH_TOZERO_INV")
    elif type == "低阈值零处理":
        type = eval("cv2.THRESH_TOZERO")
    else:
        tkinter.messagebox.showerror(title="error", message="没有此阈值处理功能！")
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        dst = cv2.imread(path_ + "/" + dirs[i])
        retval, rst = cv2.threshold(dst, thresh, 255, type)
        dst = Image.open(path_ + "/" + dirs[i])
        dst = dst.resize((150, 150))
        show_yuantu(dst, sign1)
        cv2.imwrite(dirs[i], rst)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result3.insert("1.0", "图片阈值处理已完成！")


def save_yuzhi():
    wj_name = "yuzhi_chuli"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        dst = cv2.imread(old_path)
        retval, rst = cv2.threshold(dst, thresh, 255, type)
        cv2.imwrite(wj_name + "/" + file, rst)


btn3 = Button(root, text="阈值处理图片", bg="steelblue", relief=tkinter.FLAT, command=yuzhi_chuli)
btn3.place(x=20, y=170, width=120, height=40)
label14 = Label(root, text="设定阈值（0-255）：", bg="wheat")
label14.place(x=160, y=170, width=150, height=40)
Thresh = Text(root)
Thresh.place(x=330, y=170, width=80, height=40)
Thresh.insert("1.0", "127")
label15 = Label(root, text="阈值处理方式：", bg="wheat")
label15.place(x=430, y=170, width=150, height=40)
Type = Text(root)
Type.place(x=600, y=170, width=80, height=40)
Type.insert("1.0", "二值化阈值处理")
result3 = Text(root)  # 图片阈值化处理已完成！
result3.place(x=700, y=170, width=150, height=40)



def lvbo_chuli():
    global ksize  # 滤波核大小
    ksize = eval(Ksize.get("1.0", "end-1c"))
    global type1  # 滤波处理类型
    type1 = Type1.get("1.0", "end-1c")
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        dst = cv2.imread(path_ + "/" + dirs[i])
        if type1 == "均值滤波":
            rst = cv2.blur(dst, (ksize, ksize))
        elif type1 == "方块滤波":
            rst = cv2.boxFilter(dst, -1, (ksize, ksize))
        elif type1 == "高斯滤波":
            rst = cv2.GaussianBlur(dst, (ksize, ksize), 0, 0)
        elif type1 == "中值滤波":
            if ksize / 2 == 1:
                rst = cv2.medianBlur(dst, ksize)
            else:
                tkinter.messagebox.showerror(title="error", message="中值滤波的滤波核大小必须为奇数！")
        elif type1 == "双边滤波":
            rst = cv2.bilateralFilter(dst, 5, 100, 100)
        else:
            tkinter.messagebox.showerror(title="error", message="没有此阈值处理功能！")
        img = Image.open(path_ + "/" + dirs[i])
        img = img.resize((150, 150))
        show_yuantu(img, sign1)
        cv2.imwrite(dirs[i], rst)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result4.insert("1.0", "图片滤波处理已完成！")


def save_lvbo():
    wj_name = "lvbo_chuli"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        dst = cv2.imread(old_path)
        retval, rst = cv2.threshold(dst, thresh, 255, type)
        cv2.imwrite(wj_name + "/" + file, rst)


btn4 = Button(root, text="滤波处理图片", bg="steelblue", relief=tkinter.FLAT, command=lvbo_chuli)
btn4.place(x=20, y=220, width=120, height=40)
label16 = Label(root, text="设定滤波核大小ksize=", bg="wheat")
label16.place(x=160, y=220, width=150, height=40)
Ksize = Text(root)
Ksize.place(x=330, y=220, width=80, height=40)
Ksize.insert("1.0", "5")
label17 = Label(root, text="设定滤波处理方式", bg="wheat")
label17.place(x=430, y=220, width=150, height=40)
Type1 = Text(root)
Type1.place(x=600, y=220, width=80, height=40)
Type1.insert("1.0", "均值滤波")
result4 = Text(root)  # 图片滤波处理已完成！
result4.place(x=700, y=220, width=150, height=40)


def xingtaixue():
    global kernel  # 滤波核大小
    ksize1 = eval(Ksize1.get("1.0", "end-1c"))
    kernel = np.ones((ksize1, ksize1), np.uint8)
    global op  # 形态学处理类型
    op = Op.get("1.0", "end-1c")
    if op == "腐蚀":
        op = eval("cv2.MORPH_ERODE")
    elif op == "膨胀":
        op = eval("cv2.MORPH_DILATE")
    elif op == "开运算":
        op = eval("cv2.MORPH_OPEN")
    elif op == "闭运算":
        op = eval("cv2.MORPH_CLOSE")
    elif op == "形态学梯度运算":
        op = eval("cv2.MORPH_GRADIENT")
    elif op == "礼帽运算":
        op = eval("cv2.cv2.MORPH_TOPHAT")
    elif op == "黑帽运算":
        op = eval("cv2.cv2.MORPH_BLACKHAT")
    else:
        tkinter.messagebox.showerror(title="error", message="没有此形态学处理功能！")
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i])

        dst = cv2.morphologyEx(img, op, kernel)
        img = Image.open(path_ + "/" + dirs[i])
        img = img.resize((150, 150))
        show_yuantu(img, sign1)
        cv2.imwrite(dirs[i], dst)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result5.insert("1.0", "图片形态学处理已完成！")


def save_xingtaixue():
    wj_name = "xingtaixue"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path)
        dst = cv2.morphologyEx(img, op, kernel)
        cv2.imwrite(wj_name + "/" + file, dst)


btn5 = Button(root, text="形态学处理图片", bg="steelblue", relief=tkinter.FLAT, command=xingtaixue)
btn5.place(x=20, y=270, width=120, height=40)
label18 = Label(root, text="设定滤波核大小ksize=", bg="wheat")
label18.place(x=160, y=270, width=150, height=40)
Ksize1 = Text(root)
Ksize1.place(x=330, y=270, width=80, height=40)
Ksize1.insert("1.0", "5")
label19 = Label(root, text="设定运算操作形式", bg="wheat")
label19.place(x=430, y=270, width=150, height=40)
Op = Text(root)
Op.place(x=600, y=270, width=80, height=40)
Op.insert("1.0", "腐蚀")
result5 = Text(root, width=20, height=2)  # 图片形态学处理已完成！
result5.place(x=700, y=270, width=150, height=40)


def canny():
    global threshold1, threshold2  # 阈值区间
    threshold1 = eval(Threshold1.get("1.0", "end-1c"))
    threshold2 = eval(Threshold2.get("1.0", "end-1c"))
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i], 0)
        dst = cv2.Canny(img, threshold1, threshold2)
        img = Image.open(path_ + "/" + dirs[i])
        img = img.resize((150, 150))
        show_yuantu(img, sign1)
        cv2.imwrite(dirs[i], dst)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result6.insert("1.0", "图片canny边缘检测已完成！")


def save_canny():
    wj_name = "canny"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path, 0)
        dst = cv2.Canny(img, threshold1, threshold2)
        cv2.imwrite(wj_name + "/" + file, dst)


btn6 = Button(root, text="canny边缘检测图片", bg="steelblue", relief=tkinter.FLAT, command=canny)
btn6.place(x=20, y=320, width=120, height=40)
label20 = Label(root, text="第一个阈值（0-255）：", bg="wheat")
label20.place(x=160, y=320, width=150, height=40)
Threshold1 = Text(root)
Threshold1.place(x=330, y=320, width=80, height=40)
Threshold1.insert("1.0", "30")
label21 = Label(root, text="第二个阈值（0-255）：", bg="wheat")
label21.place(x=430, y=320, width=150, height=40)
Threshold2 = Text(root)
Threshold2.place(x=600, y=320, width=80, height=40)
Threshold2.insert("1.0", "200")
result6 = Text(root)  # 图片canny边缘检测已完成！
result6.place(x=700, y=320, width=150, height=40)


def equalize_hist():
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i], 0)
        dst = cv2.equalizeHist(img)
        img = Image.open(path_ + "/" + dirs[i])
        img = img.resize((150, 150))
        show_yuantu(img, sign1)
        cv2.imwrite(dirs[i], dst)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result7.insert("1.0", "图片直方图均衡化已完成！")


def save_hist():
    wj_name = "equalize_hist"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path, 0)
        dst = cv2.equalizeHist(img)
        cv2.imwrite(wj_name + "/" + file, dst)


btn7 = Button(root, text="直方图均衡化处理", bg="steelblue", relief=tkinter.FLAT, command=equalize_hist)
btn7.place(x=20, y=520, width=120, height=40)
result7 = Text(root)  # 直方图均衡化处理已完成！
result7.place(x=700, y=520, width=150, height=40)


def fenge():  # 分水岭算法图像分割
    global kernel1  # 滤波核大小
    ksize2 = eval(Ksize2.get("1.0", "end-1c"))
    kernel1 = np.ones((ksize2, ksize2), np.uint8)
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1, iterations=2)
        sure_bg = cv2.dilate(opening, kernel1, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(img, markers)
        img[markers == -1] = [225, 0, 0]
        o = Image.open(path_ + "/" + dirs[i])
        o = o.resize((150, 150))
        show_yuantu(o, sign1)
        cv2.imwrite(dirs[i], img)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result8.insert("1.0", "分水岭算法图像分割已完成！")


def save_fenge():
    wj_name = "fen_ge"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1, iterations=2)
        sure_bg = cv2.dilate(opening, kernel1, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(img, markers)
        img[markers == -1] = [225, 0, 0]
        cv2.imwrite(wj_name + "/" + file, img)


btn8 = Button(root, text="图像分割处理", bg="steelblue", relief=tkinter.FLAT, command=fenge)
btn8.place(x=20, y=470, width=120, height=40)
label22 = Label(root, text="设定滤波核大小ksize=", bg="wheat")
label22.place(x=160, y=470, width=150, height=40)
Ksize2 = Text(root)
Ksize2.place(x=330, y=470, width=80, height=40)
Ksize2.insert("1.0", "3")
result8 = Text(root, width=20, height=2)  # 直图像分割处理已完成！
result8.place(x=700, y=470, width=150, height=40)


def houghlines():
    global minlength, maxgap
    minlength = eval(Minlength.get("1.0", "end-1c"))
    maxgap = eval(Maxgap.get("1.0", "end-1c"))
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i], -1)
        gray = cv2.imread(path_ + "/" + dirs[i], 0)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 0, minLineLength=minlength, maxLineGap=maxgap)
        if lines is None:
            tkinter.messagebox.showerror(title="error", message="第{:}张图片未检测到直线！".format(i + 1))
            continue
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        o = Image.open(path_ + "/" + dirs[i])
        o = o.resize((150, 150))
        show_yuantu(o, sign1)
        cv2.imwrite(dirs[i], img)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result9.insert("1.0", "hough直线检测已完成！")


def save_houghlines():
    wj_name = "hough_lines"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path, -1)
        gray = cv2.imread(old_path, 0)
        edges = cv2.Canny(gray, 50, 200, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 0, minLineLength=minlength, maxLineGap=maxgap)
        if not lines.any():
            continue
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite(wj_name + "/" + file, img)


btn9 = Button(root, text="hough直线检测", relief=tkinter.FLAT, bg="steelblue", command=houghlines)
btn9.place(x=20, y=70, width=120, height=40)
label23 = Label(root, text="minLineLength=", bg="wheat")
label23.place(x=160, y=70, width=150, height=40)
Minlength = Text(root)
Minlength.place(x=330, y=70, width=80, height=40)
Minlength.insert("1.0", "3")
label24 = Label(root, text="maxLineGap=", bg="wheat")  # 一条线中两点最大间隔
label24.place(x=430, y=70, width=150, height=40)
Maxgap = Text(root)
Maxgap.place(x=600, y=70, width=80, height=40)
Maxgap.insert("1.0", "3")
result9 = Text(root)  # 直图像分割处理已完成！
result9.place(x=700, y=70, width=150, height=40)


def houghcircles():
    global minradius, maxradius
    minradius = eval(minRadius.get("1.0", "end-1c"))
    maxradius = eval(maxRadius.get("1.0", "end-1c"))
    for i in range(5):
        sign1 = eval("label" + str(3 + i))
        sign2 = eval("label" + str(8 + i))
        img = cv2.imread(path_ + "/" + dirs[i], 0)
        imgo = cv2.imread(path_ + "/" + dirs[i], -1)
        img = cv2.medianBlur(img, 3)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=70, minRadius=minradius,
                                   maxRadius=maxradius)
        if circles is None:
            tkinter.messagebox.showerror(title="error", message="第{:}张图片未检测到圆！".format(i + 1))
            continue
        circles = np.uint16(np.around(circles))
        for j in circles[0, :]:
            cv2.circle(imgo, (j[0], j[1]), j[2], (255, 0, 0), 10)
            cv2.circle(imgo, (j[0], j[1]), 2, (255, 0, 0), 10)
        o = Image.open(path_ + "/" + dirs[i])
        o = o.resize((150, 150))
        show_yuantu(o, sign1)
        cv2.imwrite(dirs[i], imgo)
        rst = Image.open(dirs[i])
        rst = rst.resize((150, 150))
        show_xiantu(rst, sign2)
    result10.insert("1.0", "hough圆检测已完成！")


def save_houghcircles():
    wj_name = "hough_circles"
    if os.path.isdir(wj_name):
        shutil.rmtree(wj_name)  # 同时删除里面的所有文件
    os.mkdir(wj_name)
    for file in dirs:
        old_path = path_ + "/" + file
        img = cv2.imread(old_path, 0)
        imgo = cv2.imread(old_path, -1)
        img = cv2.medianBlur(img, 3)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=70, minRadius=minradius,
                                   maxRadius=maxradius)
        if circles is None:
            continue
        circles = np.uint16(np.around(circles))
        for j in circles[0, :]:
            cv2.circle(imgo, (j[0], j[1]), j[2], (255, 0, 0), 10)
            cv2.circle(imgo, (j[0], j[1]), 2, (255, 0, 0), 10)
        cv2.imwrite(wj_name + "/" + file, imgo)


btn10 = Button(root, text="hough圆检测", bg="steelblue", relief=tkinter.FLAT, command=houghcircles)
btn10.place(x=20, y=370, width=120, height=40)
label24 = Label(root, text="minRadius=", bg="wheat")
label24.place(x=160, y=370, width=150, height=40)
minRadius = Text(root)
minRadius.place(x=330, y=370, width=80, height=40)
minRadius.insert("1.0", "20")
label25 = Label(root, text="maxRadius=", bg="wheat")
label25.place(x=430, y=370, width=150, height=40)
maxRadius = Text(root)
maxRadius.place(x=600, y=370, width=80, height=40)
maxRadius.insert("1.0", "200")
result10 = Text(root)
result10.place(x=700, y=370, width=150, height=40)


label3 = Label(root, text="原图1")
label3.place(x=870, y=10, width=150, height=150)
label4 = Label(root, text="原图2")
label4.place(x=870, y=170, width=150, height=150)
label5 = Label(root, text="原图3")
label5.place(x=870, y=330, width=150, height=150)

label8 = Label(root, text="现图1")
label8.place(x=1030, y=10, width=150, height=150)
label9 = Label(root, text="现图2")
label9.place(x=1030, y=170, width=150, height=150)
label10 = Label(root, text="现图3")
label10.place(x=1030, y=330, width=150, height=150)

label6 = Label(root, text="原图4")
label6.place(x=1190, y=10, width=150, height=150)
label7 = Label(root, text="原图5")
label7.place(x=1190, y=170, width=150, height=150)

label11 = Label(root, text="现图4")
label11.place(x=1350, y=10, width=150, height=150)
label12 = Label(root, text="现图5")
label12.place(x=1350, y=170, width=150, height=150)

path = StringVar()
path.set(os.path.abspath("."))  # 当前目录的绝对路径

Label(root, text="目标路径:").place(x=20, y=20, width=70, height=40)
Entry(root, textvariable=path, state="readonly").place(x=100, y=20, width=400, height=40)

Button(root, text="路径选择", command=selectPath).place(x=550, y=20, width=70, height=40)

# # 创建一个顶级菜单
menubar = Menu(root)

# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = Menu(menubar, tearoff=False)
save = Menu(filemenu)
filemenu.add_command(label="打开", command=openPath)
filemenu.add_cascade(label="保存文件夹", menu=save)
save.add_command(label="翻转图像保存", command=save_fanzhaun)
save.add_command(label="旋转图像保存", command=save_xuanzhaun)
save.add_command(label="阈值处理图像保存", command=save_yuzhi)
save.add_command(label="滤波处理图像保存", command=save_lvbo)
save.add_command(label="形态学处理图像保存", command=save_xingtaixue)
save.add_command(label="canny边缘检测图像保存", command=save_canny)
save.add_command(label="直方图均衡化图像保存", command=save_hist)
save.add_command(label="分水岭算法分割图像保存", command=save_fenge)
save.add_command(label="Hough直线检测图像保存", command=save_houghlines)
save.add_command(label="Hough圆检测图像保存", command=save_houghcircles)
filemenu.add_command(label="退出", command=root.quit)
menubar.add_cascade(label="文件(F)", menu=filemenu)

# 创建另一个下拉菜单“编辑”，然后将它添加到顶级菜单中
editmenu = Menu(menubar, tearoff=False)
editmenu.add_command(label="清空界面结果", command=clear)
menubar.add_cascade(label="编辑(E)", menu=editmenu)

helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="查找操作", command=help)
menubar.add_cascade(label="帮助(H)", menu=helpmenu)

concernmenu = Menu(menubar, tearoff=False)
concernmenu.add_command(label="版权", command=concern)
menubar.add_cascade(label="关于(C)", menu=concernmenu)

# 显示菜单
root.config(menu=menubar)


# 创建一个弹出菜单
def showPopoutMenu(w, menu):
    def popout(event):
        menu.post(event.x + w.winfo_rootx(), event.y + w.winfo_rooty())
        w.update()

    w.bind('<Button-3>', popout)


menu = Menu(root, tearoff=False)
menu.add_cascade(label="翻转图像保存", command=save_fanzhaun)
menu.add_cascade(label="旋转图像保存", command=save_xuanzhaun)
menu.add_cascade(label="阈值处理图像保存", command=save_yuzhi)
menu.add_cascade(label="滤波处理图像保存", command=save_lvbo)
menu.add_cascade(label="形态学处理图像保存", command=save_xingtaixue)
menu.add_cascade(label="canny边缘检测图像保存", command=save_canny)
menu.add_cascade(label="直方图均衡化图像保存", command=save_hist)
menu.add_cascade(label="分水岭算法分割图像保存", command=save_fenge)
menu.add_cascade(label="Hough直线检测图像保存", command=save_houghlines)
menu.add_cascade(label="Hough圆检测图像保存", command=save_houghcircles)
showPopoutMenu(root, menu)

root.mainloop()
