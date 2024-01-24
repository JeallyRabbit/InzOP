import tkinter as tk
from tkinter import ttk, messagebox
from global_functions import on_click
import user as USER
import training as TRAINING
import dimensions as DIMENSIONS
import certificate as CERTIFICATE
import Survey as SURVEY


def get_user_type(username):
    with open("accounts.pydb", "r") as file:
        for line in file:
            fields = line.strip().split("~")
            if len(fields) >= 7 and fields[1] == username:
                return fields[6]  # Typ użytkownika jest na 7. pozycji
    return None
def edit_training():
    def close_selected_training():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Błąd", "Proszę wybrać szkolenie do zamknięcia.")
            return

        # Pobierz informacje o wybranym szkoleniu z drzewa (przykład)
        selected_training_id = tree.item(selected_item, "values")[0]
        selected_training_name = tree.item(selected_item, "values")[1]

         # Tutaj umieść kod, który zamknie szkolenie
        delete_training_from_database(selected_training_id)
            
        # Usuń zaznaczone szkolenie z drzewa
        tree.delete(selected_item)
        messagebox.showinfo("Zamknięcie szkolenia", f"Zamykasz szkolenie o ID {selected_training_id} - {selected_training_name}")

        username = "jgoslinski"
        user_type = get_user_type(username)
        if user_type == 'Prowadzacy':
            
            # Komunikat potwierdzający zamknięcie
            messagebox.showinfo("Szkolenie zamknięte", "Szkolenie zostało zamknięte.")
            survey(selected_training_name)

           

    # Utwórz okno do wybierania szkolenia
    edit_window = tk.Toplevel()
    edit_window.title("Edytuj szkolenie")

    # Dodaj drzewo do okna, aby wyświetlić listę szkoleń
    tree = ttk.Treeview(edit_window, columns=('ID', 'Nazwa', 'Uczestnicy', 'Koszt', 'Data'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nazwa', text='Nazwa')
    tree.heading('Uczestnicy', text='Liczba uczestników')
    tree.heading('Koszt', text='Cena')
    tree.heading('Data', text='Data')
    tree.pack()

    trainings=TRAINING.get_trainings()
    for row in trainings:
        tree.insert("",'end',iid=int(row.id),values=(row.id,row.name,"","",row.date))

    # Dodaj przycisk do zamknięcia wybranego szkolenia
    close_button = tk.Button(edit_window, text="Zamknij szkolenie", command=close_selected_training)
    close_button.pack()




def delete_training_from_database(training_id):
    try:
        # Pobierz listę szkoleń
        trainings_list = TRAINING.get_trainings()

        matching_trainings = [training for training in trainings_list if training.id == training_id]
        if matching_trainings:
            # Pobierz informacje o pierwszym pasującym szkoleniu
            deleted_training = matching_trainings[0]   
            # Zapisz zmiany w pliku
            trainings_list.remove(deleted_training)
            save_trainings_to_file(trainings_list)
            print(f"Usuwanie szkolenia: {deleted_training.name}")

            
            certificate( deleted_training.name)
            survey(deleted_training.name)



            return True  # Jeśli usunięto pomyślnie
        else:
            print("Nie znaleziono szkolenia o podanym ID.")
            return False  # Jeśli nie znaleziono szkolenia o podanym ID

    except Exception as e:
        print(f"Błąd podczas usuwania szkolenia: {e}")
        return False  # Jeśli wystąpił błąd podczas usuwania szkolenia

def save_trainings_to_file(trainings_list):
    with open("trainings.pydb", "w") as file:
        for training in trainings_list:
            file.write(f"{training.id}~{training.name}~{training.description}~{training.agenda}~{training.date}~{training.coach}~{training.products}~{training.type}~{training._for}\n")

def certificate(training_name):
    # Tutaj umieść logikę tworzenia certyfikatu
    CERTIFICATE.generate_certificate(training_name)

def survey(training_name):
    SURVEY.show_survey_dialog(training_name)