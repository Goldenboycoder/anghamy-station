import tkinter as tk
import threading
import time
class Gui:
    frt='sadas'
    GuiElements={}
    label1str=''
    def __init__(self,name): 
        self.name = name  
    def initGui(self):
        Gui.frt="aaaa"
        window = tk.Tk()
        window.title(self.name)
        label1str=tk.StringVar()
        frame1 = tk.Frame(master=window, width=500, height=900, bg="purple")
        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        Gui.GuiElements['window']=window
        Gui.GuiElements['side_frame']=frame1

        frame2 = tk.Frame(master=window, width=300, bg="whitesmoke")
        frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        Gui.GuiElements['chat_frame']=frame2

        label1 = tk.Label(
            #text="Hello, Tkinter",
            fg="white",
            bg="black",
            width=30,
            height=2,
            master=frame1)
        label1.pack(side=tk.TOP)
        
        label1['textvariable']=label1str
        Gui.GuiElements['side_top_label']=[label1,label1str]
        def setLabel1(string):
            label1str.set(string)
  
        text_box=tk.Text(bg="whitesmoke",master=frame2,state='disabled')
        text_box.pack(side=tk.TOP)
        s = tk.Scrollbar(orient='ver',command=text_box.yview)
        text_box.configure(yscrollcommand=s.set)
        Gui.GuiElements['chat_box']=text_box

        def addtotext():
            tex=entry.get()
            text_box.configure(state='normal')
            text_box.insert(tk.END, tex+"\n")
            text_box.configure(state='disabled')
            entry.delete(0,tk.END)

        sbutton=tk.Button(
            text="SEND",
            width=10,
            height=1,
            bg="#FF1493",
            fg="white",
            font=('Arial Black',9,'bold'),
            command=addtotext,
            master=frame2)
        sbutton.pack(side=tk.RIGHT)
        Gui.GuiElements['send_button']=sbutton

        entry=tk.Entry(
            fg='yellow',
            bg='blue',
            width=92,
            state='readonly',#this will be enabled once user provide info
            master=frame2
        )
        entry.pack(fill=tk.X,side=tk.LEFT)
        
        #add to frame1 
        frame3 = tk.Frame(master=frame1, width=500, height=900, bg="dodgerblue")
        frame3.pack(side=tk.TOP, expand=False)
        Gui.GuiElements['side_frame_sub_cred']=frame3

        label_userid = tk.Label(
            #text="Hello, Tkinter",
            fg="white",
            bg="fuchsia",
            text="user Id ",
            width=15,
            height=1,
            font=('Courier New',10,'bold'),
            master=frame3)
        label_userid.grid(row=0,column=0)
        Gui.GuiElements['side_frame_sub_cred_luid']=label_userid
        e_userid=tk.Entry(
            fg='black',
            bg='white',
            width=15,
            master=frame3
        )
        e_userid.grid(row=0,column=1)
        Gui.GuiElements['side_frame_sub_cred_uid']=e_userid

        label_serverip = tk.Label(
            #text="Hello, Tkinter",
            fg="white",
            bg="fuchsia",
            text="server Ip",
            width=15,
            height=1,
            font=('Courier New',10,'bold'),
            master=frame3)
        label_serverip.grid(row=1,column=0)
        Gui.GuiElements['side_frame_sub_cred_lsip']=label_serverip
        e_serverip=tk.Entry(
            fg='black',
            bg='white',
            width=15,
            master=frame3
        )
        e_serverip.grid(row=1,column=1)
        Gui.GuiElements['side_frame_sub_cred_sip']=e_serverip

        def uiddone():
            e_userid.configure(state='readonly')
            e_serverip.configure(state='readonly')
            cbutton.configure(state='disabled')

        cbutton=tk.Button(
            text="Connect",
            width=15,
            height=2,
            bg="#FF1493",
            fg="white",
            command=uiddone,
            master=frame1)
        cbutton.pack(side=tk.TOP)
        Gui.GuiElements['connect_button']=cbutton

        def handle_keypress(event):
            """Print the character associated to the key pressed"""
            if event.char=='\r':
                #send message
                setLabel1("you plessed enter") 
                addtotext()
                

        # Bind keypress event to handle_keypress()
        entry.bind("<Key>", handle_keypress)
        Gui.GuiElements['input_box']=entry
        window.mainloop()

    def setLabel1(self,string):
        Gui.GuiElements['side_top_label'][1].set(string)
    def addtobox(self,text):
            tbox=Gui.GuiElements['chat_box']
            tbox.configure(state='normal')
            tbox.insert(tk.END, text+"\n")
            tbox.configure(state='disabled')



