import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import re
import os

kontakty = []

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def dodajf():
    def zapisz_kontakt():
        imie = imieE.get()
        nazwisko = nazwiskoE.get()
        email = emailE.get()
        telefon = telefonE.get()

        if not imie or not nazwisko or not email or not telefon:
            messagebox.showerror("Błąd", "Wszystkie pola są wymagane!")
            return
        if not is_valid_email(email):
            messagebox.showerror("Błąd", "Niepoprawny adres email!")
            return

        kontakt = [imie, nazwisko, email, telefon]
        if kontakt not in kontakty:
            kontakty.append(kontakt)
            messagebox.showinfo("Sukces", "Kontakt dodany!")
            dW.destroy()
        else:
            messagebox.showwarning("Uwaga", "Ten kontakt już istnieje.")

    dW = tk.Toplevel()
    dW.title("Dodaj kontakt")
    dW.geometry("420x370")

    tk.Label(dW, text="Imię:").grid(row=0, column=0)
    imieE = tk.Entry(dW)
    imieE.grid(row=0, column=1)

    tk.Label(dW, text="Nazwisko:").grid(row=1, column=0)
    nazwiskoE = tk.Entry(dW)
    nazwiskoE.grid(row=1, column=1)

    tk.Label(dW, text="Email:").grid(row=2, column=0)
    emailE = tk.Entry(dW)
    emailE.grid(row=2, column=1)

    tk.Label(dW, text="Telefon:").grid(row=3, column=0)
    telefonE = tk.Entry(dW)
    telefonE.grid(row=3, column=1)

    zapiszB = tk.Button(dW, text="Zapisz", command=zapisz_kontakt)
    zapiszB.grid(row=4, column=1, pady=10)

def eksportf():
    if not kontakty:
        messagebox.showwarning("Uwaga", "Brak kontaktów do zapisania.")
        return

    try:
        path = os.path.join(os.getcwd(), "kontakty.csv")
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Imię", "Nazwisko", "Email", "Telefon"])
            for k in kontakty:
                writer.writerow(k)
        messagebox.showinfo("Sukces", f"Dane zapisane w pliku:\n{path}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać pliku:\n{e}")

def wczytajf():
    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file:
        try:
            with open(file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # pomiń nagłówek
                for row in reader:
                    if row not in kontakty:
                        kontakty.append(row)
            messagebox.showinfo("Sukces", "Dane wczytane.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku:\n{e}")

def analizujf():
    dW = tk.Toplevel()
    dW.title("Analiza kontaktów")
    dW.geometry("500x500")

    tk.Label(dW, text="Filtruj według imie:").pack()
    fei = tk.Entry(dW)
    fei.pack(pady=5)

    tk.Label(dW, text="Filtruj według nazwisko:").pack()
    fen = tk.Entry(dW)
    fen.pack(pady=5)

    tk.Label(dW, text="Filtruj według email:").pack()
    fee = tk.Entry(dW)
    fee.pack(pady=5)

    tk.Label(dW, text="Filtruj według telefon:").pack()
    fet = tk.Entry(dW)
    fet.pack(pady=5)

    listbox = tk.Listbox(dW, width=60)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def aktualizuj_liste(*args):
        filtr_imie = fei.get().lower()
        filtr_nazwisko = fen.get().lower()
        filtr_email = fee.get().lower()
        filtr_telefon = fet.get().lower()

        listbox.delete(0, tk.END)

        for k in kontakty:
            imie, nazwisko, email, telefon = k
            if (filtr_imie in imie.lower() and
                filtr_nazwisko in nazwisko.lower() and
                filtr_email in email.lower() and
                filtr_telefon in telefon.lower()):
                listbox.insert(tk.END, f"{imie} {nazwisko} | {email} | {telefon}")

    # Binduj każdy entry do odświeżania listy
    fei.bind("<KeyRelease>", aktualizuj_liste)
    fen.bind("<KeyRelease>", aktualizuj_liste)
    fee.bind("<KeyRelease>", aktualizuj_liste)
    fet.bind("<KeyRelease>", aktualizuj_liste)

    aktualizuj_liste()

root = tk.Tk()
root.title("Organizer Kontaktów")
root.geometry("300x300")

tk.Button(root, text="Dodaj kontakt", command=dodajf).pack(pady=10)
tk.Button(root, text="Wczytaj z pliku", command=wczytajf).pack(pady=10)
tk.Button(root, text="Eksportuj", command=eksportf).pack(pady=10)
tk.Button(root, text="Analizuj", command=analizujf).pack(pady=10)

root.mainloop()
