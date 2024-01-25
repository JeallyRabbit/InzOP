import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from global_functions import on_click
import user as USER
import training as TRAINING
import participant as PARTICIPANT
import dimensions as DIMENSIONS
import certificate as CERTIFICATE
import Survey as SURVEY
import shutil
import os

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

    def edit_selected_training():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Błąd", "Proszę wybrać szkolenie do edycji.")
            return

        # Pobierz informacje o wybranym szkoleniu z drzewa (przykład)
        selected_training_id = tree.item(selected_item, "values")[0]
        selected_training_name = tree.item(selected_item, "values")[1]

        # Tutaj umieść kod, który edytuje szkolenie
        edit_this_training(selected_training_id)

        username = "jgoslinski"
        user_type = get_user_type(username)
        if user_type == 'Prowadzacy':
            # Komunikat potwierdzający edycje
            messagebox.showinfo("Szkolenie zedytowane", "Szkolenie zostało zedytowane.")
           

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

    # Dodaj przycisk do edycji wybranego szkolenia
    close_button = tk.Button(edit_window, text="Edytuj szkolenie", command=edit_selected_training)
    close_button.pack()

    # Dodaj przycisk do zamknięcia wybranego szkolenia
    close_button = tk.Button(edit_window, text="Zamknij szkolenie", command=close_selected_training)
    close_button.pack()

def delete_training_from_database(training_id):
    try:
        # Pobierz listę szkoleń
        trainings_list = TRAINING.get_trainings()
        completed_trainings_list = TRAINING.get_trainings()

        matching_trainings = [training for training in trainings_list if training.id == training_id]
        if matching_trainings:
            # Pobierz informacje o pierwszym pasującym szkoleniu
            deleted_training = matching_trainings[0]   
            # Zapisz zmiany w pliku
            completed_trainings_list.append(deleted_training)
            trainings_list.remove(deleted_training)
            save_trainings_to_file(trainings_list)
            save_completed_trainings_to_file([completed_trainings_list[-1]])
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

def save_completed_trainings_to_file(completed_trainings_list):
    with open("trainings_completed.pydb", "a") as file:
        for training in completed_trainings_list:
            file.write(f"{training.id}~{training.name}~{training.description}~{training.agenda}~{training.date}~{training.coach}~{training.products}~{training.type}~{training._for}\n")

def edit_this_training(training_id):
    # Utwórz okno do wybierania szkolenia
    edit_window = tk.Toplevel()
    edit_window.title("Edytuj szkolenie")

    # Dodaj drzewo do okna, aby wyświetlić listę szkoleń
    tree = ttk.Treeview(edit_window, columns=('ID', 'Nazwa', 'Opis', 'Agenda'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nazwa', text='Nazwa')
    tree.heading('Opis', text='Opis')
    tree.heading('Agenda', text='Agenda')
    tree.pack()

    refresh_data(tree, training_id)

    close_button = tk.Button(edit_window, text="Zmień opis", command=lambda: edit_description(training_id))
    close_button.pack()

    close_button = tk.Button(edit_window, text="Odśwież", command=lambda: refresh_data(tree, training_id))
    close_button.pack()

    close_button = tk.Button(edit_window, text="Dodaj materiały", command=lambda: add_material(training_id))
    close_button.pack()

def certificate(training_name):
    # Tutaj umieść logikę tworzenia certyfikatu
    CERTIFICATE.generate_certificate(training_name)

def survey(training_name):
    SURVEY.show_survey_dialog(training_name)

def refresh_data(tree, training_id):
    for item in tree.get_children():
        tree.delete(item)

    trainings = TRAINING.get_trainings()
    for row in trainings:
        if (training_id == row.id):
            tree.insert("", 'end', iid=int(row.id), values=(row.id, row.name, row.description, row.agenda))

def edit_description(training_id):
    edit_window = tk.Toplevel()
    edit_window.title("Edytuj opis")
    edit_window.geometry("400x200")

    current_description = ""
    current_agenda = ""

    trainings = TRAINING.get_trainings()
    for row in trainings:
        if (row.id == training_id):
            current_description = row.description
            current_agenda = row.agenda

    label_description = tk.Label(edit_window, text="Opis:")
    label_description.pack()
    description_entry = tk.Entry(edit_window, width=150)
    description_entry.pack()
    description_entry.insert(0, current_description)

    label_agenda = tk.Label(edit_window, text="Agenda:")
    label_agenda.pack()
    agenda_entry = tk.Entry(edit_window, width=150)
    agenda_entry.pack()
    agenda_entry.insert(0, current_agenda)

    confirm_button = tk.Button(edit_window, text="Zatwierdź", command=lambda: confirm_edit(training_id, description_entry.get(), agenda_entry.get(), edit_window))
    confirm_button.pack()

def confirm_edit(training_id, new_description, new_agenda, edit_window):
    trainings = TRAINING.get_trainings()
    for row in trainings:
        if (row.id == training_id):
            row.description = new_description
            row.agenda = new_agenda
    save_trainings_to_file(trainings)
    edit_window.destroy()

def add_material(training_id):
    file_path = filedialog.askopenfilename(title="Wybierz plik")
    if file_path:
        destination_folder = os.path.join("materials", str(training_id))
        os.makedirs(destination_folder, exist_ok=True)
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("Informacja", f"Pomyślnie dodano materiał do szkolenia {training_id}: {file_path}")

def user_panel():
    def download_selected_materials():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Błąd", "Proszę wybrać szkolenie.")
            return

        selected_training_id = tree.item(selected_item, "values")[0]
        download_materials(selected_training_id)

    def download_selected_certificate():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Błąd", "Proszę wybrać szkolenie.")
            return

        selected_training_id = tree.item(selected_item, "values")[0]
        download_certificate(selected_training_id)

    # Utwórz okno do wybierania szkolenia
    edit_window = tk.Toplevel()
    edit_window.title("Przegląd szkoleń")

    # Dodaj drzewo do okna, aby wyświetlić listę szkoleń
    tree = ttk.Treeview(edit_window, columns=('ID', 'Nazwa', 'Uczestnicy', 'Koszt', 'Data'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nazwa', text='Nazwa')
    tree.heading('Uczestnicy', text='Liczba uczestników')
    tree.heading('Koszt', text='Cena')
    tree.heading('Data', text='Data')
    tree.pack()

    trainings = TRAINING.get_trainings()
    for row in trainings:
        tree.insert("", 'end', iid=int(row.id), values=(row.id, row.name, "", "", row.date))

    close_button = tk.Button(edit_window, text="Pobierz materiały", command=download_selected_materials)
    close_button.pack()

    close_button = tk.Button(edit_window, text="Pobierz certyfikat", command=download_selected_certificate)
    close_button.pack()

def download_materials(training_id):
    materials_directory = os.path.join(os.getcwd(), "materials")
    training_directory = os.path.join(materials_directory, str(training_id))
    for folder in [materials_directory, training_directory]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    file_path = filedialog.askopenfilename(title="Wybierz plik", initialdir=training_directory)
    if file_path:
        destination_folder = "downloaded"
        if not os.path.exists(destination_folder) or not os.path.isdir(destination_folder):
            os.makedirs(destination_folder, exist_ok=True)
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("Informacja", f"Pobrano materiały do szkolenia {training_id}: {file_path}")

def download_certificate(training_id):
    certificates_directory = os.path.join(os.getcwd(), "certificates")
    file_path = filedialog.askopenfilename(title="Wybierz plik", initialdir=certificates_directory)
    if not os.path.exists(certificates_directory) or not os.path.isdir(certificates_directory):
        os.makedirs(certificates_directory, exist_ok=True)
    if file_path:
        destination_folder = "downloaded"
        if not os.path.exists(destination_folder) or not os.path.isdir(destination_folder):
            os.makedirs(destination_folder, exist_ok=True)
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("Informacja", f"Pobrano certyfikat do szkolenia {training_id}: {file_path}")