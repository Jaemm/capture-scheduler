from tkinter import *
from _thread import *
from socket import *

import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title("First C&D")
        self.geometry("1280x720")
        self.resizable(True,True)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="First C&D", font=('Helvetica', 18, "bold"), bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="1번 충전기",
                  command=lambda: master.switch_frame(PageOne),width="10", height="15", bg="#1E1E2A", fg='white').pack(side="left")
        tk.Button(self, text="2번 충전기",
                  command=lambda: master.switch_frame(PageTwo),width="10", height="15", bg="#1E1E2A", fg='white').pack(side="left")
        tk.Button(self, text="3번 충전기",
                  command=lambda: master.switch_frame(PageThree),width="10", height="15", bg="#1E1E2A", fg='white').pack(side="left")
        
        

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="상세정보", font=('Helvetica', 18, "bold"),bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="처음으로",
                  command=lambda: master.switch_frame(StartPage), bg="#1E1E2A", fg='white').pack()
        tk.Frame(self, relief="solid", bd=2).pack(side="left", fill="both", expand=True)  
        tk.Button(self, text="1번 충전기 제어 버튼",command=lambda: master.switch_frame(PageOne_Control), width=30, height=2, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="iamge file",bg="#1E1E2A", fg="white", width=10, height=2).pack(side="top")
        tk.Label(self, text="충전건 상태", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="충전 전력량", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="충전 시간", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="상세정보", font=('Helvetica', 18, "bold"),bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="처음으로",
                  command=lambda: master.switch_frame(StartPage), bg="#1E1E2A", fg='white').pack()
        tk.Frame(self, relief="solid", bd=2).pack(side="left", fill="both", expand=True)  
        tk.Button(self, text="n번 충전기 제어 버튼",command=lambda: master.switch_frame(PageTwo_Control), width=30, height=2, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="iamge file",bg="#1E1E2A", fg="white").pack(side="top")
        tk.Label(self, text="충전건 상태", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="충전 전력량", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="충전 시간", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        
class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="상세정보", font=('Helvetica', 18, "bold"),bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="처음으로",
                  command=lambda: master.switch_frame(StartPage), bg="#1E1E2A", fg='white').pack()
        tk.Frame(self, relief="solid", bd=2).pack(side="left", fill="both", expand=True)  
        tk.Button(self, text="n번 충전기 제어 버튼",command=lambda: master.switch_frame(PageThree_Control), width=30, height=2, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="iamge file",bg="#1E1E2A", fg="white").pack(side="top")
        tk.Label(self, text="충전건 상태", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="충전 전력량", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, text="충전 시간", width=15, height=1, bg="#1E1E2A", fg='white').pack(side="top")
        tk.Label(self, bg="#1E1E2A", fg='white').pack(side="top")
        
class PageOne_Control(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="n번 충전기 제어", font=('Helvetica', 18, "bold"),bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="이전",
                  command=lambda: master.switch_frame(PageOne), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="충전기 시작",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="충전기 중지",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="1M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="2M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="3M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        
        
class PageTwo_Control(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="n번 충전기 제어", font=('Helvetica', 18, "bold"),bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="이전",
                  command=lambda: master.switch_frame(PageOne), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="충전기 시작",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="충전기 중지",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="1M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="2M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="3M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()

class PageThree_Control(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="n번 충전기 제어", font=('Helvetica', 18, "bold"),bg="#1E1E2A", fg='white').pack(side="top", fill="x", pady=5)
        tk.Button(self, text="이전",
                  command=lambda: master.switch_frame(PageOne), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="충전기 시작",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="충전기 중지",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="1M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="2M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()
        tk.Button(self, text="3M",
                  command=lambda: master.switch_frame(), bg="#1E1E2A", fg='white').pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()