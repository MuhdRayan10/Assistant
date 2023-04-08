from tkinter import ttk
from tkinter import *
from easy_sqlite3 import *

class DashboardGUI(Tk):
    def __init__(self, menu, name):
        super().__init__()

        menu.destroy()

        self.geometry("400x400")
        self.title("Chess")

        db = Database("./data/apps/chess/chess.db")

        self.name = name
        self.data = db.select("ratings", where={"player":name}, size=1)

        db.close()

        self.setup_dashboard()

    def setup_dashboard(self):

        title = Label(self, text=f"Name: {self.data[2]}{self.name}\nRating: {self.data[1]}",
                      fg="darkgrey", font=("Times", 20))
        title.pack(pady=10)



class ChessMenu(Tk):
    def __init__(self):
        super().__init__()

        db = Database("./data/apps/chess/chess.db")
        db.create_table("ratings", {"player": "TEXT", "rating": INT, "title": "TEXT"})
        db.close()

        self.geometry("300x250")
        self.title("Chess")

        self.menu()
        self.mainloop()

    def menu(self):

        title = Label(self, text="Chess", fg="grey", font=("Times", 25))
        title.pack(pady=10)

        ratings = Button(self, text="Ratings", bg="brown", borderwidth=1, font=("Times", 15), command=self.view_ratings)
        ratings.pack(pady=10)

        login = Button(self, text="Login", bg="brown", borderwidth=1, font=("Times", 15), command=self.login_page)
        login.pack(pady=10)

    def view_ratings(self):
        
        scr = Toplevel(self)
        scr.geometry("400x400")
        scr.title("Ratings")

        db = Database("./data/apps/chess/chess.db")
        
        ratings = db.select("ratings")
        db.close()

        title = Label(scr, text="Ratings", fg="grey", font=("Times", 20))
        title.pack(pady=10)

        for i, rating in enumerate(sorted(ratings, key=lambda x: x[1], reverse=True)[:10]):
            Label(scr, text=f"{i+1}. [{rating[1]}] {rating[2]} {rating[0]}", font=("Times", 13)).pack(pady=3)

    def login_page(self):
        
        scr = Toplevel(self)
        scr.geometry("300x175")
        scr.title("Login")

        title = Label(scr, text="Login / Register", fg="grey", font=("Times", 20))
        title.pack(pady=15)

        db = Database("./data/apps/chess/chess.db")
        ratings = db.select("ratings")

        db.close()

        account = StringVar()
        users = [r[0] for r in ratings]

        drop_down = ttk.Combobox(scr, textvariable=account)
        drop_down["values"] = users

        drop_down.pack(pady=10)

        login_btn = Button(scr, text="Login", font=("Times", 15), bg="brown", command=lambda: self.login_user(account.get(), users))
        login_btn.pack(pady=10)

    def login_user(self, name, users):
        
        if name not in users:
            db = Database("./data/apps/chess/chess.db")
            db.insert("ratings", (name, 1500, ""))
            db.close()
        
        DashboardGUI(self, name)

ChessMenu()
