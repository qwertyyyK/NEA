# Import necessary modules from tkinter and other libraries
import tkinter as tk
from tkinter import messagebox, Tk, Toplevel, StringVar, Label, Entry, Button, Radiobutton, IntVar, Canvas, Frame, ttk, Checkbutton
import bcrypt
import mysql.connector
from db_setup import setup_database
from PIL import Image, ImageTk
# Connect to MySQL

# Setup database and get the connection and cursor
db, mycursor = setup_database()


#Create a tooltip for a given widget as the mouse goes on it.
class ToolTip(object):
    """
    Create a tooltip for a given widget as the mouse goes on it.
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # milliseconds
        self.wraplength = 180   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.id = None
        self.tw = None

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide_tooltip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show_tooltip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tooltip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hide_tooltip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


# Create a class for the Quiz App
class QuizApp:
   def __init__(self,master):
       self.master = master
       self.master.geometry("300x250")
       self.master.title("Quiz")
       
       # Initialise instance variables  

       #username of user currently logged in
       self.name = ""

       #questions done in a quiz, it's reset at the end of every quiz
       self.count = 0

       #marks obtained in each quiz, it's reset at the end of every quiz
       self.mark = []

       self.previous_questions = []  # Stack to hold previous questions     
       self.current_question = None  # Current active question
       self.question_index = 0    
       self.question_scores = []

       self.quiz_title_id_map = {}  # Dictionary to map quiz titles to their IDs  

       self.quiz_title = StringVar() 

       # Create and display labels and buttons on the main screen
       Label(self.master, text="Quiz App", width="300", height="2", font=("Blackadder ITC", 25)).pack()
       Label(self.master, text="").pack()
       Button(self.master, text="Login", height="2", bg="medium spring green", width="30",
               command=self.login).pack()
       Label(self.master, text="").pack()
       Button(self.master, text="Register", height="2", bg="light cyan", width="30",
               command=self.register).pack()





   def login(self):
       # Create a login window
       login_screen = Toplevel(self.master)
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
       command=lambda: self.login_verify(login_screen)).pack()
    
   def log_out(self):
        global menu
        menu.destroy()  # Close the dashboard window
        self.master.deiconify()  # Show the main login window again
        self.user_id = None  # Reset the user_id


   def register(self):
       # Create a registration window
       global registering_screen
       registering_screen = Toplevel(self.master)
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
       command=lambda: self.register_user(registering_screen)).pack()


       # Method to verify passwords and register a user
   def verify_passwords_then_register_user(self):
       password = self.password.get()
       confirm_password = self.confirm_password.get()


       if password != confirm_password:
           messagebox.showerror("Error", "Passwords do not match")
           return


       self.register_user()

   def login_verify(self, login_window):
    username = self.username_verify.get()
    password = self.password_verify.get().encode('utf-8')

    # Fetch user details
    mycursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
    result = mycursor.fetchone()

    if result:
        user_id, user_hash = result
        user_hash = user_hash.encode()

        if bcrypt.checkpw(password, user_hash):
            self.user_id = user_id  # Store the user ID for session management
            login_window.destroy()
            self.login_success()
        else:
            self.password_not_recognised()
    else:
        self.user_not_found()





   def register_user(self, registering_window):
    username_info = self.username.get()
    password_info = self.password.get().encode('utf-8')
    
    if username_info == password_info.decode():
        messagebox.showerror("Error", "Username and password cannot be the same")
        return
    # Check if the fields are empty
    if not username_info or not password_info:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Check if the password meets the requirements
    if len(password_info) < 8 or not any(char.isupper() for char in password_info.decode()):
        messagebox.showerror("Error", "Password must be at least 8 characters long and include an uppercase letter")
        return

    # Check if username already exists
    mycursor.execute("SELECT * FROM users WHERE username = %s", (username_info,))
    if mycursor.fetchone() is not None:
        messagebox.showerror("Error", "Username already taken!")
        return

    # Hash the password
    hashed_password = bcrypt.hashpw(password_info, bcrypt.gensalt()).decode('utf-8')

    # Insert new user into database
    try:
        mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username_info, hashed_password))
        db.commit()
        registering_window.destroy()
        messagebox.showinfo("Success", "Registration successful!")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to register user: {err}")
        db.rollback()



   def login_success(self):
       
        self.master.withdraw()

        # Show a success message upon successful login
        messagebox.showinfo("Success", "Login successful!")
        self.menu()


   # Define a method to handle an invalid password
   def password_not_recognised(self):
       # Create a new window for displaying an error message
       messagebox.showerror("Error," "Incorrect password")



   # Define a method to handle a user not found error
   def user_not_found(self):
       # Create a new window for displaying an error message
       messagebox.showerror("Error", "Username doesn't exist")


   # Define a method to create the main menu
   def menu(self):
       # Create the main menu window
       global menu
       menu = Toplevel()
       menu.geometry("600x400")
       menu.title("Dashboard")
        # Create buttons for different options in the menu
       Label(menu, text="Dashboard", width="300", height="2", font=("Blackadder ITC", 25)).pack()
       Button(menu, text="Quizzes", height="2", bg="LightCyan2", width="30", command=self.assignments).pack()
       Label(menu, text="").pack()
       Button(menu, text="Analytics", height="2", bg="MistyRose2", width="30", command=self.summary).pack()
       Label(menu, text="").pack()
       Button(menu, text="Manage custom quizzes", height="2", bg="orchid1", width="30", command=self.manage_quizzes).pack()
       Label(menu, text="").pack()
       Label(menu, text="").pack()
       Button(menu, text="Log Out", height="2", bg="IndianRed1", width="30", command=self.log_out).pack() 


       menu.protocol("WM_DELETE_WINDOW", self.close_application)


    # This method will be called when the Dashboard window is closed.
   def close_application(self):
        print("Closing application")
        self.master.quit()
        self.master.destroy()

   # Define a method to handle assignments
   def assignments(self):
        self.assignments_window = Toplevel()
        self.assignments_window.geometry("600x600")
        self.assignments_window.title("Topics")
        Label(self.assignments_window, text="Select a Topic", width="300", height="2", font=("Blackadder ITC", 25)).pack()

        # Fetch and create buttons for preloaded quiz topics from the database
        mycursor.execute("SELECT quiz_id, title FROM quizzes WHERE is_custom = FALSE ORDER BY quiz_id ASC")
        self.preloaded_quizzes = mycursor.fetchall()

        for quiz in self.preloaded_quizzes:
            Button(self.assignments_window, text=quiz[1], height="2", bg="green yellow", width="30",
                   command=lambda q_id=quiz[0]: self.start_quiz(q_id)).pack(pady=5)

        # Separator label for custom quizzes
        Label(self.assignments_window, text="Or select a custom quiz:", height="2").pack()

        # Fetch custom quiz topics from the database for the dropdown, which are either public or created by the own user
        mycursor.execute(
        "SELECT quiz_id, title FROM quizzes WHERE user_id = %s OR is_public = 1 ORDER BY quiz_id ASC",
        (self.user_id,)
    )
        self.custom_quizzes = mycursor.fetchall()

        # Create a combobox for custom quizzes
        self.quiz_combobox = ttk.Combobox(self.assignments_window, state="readonly", 
                                          values=[q[1] for q in self.custom_quizzes], width=27)
        self.quiz_combobox.pack(pady=5)
        Label(self.assignments_window, text="").pack()

        # Button to start the selected custom quiz
        Button(self.assignments_window, text="Start Custom Quiz", height="2", bg="light sky blue", width="30",
               command=self.start_selected_custom_quiz).pack()



   def manage_quizzes(self):
        self.manage_quizzes_window = Toplevel(self.master)
        self.manage_quizzes_window.geometry("600x400")
        self.manage_quizzes_window.title("Manage Quizzes")
        Label(menu, text="").pack()
        Label(self.manage_quizzes_window, text="Manage Quizzes", width="300", height="2", font=("Blackadder ITC", 25)).pack()

        # Button for adding a new quiz
        Button(self.manage_quizzes_window, text="Create New Quiz", height = "4", bg="LightCyan2", width = "60",command=self.create_new_quiz).pack()
        Label(self.manage_quizzes_window, text="").pack()

        #Create a dropdown menu which will display the custom quizzes owned by the user
        mycursor.execute("SELECT quiz_id, title FROM quizzes WHERE user_id = %s", (self.user_id,))
        self.custom_quizzes = mycursor.fetchall()

        # Define the quiz_combobox before calling fetch_and_setup_quiz_combobox
        self.quiz_combobox = ttk.Combobox(self.manage_quizzes_window, state="readonly", width=27)
        self.fetch_and_setup_quiz_combobox()  # Now you can safely call this method
        self.quiz_combobox.pack(pady=5)
        Label(self.manage_quizzes_window, text="").pack()

        # Buttons for editing and deleting a quiz
        Button(self.manage_quizzes_window, text="Edit selected quiz", height="2", bg="LightYellow2", width="30", command=self.edit_selected_quiz).pack()
        Label(self.manage_quizzes_window, text="").pack()
        Button(self.manage_quizzes_window, text="Delete selected quiz", height="2", bg="IndianRed1", width="30", command=self.delete_selected_quiz).pack()

   def fetch_and_setup_quiz_combobox(self):
         # Fetch quizzes from the database
        mycursor.execute("SELECT quiz_id, title FROM quizzes WHERE user_id = %s", (self.user_id,))
        self.custom_quizzes = mycursor.fetchall()

    # Reset the dictionary mapping quiz titles to their ids
        self.quiz_title_id_map = {}

    # Create a list of titles for the Combobox, and populate the map
        combobox_values = []
        for quiz_id, title in self.custom_quizzes:
        # Use the title as the key, and the quiz_id as the value
            self.quiz_title_id_map[title] = quiz_id
            combobox_values.append(title)

    # Update the Combobox with these values
        self.quiz_combobox['values'] = combobox_values
        self.quiz_combobox.set('')

    # Update the Combobox with these values
        self.quiz_combobox['values'] = combobox_values
        self.quiz_combobox.set('')

        # This method will be used to update the quiz combobox dynamically in the same window

   def update_quiz_combobox(self):

    # Fetch updated list of quizzes
    mycursor.execute("SELECT quiz_id, title FROM quizzes WHERE user_id = %s", (self.user_id,))
    self.custom_quizzes = mycursor.fetchall()
    
    # Clear the previous map and repopulate it with the new values
    self.quiz_title_id_map.clear()
    for quiz_id, title in self.custom_quizzes:
        self.quiz_title_id_map[title] = quiz_id

    # Set the combobox to display only quiz titles
    self.quiz_combobox['values'] = [title for _, title in self.custom_quizzes]
    self.quiz_combobox.set('')

   def fetch_quiz_data(self, quiz_id):
    # Fetch the quiz details
    try:
        mycursor.execute("SELECT title, is_public FROM quizzes WHERE quiz_id = %s", (quiz_id,))
        quiz_details = mycursor.fetchone()

        mycursor.execute("SELECT question_id, question_text, option_1, option_2, option_3, option_4, correct_option FROM questions WHERE quiz_id = %s ORDER BY question_id ASC", (quiz_id,))
        questions = mycursor.fetchall()

        return (quiz_details, questions)
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

   def edit_selected_quiz(self):
    selected_title = self.quiz_combobox.get()
    if not selected_title:
        messagebox.showinfo("Edit Quiz", "Please select a quiz to edit.")
        return
    
    selected_quiz_id = self.quiz_title_id_map.get(selected_title)
    if not selected_quiz_id:
        messagebox.showinfo("Edit Quiz", "Please select a valid quiz to edit.")
        return

    quiz_data = self.fetch_quiz_data(selected_quiz_id)  # Call fetch_quiz_data here
    if quiz_data:
        self.editing_quiz_id = selected_quiz_id  # Set the quiz ID here
        self.create_edit_quiz_window(quiz_data, selected_quiz_id)
    else:
        messagebox.showerror("Error", "Failed to fetch quiz data for editing.")

   def create_edit_quiz_window(self, quiz_data, quiz_id):
        quiz_details, questions = quiz_data
        self.create_quiz_window = Toplevel(self.manage_quizzes_window)
        self.create_quiz_window.geometry("1022x572")  
        self.create_quiz_window.title("Edit Quiz")


        # Initialize the StringVar and IntVar before setting their values
        self.quiz_title = StringVar(self.create_quiz_window)
        self.is_public_var = IntVar(self.create_quiz_window)
    
        self.quiz_title.set(quiz_details[0])
        self.is_public_var.set(quiz_details[1])

        Label(self.create_quiz_window, text="Quiz Title:").grid(row=0, column=0, columnspan=2)
        Entry(self.create_quiz_window, textvariable=self.quiz_title).grid(row=0, column=2, sticky="ew", columnspan=8)


        public_checkbutton = Checkbutton(
            self.create_quiz_window,
            text="Make this quiz public",
            variable=self.is_public_var
        )
        public_checkbutton.grid(row=7, columnspan=10)

        # This will create a ? icon where hovering 
        help_image = Image.open("help-icon.png")
        help_image.thumbnail((16, 16))  # ensure 'help-icon.png' is in the same folder
        help_photo = ImageTk.PhotoImage(help_image)
        help_label = Label(self.create_quiz_window, image=help_photo)
        help_label.image = help_photo  # keep a reference to the image
        help_label.grid(row=0, column=10, padx=5, pady=5)

        # Create a tooltip for the help icon
        tooltip_text = ("Enter the quiz title in the box on top.\n"
                        "\n"
                        "The first box in each row is for the question,\n"
                        "The rest are for the options.\n"
                        "\n"
                        "Select the correct answer using the buttons on the right.\n"
                        "For instance if the correct answer is option 2, select the button labeled '2'.")
        ToolTip(help_label, text=tooltip_text)

        self.questions = []  # Reset the questions list to populate with existing questions
        for i, question_data in enumerate(questions):
            print(f"Debug: Question {i+1} data: {question_data}")  # This will print the question data
            question_id = question_data[0]
            question_text = question_data[1]  # index 1 for question_text
            options_texts = question_data[2:6]  # options start from index 2 to 5
            correct_answer = question_data[6]  # index 6 for correct_option

            Label(self.create_quiz_window, text=f"Q{i+1}:").grid(row=i+1, column=0)
            question_entry = Entry(self.create_quiz_window)
            question_entry.insert(0, question_text)
            question_entry.grid(row=i+1, column=1, sticky="ew")

            options = []
            correct_answer_var = IntVar(self.create_quiz_window, value=correct_answer)
            for j, option_text in enumerate(options_texts):
                option_entry = Entry(self.create_quiz_window)
                option_entry.insert(0, option_text)
                option_entry.grid(row=i+1, column=j+2, sticky="ew")
                options.append(option_entry)

                # Create a radio button for each option
                Radiobutton(self.create_quiz_window, text=str(j+1), variable=correct_answer_var, value=j+1).grid(row=i+1, column=j+6)

            self.questions.append((question_id, question_entry, options, correct_answer_var))

        Button(self.create_quiz_window, text="Save Quiz", command=self.save_updated_quiz).grid(row=6, column=0, columnspan=10)

        # Ensure all columns have the same weight so they distribute space evenly
        for j in range(10):
            self.create_quiz_window.grid_columnconfigure(j, weight=1)

        # Adjust the window's row and column configuration for proper spacing
        self.create_quiz_window.grid_rowconfigure(0, weight=1)
        for i in range(1, 6):
            self.create_quiz_window.grid_rowconfigure(i, weight=3)

   def save_updated_quiz(self):
    title = self.quiz_title.get()
    is_public = self.is_public_var.get()  
    quiz_id = self.editing_quiz_id

    if not title:
        messagebox.showerror("Error", "Please enter a quiz title.")
        return

    # Prepare data for update
    question_data = []
    for question_info in self.questions:
        question_id, question_entry, options, correct_answer_var = question_info  # Unpack 4 values
        question_text = question_entry.get()
        if not question_text or not all(option.get() for option in options):
            messagebox.showerror("Error", "Please fill in all fields for questions and options.")
            return

        correct_option = correct_answer_var.get()
        if not correct_option:
            messagebox.showerror("Error", "Please select a correct option for each question.")
            return

        option_texts = [option.get() for option in options]
        question_data.append((question_id, question_text, option_texts, correct_option))

    # Start a transaction
    mycursor.execute("START TRANSACTION")

    try:
        # Update the quiz title and privacy
        mycursor.execute("UPDATE quizzes SET title = %s, is_public = %s WHERE quiz_id = %s", (title, is_public, quiz_id))

        # Update questions linked to the quiz_id using their question_id
        for question_id, question_text, options, correct_option in question_data:
            mycursor.execute("""
                UPDATE questions SET question_text = %s, option_1 = %s, option_2 = %s, option_3 = %s, option_4 = %s, correct_option = %s
                WHERE quiz_id = %s AND question_id = %s
                """, (question_text, *options, correct_option, quiz_id, question_id))
            print(question_id, question_text, options, correct_option, quiz_id)

        # Commit the transaction if everything is successful
        db.commit()
        messagebox.showinfo("Success", "The quiz has been updated successfully.")
        self.update_quiz_combobox()
    except mysql.connector.Error as err:
        # Rollback if there are any errors
        db.rollback()
        messagebox.showerror("Database Error", f"Failed to update quiz: {err}")
    finally:
        # Close the quiz editing window
        self.create_quiz_window.destroy()

   def delete_selected_quiz(self):
    # Get the selected quiz ID from the dropdown
    selected_title = self.quiz_combobox.get()

    # Check if a quiz is selected
    if not selected_title:
        messagebox.showinfo("Delete Quiz", "Please select a quiz to delete.")
        return

    selected_quiz_id = self.quiz_title_id_map.get(selected_title)
    print(selected_title)


    # Begin transaction
    mycursor.execute("START TRANSACTION;")

    try:
        # Delete related scores
        mycursor.execute("DELETE FROM scores WHERE quiz_id = %s", (selected_quiz_id,))
        
        # Delete related questions
        mycursor.execute("DELETE FROM questions WHERE quiz_id = %s", (selected_quiz_id,))
        
        # Delete the quiz
        mycursor.execute("DELETE FROM quizzes WHERE quiz_id = %s", (selected_quiz_id,))
        
        db.commit()
        
        self.update_quiz_combobox()

        # Show confirmation message
        messagebox.showinfo("Delete Quiz", "Quiz and associated data deleted successfully.")
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        messagebox.showerror("Delete Quiz", f"An error occurred: {e}")

           


        # This method will allow the user to make their own quiz

   def create_new_quiz(self):
        self.create_quiz_window = Toplevel(self.manage_quizzes_window)
        self.create_quiz_window.geometry("1022x572")  # Adjust size as needed
        self.create_quiz_window.title("Create Quiz")
        self.is_public_var = IntVar()
        self.quiz_title = StringVar()
        Label(self.create_quiz_window, text="Quiz Title:").grid(row=0, column=0, columnspan=2)
        Entry(self.create_quiz_window, textvariable=self.quiz_title).grid(row=0, column=2, sticky="ew", columnspan=8)
        public_checkbutton = Checkbutton(
            self.create_quiz_window,
            text="Make this quiz public",
            variable=self.is_public_var
        )
        public_checkbutton.grid(row=7, columnspan=10)

        # This will create a ? icon where hovering 
        help_image = Image.open("help-icon.png")
        help_image.thumbnail((16, 16))  # ensure 'help-icon.png' is in the same folder
        help_photo = ImageTk.PhotoImage(help_image)
        help_label = Label(self.create_quiz_window, image=help_photo)
        help_label.image = help_photo  # keep a reference to the image
        help_label.grid(row=0, column=10, padx=5, pady=5)

        # Create a tooltip for the help icon
        tooltip_text = ("Enter the quiz title in the box on top.\n"
                        "\n"
                        "The first box in each row is for the question,\n"
                        "The rest are for the options.\n"
                        "\n"
                        "Select the correct answer using the buttons on the right.\n"
                        "For instance if the correct answer is option 2, select the button labeled '2'.")
        ToolTip(help_label, text=tooltip_text)

        self.questions = []  # This will hold the question and options entries
        for i in range(5):
            Label(self.create_quiz_window, text=f"Q{i+1}:").grid(row=i+1, column=0)
            question_entry = Entry(self.create_quiz_window)
            question_entry.grid(row=i+1, column=1, sticky="ew")

            options = []
            correct_answer_var = IntVar()
            for j in range(4):
                option_entry = Entry(self.create_quiz_window)
                option_entry.grid(row=i+1, column=j+2, sticky="ew")
                options.append(option_entry)

                Radiobutton(self.create_quiz_window, text=f"{j+1}", variable=correct_answer_var, value=j+1).grid(row=i+1, column=j+6)

            self.questions.append((question_entry, options, correct_answer_var))

        Button(self.create_quiz_window, text="Save Quiz", command=self.save_new_quiz).grid(row=6, column=0, columnspan=10)

        # Ensure all columns have the same weight so they distribute space evenly
        for j in range(10):
            self.create_quiz_window.grid_columnconfigure(j, weight=1)

        # Adjust the window's row and column configuration for proper spacing
        self.create_quiz_window.grid_rowconfigure(0, weight=1)
        for i in range(1, 6):
            self.create_quiz_window.grid_rowconfigure(i, weight=3)


        # This method will be used to validate and save the new quiz to the database
   def save_new_quiz(self):
    title = self.quiz_title.get()
    if not title:
        messagebox.showerror("Error", "Please enter a quiz title.")
        return

    # Prepare data for insertion
    question_data = []
    for question_entry, options, correct_answer_var in self.questions:
        question_text = question_entry.get()
        if not question_text or not all(option.get() for option in options):
            messagebox.showerror("Error", "Please fill in all fields for questions and options.")
            return

        correct_option = correct_answer_var.get()
        if not correct_option:
            messagebox.showerror("Error", "Please select a correct option for each question.")
            return

        option_texts = [option.get() for option in options]
        question_data.append((question_text, option_texts, correct_option))

    # Start a transaction
    mycursor.execute("START TRANSACTION")

    try:
        # Insert the quiz title and privacy and get the quiz_id
        is_public = self.is_public_var.get()  # This gets the value from the checkbutton
        mycursor.execute("INSERT INTO quizzes (title, is_custom, is_public, user_id) VALUES (%s, TRUE, %s, %s)", (title, is_public, self.user_id))  #is_custom should always be TRUE
        quiz_id = mycursor.lastrowid  # Get the auto-incremented ID

        # Insert questions linked to the quiz_id
        for question, options, correct_option in question_data:
            mycursor.execute("""
                INSERT INTO questions (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (quiz_id, question, *options, correct_option))

        # Commit the transaction if everything is successful
        db.commit()
        messagebox.showinfo("Success", "The new quiz has been saved.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to save quiz: {err}")
        # Rollback if there are any errors
        db.rollback()
    finally:
        # Close the quiz creation window
        self.create_quiz_window.destroy()    


   def start_selected_custom_quiz(self):
        selected_quiz_title = self.quiz_combobox.get()
        quiz_id = None
        for id, title in self.custom_quizzes:
            if title == selected_quiz_title:
                quiz_id = id
                break
        
        if quiz_id is not None:
            self.start_quiz(quiz_id)   

   def start_quiz(self, quiz_id):
        self.current_quiz_id = quiz_id
        mycursor.execute("SELECT question_text, option_1, option_2, option_3, option_4, correct_option FROM questions WHERE quiz_id = %s", (quiz_id,))
        self.questions = mycursor.fetchall()
        self.mark = [0] * len(self.questions)  # Initialize scores for all questions
        self.question_scores = [None] * len(self.questions)  # Initialize answer tracking
        self.question_index = 0
        self.load_question(self.question_index)
        self.assignments_window.destroy()
        menu.withdraw()


   def load_question(self, question_index):
        if hasattr(self, 'quiz'):
            self.quiz.destroy()
        
        self.quiz = Toplevel()
        self.quiz.geometry("1100x250")
        self.quiz.title("Quiz Question")
        
        self.current_question = self.questions[question_index]
        self.question_index = question_index

        # Set up the question text and options
        question_text = self.current_question[0]
        options = self.current_question[1:5]
        correct_option = self.current_question[5]

        self.var = StringVar(value=question_text)
        Label(self.quiz, textvariable=self.var, width="250", height="2", font=("Verdana", 13)).pack()
        
        self.var1 = IntVar(value=self.question_scores[question_index] if self.question_scores[question_index] is not None else 0)
        Label(self.quiz, text="Select an answer:").pack(anchor='w')

        for i, option in enumerate(options, start=1):
            Radiobutton(self.quiz, text=option, variable=self.var1, value=i).pack(anchor='w')

        Button(self.quiz, text="Submit", height="2", bg="DeepSkyBlue3", fg="black", width="30", command=self.submit).pack()

        if question_index > 0:
            Button(self.quiz, text="Back", height="2", bg="IndianRed1", fg="black", width="30", command=self.go_back).pack(pady=5)
        
        self.quiz.protocol("WM_DELETE_WINDOW", self.close_application)

   def go_back(self):
    if self.previous_questions:
        last_question_index = self.previous_questions.pop()  # Pop only the index from the stack
        self.load_question(last_question_index)

   # Define a method to submit quiz answers, which checks whether the answers submitted are right or wrong
   def submit(self):
    selected_option = self.var1.get()
    if selected_option == 0:
        messagebox.showwarning("No Selection", "Please select an option.")
        return
    
    # Update score and selected option tracking
    if selected_option == self.current_question[5]:
        self.mark[self.question_index] = 20  # Assume each question scores 20 points
    else:
        self.mark[self.question_index] = 0
    
    self.question_scores[self.question_index] = selected_option

    # Navigate to next question or finalize quiz
    if self.question_index < len(self.questions) - 1:
        self.previous_questions.append(self.question_index)  # Push only the index onto the stack
        self.load_question(self.question_index + 1)
    else:
        self.finalize_quiz()

   def finalize_quiz(self):
    total_score = sum(self.mark)
    self.mark = []  # Reset the marks for the next quiz
    self.quiz.destroy()  # Close the quiz window

    try:
        mycursor.execute("INSERT INTO scores (user_id, quiz_id, score) VALUES (%s, %s, %s)", (self.user_id,self.current_quiz_id, total_score))
        db.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to insert score: {err}")
        db.rollback()

    self.submit_scores(total_score)  # Show the results to the user



   # Define a method to display the submitted score
   def submit_scores(self, total_score):
       self.after_quiz = Toplevel()
       self.after_quiz.geometry("350x250")
       self.after_quiz.title("Submitted Mark")
       Label(self.after_quiz, text="Thank You, your score is:", width="300", height="2", font=("Calibri", 13)).pack()
       Label(self.after_quiz, text=str(total_score) + "%", width="300", height="2", font=("Calibri", 13)).pack()
       Label(self.after_quiz, text="Your score will update now with the database", width="300", height="2",
             font=("Calibri", 13)).pack()
       #Button to allow the user to return to the dashboard
       Button(self.after_quiz, text="Return to Dashboard", width="20", height="2", command=self.return_to_dashboard).pack()

       
    # This method will destroy the after_quiz window and open the dashboard menu
   def return_to_dashboard(self):
    
    self.after_quiz.destroy()
    self.menu()
    
    # Extract scores from query results

   def fetch_scores(self, user_id):
    mycursor.execute("""
    SELECT q.title, s.score 
    FROM scores s
    INNER JOIN quizzes q ON s.quiz_id = q.quiz_id
    WHERE s.user_id = %s 
    """, (user_id,))
    return mycursor.fetchall()  # This will return a list of tuples (quiz_title, score)  
   
   # Define a method to display a summary of previous scores
   def summary(self):

    # Fetches list of tuples with (quiz_title, score)
    scored_quizzes = self.fetch_scores(self.user_id)
    scores = [score for _, score in scored_quizzes]
    average = sum(scores) / len(scores) if scores else 0
    summary_window = Toplevel()
    summary_window.geometry("610x720")
    summary_window.title("Analytics")

    # Sort dropdown
    Label(summary_window, text="Sort by:", width=10, height=2, font=("Calibri", 12)).pack(side="top", anchor='nw')

    self.sort_var = StringVar()
    sort_options = ttk.Combobox(summary_window, width=10, textvariable=self.sort_var)
    sort_options['values'] = ('Ascending', 'Descending')
    sort_options.pack(side="top", anchor='nw')
    sort_options.bind("<<ComboboxSelected>>", lambda event: self.update_display(scored_quizzes, summary_window, average))

    # Initial display update
    self.update_display(scored_quizzes, summary_window, average)

   def on_sort_selection(self, scored_quizzes, window, average):
        self.update_display(self.merge_sort(scored_quizzes, self.sort_var.get() == 'Ascending'), window, average)
    
    
    # This method will be used for ordering the scores according to the user's choice, using merge sort

   def merge_sort(self, scores, ascending=True):
    # Check if the list is longer than 1 element, else return the list as it is.
    if len(scores) > 1:
        # Find the midpoint of the list to divide it into two halves.
        mid = len(scores) // 2
        left_half = scores[:mid]  
        right_half = scores[mid:]  

        # Use of recursion to sort both halves
        self.merge_sort(left_half, ascending)
        self.merge_sort(right_half, ascending)

        i = j = k = 0

        # Merge the two halves back into scores
        while i < len(left_half) and j < len(right_half):
            if ascending:
                if left_half[i][1] < right_half[j][1]:
                    scores[k] = left_half[i]
                    i += 1
                else:
                    scores[k] = right_half[j]
                    j += 1
            else:
                if left_half[i][1] > right_half[j][1]:
                    scores[k] = left_half[i]
                    i += 1
                else:
                    scores[k] = right_half[j]
                    j += 1
            k += 1

        # If there are remaining elements in left_half, add them to the scores list.
        while i < len(left_half):
            scores[k] = left_half[i]
            i += 1
            k += 1

        # If there are remaining elements in right_half, add them to the scores list.
        while j < len(right_half):
            scores[k] = right_half[j]
            j += 1
            k += 1

    
    return scores


   def update_display(self, scored_quizzes, window, average):
    sort_order = self.sort_var.get()
    self.merge_sort(scored_quizzes, ascending=(sort_order == "Ascending"))

    for widget in window.pack_slaves():
        widget.destroy()

    content_frame = Frame(window)
    content_frame.pack(fill="both", expand=True)

    scores_frame = Frame(content_frame)
    scores_frame.pack(side="left", fill="y")

    Label(scores_frame, text="Scores:", font=("Calibri", 13, "bold")).pack(anchor="w")
    for index, (quiz_title, score) in enumerate(scored_quizzes):
        Label(scores_frame, text=f"{quiz_title}: {score}%", font=("Calibri", 13)).pack(anchor="w")

    graph_frame = Frame(content_frame)
    graph_frame.pack(side="left", fill="both", expand=True)

    # Average score label, moved to the top-right
    avg_score_label = Label(graph_frame, text=f"Average score: {average:.2f}%", font=("Calibri", 13, "bold"))
    avg_score_label.pack(side="top", anchor='e')

    self.show_grades_graph(scored_quizzes, graph_frame)


   # Define a method to display a bar graph of scores
   def show_grades_graph(self, scored_quizzes, frame):
    # Determine graph width based on the number of scores
    graph_width = max(300, len(scored_quizzes) * 50)  # At least 300 pixels or dynamic based on scores
    canvas = Canvas(frame, width=graph_width, height=300)
    canvas.pack(side="top", fill="x", expand=True)

    bar_width = 55
    padding = 20
    spacing = 10
    max_score = max(score for _, score in scored_quizzes) if scored_quizzes else 1

    for i, (quiz_title, score) in enumerate(scored_quizzes):
        x1 = padding + i * (bar_width + spacing)
        y1 = 280 - (score / max_score) * 250  # Scale score to canvas height
        x2 = x1 + bar_width
        y2 = 280  # Base line for scores
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        canvas.create_text(x1 + bar_width / 2, y1 - 10, text=f"{score}%", anchor="s")
        canvas.create_text(x1 + bar_width / 2, y2 + 10, text=quiz_title, anchor="n", width=bar_width)

    canvas.create_line(padding, 280, graph_width - padding, 280)  # Base line for graph
    canvas.create_text(padding, 280, text="0%", anchor="s", angle=90)
    canvas.create_text(padding, 30, text=f"{max_score}%", anchor="s", angle=90)


# Check if the script is being run directly
if __name__ == "__main__":
   root = Tk()
   app = QuizApp(root)
   root.mainloop()
