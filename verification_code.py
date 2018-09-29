# -*- coding: UTF-8 -*-
from Tkinter import *
from PIL import Image, ImageTk
root = Tk()
var1 = StringVar()


def print_button():
    # 关闭窗口
    root.quit()


# 打开图片手动输入验证码 返回输入的验证码
def get_code():
    root.title('验证码')
    # 打开code.jpg
    img = Image.open('code.jpg')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    img_label = Label(root, image=photo)
    img_label.grid(row=0, column=0, columnspan=3)
    Label(root, text="验证码:").grid(row=1, column=0, sticky=S + N)
    # 输入的值var1
    answer_entry = Entry(root, textvariable=var1)
    btn = Button(root, text="确定", command=print_button)
    answer_entry.grid(row=1, column=1)
    btn.grid(row=1, column=2)
    mainloop()
    # 返回验证码
    return var1.get()



