import tkinter as tk
from tkinter import ttk, messagebox
import training as TRAINING

def get_participants():
    participants = []
    with open("accounts.pydb", "r") as file:
        for line in file:
            fields = line.strip().split("~")
            if len(fields) >= 8:
                participant_id, name = fields[0], fields[2]
                participants.append((name))
    return participants

def get_participant_name(participant_id):
    with open("accounts.pydb", "r") as file:
        for line in file:
            fields = line.strip().split("~")
            if len(fields) >= 8 and fields[0] == participant_id:
                return fields[2]

def get_training_name(training_id):
    try:
        with open("trainings.pydb", "r") as file:
            for line in file:
                fields = line.strip().split("~")
                if len(fields) >= 2 and fields[0] == training_id:
                    return fields[1]
    except FileNotFoundError:
        return None

def refresh_participants_list(participants_listbox, selected_training_name):
    # Po dodaniu uczestnika odśwież listę uczestników w widoku
    participants_listbox.delete(0, tk.END)

    # Pobierz i wyświetl zawartość pliku participants.pydb
    participants_file = "participants.pydb"
    try:
        with open(participants_file, "r") as file:
            for line in file:
                fields = line.strip().split("~")
                if len(fields) >= 2:
                    training_id, participant_id = fields[0], fields[1]
    
                   
                    participants_listbox.insert(tk.END, f"{participant_id} - KURS: {training_id}")
    except FileNotFoundError:
        messagebox.showinfo("Błąd", "Brak pliku participants.pydb")
        print("Plik 'participants.pydb' nie istnieje.")

def add_participant_to_training():
    def add_participant():
        selected_training_name = training_var.get()
        selected_participant_id = participant_var.get()

        # Pobierz aktualną listę uczestników przypisanych do szkolenia
        participants_list = get_participants_for_training(selected_training_name)

        # Sprawdź, czy wybrany uczestnik już uczestniczy w szkoleniu
        if any(participant[0] == selected_participant_id for participant in participants_list):
            messagebox.showinfo("Błąd", "Ten uczestnik już uczestniczy w tym szkoleniu.")
            return

        # Dodaj uczestnika do listy przypisanych do szkolenia
        participants_list.append((selected_participant_id, get_participant_name(selected_participant_id)))

        # Zapisz listę uczestników przypisanych do szkolenia
        save_participants_to_file(selected_training_name, participants_list)

        messagebox.showinfo("Dodano uczestnika", f"Dodano uczestnika do szkolenia o nazwie {selected_training_name}")

        # Odśwież listę uczestników po dodaniu uczestnika
        refresh_participants_list(participants_listbox, selected_training_name)

    

    def get_participants_for_training(training_name):
        # Pobierz aktualną listę uczestników przypisanych do szkolenia
        participants_file = f"participants.pydb"
        try:
            with open(participants_file, "r") as file:
                participants_list = [tuple(line.strip().split("~")) for line in file]
        except FileNotFoundError:
            participants_list = []
        return participants_list

    def save_participants_to_file(training_id, participants_list):
        participants_file = "participants.pydb"
        try:
            with open(participants_file, "r") as file:
                existing_participants = [line.strip().split("~") for line in file]
        except FileNotFoundError:
            existing_participants = []

        with open(participants_file, "a") as file:
            for participant in participants_list:
                existing = any(participant[0] == existing_participant[0] for existing_participant in existing_participants)
                if not existing:
                    file.write(f"{training_id}~{participant[0]}\n")

    # Utwórz okno dialogowe do dodawania uczestników
    add_participant_window = tk.Toplevel()
    add_participant_window.title("Dodaj uczestnika do szkolenia")

    # Pobierz listę uczestników i szkoleń
    participants = get_participants()
    trainings = TRAINING.get_trainings()

    # Utwórz etykietę i listę rozwijaną z uczestnikami
    tk.Label(add_participant_window, text="Wybierz uczestnika:").grid(row=0, column=0, padx=10, pady=10)
    participant_var = tk.StringVar()
    participant_combobox = ttk.Combobox(add_participant_window, textvariable=participant_var)
    participant_combobox['values'] = participants
    participant_combobox.grid(row=0, column=1, padx=10, pady=10)

    # Utwórz etykietę i listę rozwijaną ze szkoleniami
    tk.Label(add_participant_window, text="Wybierz szkolenie:").grid(row=1, column=0, padx=10, pady=10)
    training_var = tk.StringVar()
    training_combobox = ttk.Combobox(add_participant_window, textvariable=training_var)
    training_combobox['values'] = [(training.name) for training in trainings]
    training_combobox.grid(row=1, column=1, padx=10, pady=10)

    # Utwórz listbox do wyświetlenia listy uczestników
    participants_listbox = tk.Listbox(add_participant_window)
    participants_listbox.grid(row=4, column=0, columnspan=2, pady=10)
    participants_listbox.config(width=50, height=10)

    # Dodaj przycisk potwierdzający dodanie uczestnika
    tk.Button(add_participant_window, text="Dodaj Uczestnika", command=add_participant).grid(row=2, column=0, columnspan=2, pady=10)

    # Dodaj przycisk do odświeżania listy uczestników
    tk.Button(add_participant_window, text="Odśwież listę uczestników", command=lambda: refresh_participants_list(participants_listbox, training_var.get())).grid(row=3, column=0, columnspan=2, pady=10)

    # Po utworzeniu okna, odśwież listę uczestników na widoku
    refresh_participants_list(participants_listbox, training_var.get())

    # Uruchom pętlę zdarzeń dla okna dodawania uczestnika
    add_participant_window.mainloop()




    






