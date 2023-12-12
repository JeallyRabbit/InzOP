import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import dimensions as DIMENSIONS
def get_trainings():
    users=[]
    file=open("accounts.pydb","r")
    for line in file:
        r=line.replace("\n","").split("~")
        users.append(user(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]))
    file.close()

    return users

def add_user():

    def can_you_add_it_finally():
        current_db=[]
        file = open("accounts.pydb",'r')
        for line in file:
            current_db.append(line.split("~"))
        file.close()
        id=int(current_db[-1][0])+1
        current_db.clear()

        login = labels[0].get()
        name = labels[1].get()
        surname = labels[2].get()
        mail = labels[3].get()
        number = labels[4].get()
        password = labels[5].get()
        type = labels[6].get()
        _for = labels[7].get()

        line = str(id)+"~"+login+"~"+name+"~"+surname+"~"+mail+"~"+number+"~"+password+"~"+type+"~"+_for+"\n"
        #(self,id,login,name,surname,mail,number,password,type):
        #current_db.append(training(name,descripton,agenda,data,coach,products,type,_for))

        file = open("accounts.pydb",'a')
        file.write(line)
        file.close()
        labels.clear()
        root.destroy()


    def leave():
        labels.clear()
        root.destroy()

    labels=[]

    root = tk.Tk()
    root.title("Training System - Add User")
    root.geometry("1000x800")

    #Teksty

    labels.append(tk.Label(root,text="Login"))
    labels[0].grid(row=0,column=0)

    labels.append(tk.Label(root,text="Name"))
    labels[1].grid(row=1,column=0)

    labels.append(tk.Label(root,text="Surname"))
    labels[2].grid(row=2,column=0)

    labels.append(tk.Label(root,text="Mail"))
    labels[3].grid(row=3,column=0)

    labels.append(tk.Label(root,text="Phone Number"))
    labels[4].grid(row=4,column=0)

    labels.append(tk.Label(root,text="Password"))
    labels[5].grid(row=5,column=0)

    labels.append(tk.Label(root,text="Type"))
    labels[6].grid(row=6,column=0)

    #Inserty
    labels.append(tk.Entry(root,width=150))
    labels[7].grid(row=0,column=1)

    labels.append(tk.Entry(root, width=150))
    labels[8].grid(row=1,column=1)

    labels.append(tk.Entry(root, width=150))
    labels[9].grid(row=2,column=1)

    labels.append(tk.Entry(root, width=150))
    labels[10].grid(row=3, column=1)

    labels.append(tk.Entry(root, width=150))
    labels[11].grid(row=4, column=1)

    labels.append(tk.Entry(root, width=150))
    labels[12].grid(row=5, column=1)

    labels.append(tk.Entry(root, width=150))
    labels[13].grid(row=6, column=1)



    #Listy
    """
    labels.append(ttk.Combobox(root))
    labels[11].grid(row=4,column=1)

    labels.append(ttk.Combobox(root))
    labels[12].grid(row=5,column=1)
    labels[12]['values']=DIMENSIONS.get_current_dimensions_by_type("Produkty")

    labels.append(ttk.Combobox(root))
    labels[13].grid(row=6,column=1)
    labels[13]['values'] = DIMENSIONS.get_current_dimensions_by_type("Rodzaj")

    labels.append(ttk.Combobox(root))
    labels[14].grid(row=7,column=1)
    labels[14]['values'] = DIMENSIONS.get_current_dimensions_by_type("klienta")
    """

    #Przyciski

    labels.append(tk.Button(root,text="Dodaj user'a",command=can_you_add_it_finally))
    labels[14].grid(row=8,column=1)

    labels.append(tk.Button(root,text="Anuluj",command=leave))
    labels[15].grid(row=8,column=0)


    root.mainloop()

class user():
    def __init__(self,id,login,name,surname,mail,number,password,type):
        self.id=id
        self.login=login
        self.name=name
        self.surname=surname
        self.mail=mail
        self.number=number
        self.password=password
        self.type=type