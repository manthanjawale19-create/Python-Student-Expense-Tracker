# Smart Student Expense Tracker
# Mini project using python and tkinter

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime

filename = "expenses.csv"
setting_file = "settings.csv"

# list to store all expenses
expense_list = []

student_name = "Student"
monthly_budget = 5000

categories = ["Food", "Transport", "Books", "Hostel", "Recharge", "Fun", "Other"]

# colors for ui
BG = "#f3f6fb"
CARD = "#ffffff"
BLUE = "#2563eb"
DARK = "#0f172a"
GRAY = "#64748b"
LINE = "#e2e8f0"


def load_settings():
    global student_name, monthly_budget
    if os.path.exists(setting_file):
        f = open(setting_file, "r")
        data = f.read().split(",")
        f.close()
        if len(data) >= 2:
            student_name = data[0].strip()
            monthly_budget = float(data[1].strip())


def save_settings():
    f = open(setting_file, "w")
    f.write(student_name + "," + str(monthly_budget))
    f.close()


def load_expenses():
    global expense_list
    expense_list = []
    if os.path.exists(filename) == False:
        return
    f = open(filename, "r")
    reader = csv.reader(f)
    for row in reader:
        if len(row) == 4:
            # skip heading if present
            if row[0] == "date":
                continue
            expense_list.append(row)
    f.close()


def save_expenses():
    f = open(filename, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(["date", "category", "amount", "note"])
    for item in expense_list:
        writer.writerow(item)
    f.close()


def get_month_total():
    total = 0
    now = datetime.now()
    month = now.month
    year = now.year
    for item in expense_list:
        d = item[0]
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            if dt.month == month and dt.year == year:
                total = total + float(item[2])
        except:
            continue
    return total


def refresh_list():
    listbox.delete(0, END)
    for item in expense_list:
        line = "  " + item[0] + "     " + item[1].ljust(12) + "     Rs " + str(item[2]).ljust(8) + "     " + item[3]
        listbox.insert(END, line)
    show_summary()


def show_summary():
    spent = get_month_total()
    left = monthly_budget - spent

    lbl_hello.config(text="Hi, " + student_name)
    lbl_spent_val.config(text="Rs " + str(round(spent, 2)))
    lbl_left_val.config(text="Rs " + str(round(left, 2)))
    lbl_budget_val.config(text="Rs " + str(round(monthly_budget, 2)))

    if monthly_budget > 0:
        percent = (spent / monthly_budget) * 100
    else:
        percent = 0

    if percent > 100:
        bar_val = 100
    else:
        bar_val = percent

    progress["value"] = bar_val
    lbl_percent.config(text=str(int(percent)) + "% of budget used")

    if left < 0:
        lbl_left_val.config(fg="#dc2626")
        lbl_msg.config(text="Budget exceeded. Try to cut extra spending.", fg="#dc2626")
    elif percent > 80:
        lbl_left_val.config(fg="#d97706")
        lbl_msg.config(text="You have used more than 80% of your budget.", fg="#d97706")
    else:
        lbl_left_val.config(fg="#16a34a")
        lbl_msg.config(text="Looking good. You are within budget.", fg="#16a34a")


def add_expense():
    d = e_date.get()
    cat = cat_var.get()
    amt = e_amt.get()
    note = e_note.get()

    if d == "" or amt == "":
        messagebox.showerror("Error", "Please enter date and amount")
        return

    try:
        datetime.strptime(d, "%Y-%m-%d")
    except:
        messagebox.showerror("Error", "Date format should be YYYY-MM-DD")
        return

    try:
        a = float(amt)
        if a <= 0:
            messagebox.showerror("Error", "Amount should be greater than 0")
            return
    except:
        messagebox.showerror("Error", "Enter valid amount")
        return

    expense_list.append([d, cat, str(a), note])
    save_expenses()
    e_amt.delete(0, END)
    e_note.delete(0, END)
    refresh_list()
    messagebox.showinfo("Saved", "Expense added")


def delete_expense():
    sel = listbox.curselection()
    if len(sel) == 0:
        messagebox.showerror("Error", "Select an expense first")
        return
    index = sel[0]
    expense_list.pop(index)
    save_expenses()
    refresh_list()


def save_budget_values(n, b):
    global student_name, monthly_budget
    if n == "" or b == "":
        messagebox.showerror("Error", "Enter name and budget")
        return False
    try:
        val = float(b)
        if val <= 0:
            messagebox.showerror("Error", "Budget should be greater than 0")
            return False
        monthly_budget = val
    except:
        messagebox.showerror("Error", "Budget should be a number")
        return False
    student_name = n
    save_settings()
    e_sname.delete(0, END)
    e_sname.insert(0, student_name)
    e_budget.delete(0, END)
    e_budget.insert(0, str(monthly_budget))
    show_summary()
    messagebox.showinfo("Done", "Budget saved: Rs " + str(monthly_budget))
    return True


def change_budget():
    save_budget_values(e_sname.get(), e_budget.get())


def open_set_budget():
    win = Toplevel(root)
    win.title("Set Budget")
    win.geometry("360x280")
    win.config(bg=CARD)
    win.resizable(False, False)

    Label(win, text="Set Budget", font=("Segoe UI", 14, "bold"), bg=CARD, fg=DARK).pack(pady=(18, 6))
    Label(win, text="Enter your name and monthly pocket money", bg=CARD, fg=GRAY,
          font=("Segoe UI", 9)).pack(pady=(0, 10))

    Label(win, text="Student name", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=24)
    n_entry = Entry(win, font=("Segoe UI", 10), bd=1, relief=SOLID)
    n_entry.pack(fill=X, padx=24, pady=(2, 10), ipady=5)
    n_entry.insert(0, student_name)

    Label(win, text="Monthly budget (Rs)", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=24)
    b_entry = Entry(win, font=("Segoe UI", 10), bd=1, relief=SOLID)
    b_entry.pack(fill=X, padx=24, pady=(2, 16), ipady=5)
    b_entry.insert(0, str(monthly_budget))

    def save_from_win():
        ok = save_budget_values(n_entry.get(), b_entry.get())
        if ok:
            win.destroy()

    Button(win, text="Save Budget", command=save_from_win, bg=BLUE, fg="white",
           font=("Segoe UI", 10, "bold"), bd=0, pady=8, cursor="hand2").pack(fill=X, padx=24)


def show_report():
    now = datetime.now()
    totals = {}
    for c in categories:
        totals[c] = 0

    for item in expense_list:
        try:
            dt = datetime.strptime(item[0], "%Y-%m-%d")
            if dt.month == now.month and dt.year == now.year:
                cat = item[1]
                if cat in totals:
                    totals[cat] = totals[cat] + float(item[2])
                else:
                    totals[cat] = totals[cat] + float(item[2])
        except:
            pass

    msg = "Category wise spending this month:\n\n"
    max_cat = "Other"
    max_val = 0
    for c in categories:
        msg = msg + c + " : Rs " + str(round(totals[c], 2)) + "\n"
        if totals[c] > max_val:
            max_val = totals[c]
            max_cat = c

    spent = get_month_total()
    left = monthly_budget - spent
    msg = msg + "\nTotal spent: Rs " + str(round(spent, 2))
    msg = msg + "\nRemaining: Rs " + str(round(left, 2))

    if max_val > 0:
        msg = msg + "\n\nYou spent most on " + max_cat

    if left < 0:
        msg = msg + "\nTry to spend less next time."

    messagebox.showinfo("Monthly Report", msg)


# ---------- GUI starts here ----------
root = Tk()
root.title("Smart Student Expense Tracker")
root.geometry("1000x640")
root.config(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", padding=4, font=("Segoe UI", 10))
style.configure("bar.Horizontal.TProgressbar", troughcolor=LINE, background=BLUE, thickness=10)

# header
header = Frame(root, bg=BLUE, height=70)
header.pack(fill=X)
header.pack_propagate(False)

Label(header, text="Smart Student Expense Tracker", font=("Segoe UI", 18, "bold"),
      bg=BLUE, fg="white").pack(side=LEFT, padx=24, pady=16)

lbl_hello = Label(header, text="", font=("Segoe UI", 11), bg=BLUE, fg="#dbeafe")
lbl_hello.pack(side=RIGHT, padx=18)

Button(header, text="Set Budget", command=open_set_budget, bg="white", fg=BLUE,
       font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=6, cursor="hand2").pack(side=RIGHT)

# menu option
menubar = Menu(root)
opt_menu = Menu(menubar, tearoff=0)
opt_menu.add_command(label="Set Budget", command=open_set_budget)
opt_menu.add_command(label="Monthly Report", command=show_report)
menubar.add_cascade(label="Options", menu=opt_menu)
root.config(menu=menubar)

# main area
main = Frame(root, bg=BG)
main.pack(fill=BOTH, expand=True, padx=18, pady=16)

left = Frame(main, bg=BG)
left.pack(side=LEFT, fill=BOTH, expand=True)

right = Frame(main, bg=BG, width=300)
right.pack(side=RIGHT, fill=Y, padx=(16, 0))
right.pack_propagate(False)

# add expense card
card1 = Frame(left, bg=CARD, highlightbackground=LINE, highlightthickness=1)
card1.pack(fill=X, pady=(0, 12))

Label(card1, text="Add expense", font=("Segoe UI", 12, "bold"), bg=CARD, fg=DARK).grid(
    row=0, column=0, columnspan=4, sticky=W, padx=16, pady=(14, 8)
)

Label(card1, text="Date", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).grid(row=1, column=0, sticky=W, padx=16)
Label(card1, text="Category", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).grid(row=1, column=1, sticky=W, padx=8)
Label(card1, text="Amount", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).grid(row=1, column=2, sticky=W, padx=8)
Label(card1, text="Note", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).grid(row=1, column=3, sticky=W, padx=8)

e_date = Entry(card1, font=("Segoe UI", 10), bd=1, relief=SOLID, width=14)
e_date.grid(row=2, column=0, padx=16, pady=(0, 8), ipady=5)
today = datetime.now().strftime("%Y-%m-%d")
e_date.insert(0, today)

cat_var = StringVar()
cat_var.set(categories[0])
cat_box = ttk.Combobox(card1, textvariable=cat_var, values=categories, state="readonly", width=14)
cat_box.grid(row=2, column=1, padx=8, pady=(0, 8), ipady=2)

e_amt = Entry(card1, font=("Segoe UI", 10), bd=1, relief=SOLID, width=12)
e_amt.grid(row=2, column=2, padx=8, pady=(0, 8), ipady=5)

e_note = Entry(card1, font=("Segoe UI", 10), bd=1, relief=SOLID, width=22)
e_note.grid(row=2, column=3, padx=8, pady=(0, 8), ipady=5)

btn_row = Frame(card1, bg=CARD)
btn_row.grid(row=3, column=0, columnspan=4, sticky=W, padx=16, pady=(4, 14))

Button(btn_row, text="Add Expense", command=add_expense, bg=BLUE, fg="white",
       font=("Segoe UI", 10, "bold"), bd=0, padx=16, pady=7, cursor="hand2").pack(side=LEFT)

Button(btn_row, text="Delete Selected", command=delete_expense, bg="#fee2e2", fg="#b91c1c",
       font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=7, cursor="hand2").pack(side=LEFT, padx=8)

Button(btn_row, text="Monthly Report", command=show_report, bg="#e0e7ff", fg="#3730a3",
       font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=7, cursor="hand2").pack(side=LEFT)

# list card
card2 = Frame(left, bg=CARD, highlightbackground=LINE, highlightthickness=1)
card2.pack(fill=BOTH, expand=True)

Label(card2, text="All expenses", font=("Segoe UI", 12, "bold"), bg=CARD, fg=DARK).pack(anchor=W, padx=16, pady=(12, 4))
Label(card2, text="Date            Category           Amount              Note",
      bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=16)

f3 = Frame(card2, bg=CARD)
f3.pack(fill=BOTH, expand=True, padx=12, pady=(0, 12))

scroll = Scrollbar(f3)
scroll.pack(side=RIGHT, fill=Y)

listbox = Listbox(f3, yscrollcommand=scroll.set, font=("Consolas", 10), bd=0,
                  highlightthickness=0, fg=DARK, bg="#f8fafc", selectbackground=BLUE,
                  selectforeground="white", activestyle="none")
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scroll.config(command=listbox.yview)

# right side summary cards
def small_card(parent, title):
    box = Frame(parent, bg=CARD, highlightbackground=LINE, highlightthickness=1)
    box.pack(fill=X, pady=(0, 10))
    Label(box, text=title, bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=14, pady=(12, 0))
    val = Label(box, text="Rs 0", bg=CARD, fg=DARK, font=("Segoe UI", 16, "bold"))
    val.pack(anchor=W, padx=14, pady=(2, 12))
    return val

lbl_spent_val = small_card(right, "SPENT THIS MONTH")
lbl_left_val = small_card(right, "REMAINING")
lbl_budget_val = small_card(right, "MONTHLY BUDGET")

card3 = Frame(right, bg=CARD, highlightbackground=LINE, highlightthickness=1)
card3.pack(fill=X, pady=(0, 10))
Label(card3, text="Budget usage", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=14, pady=(12, 6))
progress = ttk.Progressbar(card3, style="bar.Horizontal.TProgressbar", length=250, mode="determinate")
progress.pack(padx=14, fill=X)
lbl_percent = Label(card3, text="0% of budget used", bg=CARD, fg=GRAY, font=("Segoe UI", 9))
lbl_percent.pack(anchor=W, padx=14, pady=(6, 4))
lbl_msg = Label(card3, text="", bg=CARD, font=("Segoe UI", 9), wraplength=250, justify=LEFT)
lbl_msg.pack(anchor=W, padx=14, pady=(0, 12))

card4 = Frame(right, bg=CARD, highlightbackground=LINE, highlightthickness=1)
card4.pack(fill=BOTH, expand=True)
Label(card4, text="Profile & budget", font=("Segoe UI", 11, "bold"), bg=CARD, fg=DARK).pack(anchor=W, padx=14, pady=(12, 8))

Label(card4, text="Your name", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=14)
e_sname = Entry(card4, font=("Segoe UI", 10), bd=1, relief=SOLID)
e_sname.pack(fill=X, padx=14, pady=(2, 8), ipady=5)

Label(card4, text="Monthly budget", bg=CARD, fg=GRAY, font=("Segoe UI", 9)).pack(anchor=W, padx=14)
e_budget = Entry(card4, font=("Segoe UI", 10), bd=1, relief=SOLID)
e_budget.pack(fill=X, padx=14, pady=(2, 10), ipady=5)

Button(card4, text="Save Budget", command=change_budget, bg=DARK, fg="white",
       font=("Segoe UI", 10, "bold"), bd=0, pady=8, cursor="hand2").pack(fill=X, padx=14, pady=(0, 14))

# load old data
load_settings()
load_expenses()
e_sname.insert(0, student_name)
e_budget.insert(0, str(monthly_budget))
refresh_list()

root.mainloop()
