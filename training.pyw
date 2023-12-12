import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import dimensions as DIMENSIONS

def get_trainings():
    trainings=[]
    file=open("trainings.pydb","r")
    for line in file:
        r=line.replace("\n","").split("~")
        trainings.append(training(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]))
    file.close()

    return trainings

def add_training():

    def can_you_add_it_finally():
        current_db=[]
        file = open("trainings.pydb",'r')
        for line in file:
            current_db.append(line.split("~"))
        file.close()
        id=int(current_db[-1][0])+1
        current_db.clear()

        name = labels[8].get()
        descripton = labels[9].get()
        agenda = labels[10].get()
        data = labels[11].get()
        coach = labels[12].get()
        products = labels[13].get()
        type = labels[14].get()
        _for = labels[15].get()

        line = str(id)+"~"+name+"~"+descripton+"~"+agenda+"~"+str(data)+"~"+coach+"~"+products+"~"+type+"~"+_for+"\n"

        #current_db.append(training(name,descripton,agenda,data,coach,products,type,_for))

        file = open("trainings.pydb",'a')
        file.write(line)
        file.close()
        labels.clear()
        root.destroy()


    def leave():
        labels.clear()
        root.destroy()

    labels=[]

    root = tk.Tk()
    root.title("Training System - Add Training")
    root.geometry("1000x800")

    #Teksty
    labels.append(tk.Label(root,text="Nazwa szkolenia"))
    labels[0].grid(row=0,column=0)

    labels.append(tk.Label(root,text="Opis szkolenia"))
    labels[1].grid(row=1,column=0)

    labels.append(tk.Label(root,text="Agenda skolenia"))
    labels[2].grid(row=2,column=0)

    labels.append(tk.Label(root,text="Data szkolenia"))
    labels[3].grid(row=3,column=0)

    labels.append(tk.Label(root,text="Trener"))
    labels[4].grid(row=4,column=0)

    labels.append(tk.Label(root,text="Produkty"))
    labels[5].grid(row=5,column=0)

    labels.append(tk.Label(root,text="Rodzaj szkolenia"))
    labels[6].grid(row=6,column=0)

    labels.append(tk.Label(root,text="Dla kogo"))
    labels[7].grid(row=7,column=0)

    #Inserty
    labels.append(tk.Entry(root,width=150))
    labels[8].grid(row=0,column=1)

    labels.append(tk.Entry(root, width=150))
    labels[9].grid(row=1,column=1)

    labels.append(tk.Entry(root, width=150))
    labels[10].grid(row=2,column=1)

    #Kalendarz

    labels.append(DateEntry(root))
    labels[11].grid(row=3,column=1)

    #Listy

    labels.append(ttk.Combobox(root))
    labels[12].grid(row=4,column=1)

    labels.append(ttk.Combobox(root))
    labels[13].grid(row=5,column=1)
    labels[13]['values']=DIMENSIONS.get_current_dimensions_by_type("Produkty")

    labels.append(ttk.Combobox(root))
    labels[14].grid(row=6,column=1)
    labels[14]['values'] = DIMENSIONS.get_current_dimensions_by_type("Rodzaj")

    labels.append(ttk.Combobox(root))
    labels[15].grid(row=7,column=1)
    labels[15]['values'] = DIMENSIONS.get_current_dimensions_by_type("klienta")

    #Przyciski

    labels.append(tk.Button(root,text="Dodaj szkolenie",command=can_you_add_it_finally))
    labels[16].grid(row=8,column=1)

    labels.append(tk.Button(root,text="Anuluj",command=leave))
    labels[17].grid(row=8,column=0)


    root.mainloop()

class training():
    def __init__(self,id,name,description,agenda,date,coach,products,type,_for):
        self.id=id
        self.name=name
        self.description=description
        self.agenda=agenda
        self.date=date
        self.coach=coach
        self.products=products
        self.type=type
        self._for=_for
