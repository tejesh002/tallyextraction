# from tkinter import *

# root = Tk()
# scrollbar = Scrollbar(root)
# scrollbar.pack( side = RIGHT, fill = Y )

# mylist = Listbox(root, yscrollcommand = scrollbar.set )
# for line in range(100):
#    mylist.insert(END, "This is line number " + str(line))

# mylist.pack( side = LEFT, fill = BOTH )
# scrollbar.config( command = mylist.yview )

# mainloop()

# import tkinter as tk

# class App:
#     def __init__(self):
#         self.root=tk.Tk()
#         self.vsb = tk.Scrollbar(orient="vertical", command=self.OnVsb)
#         self.lb1 = tk.Listbox(self.root, yscrollcommand=self.vsb.set)
#         self.lb2 = tk.Listbox(self.root, yscrollcommand=self.vsb.set)
#         self.vsb.pack(side="right",fill="y")
#         self.lb1.pack(side="left",fill="x", expand=True)
#         # self.lb2.pack(side="left",fill="x", expand=True)
#         self.lb1.bind("<MouseWheel>", self.OnMouseWheel)
#         # self.lb2.bind("<MouseWheel>", self.OnMouseWheel)
#         for i in range(100):
#             self.lb1.insert("end","item %s" % i)
#             self.lb2.insert("end","item %s" % i)
#         self.root.mainloop()

#     def OnVsb(self, *args):
#         self.lb1.yview(*args)
#         self.lb2.yview(*args)

#     def OnMouseWheel(self, event):
#         self.lb1.yview("scroll", event.delta,"units")
#         self.lb2.yview("scroll",event.delta,"units")
#         # this prevents default bindings from firing, which
#         # would end up scrolling the widget twice
#         return "break"

# app=App()
# from tkinter import *

# class MultiListbox(Frame):
#     def __init__(self, master, lists):
#         Frame.__init__(self, master)
#         self.lists = []
#         for l,w in lists:
#             frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
#             Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
#             lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
#                          relief=FLAT, exportselection=FALSE)
#             lb.pack(expand=YES, fill=BOTH)
#             self.lists.append(lb)
#             lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
#             lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
#             lb.bind('<Leave>', lambda e: 'break')
#             lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
#             lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
#         frame = Frame(self); frame.pack(side=LEFT, fill=Y)
#         Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
#         sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
#         sb.pack(expand=YES, fill=Y)
#         self.lists[0]['yscrollcommand']=sb.set

#     def _select(self, y):
#         row = self.lists[0].nearest(y)
#         self.selection_clear(0, END)
#         self.selection_set(row)
#         return 'break'

#     def _button2(self, x, y):
#         for l in self.lists: l.scan_mark(x, y)
#         return 'break'

#     def _b2motion(self, x, y):
#         for l in self.lists: l.scan_dragto(x, y)
#         return 'break'

#     def _scroll(self, *args):
#         for l in self.lists:
#             apply(l.yview, args)

#     def curselection(self):
#         return self.lists[0].curselection(  )

#     def delete(self, first, last=None):
#         for l in self.lists:
#             l.delete(first, last)

#     def get(self, first, last=None):
#         result = []
#         for l in self.lists:
#             result.append(l.get(first,last))
#         if last: return apply(map, [None] + result)
#         return result

#     def index(self, index):
#         self.lists[0].index(index)

#     def insert(self, index, *elements):
#         for e in elements:
#             i = 0
#             for l in self.lists:
#                 l.insert(index, e[i])
#                 i = i + 1

#     def size(self):
#         return self.lists[0].size(  )

#     def see(self, index):
#         for l in self.lists:
#             l.see(index)

#     def selection_anchor(self, index):
#         for l in self.lists:
#             l.selection_anchor(index)

#     def selection_clear(self, first, last=None):
#         for l in self.lists:
#             l.selection_clear(first, last)

#     def selection_includes(self, index):
#         return self.lists[0].selection_includes(index)

#     def selection_set(self, first, last=None):
#         for l in self.lists:
#             l.selection_set(first, last)

# if __name__ == '__main__':
#     tk = Tk(  )
#     Label(tk, text='MultiListbox').pack(  )
#     mlb = MultiListbox(tk, (('Subject', 40), ('Sender', 20), ('Date', 10)))
#     for i in range(1000):
#       mlb.insert(END, 
#           ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
#     mlb.pack(expand=YES,fill=BOTH)
#     tk.mainloop(  )
# Program to explain how to use recycleview in kivy 

# import the kivy module 
# from kivy.app import App 

# The ScrollView widget provides a scrollable view 
# from tkinter import *
# from tkinter import ttk

# master = Tk()

# variable = StringVar(master)
# variable.set("one") # default value

# w = ttk.Combobox(master, textvariable=variable, values=["Carrier 19EX 4667kW/6.16COP/Vanes", "Carrier 19EX 4997kW/6.40COP/Vanes", "Carrier 19EX 5148kW/6.34COP/Vanes", "Carrier 19EX 5208kW/6.88COP/Vanes", "Carrier 19FA 5651kW/5.50COP/Vanes", "Carrier 19XL 1674kW/7.89COP/Vanes", "Carrier 19XL 1779kW/6.18COP/Vanes", "Carrier 19XL 1797kW/5.69COP/Vanes", "Carrier 19XL 1871kW/6.49COP/Vanes", "Carrier 19XL 2057kW/6.05COP/Vanes", "Carrier 19XR 1076kW/5.52COP/Vanes", "Carrier 19XR 1143kW/6.57COP/VSD", "Carrier 19XR 1157kW/5.62COP/VSD", "Carrier 19XR 1196kW/6.50COP/Vanes", "Carrier 19XR 1213kW/7.78COP/Vanes", "Carrier 19XR 1234kW/5.39COP/VSD", "Carrier 19XR 1259kW/6.26COP/Vanes", "Carrier 19XR 1284kW/6.20COP/Vanes", "Carrier 19XR 1294kW/7.61COP/Vanes", "Carrier 19XR 1350kW/7.90COP/VSD", "Carrier 19XR 1403kW/7.09COP/VSD", "Carrier 19XR 1407kW/6.04COP/VSD", "Carrier 19XR 1410kW/8.54COP/VSD", "Carrier 19XR 1558kW/5.81COP/VSD", "Carrier 19XR 1586kW/5.53COP/VSD", "Carrier 19XR 1635kW/6.36COP/Vanes", "Carrier 19XR 1656kW/8.24COP/VSD", "Carrier 19XR 1723kW/8.32COP/VSD", "Carrier 19XR 1727kW/9.04COP/Vanes", "Carrier 19XR 1758kW/5.86COP/VSD", "Carrier 19XR 1776kW/8.00COP/Vanes", "Carrier 19XR 1801kW/6.34COP/VSD", "Carrier 19XR 2391kW/6.44COP/VSD", "Carrier 19XR 2391kW/6.77COP/Vanes", "Carrier 19XR 742kW/5.42COP/VSD", "Carrier 19XR 823kW/6.28COP/Vanes", "Carrier 19XR 869kW/5.57COP/VSD", "Carrier 19XR 897kW/6.23COP/VSD", "Carrier 19XR 897kW/6.50COP/Vanes", "Carrier 19XR 897kW/7.23COP/VSD", "Carrier 23XL 1062kW/5.50COP/Valve", "Carrier 23XL 1108kW/6.92COP/Valve", "Carrier 23XL 1196kW/6.39COP/Valve", "Carrier 23XL 686kW/5.91COP/Valve", "Carrier 23XL 724kW/6.04COP/Vanes", "Carrier 23XL 830kW/6.97COP/Valve", "Carrier 23XL 862kW/6.11COP/Valve", "Carrier 23XL 862kW/6.84COP/Valve", "Carrier 23XL 865kW/6.05COP/Valve", "Carrier 30RB100 336.5kW/2.8COP", "Carrier 30RB110 371kW/2.8COP", "Carrier 30RB120 416.4kW/2.8COP", "Carrier 30RB130 447.7kW/2.8COP", "Carrier 30RB150 507.8kW/2.8COP", "Carrier 30RB160 538kW/2.9COP", "Carrier 30RB170 585.5kW/2.8COP", "Carrier 30RB190 662.9kW/2.8COP", "Carrier 30RB210 710kW/2.9COP", "Carrier 30RB225 753.3kW/2.8COP", "Carrier 30RB250 836.2kW/2.8COP", "Carrier 30RB275 915kW/2.8COP", "Carrier 30RB300 993.8kW/2.8COP", "Carrier 30RB315 1076.1kW/2.9COP", "Carrier 30RB330 1123.6kW/2.8COP", "Carrier 30RB345 1170.7kW/2.8COP", "Carrier 30RB360 1248.4kW/2.8COP", "Carrier 30RB390 1325.8kW/2.8COP", "Carrier 30RB90 303.8kW/2.9COP", "Carrier 30XA100 330.1kW/3.1COP", "Carrier 30XA110 359.9kW/3COP", "Carrier 30XA120 389kW/3COP", "Carrier 30XA140 466.7kW/3.1COP", "Carrier 30XA160 535.1kW/3.1COP", "Carrier 30XA180 601.9kW/3.1COP", "Carrier 30XA200 681.7kW/3.1COP", "Carrier 30XA220 743.7kW/3.1COP", "Carrier 30XA240 801.6kW/3COP", "Carrier 30XA260 881.7kW/3.1COP", "Carrier 30XA280 943.4kW/3.1COP", "Carrier 30XA300 1010.2kW/3.1COP", "Carrier 30XA325 1077.4kW/3.1COP", "Carrier 30XA350 1138.7kW/3COP", "Carrier 30XA400 1348kW/3COP", "Carrier 30XA450 1499.5kW/2.9COP", "Carrier 30XA500 1609.4kW/2.9COP", "Carrier 30XA80 265.5kW/2.9COP", "Carrier 30XA90 297.8kW/3.1COP", "DOE-2 Centrifugal/5.50COP", "DOE-2 Reciprocating/3.67COP", "McQuay AGZ010BS 34.5kW/2.67COP", "McQuay AGZ013BS 47.1kW/2.67COP", "McQuay AGZ017BS 54.5kW/2.67COP", "McQuay AGZ020BS 71kW/2.67COP", "McQuay AGZ025BS 78.1kW/2.67COP", "McQuay AGZ025D 96kW/2.81COP", "McQuay AGZ029BS 95.7kW/2.67COP", "McQuay AGZ030D 111.1kW/2.81COP", "McQuay AGZ034BS 117.1kW/2.61COP", "McQuay AGZ035D 122.7kW/2.93COP", "McQuay AGZ040D 133.3kW/2.96COP", "McQuay AGZ045D 149.8kW/3.02COP", "McQuay AGZ050D 169.2kW/2.96COP", "McQuay AGZ055D 181.5kW/2.93COP", "McQuay AGZ060D 197.3kW/2.87COP", "McQuay AGZ065D 204.3kW/3.02COP", "McQuay AGZ070D 225.4kW/2.84COP", "McQuay AGZ075D 257.1kW/2.93COP", "McQuay AGZ080D 285.2kW/2.87COP", "McQuay AGZ090D 313.7kW/2.87COP", "McQuay AGZ100D 351kW/2.81COP", "McQuay AGZ110D 373.1kW/2.87COP", "McQuay AGZ125D 411.8kW/2.87COP", "McQuay AGZ130D 455.8kW/2.81COP", "McQuay AGZ140D 479kW/2.99COP", "McQuay AGZ160D 539.1kW/2.93COP", "McQuay AGZ180D 605.6kW/2.81COP", "McQuay AGZ190D 633.4kW/2.96COP", "McQuay PEH 1030kW/8.58COP/Vanes", "McQuay PEH 1104kW/8.00COP/Vanes", "McQuay PEH 1231kW/6.18COP/Vanes", "McQuay PEH 1635kW/7.47COP/Vanes", "McQuay PEH 1895kW/6.42COP/Vanes", "McQuay PEH 1934kW/6.01COP/Vanes", "McQuay PEH 703kW/7.03COP/Vanes", "McQuay PEH 819kW/8.11COP/Vanes", "McQuay PFH 1407kW/6.60COP/Vanes", "McQuay PFH 2043kW/8.44COP/Vanes", "McQuay PFH 2124kW/6.03COP/Vanes", "McQuay PFH 2462kW/6.67COP/Vanes", "McQuay PFH 3165kW/6.48COP/Vanes", "McQuay PFH 4020kW/7.35COP/Vanes", "McQuay PFH 932kW/5.09COP/Vanes", "McQuay WDC 1973kW/6.28COP/Vanes", "McQuay WSC 1519kW/7.10COP/Vanes", "McQuay WSC 1751kW/6.73COP/Vanes", "McQuay WSC 471kW/5.89COP/Vanes", "McQuay WSC 816kW/6.74COP/Vanes", "Multistack MS 172kW/3.67COP/None", "Trane CGAM100 337.6kW/3.11COP", "Trane CGAM110 367.2kW/3.02COP"])
# w.pack()

# master.mainloop()
# from tkinter import *
# from tkinter import ttk
# root = Tk()
# string = 'Question #'
# nums = ['1', '2', '3']
# labels=[] #creates an empty list for your labels
# maping = []
# def SUBMIT():
#     print(maping)
    
# for x in nums: #iterates over your nums
#     jk = string + x
#     label = Label(root,text=jk) #set your text
#     variable = StringVar(root)
#     # variable.set("Others") # default value

#     w = ttk.Combobox(root, textvariable=variable, values=["Carrier 19EX 4667kW/6.16COP/Vanes", "Carrier 19EX 4997kW/6.40COP/Vanes", "Carrier 19EX 5148kW/6.34COP/Vanes", "Carrier 19EX 5208kW/6.88COP/Vanes", "Carrier 19FA 5651kW/5.50COP/Vanes", "Carrier 19XL 1674kW/7.89COP/Vanes", "Carrier 19XL 1779kW/6.18COP/Vanes", "Carrier 19XL 1797kW/5.69COP/Vanes", "Carrier 19XL 1871kW/6.49COP/Vanes", "Carrier 19XL 2057kW/6.05COP/Vanes", "Carrier 19XR 1076kW/5.52COP/Vanes", "Carrier 19XR 1143kW/6.57COP/VSD", "Carrier 19XR 1157kW/5.62COP/VSD", "Carrier 19XR 1196kW/6.50COP/Vanes", "Carrier 19XR 1213kW/7.78COP/Vanes", "Carrier 19XR 1234kW/5.39COP/VSD", "Carrier 19XR 1259kW/6.26COP/Vanes", "Carrier 19XR 1284kW/6.20COP/Vanes", "Carrier 19XR 1294kW/7.61COP/Vanes", "Carrier 19XR 1350kW/7.90COP/VSD", "Carrier 19XR 1403kW/7.09COP/VSD", "Carrier 19XR 1407kW/6.04COP/VSD", "Carrier 19XR 1410kW/8.54COP/VSD", "Carrier 19XR 1558kW/5.81COP/VSD", "Carrier 19XR 1586kW/5.53COP/VSD", "Carrier 19XR 1635kW/6.36COP/Vanes", "Carrier 19XR 1656kW/8.24COP/VSD", "Carrier 19XR 1723kW/8.32COP/VSD", "Carrier 19XR 1727kW/9.04COP/Vanes", "Carrier 19XR 1758kW/5.86COP/VSD", "Carrier 19XR 1776kW/8.00COP/Vanes", "Carrier 19XR 1801kW/6.34COP/VSD", "Carrier 19XR 2391kW/6.44COP/VSD", "Carrier 19XR 2391kW/6.77COP/Vanes", "Carrier 19XR 742kW/5.42COP/VSD", "Carrier 19XR 823kW/6.28COP/Vanes", "Carrier 19XR 869kW/5.57COP/VSD", "Carrier 19XR 897kW/6.23COP/VSD", "Carrier 19XR 897kW/6.50COP/Vanes", "Carrier 19XR 897kW/7.23COP/VSD", "Carrier 23XL 1062kW/5.50COP/Valve", "Carrier 23XL 1108kW/6.92COP/Valve", "Carrier 23XL 1196kW/6.39COP/Valve", "Carrier 23XL 686kW/5.91COP/Valve", "Carrier 23XL 724kW/6.04COP/Vanes", "Carrier 23XL 830kW/6.97COP/Valve", "Carrier 23XL 862kW/6.11COP/Valve", "Carrier 23XL 862kW/6.84COP/Valve", "Carrier 23XL 865kW/6.05COP/Valve", "Carrier 30RB100 336.5kW/2.8COP", "Carrier 30RB110 371kW/2.8COP", "Carrier 30RB120 416.4kW/2.8COP", "Carrier 30RB130 447.7kW/2.8COP", "Carrier 30RB150 507.8kW/2.8COP", "Carrier 30RB160 538kW/2.9COP", "Carrier 30RB170 585.5kW/2.8COP", "Carrier 30RB190 662.9kW/2.8COP", "Carrier 30RB210 710kW/2.9COP", "Carrier 30RB225 753.3kW/2.8COP", "Carrier 30RB250 836.2kW/2.8COP", "Carrier 30RB275 915kW/2.8COP", "Carrier 30RB300 993.8kW/2.8COP", "Carrier 30RB315 1076.1kW/2.9COP", "Carrier 30RB330 1123.6kW/2.8COP", "Carrier 30RB345 1170.7kW/2.8COP", "Carrier 30RB360 1248.4kW/2.8COP", "Carrier 30RB390 1325.8kW/2.8COP", "Carrier 30RB90 303.8kW/2.9COP", "Carrier 30XA100 330.1kW/3.1COP", "Carrier 30XA110 359.9kW/3COP", "Carrier 30XA120 389kW/3COP", "Carrier 30XA140 466.7kW/3.1COP", "Carrier 30XA160 535.1kW/3.1COP", "Carrier 30XA180 601.9kW/3.1COP", "Carrier 30XA200 681.7kW/3.1COP", "Carrier 30XA220 743.7kW/3.1COP", "Carrier 30XA240 801.6kW/3COP", "Carrier 30XA260 881.7kW/3.1COP", "Carrier 30XA280 943.4kW/3.1COP", "Carrier 30XA300 1010.2kW/3.1COP", "Carrier 30XA325 1077.4kW/3.1COP", "Carrier 30XA350 1138.7kW/3COP", "Carrier 30XA400 1348kW/3COP", "Carrier 30XA450 1499.5kW/2.9COP", "Carrier 30XA500 1609.4kW/2.9COP", "Carrier 30XA80 265.5kW/2.9COP", "Carrier 30XA90 297.8kW/3.1COP", "DOE-2 Centrifugal/5.50COP", "DOE-2 Reciprocating/3.67COP", "McQuay AGZ010BS 34.5kW/2.67COP", "McQuay AGZ013BS 47.1kW/2.67COP", "McQuay AGZ017BS 54.5kW/2.67COP", "McQuay AGZ020BS 71kW/2.67COP", "McQuay AGZ025BS 78.1kW/2.67COP", "McQuay AGZ025D 96kW/2.81COP", "McQuay AGZ029BS 95.7kW/2.67COP", "McQuay AGZ030D 111.1kW/2.81COP", "McQuay AGZ034BS 117.1kW/2.61COP", "McQuay AGZ035D 122.7kW/2.93COP", "McQuay AGZ040D 133.3kW/2.96COP", "McQuay AGZ045D 149.8kW/3.02COP", "McQuay AGZ050D 169.2kW/2.96COP", "McQuay AGZ055D 181.5kW/2.93COP", "McQuay AGZ060D 197.3kW/2.87COP", "McQuay AGZ065D 204.3kW/3.02COP", "McQuay AGZ070D 225.4kW/2.84COP", "McQuay AGZ075D 257.1kW/2.93COP", "McQuay AGZ080D 285.2kW/2.87COP", "McQuay AGZ090D 313.7kW/2.87COP", "McQuay AGZ100D 351kW/2.81COP", "McQuay AGZ110D 373.1kW/2.87COP", "McQuay AGZ125D 411.8kW/2.87COP", "McQuay AGZ130D 455.8kW/2.81COP", "McQuay AGZ140D 479kW/2.99COP", "McQuay AGZ160D 539.1kW/2.93COP", "McQuay AGZ180D 605.6kW/2.81COP", "McQuay AGZ190D 633.4kW/2.96COP", "McQuay PEH 1030kW/8.58COP/Vanes", "McQuay PEH 1104kW/8.00COP/Vanes", "McQuay PEH 1231kW/6.18COP/Vanes", "McQuay PEH 1635kW/7.47COP/Vanes", "McQuay PEH 1895kW/6.42COP/Vanes", "McQuay PEH 1934kW/6.01COP/Vanes", "McQuay PEH 703kW/7.03COP/Vanes", "McQuay PEH 819kW/8.11COP/Vanes", "McQuay PFH 1407kW/6.60COP/Vanes", "McQuay PFH 2043kW/8.44COP/Vanes", "McQuay PFH 2124kW/6.03COP/Vanes", "McQuay PFH 2462kW/6.67COP/Vanes", "McQuay PFH 3165kW/6.48COP/Vanes", "McQuay PFH 4020kW/7.35COP/Vanes", "McQuay PFH 932kW/5.09COP/Vanes", "McQuay WDC 1973kW/6.28COP/Vanes", "McQuay WSC 1519kW/7.10COP/Vanes", "McQuay WSC 1751kW/6.73COP/Vanes", "McQuay WSC 471kW/5.89COP/Vanes", "McQuay WSC 816kW/6.74COP/Vanes", "Multistack MS 172kW/3.67COP/None", "Trane CGAM100 337.6kW/3.11COP", "Trane CGAM110 367.2kW/3.02COP"])
#     w.pack()
#     label.pack()
#     maping.append(variable.get())
#     labels.append(label)#appends the label to the list for further use
# button =Button(root,text="submit",command=SUBMIT)
# button.pack()

# root.mainloop()

# import tkinter as tk

# def populate(frame):
#     '''Put in some fake data'''
#     for row in range(100):
#         tk.Label(frame, text="%s" % row, width=3, borderwidth="1", 
#                  relief="solid").grid(row=row, column=0)
#         t="this is the second column for row %s" %row
#         tk.Label(frame, text=t).grid(row=row, column=1)

# def onFrameConfigure(canvas):
#     '''Reset the scroll region to encompass the inner frame'''
#     canvas.configure(scrollregion=canvas.bbox("all"))

# root = tk.Tk()
# canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
# frame = tk.Frame(canvas, background="#ffffff")
# vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
# canvas.configure(yscrollcommand=vsb.set)

# vsb.pack(side="right", fill="y")
# canvas.pack(side="left", fill="both", expand=True)
# canvas.create_window((4,4), window=frame, anchor="nw")

# frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

# populate(frame)

# root.mainloop()


# import tkinter as tk

# class Example(tk.Frame):
#     def __init__(self, parent):

#         tk.Frame.__init__(self, parent)
#         self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
#         self.frame = tk.Frame(self.canvas, background="#ffffff")
#         self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.vsb.set)

#         self.vsb.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((4,4), window=self.frame, anchor="nw",
#                                   tags="self.frame")

#         self.frame.bind("<Configure>", self.onFrameConfigure)
#         self.canvas.bind_all("<MouseWheel>",self.on_mouse_wheel)
#         self.populate()
#     def on_mouse_wheel(self,event):
#         self.canvas.yview_scroll(-1*(event.delta/120), "units")
#     def populate(self):
#         '''Put in some fake data'''
#         for row in range(100):
#             tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
#                      relief="solid").grid(row=row, column=0)
#             t="this is the second column for row %s" %row
#             tk.Label(self.frame, text=t).grid(row=row, column=1)

#     def onFrameConfigure(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# if __name__ == "__main__":
#     root=tk.Tk()
#     example = Example(root)
#     example.pack(side="top", fill="both", expand=True)
#     root.mainloop()


'''
Example of  canvas with that can be scrolled with mouse and 
dragged around with middle mouse of the button.
Written and tested using Python 3.4 on Ubuntu x64 14.04
'''

from tkinter import *
import tkinter as tk


class MyCanvas(Canvas):
    
    def __init__(self, parent=None, img=None, *parms, **kparms):
        Canvas.__init__(self, parent, *parms, **kparms)
        
        self._width =  1000;
        self._height = 1000;
         
        self._starting_drag_position = ()

        self.config(width = self._width, height=self._height, bg='green')
        self.frame = Frame(self)
        self.frame.bind("<Configure>",self.configure(scrollregion=self.bbox("all")))
        # self.config(scrollregion=self.bbox("all"))
        self._draw_some_example_objects()
                
        self._add_scrollbars()        
        self._addMouseBindings()
        
        self.pack(fill=BOTH, expand=YES)
        
    def _add_scrollbars(self):
        
        self.sbarV = Scrollbar(self.master, orient=VERTICAL)
        # self.sbarH = Scrollbar(self.master, orient=HORIZONTAL)
        
        self.sbarV.configure(command=self.yview)
        # self.sbarH.config(command=self.xview)
        
        self.configure(yscrollcommand=self.sbarV.set)  
        # self.config(scrollregion=self.bbox("all"))
        # self.config(xscrollcommand=self.sbarH.set)
        
        self.sbarV.pack(side=RIGHT, fill=Y)  
        # self.sbarH.pack(side=BOTTOM, fill=X)


    def _addMouseBindings(self):
    
        # mouse wheel scroll
        self.bind('<4>', lambda event : self.yview('scroll', -1, 'units'))
        self.bind('<5>', lambda event : self.yview('scroll', 1, 'units'))        
        
        # dragging canvas with mouse middle button 
        self.bind("<Button-2>", self.__start_scroll)
        self.bind("<B2-Motion>", self.__update_scroll)
        self.bind("<ButtonRelease-2>", self.__stop_scroll)

      
    def __start_scroll(self, event):
        
        # set the scrolling increment. 
        # value of 0 is unlimited and very fast
        # set it to 1,2,3 or whatever to make it slower
        self.configure(yscrollincrement=3) 
        self.config(xscrollincrement=3) 
       
        self._starting_drag_position = (event.x, event.y)
        
        self.config(cursor="fleur")
    
        
    def __update_scroll(self, event):
       
        deltaX = event.x - self._starting_drag_position[0]
        deltaY = event.y - self._starting_drag_position[1]
       
        
        self.xview('scroll', deltaX, 'units')
        self.yview('scroll', deltaY, 'units')
      
            
        self._starting_drag_position =  (event.x, event.y)
        
        
        
    def __stop_scroll(self, event):
        
        # set scrolling speed back to 0, so that mouse scrolling 
        # works as expected.
        self.config(xscrollincrement=0) 
        self.config(yscrollincrement=0)
        
        self.config(cursor="")

        
    def _draw_some_example_objects(self):
        
        # colors = dict(outline="black")
        labels = [Label(self.frame, text=str(i)) for i in range(0,100)]
        for l in labels:
            l.pack(side="bottom",expand="True")
        
        # for i in range(0,10):
        #     label = Label(self,text=i)
        #     label.pack()
        self.create_window((0,0),window=self.frame)
        # self.config(scrollregion=(0,0, self._width, self._height))  
        # self.config(scrollregion=self.bbox("all"))
        #     tk.Label(self.config,text=i)
        
        # self.create_rectangle(30, 10, 120, 120, fill="red", **colors)        
        # self.create_rectangle(330, 410, 420, 460, fill="blue", **colors)
        # self.create_rectangle(830, 810, 920, 960, fill="yellow", **colors)
        # self.create_rectangle(830, 210, 990, 500, fill="cyan", **colors)
        # self.create_rectangle(130, 810, 290, 999, fill="gray", **colors)
                
      

class MyGUI(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Drag canvas with mouse")
        self.geometry("500x500")
        
        self._addWidgets()
    
    def _addWidgets(self):
        MyCanvas(self)
                    
        
    
        
if __name__ == '__main__':
    
    MyGUI().mainloop()      

# import tkinter as tk
# from tkinter import ttk
# from tkinter import *

# root = tk.Tk()
# root.grid_rowconfigure(0, weight=1)
# root.columnconfigure(0, weight=1)

# frame_main = tk.Frame(root, bg="gray")
# frame_main.grid(sticky='news')

# label1 = tk.Label(frame_main, text="Label 1", fg="green")
# label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

# label2 = tk.Label(frame_main, text="Label 2", fg="blue")
# label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')

# label3 = tk.Label(frame_main, text="Label 3", fg="red")
# label3.grid(row=3, column=0, pady=5, sticky='nw')

# # Create a frame for the canvas with non-zero row&column weights
# frame_canvas = tk.Frame(frame_main)
# frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
# frame_canvas.grid_rowconfigure(0, weight=1)
# frame_canvas.grid_columnconfigure(0, weight=1)
# # Set grid_propagate to False to allow 5-by-5 buttons resizing later
# frame_canvas.grid_propagate(False)

# # Add a canvas in that frame
# canvas = tk.Canvas(frame_canvas, bg="yellow")
# canvas.grid(row=0, column=0, sticky="news")

# # Link a scrollbar to the canvas
# vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
# vsb.grid(row=0, column=1, sticky='ns')
# canvas.configure(yscrollcommand=vsb.set)

# # Create a frame to contain the buttons
# # frame_buttons = tk.Frame(canvas, bg="blue")
# label_frame = tk.Label(canvas)
# canvas.create_window((0, 0), window=label_frame, anchor='nw')

# # Add 9-by-5 buttons to the frame
# rows = 9
# columns = 2
# values=['1','2','3','4','5','6']
# for i in range(0,rows):
#     for j in range(0,columns):
#         frame_buttons = tk.Label(label_frame,text=i)
#         frame_buttons.grid(row=i,column=j)
# # buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
# # buttons = [[ttk.Combobox() for j in range(columns)] for i in range(rows)]
# # for i in range(0, rows):
# #     for j in range(0, columns):
# #         if j == 1:
# #             buttons[i][j] = ttk.Combobox(root,*values)
# #         elif j==0:
# #             buttons[i][j] = tk.Label(root,text="MY text")
# #         # buttons[i][j] = tk.Button(frame_buttons, text=("%d,%d" % (i+1, j+1)))
# #         buttons[i][j].grid(row=i, column=j, sticky='news')

# # # Update buttons frames idle tasks to let tkinter calculate buttons sizes
# frame_buttons.update_idletasks()

# # # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
# # first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 2)])
# # first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 2)])
# # frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
# #                     height=first5rows_height)

# # Set the canvas scrolling region
# canvas.config(scrollregion=canvas.bbox("all"))

# # Launch the GUI
# root.mainloop()