import tkinter as tk
from tkinter import ttk



def get_current_dimensions():
    current_dimensions = []

    file = open("dimensions.pydb","r")

    for line in file:
        current_dimensions.append(dimension(line.split("~")[0],line.split("~")[1],line.split("~")[2]))

    file.close()

    return current_dimensions

def get_current_dimensions_by_type(type):
    current_dimensions=get_current_dimensions()
    typeDimension=[]

    for dim in current_dimensions:
        print(type)
        print(dim.name)
        if(type in dim.type):
            typeDimension.append(dim.name.replace("\n",""))


    return typeDimension



def get_current_dimensions_to_string():
    current_dimensions = []

    file = open("dimensions.pydb", "r")

    for line in file:
        current_dimensions.append(line.replace("~"," "))

    file.close()

    return current_dimensions

def add_dimension():

    def add_dimension_finally():
        current_dimensions=get_current_dimensions()
        if(len(current_dimensions)!=0):
            id=str(int(current_dimensions[-1].id)+1)
        else:
            id="0"

        type=labels[2].get()
        name=labels[3].get()

        current_dimensions.append(dimension(id,type,name))

        file=open("dimensions.pydb","w")
        file.truncate(0)
        for line in current_dimensions:
            file.write(line.id+"~"+line.type+"~"+line.name.replace("\n","")+"\n")
        file.close()

    def del_dimension():
        dim=labels[4].get().replace("\n","").split(" ")

        current_dimensions=get_current_dimensions()

        for i in range(0,len(current_dimensions)):
            if dim[0]==current_dimensions[i].id:
                del(current_dimensions[i])
                break

        file=open("dimensions.pydb","w")
        file.truncate(0)
        for line in current_dimensions:
            file.write(line.id+"~"+line.type+"~"+line.name.replace("\n","")+"\n")
        file.close()



    labels=[]
    types=['Produkty','Rodzaj szkolenia','Typ klienta','Typ użytkownika']

    root = tk.Tk()
    root.title("Training System - Add Dimension")
    root.geometry("300x200")

    labels.append(tk.Label(root, text="Typ wymiaru"))
    labels[0].grid(row=0,column=0)

    labels.append(tk.Label(root, text="Nazwa wymiaru"))
    labels[1].grid(row=1,column=0)

    labels.append(ttk.Combobox(root))
    labels[2].grid(row=0,column=1)
    labels[2]['values'] = types

    labels.append(tk.Entry(root))
    labels[3].grid(row=1,column=1)

    labels.append(ttk.Combobox(root))
    labels[4].grid(row=3,column=0)
    labels[4]['values']=get_current_dimensions_to_string()

    labels.append(tk.Button(root,text="Dodaj",command=add_dimension_finally))
    labels[5].grid(row=2,column=1)

    labels.append(tk.Button(root,text="Usuń",command=del_dimension))
    labels[6].grid(row=3,column=1)



    root.mainloop()

class dimension:
    def __init__(self,id,type,name):
        self.id=id
        self.type=type
        self.name=name