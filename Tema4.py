import tkinter as tk  # Importa modulul tkinter pentru GUI
from tkinter import messagebox  # Importa messagebox pentru a afisa mesaje popup
import json  # Importa json pentru a salva/incarca datele
import os  # Importa os pentru a verifica existenta fisierului

# Numele fisierului JSON in care se vor salva datele
DATA_FILE = "carti.json"

# Functie care incarca cartile din fisierul JSON
def load_data():
    if not os.path.exists(DATA_FILE):  # Verifica daca fisierul exista
        return []  # Daca nu exista, returneaza o lista goala
    with open(DATA_FILE, "r") as file:  # Deschide fisierul in modul citire
        return json.load(file)  # Incarca si returneaza continutul JSON

# Functie care salveaza cartile in fisierul JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:  # Deschide fisierul in modul scriere
        json.dump(data, file, indent=4)  # Scrie datele in fisier cu indentare

# Clasa pentru fereastra principala
class CatalogApp:
    def __init__(self, root):
        self.root = root  # Salveaza fereastra root
        self.root.title("Catalog de Carti")  # Seteaza titlul ferestrei
        self.books = load_data()  # Incarca cartile din fisier
        self.selected_index = None  # Indexul cartii selectate

        self.frame = tk.Frame(root)  # Creeaza un cadru principal
        self.frame.pack(padx=10, pady=10)  # Afiseaza cadrul cu margini

        self.listbox = tk.Listbox(self.frame, width=50)  # Creeaza o lista
        self.listbox.pack()  # Afiseaza lista
        self.listbox.bind("<<ListboxSelect>>", self.on_select)  # Lega selectie

        self.refresh_list()  # Afiseaza cartile

        # Creeaza butoane CRUD
        tk.Button(self.frame, text="Adauga", command=self.add_book).pack(fill="x")
        tk.Button(self.frame, text="Editeaza", command=self.edit_book).pack(fill="x")
        tk.Button(self.frame, text="Sterge", command=self.delete_book).pack(fill="x")

    # Functie care actualizeaza lista afisata
    def refresh_list(self):
        self.listbox.delete(0, tk.END)  # Sterge tot din lista
        for book in self.books:  # Parcurge fiecare carte
            self.listbox.insert(tk.END, f"{book['titlu']} - {book['autor']}")  # Adauga in lista

    # Functie apelata cand se selecteaza un element
    def on_select(self, event):
        try:
            self.selected_index = self.listbox.curselection()[0]  # Salveaza indexul selectat
        except IndexError:
            self.selected_index = None  # Daca nu e selectat nimic

    # Functie pentru adaugare
    def add_book(self):
        BookForm(self, "Adauga Carte")  # Deschide formularul pentru adaugare

    # Functie pentru editare
    def edit_book(self):
        if self.selected_index is None:
            messagebox.showwarning("Atentie", "Selectati o carte!")  # Avertizare daca nu e selectat nimic
            return
        BookForm(self, "Editeaza Carte", self.books[self.selected_index])  # Deschide formularul de editare

    # Functie pentru stergere
    def delete_book(self):
        if self.selected_index is None:
            messagebox.showwarning("Atentie", "Selectati o carte!")  # Avertizare daca nu e selectat nimic
            return
        confirm = messagebox.askyesno("Confirmare", "Esti sigur ca vrei sa stergi cartea?")  # Confirmare
        if confirm:
            del self.books[self.selected_index]  # Sterge cartea din lista
            save_data(self.books)  # Salveaza lista actualizata
            self.refresh_list()  # Actualizeaza afisarea

# Clasa pentru formularul de adaugare/editare
class BookForm:
    def __init__(self, app, title, book=None):
        self.app = app  # Salveaza referinta la aplicatie
        self.book = book  # Cartea curenta (None daca adaugam)

        self.window = tk.Toplevel()  # Creeaza o fereastra noua
        self.window.title(title)  # Seteaza titlul

        # Camp pentru titlu
        tk.Label(self.window, text="Titlu:").pack()
        self.title_entry = tk.Entry(self.window)  # Creeaza un camp text
        self.title_entry.pack()

        # Camp pentru autor
        tk.Label(self.window, text="Autor:").pack()
        self.author_entry = tk.Entry(self.window)
        self.author_entry.pack()

        # Daca cartea exista (editare), precompleta campurile
        if book:
            self.title_entry.insert(0, book["titlu"])
            self.author_entry.insert(0, book["autor"])

        # Buton pentru salvare
        tk.Button(self.window, text="Salveaza", command=self.save).pack(pady=10)

    # Functie care salveaza cartea (noua sau modificata)
    def save(self):
        titlu = self.title_entry.get().strip()  # Ia titlul din camp
        autor = self.author_entry.get().strip()  # Ia autorul din camp

        if not titlu or not autor:
            messagebox.showerror("Eroare", "Toate campurile sunt obligatorii!")  # Mesaj eroare
            return

        new_book = {"titlu": titlu, "autor": autor}  # Creeaza obiectul carte

        if self.book:  # Daca editam
            index = self.app.selected_index  # Ia indexul curent
            self.app.books[index] = new_book  # Inlocuieste cartea
        else:  # Daca adaugam
            self.app.books.append(new_book)  # Adauga cartea noua

        save_data(self.app.books)  # Salveaza datele
        self.app.refresh_list()  # Actualizeaza lista
        self.window.destroy()  # Inchide formularul

# Punctul de intrare al aplicatiei
if __name__ == "__main__":
    root = tk.Tk()  # Creeaza fereastra principala
    app = CatalogApp(root)  # Creeaza aplicatia
    root.mainloop()  # Ruleaza bucla principala
