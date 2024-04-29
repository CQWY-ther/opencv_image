from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk  # 图像控件
import cv2

root = Tk()
root.title("capture_smile")
root.geometry("820x500")
cap = cv2.VideoCapture(0)  # 创建摄像头对象

canvas = Canvas(root, bg='steelblue')  # 绘制画布
canvas.place(x=0, y=0, height=400, width=400)

Label(root, text='捕获笑脸！', font=("黑体", 14), width=15, height=1).place(x=0, y=0, anchor='nw')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

smile = 0

smile1 = Label(root, bg="steelblue")
smile1.place(x=410, y=0, height=95, width=95)
smile2 = Label(root, bg="steelblue")
smile2.place(x=510, y=0, height=95, width=95)
smile3 = Label(root, bg="steelblue")
smile3.place(x=610, y=0, height=95, width=95)
smile4 = Label(root, bg="steelblue")
smile4.place(x=710, y=0, height=95, width=95)
smile5 = Label(root, bg="steelblue")
smile5.place(x=410, y=100, height=95, width=95)
smile6 = Label(root, bg="steelblue")
smile6.place(x=510, y=100, height=95, width=95)
smile7 = Label(root, bg="steelblue")
smile7.place(x=610, y=100, height=95, width=95)
smile8 = Label(root, bg="steelblue")
smile8.place(x=710, y=100, height=95, width=95)
smile9 = Label(root, bg="steelblue")
smile9.place(x=410, y=200, height=95, width=95)
smile10 = Label(root, bg="steelblue")
smile10.place(x=510, y=200, height=95, width=95)
smile11 = Label(root, bg="steelblue")
smile11.place(x=610, y=200, height=95, width=95)
smile12 = Label(root, bg="steelblue")
smile12.place(x=710, y=200, height=95, width=95)
smile13 = Label(root, bg="steelblue")
smile13.place(x=410, y=300, height=95, width=95)
smile14 = Label(root, bg="steelblue")
smile14.place(x=510, y=300, height=95, width=95)
smile15 = Label(root, bg="steelblue")
smile15.place(x=610, y=300, height=95, width=95)
smile16 = Label(root, bg="steelblue")
smile16.place(x=710, y=300, height=95, width=95)


def re_capture():
    global smile
    a = messagebox.askyesno("提示", "需要重新捕获笑脸吗？")
    if a:
        for i in range(16):
            sign = eval("smile" + str(i + 1))
            sign.config(image="")
        smile = 0


btn1 = Button(root, text="重新捕获笑脸", bg="steelblue", relief=FLAT, command=re_capture)
btn1.place(x=560, y=430, width=120, height=40)

while True:
    ref, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 摄像头翻转

    # 获取摄像头拍摄到的画面
    faces = face_cascade.detectMultiScale(frame, 1.3, 2)
    img = frame
    for (x, y, w, h) in faces:
        # 画出人脸框，蓝色，画笔宽度微
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
        face_area = img[y:y + h, x:x + w]

        # 人眼检测
        # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
        eyes = eye_cascade.detectMultiScale(face_area, 1.3, 10)
        for (ex, ey, ew, eh) in eyes:
            # 画出人眼框，绿色，画笔宽度为1
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

        # 微笑检测
        # 用微笑级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
        smiles = smile_cascade.detectMultiScale(face_area, scaleFactor=1.16, minNeighbors=65, minSize=(25, 25),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        for (ex, ey, ew, eh) in smiles:
            # 画出微笑框，红色（BGR色彩体系），画笔宽度为1
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
            cv2.putText(img, 'Smile', (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)

        for (ex, ey, ew, eh) in smiles:
            if smile < 16:
                smile = smile + 1
                sign = eval("smile" + str(smile))
                cv2.imwrite("smile\smile" + str(smile) + ".jpg", frame)
                rst = Image.open("smile\smile" + str(smile) + ".jpg")
                rst = rst.resize((95, 95))
                pic = ImageTk.PhotoImage(image=rst)
                sign.config(image=pic)
                sign.image = pic
            else:
                break

    pilImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(pilImage)
    pilImage = pilImage.resize((350, 350), Image.LANCZOS)
    pic = ImageTk.PhotoImage(image=pilImage)
    canvas.create_image(50, 50, anchor='nw', image=pic)
    # 每5毫秒监听一次键盘动作
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    root.update()
    root.after(1)

cap.release()  # 释放摄像头
root.mainloop()  # 关闭窗口
