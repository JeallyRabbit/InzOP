import tkinter as tk
from tkinter import ttk, messagebox
from global_functions import on_click
import user as USER
import training as TRAINING
import dimensions as DIMENSIONS
import edit_training as EDIT
import participant as PART
#globalne
root=0

def main_menu(usr):


    labels=[]
    root=tk.Tk()

    root.title("Training System - Main Menu")
    root.geometry("1000x800")

    #Tabela
    columns=['id','nazwa','uczestnicy','koszt','data']
    labels.append(ttk.Treeview(root,columns=columns,show='headings'))
    labels[0].heading('id',text='ID')
    labels[0].heading('nazwa',text='Nazwa')
    labels[0].heading('uczestnicy',text='Liczba uczestników')
    labels[0].heading('koszt',text='Cena')
    labels[0].heading('data',text='Data')
    labels[0].grid(row=0,column=0)
    trainings=TRAINING.get_trainings()
    for row in trainings:
        labels[0].insert("",'end',iid=int(row.id),values=(row.id,row.name,"","",row.date))

    #Teksty
    labels.append(tk.Label(root,text="Opis"))
    labels[1].place(x=200,y=250)

    labels.append(tk.Label(root,text="Agenda"))
    labels[2].place(x=750,y=250) 

    #Opis i agenda
    labels.append(tk.Entry(root,state='disabled',width=80))
    labels[3].place(x=2,y=300,height=300)

    labels.append(tk.Entry(root,state='disabled',width=80))
    labels[4].place(x=515,y=300,height=300)

    #Przyciski
    if(usr.type=='Uczestnik' or usr.type=='Przedstawiciel' or usr.type=='Prowadzacy'):
        labels.append(tk.Button(root, text=""))
        labels[5].place(x=2, y=620, width=200, height=100)
        labels.append(tk.Button(root,text=""))
        labels[6].place(x=202,y=620,width=200,height=100)
    else:
        labels.append(tk.Button(root, text="Dodaj szkolenie", command=TRAINING.add_training))
        labels[5].place(x=2, y=620, width=200, height=100)
        labels.append(tk.Button(root, text="Dodaj użytkownika", command=USER.add_user))
        labels[6].place(x=202, y=620, width=200, height=100)
    if(usr.type == 'Prowadzacy' or usr.type=='admin'):
        labels.append(tk.Button(root,text="Zobacz listę uczestników", command=PART.add_participant_to_training))
        labels[7].place(x=402,y=620,width=200,height=100)
    else:
        labels.append(tk.Button(root, text=""))
        labels[7].place(x=402, y=620, width=200, height=100)
  
    if(usr.type=='admin'):
        labels.append(tk.Button(root, text="Edytuj wymiary", command=DIMENSIONS.add_dimension))
        labels[8].place(x=602, y=620, width=200, height=100)
    else:
        labels.append(tk.Button(root, text=""))
        labels[8].place(x=602, y=620, width=200, height=100)

    if(usr.type=='admin' or usr.type=='Prowadzacy'):
        labels.append(tk.Button(root, text="Edytuj szkolenie", command=EDIT.edit_training))
        labels[9].place(x=802, y=620, width=200, height=100)
    else:
        labels.append(tk.Button(root, text=""))
        labels[9].place(x=802, y=620, width=200, height=100)
    
    

    if(usr.type=='Uczestnik'):
        labels[5].text="asd"
        print(usr.type)

    root.mainloop()

def login():

    def authenticate():
        users=[]
        accounts=open("accounts.pydb",'r')
        for line in accounts:
            temp=line.replace("\n","").split("~")
            users.append(USER.user(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7]))
        accounts.close()

        userLogin=labels[2].get()
        userPassword=labels[3].get()
        flag=True
        signed_as=0

        for i in users:
            if(userLogin==i.login):
                flag=False
                if(userPassword==i.password):
                    login_root.destroy()
                    signed_as=i
                    break
                else:
                    on_click("Błąd logowania","Błędne hasło")

        if(flag):
            on_click("Błąd logowania","Brak użytkownika w bazie")
        else:
            users.clear()
            del(userLogin)
            del(userPassword)
            del(flag)
            return main_menu(signed_as)


    labels=[] #tablica przechowująca wszysktie zawartości okna
    login_root = tk.Tk()

    login_root.title("Training System - Login")
    login_root.geometry("400x300")

    #Napisy
    labels.append(tk.Label(login_root,text="Nazwa użytkownika", width=20,height=5))
    labels[0].grid(row=0,column=0)

    labels.append(tk.Label(login_root,text="Hasło", width=20,height=5))
    labels[1].grid(row=1,column=0)

    #Wejścia tekstu
    labels.append(tk.Entry(login_root,width=40))
    labels[2].grid(row=0,column=1)
    labels[2].insert(0,"admin")

    labels.append(tk.Entry(login_root,width=40,show="*"))
    labels[3].grid(row=1,column=1)
    labels[3].insert(0,"admin")

    #Przyciski
    labels.append(tk.Button(login_root,width=30,height=3,text="Zaloguj się",command=authenticate))
    labels[4].grid(row=2,column=1)

    labels.append(tk.Button(login_root,width=30,height=3, text="Przejrzyj dostępne szkolenia"))
    labels[5].grid(row=3,column=1)

   
    login_root.mainloop()

def main():

    login()


main()