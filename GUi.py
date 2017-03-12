

from tkinter import *


class CheckBar(Frame):

    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


def send():
    print(list(lng.state()))


def setdestination(Frame):
    print("click")


top = tkinter.Tk()
B = tkinter.Button(top, text="Start", command=send)
Label(text='Enter Hosts:').pack(side=TOP)
hosts = Entry(top, width=20)
hosts.pack(side=TOP, padx=10, pady=10)

Label(text='Enter Destinations (<10):').pack(side=TOP)
dest = Entry(top, width=20)
dest.pack(side=TOP, padx=10, pady=10)

Label(text='Enter Noise level:').pack(side=TOP)
nosie= Entry(top, width=20)
nosie.pack(side=TOP, padx=10, pady=10)

Label(text='Enter Speed:').pack(side=TOP)
speed = Entry(top, width=20)
speed.pack(side=TOP, padx=10, pady=10)


lng = CheckBar(top, ['STAR', 'MESH', 'BUS'])
lng.pack(side=TOP,  fill=X)
lng.config(relief=GROOVE, bd=2)

#photo = PhotoImage(file= r"pic.gif")
#cv = Canvas()
#cv.pack(side='top', fill='both', expand='yes')
#cv.create_image(10, 10, image=photo, anchor='nw')

B.pack()
top.mainloop()


