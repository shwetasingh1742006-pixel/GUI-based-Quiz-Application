import tkinter as tk
from tkinter import messagebox
from auth import login, register
from quiz_engine import get_categories, get_questions, save_result
from email_service import send_result
import re

def is_valid_username(username):
    pattern = r'^[A-Z][a-zA-Z ]+$'
    return re.match(pattern, username)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Quiz System")
        self.root.configure(bg="#eaeaee")

        # Window center
        w, h = 700, 600
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.user = None
        self.login_screen()

    def clear(self):

        # STOP running timer
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)

        for w in self.root.winfo_children():
            w.destroy()

    # ---------------- LOGIN ----------------
    def login_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg="#2c2f4a")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

        tk.Label(frame, text="Login", font=("Arial", 26, "bold"),
                 bg="#2c2f4a", fg="white").pack(pady=20)

        tk.Label(frame, text="Username",font=("Arial",14,"bold"),bg="#2c2f4a", fg="white").pack()
        self.u = tk.Entry(frame, width=25,font=("Arial",14))
        self.u.pack(pady=8)

        tk.Label(frame, text="Password",font=("Arial",14,"bold"),bg="#2c2f4a", fg="white").pack()
        self.p = tk.Entry(frame, show="*", width=25,font=("Arial",14))
        self.p.pack(pady=8)

        tk.Button(frame, text="Login",font=("Arial",14,"bold"),bg="#4CAF50", fg="white",
                  width=18,height=2, command=self.do_login).pack(pady=5)

        tk.Button(frame, text="Register",font=("Arial",14,"bold"),bg="#2196F3", fg="white",
                  width=18,height=2, command=self.register_screen).pack()

    # ---------------- REGISTER ----------------
    def register_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg="#2c2f4a")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

        tk.Label(frame, text="Register", font=("Arial", 26, "bold"),
                 bg="#2c2f4a", fg="white").pack(pady=20)

        tk.Label(frame, text="Username",font=("Arial",14,"bold"),bg="#2c2f4a", fg="white").pack()
        self.ru = tk.Entry(frame,font=("Arial",14))
        self.ru.pack(pady=5)

        tk.Label(frame, text="Email",font=("Arial",14,"bold"), bg="#2c2f4a", fg="white").pack()
        self.re = tk.Entry(frame,font=("Arial",14))
        self.re.pack(pady=8)

        tk.Label(frame, text="Password",font=("Arial",14,"bold"),bg="#2c2f4a", fg="white").pack()
        self.rp = tk.Entry(frame, show="*",font=("Arial",14))
        self.rp.pack(pady=8)

        tk.Button(frame, text="Submit",font=("Arial",14,"bold"), bg="#FF9800", fg="white",
                  width=18,height=2, command=self.do_register).pack(pady=15)

    def do_register(self):

        username = self.ru.get()
        email = self.re.get()
        password = self.rp.get()

        # 1. Empty check
        if username == "" or email == "" or password == "":
           messagebox.showerror("Error", "All fields are required")
           return

        print("[DEBUG] Fields received OK")

        # 2. Username validation
        if not is_valid_username(username):
            messagebox.showerror(
                "Wrong Format",
                "Username must start with capital letter and contain only alphabets"
            )
            print("[ERROR] Invalid username format")
            return

        # 3. Email validation
        if not is_valid_email(email):
           messagebox.showerror("Wrong Email", "Invalid email format")
           print("[ERROR] Invalid email format")
           return

        print("[DEBUG] Validation passed, calling register()")

        # 4. Register DB call
        result = register(username, email, password)

        print("[DEBUG] Register result:", result)

        # 5. Result handling
        if result == "success":
           messagebox.showinfo("Success", "Registration Successful")
           print("[INFO] User registered successfully")

        elif result == "email_exists":
             messagebox.showerror("Error", "Email already registered")
             print("[ERROR] Email already exists")

        elif result == "weak_password":
             messagebox.showerror("Error", "Password must be at least 6 characters")
             print("[ERROR] Weak password")

        else:
            messagebox.showerror("Error", str(result))
            print("[ERROR]", result)

        # 6. Go to login
        self.login_screen()
    
    def do_login(self):
        user = login(self.u.get(), self.p.get())
        if user:
            self.user = user
            self.category_screen()

    # ---------------- CATEGORY ----------------
    def category_screen(self):
        self.clear()

        tk.Label(self.root, text="Select Category",
                 font=("Arial", 24, "bold"),
                 fg="#2c2f4a", bg="#f0f0f0").pack(pady=30)

        colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#E91E63"]
        cats = get_categories()

        for i, (cid, name) in enumerate(cats):
            tk.Button(
                self.root,
                text=name,
                font=("Arial", 16, "bold"),
                bg=colors[i % len(colors)],
                fg="white",
                width=20,
                height=2,
                bd=0,
                command=lambda c=cid: self.start_quiz(c)
            ).pack(pady=10)

    # ---------------- QUIZ ----------------
    def start_quiz(self, category_id):
        self.category_id = category_id
        self.questions = get_questions(category_id)

        self.index = 0
        self.score = 0
        self.timer = 60

        self.quiz_screen()

    def quiz_screen(self):
        self.clear()
        self.root.configure(bg="#f5f5f5")

        # Question
        self.q_label = tk.Label(
             self.root,
             font=("Arial", 18, "bold"),
             bg="#1B1A1A",
             fg="white",
             wraplength=600,
            padx=10,
            pady=10
        )
        self.q_label.pack(pady=20)

        # Options frame
        self.option_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.option_frame.pack()

        self.opts = []
        self.selected = None

        for i in range(4):
            btn = tk.Button(
                self.option_frame,
                text="",
                font=("Arial", 14, "bold"),
                bg="#7CFC00",
                fg="black",
                width=50,
                height=2,
                bd=0,
                cursor="hand2",
                command=lambda i=i: self.select_option(i)
            )
            btn.pack(fill="x", padx=80, pady=6)
            self.opts.append(btn)

        # Timer
        self.timer_label = tk.Label(
            self.root,
            font=("Arial", 14, "bold"),
            bg="#121212",
            fg="yellow"
        )
        self.timer_label.pack(pady=10)

        # Buttons (SIMPLE PACK ONLY)
        self.prev_btn = tk.Button(
            self.root,
            text="Previous",
            font=("Arial", 14, "bold"),
            bg="#FF9800",
            fg="white",
            width=12,
            command=self.prev_q
        )
        self.prev_btn.pack(pady=5)

        self.next_btn = tk.Button(
            self.root,
            text="Next",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self.next_q
        )
        self.next_btn.pack(pady=5)

        self.submit_btn = tk.Button(
            self.root,
            text="Submit",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            width=12,
            command=self.finish
        )
        self.submit_btn.pack(pady=5)

        self.load_q()
        self.countdown()

    
    def load_q(self):

        if self.index >= len(self.questions):
           return

        q = self.questions[self.index]

        self.q_label.config(text=q[0])

        for i in range(4):
         self.opts[i].config(text=q[i+1], bg="#7CFC00")

        self.selected = None
        self.timer = 60

        # Previous button hide/show
        if self.index == 0:
            self.prev_btn.config(state="disabled")
        else:
            self.prev_btn.config(state="normal")

        # Last question
        if self.index == len(self.questions) - 1:
             
            self.next_btn.pack_forget()
            self.submit_btn.pack(pady=5)
            
        else:
            
            self.submit_btn.pack_forget()
            self.next_btn.pack(pady=5)

    def countdown(self):

        # STOP if label doesn't exist
        if not hasattr(self, "timer_label"):
            return

        try:
            self.timer_label.config(text=f"Time: {self.timer}")
        except:
            return

        if self.timer > 0:
           self.timer -= 1
           self.timer_id = self.root.after(1000, self.countdown)
        else:
           self.next_q()
    
    def next_q(self):

        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)

        if self.index >= len(self.questions):
            return

        options = ["a", "b", "c", "d"]

        correct = self.questions[self.index][5]

        if self.selected is not None:
           if options[self.selected] == correct:
               self.score += 1

        self.index += 1

        if self.index < len(self.questions):
           self.load_q()
           self.countdown()
        else:
           self.finish()
    
    def prev_q(self):

        if self.index > 0:

          if hasattr(self, "timer_id"):
             self.root.after_cancel(self.timer_id)

          self.index -= 1

          self.load_q()
          self.countdown()
        
    def select_option(self, index):
        self.selected = index

        for btn in self.opts:
            btn.config(bg="#7CFC00")

        self.opts[index].config(bg="#32CD32")

    def finish(self):
        
         # ✅ STEP 3: STOP TIMER HERE (IMPORTANT)
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id) 
        
        save_result(
            self.user[0],
            self.score,
            len(self.questions),
            self.category_id
        )

        self.clear()

        self.root.configure(bg="#f5f5f5")

        # Result Heading
        tk.Label(
           self.root,
           text="Quiz Completed",
           font=("Arial", 24, "bold"),
           fg="green",
           bg="#f5f5f5"
        ).pack(pady=20)

        # Score
        tk.Label(
           self.root,
           text=f"Your Score: {self.score}/{len(self.questions)}",
           font=("Arial", 20, "bold"),
           bg="#f5f5f5"
        ).pack(pady=10)

        # Acknowledgement
        if self.score >= len(self.questions)//2:
           msg = "Excellent Performance 🎉"
        else:
           msg = "Good Try 👍 Keep Practicing"

        tk.Label(
          self.root,
          text=msg,
          font=("Arial", 18),
          fg="blue",
          bg="#f5f5f5"
        ).pack(pady=15)

        # Buttons
        tk.Button(
          self.root,
          text="Go To Home",
          font=("Arial", 14, "bold"),
          bg="#FF9800",
          fg="white",
          width=20,
          command=self.login_screen
        ).pack(pady=10)

        tk.Button(
          self.root,
          text="Choose Another Category",
          font=("Arial", 14, "bold"),
          bg="#4CAF50",
          fg="white",
          width=25,
          command=self.category_screen
        ).pack(pady=10)
        
        tk.Button(
          self.root,
          text="Send Result On Email",
          font=("Arial", 14, "bold"),
          bg="#2196F3",
          fg="white",
          width=25,
          command=lambda: send_result(
               self.user[2],
               self.score,
               len(self.questions)
          )
        ).pack(pady=10)
    
# Run App
root = tk.Tk()
app = QuizApp(root)
root.mainloop()