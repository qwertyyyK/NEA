# Import necessary modules from tkinter and other libraries
from tkinter import messagebox, Tk, Toplevel, StringVar, Label, Entry, Button, Radiobutton, IntVar, Canvas, Frame
import hashlib
import sqlite3
import os
import bcrypt


# Define a global variable for the file name
file = "FILE NAME"


# Create a class for the Quiz App
class QuizApp:
   def __init__(self):
       # Initialise instance variables
       self.name = ""
       self.count = 0
       self.mark = []


       # Create the main application window
       self.first_screen = Tk()
       self.first_screen.geometry("300x250")
       self.first_screen.title("Login:")


       # Create and display labels and buttons on the main screen
       Label(self.first_screen, text="Login Screen", width="300", height="2", font=("Blackadder ITC", 25)).pack()
       Label(self.first_screen, text="").pack()
       Button(self.first_screen, text="Login", height="2", bg="medium spring green", width="30",
              command=self.login).pack()
       Label(self.first_screen, text="").pack()
       Button(self.first_screen, text="Register", height="2", bg="light cyan", width="30",
              command=self.register).pack()


       # Start the main application loop
       self.first_screen.mainloop()


   def login(self):
       # Create a login window
       login_screen = Toplevel(self.first_screen)
       login_screen.title("Login")
       login_screen.geometry("300x250")


       # Create and display labels, entry widgets, and a login button in the login window
       Label(login_screen, text="Please enter details below to login").pack()
       Label(login_screen, text="").pack()


       self.username_verify = StringVar()
       self.password_verify = StringVar()


       Label(login_screen, text="Username").pack()
       username_login_entry = Entry(login_screen, textvariable=self.username_verify)
       username_login_entry.pack()


       Label(login_screen, text="").pack()
       Label(login_screen, text="Password").pack()
       password_login_entry = Entry(login_screen, textvariable=self.password_verify, show='*')
       password_login_entry.pack()


       Label(login_screen, text="").pack()
       Button(login_screen, text="Login", bg="medium spring green", width=10, height=1,
              command=self.login_verify).pack()


   def register(self):
       # Create a registration window
       global registering_screen
       registering_screen = Toplevel(self.first_screen)
       registering_screen.title("Register")
       registering_screen.geometry("300x250")


       self.username = StringVar()
       self.password = StringVar()
       self.confirm_password = StringVar()


       # Create and display labels, entry widgets, and a register button in the registration window
       Label(registering_screen, text="Please enter the credentials below").pack()
       Label(registering_screen, text="").pack()


       username_lable = Label(registering_screen, text="Username")
       username_lable.pack()
       username_entry = Entry(registering_screen, textvariable=self.username)
       username_entry.pack()


       password_lable = Label(registering_screen, text="Password")
       password_lable.pack()
       password_entry = Entry(registering_screen, textvariable=self.password, show='*')
       password_entry.pack()


       confirm_password_lable = Label(registering_screen, text="Confirm Password")
       confirm_password_lable.pack()
       confirm_password_entry = Entry(registering_screen, textvariable=self.confirm_password, show='*')
       confirm_password_entry.pack()


       Label(registering_screen, text="").pack()
       Button(registering_screen, text="Register", width=10, bg="light cyan", height=1,
              command=self.verify_passwords_then_register_user).pack()

       # Method to verify passwords and register a user
   def verify_passwords_then_register_user(self):
       password = self.password.get()
       confirm_password = self.confirm_password.get()


       if password != confirm_password:
           messagebox.showerror("Error", "Passwords do not match")
           return


       self.register_user()

   def login_verify(self):
       # Verify user login credentials
       username1 = self.username_verify.get()
       password1 = self.password_verify.get()
       self.name = username1


       list_of_files = os.listdir()
       if username1 in list_of_files:
           file1 = open(username1, "r")
           verify = file1.read().splitlines()
           str_hash = hashlib.sha256(password1.encode('utf-8'))
           pass_hash = str_hash.hexdigest()


           if pass_hash in verify[1]:
               self.login_success()
           else:
               self.password_not_recognised()
       else:
           self.user_not_found()


   def register_user(self):
    # Register a new user
    username_info = self.username.get()
    password_info = self.password.get().encode('utf-8')  # encode the password to bytes
    list_of_files = os.listdir()

    for i in range(1):
        if not username_info or not password_info:
            registering_screen.destroy()
            messagebox.showerror("Error", "Blank Entries!")
            self.register()
        elif username_info == password_info.decode():
            registering_screen.destroy()
            messagebox.showerror("Error", "Username and Password can't be the same")
            self.register()
        elif username_info in list_of_files:
            registering_screen.destroy()
            messagebox.showerror("Error", "Username already taken!")
            self.register()

        # Checks if the user entered a password with less than 8 characters or without an uppercase letter
        elif len(password_info) < 8 or not any(char.isupper() for char in password_info.decode()):
            registering_screen.destroy()
            messagebox.showerror("Error", "Password has to be 8 characters or more and must contain at least 1 uppercase letter!")
            self.register()
        else:
            # Generate a salt and hash the password
            hashed_password = bcrypt.hashpw(password_info, bcrypt.gensalt())
            print(hashed_password)
            file = open(username_info, "w")
            file.write(username_info + "\n")
            file.write(hashed_password.decode())  # store the hash as a string
            file.close()

            # Display registration success message
            Label(registering_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username_info, hashed_password))
            conn.commit()
            print(f"User '{username_info}' added to the database.")
            conn.close()
            break


   def login_success(self):
       # Show a success message upon successful login
       login_success_screen = Toplevel(self.first_screen)
       login_success_screen.title("Success")
       login_success_screen.geometry("150x100")
       Label(login_success_screen, text="Successfully logged in").pack()
       Button(login_success_screen, text="OK", command=login_success_screen.destroy).pack()
       self.first_screen.destroy()
       self.menu()


   # Define a method to handle an invalid password
   def password_not_recognised(self):
       # Create a new window for displaying an error message
       password_not_recognised_screen = Toplevel(self.first_screen)
       password_not_recognised_screen.title("Error")
       password_not_recognised_screen.geometry("150x100")
       Label(password_not_recognised_screen, text="Incorrect Password ").pack()
       Button(password_not_recognised_screen, text="OK", command=password_not_recognised_screen.destroy).pack()


   # Define a method to handle a user not found error
   def user_not_found(self):
       # Create a new window for displaying an error message
       unknown_user_screen = Toplevel(self.first_screen)
       unknown_user_screen.title("Error")
       unknown_user_screen.geometry("150x100")
       Label(unknown_user_screen, text="Error, User Not Found").pack()
       Button(unknown_user_screen, text="OK", command=unknown_user_screen.destroy).pack()


   # Define a method to create the main menu
   def menu(self):
       # Create the main menu window
       global menu
       menu = Tk()
       menu.geometry("300x250")
       menu.title("Dashboard")
       Label(menu, text="Dashboard", width="300", height="2", font=("Blackadder ITC", 25)).pack()
       # Create buttons for different options in the menu
       Button(menu, text="Topics", height="2", bg="LightCyan2", width="30", command=self.assignments).pack()
       Label(menu, text="").pack()
       Button(menu, text="Analytics", height="2", bg="MistyRose2", width="30", command=self.summary).pack()
       menu.mainloop()


   # Define a method to handle assignments
   def assignments(self):
       # Create a new window for displaying assignment options
       global assignments
       self.delete_menu()
       assignments = Tk()
       assignments.geometry("350x350")
       assignments.title("Topics")
       Label(assignments, text="Select a Topic", width="300", height="2", font=("Blackadder ITC", 25)).pack()
       # Create buttons for different assignment topics
       Button(assignments, text="Planets", height="2", bg="green yellow", width="30",
              command=lambda f=open("Planets.txt"): self.quiz(f)).pack()
       Label(assignments, text="").pack()
       Button(assignments, text="Stars", height="2", bg="green yellow", width="30",
              command=lambda f=open("Stars.txt"): self.quiz(f)).pack()
       Label(assignments, text="").pack()
       Button(assignments, text="Blackholes", height="2", bg="yellow", width="30",
              command=lambda f=open("Blackholes.txt"): self.quiz(f)).pack()
       Label(assignments, text="").pack()
       Button(assignments, text="The Cosmos", height="2", bg="yellow", width="30",
              command=lambda f=open("The_Cosmos.txt"): self.quiz(f)).pack()
       Label(assignments, text="").pack()


   # Define a method to conduct a quiz
   def quiz(self, f):
       # Create a quiz window
       global quiz, file, var1, var, button1, button2, button3, button4
       assignments.destroy()
       repeat = True
       # Determine the file to use based on the selected topic
       if str(f) == "<_io.TextIOWrapper name='Planets.txt' mode='r' encoding='UTF-8'>":
           f = open("Planets.txt")
           file = "Planets.txt"
       elif str(f) == "<_io.TextIOWrapper name='Stars.txt' mode='r' encoding='UTF-8'>":
           f = open("Stars.txt")
           file = "Stars.txt"
       elif str(f) == "<_io.TextIOWrapper name='Blackholes.txt' mode='r' encoding='UTF-8'>":
           f = open("Blackholes.txt")
           file = "Blackholes.txt"
       elif str(f) == "<_io.TextIOWrapper name='The_Cosmos.txt' mode='r' encoding='UTF-8'>":
           f = open("The_Cosmos.txt")
           file = "The_Cosmos.txt"
       content = f.readlines()
       while self.count <= 4 and repeat:
           repeat = False
           quiz = Tk()
           quiz.geometry("1100x250")
           quiz.title("Quiz")
           # Extract quiz question and answer choices from the content
           question = content[2 * (self.count + 1)].split(",")[:-1]
           var = StringVar()
           var.set(content[1 + (self.count) * 2][:-1])
           l = Label(quiz, textvariable=var, width="250", height="2", font=("Verdana", 13)).pack()
           var1 = IntVar()
           var1 = StringVar(quiz, " ")
           Label(quiz, text="Select an answer:").pack(anchor='w')
           # Create radio buttons for answer choices
           button1 = Radiobutton(quiz, text=question[0], variable=var1, value=0 + 1)
           button1.pack(anchor='w')
           button2 = Radiobutton(quiz, text=question[1], variable=var1, value=1 + 1)
           button2.pack(anchor='w')
           button3 = Radiobutton(quiz, text=question[2], variable=var1, value=2 + 1)
           button3.pack(anchor='w')
           button4 = Radiobutton(quiz, text=question[3], variable=var1, value=3 + 1)
           button4.pack(anchor='w')
           Button(text="Submit", height="2", bg="DeepSkyBlue3", fg="black", width="30", command=self.submit).pack()


   # Define a method to submit quiz answers
   def submit(self):
       print(file)
       f = open(file)
       content = f.readlines()
       if self.count <= 3:
           if var1.get() == content[2 * (self.count + 1)].split(",")[4][:-1]:
               self.mark.append(20)
               self.count += 1
           else:
               self.count += 1
           var.set(content[1 + (self.count) * 2][:-1])
           button1['text'] = content[2 * (self.count + 1)].split(",")[:-1][0]
           button2['text'] = content[2 * (self.count + 1)].split(",")[:-1][1]
           button3['text'] = content[2 * (self.count + 1)].split(",")[:-1][2]
           button4['text'] = content[2 * (self.count + 1)].split(",")[:-1][3]
           quiz.update_idletasks()
       else:
           self.delete_quiz()
           if var1.get() == content[2 * (5)].split(",")[4][:-1]:
               self.mark.append(20)
           list_of_files = os.listdir()
           if self.name in list_of_files:
               f = open(self.name, "a+")
               f.write("\n" + str(sum(self.mark)))
               f.close()
               self.submit_scores()


   # Define a method to display the submitted score
   def submit_scores(self):
       after_quiz = Tk()
       after_quiz.geometry("350x250")
       after_quiz.title("Submitted Mark")
       Label(after_quiz, text="Thank You, your score is:", width="300", height="2", font=("Calibri", 13)).pack()
       Label(after_quiz, text=str(sum(self.mark)) + "%", width="300", height="2", font=("Calibri", 13)).pack()
       Label(after_quiz, text="Your score will update now with the database", width="300", height="2",
             font=("Calibri", 13)).pack()


   # Define a method to display a summary of previous scores
   def summary(self):
       # Read and analyze previous scores from a file
       with open(self.name, "r") as file1:
           scores = file1.read().splitlines()
       previous_scores = [int(score) for score in scores[::-1][:-2]]
       total_sum = sum(previous_scores)
       number_of_previous_scores = len(previous_scores)
       average = round(total_sum / number_of_previous_scores, 2)


       # Create a summary window to display the scores and average
       summary_window = Toplevel()
       summary_window.geometry("600x400")
       summary_window.title("Analytics")


       Label(summary_window, text="Here is a list of all your previous scores:", width="300", height="2",
             font=("Calibri", 13)).pack()
       Label(summary_window, text=previous_scores, width="300", height="2", font=("Calibri", 13)).pack()
       Label(summary_window, text="The average score is:", width="300", height="2", font=("Calibri", 13)).pack()
       Label(summary_window, text=str(average), width="300", height="2", font=("Calibri", 13)).pack()


       # Create a bar graph to visualize the scores
       graph_frame = Frame(summary_window)
       graph_frame.pack()
       self.show_grades_graph(previous_scores, graph_frame)


   # Define a method to display a bar graph of scores
   def show_grades_graph(self, grades, frame):
       WIDTH = str(len(grades) * 100)
       canvas = Canvas(frame, width=int(WIDTH), height=300)
       canvas.pack()


       bar_width = 50
       x_start = 50
       y_scale = 2


       for i, grade in enumerate(grades):
           x = x_start + i * (bar_width + 20)
           y = 200 - grade * y_scale
           canvas.create_rectangle(x, y, x + bar_width, 200, fill="blue")
           canvas.create_text(x + bar_width / 2, y - 10, text=str(grade))


       canvas.create_text(20, 175, text="Grades", angle=90)


   # Define a method to delete the main menu window
   def delete_menu(self):
       menu.destroy()


   # Define a method to delete the quiz window
   def delete_quiz(self):
       quiz.destroy()




# Check if the script is being run directly
if __name__ == "__main__":
   app = QuizApp()
