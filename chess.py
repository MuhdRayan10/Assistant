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

        self.t = Label(self, text=f"Name: {self.data[2]}{self.name}\nRating: {self.data[1]}",
                      fg="darkgrey", font=("Times", 20))
        self.t.pack(pady=10)

        match_btn = Button(self, text=f"Match", bg="brown", font=("Times", 15), command=self.add_match)
        match_btn.pack(pady=10)

    def add_match(self):
        scr = Toplevel(self)
        scr.title("Add Match")
        scr.geometry("200x200")

        opponent = StringVar(scr)

        drop_down = ttk.Combobox(scr, textvariable=opponent)
        drop_down.pack(pady=10)

        db = Database("./data/apps/chess/chess.db")
        drop_down["values"] = [r[0] for r in db.select("ratings")]

        db.close()

        winner = StringVar(scr)

        winner_drop = ttk.Combobox(scr, textvariable=winner)
        winner_drop.pack(pady=10)

        winner_drop["values"] = ["You", "Opponent"]

        add = Button(scr, text="Add Match", bg="brown", font=("Times", 15), command=lambda:self.conduct_match(opponent.get(), winner.get()))
        add.pack(pady=10)

    def conduct_match(self, opponent, winner):
        db = Database("./data/apps/chess/chess.db")
        ratings = db.select("ratings")

        opponent_rating = [r[1] for r in ratings if r[0] == opponent][0]
        user_rating = [r[1] for r in ratings if r[0] == self.name][0]

        expected = 1 / (1 + 10 ** ((opponent_rating - user_rating)/400))
        score = 1 if winner == "You" else 0

        db.update("ratings", information={"rating": round(user_rating + 32 * (score - expected), 2)}, where={"player":self.name})
        db.update("ratings", information={"rating": round(opponent_rating + 32 * ((not score) + expected - 1), 2)}, where={"player": opponent})

        db.close()

        self.t.config(text=f"Name: {self.name}\nRating: {round(user_rating + 32 * (score - expected), 2)}")





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
