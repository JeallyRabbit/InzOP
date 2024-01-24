import tkinter as tk
from tkinter import simpledialog

def show_survey_dialog(training_name):
    root = tk.Tk()
    
    # Pobierz odpowiedzi od użytkownika za pomocą simpledialog
    rating = simpledialog.askinteger("Ankieta", f"Oceń szkolenie '{training_name}' (1-5):", minvalue=1, maxvalue=5)
    helpful = simpledialog.askstring("Ankieta", f"Czy szkolenie '{training_name}' było pomocne? (Tak/Nie):")
    recommend = simpledialog.askstring("Ankieta", f"Czy zalecałbyś szkolenie '{training_name}' innym? (Tak/Nie):")

    # Tutaj możesz przekazać uzyskane odpowiedzi do funkcji lub je zapisać

    # Wypisz na konsolę uzyskane odpowiedzi (do celów testowych)
    print(f"Ocena: {rating}, Czy szkolenie było pomocne?: {helpful}, Czy zalecałbyś to szkolenie innym?: {recommend}")

    root.destroy()


