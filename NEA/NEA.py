from tkinter import messagebox
from tkinter import *
import os

class QuizApp:
    def __init__(self):
        self.name = ""
        self.file = "FILE NAME"
        self.count = 0
        self.mark = []

    def main_account_screen(self):
        self.first_screen = Tk()
        self.first_screen.geometry("300x250")
        self.first_screen.title("Login:")
        Label(text="Login Screen", width="300", height="2", font=("Blackadder ITC", 25)).pack()
        Label(text="").pack()
        Button(text="Login", height="2",bg="medium spring green", width="30", command=self.login).pack()
        Label(text="").pack()
        Button(text="Register", height="2",bg="light cyan", width="30", command=self.register).pack()
        self.first_screen.mainloop()

    def register(self):
        self.registering_screen = Toplevel(self.first_screen)
        self.registering_screen.title("Register")
        self.registering_screen.geometry("300x250")

        self.username = StringVar()
        self.password = StringVar()

        Label(self.registering_screen, text="Please enter the credentials below").pack()
        Label(self.registering_screen, text="").pack()

        username_lable = Label(self.registering_screen, text="Username")
        username_lable.pack()
        self.username_entry = Entry(self.registering_screen, textvariable=self.username)
        self.username_entry.pack()

        password_lable = Label(self.registering_screen, text="Password")
        password_lable.pack()
        self.password_entry = Entry(self.registering_screen, textvariable=self.password, show='*')
        self.password_entry.pack()

        Label(self.registering_screen, text="").pack()
        Button(self.registering_screen, text="Register", width=10, bg="light cyan", height=1, command=self.register_user).pack()

    def login(self):
        self.login_screen = Toplevel(self.first_screen)
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")

        Label(self.login_screen, text="Please enter details below to login").pack()
        Label(self.login_screen, text="").pack()

        self.username_verify = StringVar()
        self.password_verify = StringVar()

        Label(self.login_screen, text="Username").pack()
        self.username_login_entry = Entry(self.login_screen, textvariable=self.username_verify)
        self.username_login_entry.pack()

        Label(self.login_screen, text="").pack()
        Label(self.login_screen, text="Password").pack()
        self.password_login_entry = Entry(self.login_screen, textvariable=self.password_verify, show='*')
        self.password_login_entry.pack()

        Label(self.login_screen, text="").pack()
        Button(self.login_screen, text="Login", bg="medium spring green", width=10, height=1, command=self.login_verify).pack()

    def register_user(self):
        username_info = self.username.get()
        password_info = self.password.get()
        list_of_files = os.listdir()

        for i in range(1):
            if not self.username.get() and not self.password.get():
                self.registering_screen.destroy()
                messagebox.showerror("Error", "Blank Entries!")
                self.register()

            elif username_info == password_info:
                self.registering_screen.destroy()
                messagebox.showerror("Error", "Username and Password cant be the same")
                self.register()

            elif username_info in list_of_files:
                self.registering_screen.destroy()
                messagebox.showerror("Error", "Username already taken!")
                self.register()

            elif len(password_info) >= 9:
                self.registering_screen.destroy()
                messagebox.showerror("Error", "Password has to be 8 characters or less!")
                self.register()

            else:
                file = open(username_info, "w")
                file.write(username_info + "\n")
                file.write(password_info)
                file.close()

                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)

                Label(self.registering_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
                break

    def login_verify(self):
        self.name = self.username_verify.get()
        password1 = self.password_verify.get()
        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

        list_of_files = os.listdir()
        if self.name in list_of_files:
            file1 = open(self.name, "r")
            verify = file1.read().splitlines()
            if password1 in verify[1]:
                self.login_success()
            else:
                self.password_not_recognised()
        else:
            self.user_not_found()

    def login_success(self):
        self.login_success_screen = Toplevel(self.login_screen)
        self.login_success_screen.title("Success")
        self.login_success_screen.geometry("150x100")

        Label(self.login_success_screen, text="Successfully logged in").pack()
        Button(self.login_success_screen, text="OK", command=self.delete_login_success).pack()
        self.first_screen.destroy()
        self.menu()

    def password_not_recognised(self):
        self.password_not_recogognised_screen = Toplevel(self.login_screen)
        self.password_not_recogognised_screen.title("Success")
        self.password_not_recogognised_screen.geometry("150x100")

        Label(self.password_not_recogognised_screen, text="Invalid Password ").pack()
        Button(self.password_not_recogognised_screen, text="OK", command=self.delete_password_not_recognised).pack()

    def user_not_found(self):
        self.unknown_user_screen = Toplevel(self.login_screen)
        self.unknown_user_screen.title("Success")
        self.unknown_user_screen.geometry("150x100")

        Label(self.unknown_user_screen, text="Error, User Not Found").pack()
        Button(self.unknown_user_screen, text="OK", command=self.delete_user_not_found_screen).pack()

    def menu(self):
        self.menu = Tk()
        self.menu.geometry("300x250")
        self.menu.title("Dashboard")

        Label(self.menu, text="Dashboard", width="300", height="2", font=("Blackadder ITC", 25)).pack()
        Label(self.menu, text="").pack()
        Button(self.menu, text="Choose A Quiz!", height="2", bg="LightCyan2", width="30", command=self.assingments).pack()
        Label(self.menu, text="").pack()
        Button(self.menu, text="Analytics", height="2", bg="MistyRose2", width="30", command=self.summary).pack()
        self.menu.mainloop()

    def assingments(self):
        self.delete_menu()
        self.assingments = Tk()
        self.assingments.geometry("350x350")
        self.assingments.title("Select a Topic!")

        Label(self.assingments, text="Topics", width="300", height="2", font=("Blackadder ITC", 25)).pack()
        Label(self.assingments, text="").pack()
        Button(self.assingments, text="Planets", height="2", bg="green yellow", width="30", command=lambda f=open("Planets.txt"): self.quiz(f)).pack()
        Label(self.assingments, text="").pack()
        Button(self.assingments, text="Stars", height="2", bg="green yellow", width="30", command=lambda f=open("Stars.txt"): self.quiz(f)).pack()
        Label(self.assingments, text="").pack()
        Button(self.assingments, text="Blackholes", height="2", bg="yellow", width="30", command=lambda f=open("Blackholes.txt"): self.quiz(f)).pack()
        Label(self.assingments, text="").pack()
        Button(self.assingments, text="The Cosmos", height="2", bg="yellow", width="30", command=lambda f=open("The_Cosmos.txt"): self.quiz(f)).pack()

    def quiz(self, f):
        self.assingments.destroy()

        self.repeat = True
        if str(f) == "<_io.TextIOWrapper name='Planets.txt' mode='r' encoding='cp1252'>":
            f = open("Planets.txt")
            self.file = "Planets.txt"
        elif str(f) == "<_io.TextIOWrapper name='Stars.txt' mode='r' encoding='cp1252'>":
            f = open("Stars.txt")
            self.file = "Stars.txt"
        elif str(f) == "<_io.TextIOWrapper name='Blackholes.txt' mode='r' encoding='cp1252'>":
            f = open("Blackholes.txt")
            self.file = "Blackholes.txt"
        elif str(f) == "<_io.TextIOWrapper name='The_Cosmos.txt' mode='r' encoding='cp1252'>":
            f = open("The_Cosmos.txt")
            self.file = "The_Cosmos.txt"

        content = f.readlines()

        while self.count <= 4 and self.repeat == True:
            self.repeat = False

            self.quiz = Tk()
            self.quiz.geometry("1100x250")
            self.quiz.title("Quiz")

            self.question = content[2*(self.count+1)].split(",")[:-1]
            self.var = StringVar()
            self.var.set(content[1+(self.count)*2][:-1])

            l = Label(self.quiz, textvariable=self.var, width="250", height="2", font=("Verdana", 13)).pack()

            self.var1 = IntVar()
            self.var1 = StringVar(self.quiz, " ")

            Label(self.quiz, text="Select an answer:").pack(anchor='w')

            self.button1 = Radiobutton(self.quiz, text=self.question[0], variable=self.var1, value=0+1)
            self.button1.pack(anchor='w')
            self.button2 = Radiobutton(self.quiz, text=self.question[1], variable=self.var1, value=1+1)
            self.button2.pack(anchor='w')
            self.button3 = Radiobutton(self.quiz, text=self.question[2], variable=self.var1, value=2+1)
            self.button3.pack(anchor='w')
            self.button4= Radiobutton(self.quiz, text=self.question[3], variable=self.var1, value=3+1)
            self.button4.pack(anchor='w')
            Button(text="Submit", height="2", bg="DeepSkyBlue3", fg="black", width="30", command=self.submit).pack()

    def submit(self):
        print(self.file)

        f = open(self.file)
        content = f.readlines()

        if self.count <= 3:
            if self.var1.get() == content[2*(self.count+1)].split(",")[4][:-1]:
                self.mark.append(20)
                self.count += 1            
            else:
                self.count += 1
            self.var.set(content[1+(self.count)*2][:-1])
            self.button1['text'] = content[2*(self.count+1)].split(",")[:-1][0]
            self.button2['text'] = content[2*(self.count+1)].split(",")[:-1][1]
            self.button3['text'] = content[2*(self.count+1)].split(",")[:-1][2]
            self.button4['text'] = content[2*(self.count+1)].split(",")[:-1][3]
            self.quiz.update_idletasks()
        else:
            self.delete_quiz()
            if self.var1.get() == content[2*(5)].split(",")[4][:-1]:
                self.mark.append(20)

            list_of_files = os.listdir()
            if self.name in list_of_files:
                f = open(self.name, "a+")
                f.write("\n"+ str(sum(self.mark)))
                f.close()
                self.submit_scores()

    def submit_scores(self):
        after_quiz = Tk()
        after_quiz.geometry("350x250")
        after_quiz.title("Submitted Mark")

        Label(after_quiz, text="Thank You, your score is:", width="300", height="2", font=("Calibri", 13)).pack()
        Label(after_quiz, text=str(sum(self.mark))+"%", width="300", height="2", font=("Calibri", 13)).pack()
        Label(after_quiz, text="Your score will update now with the database", width="300", height="2", font=("Calibri", 13)).pack()

    def summary(self):
        file1 = open(self.name, "r")
        scores = file1.read().splitlines()
        total_sum = 0
        for i in range(len(scores[::-1][:-2])):
            total_sum += int(scores[::-1][i])
        number_of_previous_scores = int(len(scores[::-1][:-2]))
        average = str(round(total_sum/number_of_previous_scores, 2))

        self.summary = Tk()
        self.summary.geometry("300x250")
        self.summary.title("Analytics")

        Label(self.summary, text="Here is a list of all your previous scores:", width="300", height="2", font=("Calibri", 13)).pack()
        Label(self.summary, text=scores[::-1][:-2], width="300", height="2", font=("Calibri", 13)).pack()
        Label(self.summary, text="The average score is:", width="300", height="2", font=("Calibri", 13)).pack()
        Label(self.summary, text=average, width="300", height="2", font=("Calibri", 13)).pack()

    def delete_menu(self):
        self.menu.destroy()

    def delete_quiz(self):
        self.quiz.destroy()

    def delete_login_success(self):
        self.login_success_screen.destroy()

    def delete_password_not_recognised(self):
        self.password_not_recogognised_screen.destroy()

    def delete_user_not_found_screen(self):
        self.unknown_user_screen.destroy()


if __name__ == "__main__":
    app = QuizApp()
    app.main_account_screen()