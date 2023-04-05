from tkinter import messagebox, ttk
from tkinter import *
from easy_sqlite3 import *
import random


class VocabGUI(Tk):
    def __init__(self):
        super().__init__()

        self.order = -1

        db = Database("./data/apps/vocabulary/vocab.db")
        db.create_table("vocab", {"word": "TEXT", "meaning": "TEXT"})

        self.word_list = [entry for entry in db.select('vocab')]
        
        db.close()

        self.style = ttk.Style()
        self.style.configure('TButton', font=("Futura", 10))

        self.title("Vocabulary")
        self.geometry("300x250")

        self.start_menu()
        self.mainloop()

    def start_menu(self):
        new_word = ttk.Entry(self, font=("Futura", 10))
        new_word.pack(pady=10)

        add_word = ttk.Button(self, text="Add word", style='TButton', command=lambda: self.add_word(new_word.get(), new_word))
        add_word.pack(pady=10)

        reverse = ttk.Button(self, text="Reverse order", style='TButton', command=self.reverse_order)
        reverse.pack(pady=2)

        separator = ttk.Separator(self, orient=HORIZONTAL)
        separator.pack(pady=10, expand=True, fill='x')

        next_word = ttk.Button(self, text="Next Word", command=self.next_word, style='TButton')
        next_word.pack()

        color = ttk.Style()
        color.configure('TFrame', foreground="brown")

        self.card_frame = ttk.Frame(self, style='TFrame')
        self.card_frame.pack(pady=10, fill='both', expand=True)

        new_word.bind("<Return>", lambda x:self.add_word(new_word.get(), new_word))

    def reverse_order(self):
        self.order = not self.order

    def next_word(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        word = random.choice(self.word_list)
        
        word_title = Label(self.card_frame, text=word[0-self.order], font=("Futura", 15, "bold"), fg="grey")
        word_title.pack(pady=10)

        show_answers = ttk.Button(self.card_frame, text="Show Answer", command=lambda:word_title.config(text=word[0-self.order] + " -> " + word[1-self.order]))
        show_answers.pack(pady=10)


    def add_word(self, word, entry:ttk.Entry):
        word, meaning = [w.strip() for w in word.split('=')]
        
        db = Database("./data/apps/vocabulary/vocab.db")

        if db.if_exists("vocab", {"word": word}):
            messagebox.showerror("Word already exists.", f"{word} already exists in the database")
            return

        db.insert("vocab", (word, meaning))
        db.close()

        messagebox.showinfo("Word added", f"{word} has been added to the database with the meaning {meaning}.")
        entry.delete(0, END)

        self.word_list.append((word, meaning))

class TestGUI(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("300x300")
        self.title("Test")


VocabGUI()