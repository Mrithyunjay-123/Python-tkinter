from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

root = Tk()
root.title("Student Database")
root.iconbitmap("F:/Python/Icons/Student.ico")
root.geometry("1410x550")


conn = sqlite3.connect("StudentData.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS student (
		ID integer,
		Name text,
		Grade integer,
		Section text,
		RollNo integer,
		Age integer,
		Gender text,
		ParentsName text,
		ParentsNo integer,
		Address text
	)""")	

conn.commit()
conn.close()


style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#D3D3D3", foreground='black', rowheight=25, fieldbackground="D3D3D3")
style.map('Treeview', background=[('selected', "#347083")])

tree_frame = Frame(root)
tree_frame.pack(pady=10)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

tree_scroll.config(command=my_tree.yview)

my_tree['columns'] = ("ID", "Name", "Grade", "Section", "RollNo", "Age", "Gender", "ParentsName", "ParentsNo", "Address")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=140)
my_tree.column("Name", anchor=CENTER, width=140)
my_tree.column("Grade", anchor=CENTER, width=140)
my_tree.column("Section", anchor=CENTER, width=140)
my_tree.column("RollNo", anchor=CENTER, width=140)
my_tree.column("Age", anchor=CENTER, width=140)
my_tree.column("Gender", anchor=CENTER, width=140)
my_tree.column("ParentsName", anchor=CENTER, width=140)
my_tree.column("ParentsNo", anchor=CENTER, width=140)
my_tree.column("Address", anchor=CENTER, width=140)

my_tree.heading("#0", text="", anchor=CENTER)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)
my_tree.heading("Grade", text="Grade", anchor=CENTER)
my_tree.heading("Section", text="Section", anchor=CENTER)
my_tree.heading("RollNo", text="Roll No", anchor=CENTER)
my_tree.heading("Age", text="Age", anchor=CENTER)
my_tree.heading("Gender", text="Gender", anchor=CENTER)
my_tree.heading("ParentsName", text="Parents Name", anchor=CENTER)
my_tree.heading("ParentsNo", text="Parents No", anchor=CENTER)
my_tree.heading("Address", text="Address", anchor=CENTER)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")



def query_our_database():
	conn = sqlite3.connect("StudentData.db")
	c = conn.cursor()


	c.execute("SELECT rowid, * FROM student")
	records = c.fetchall()

	global count
	count = 0

	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index="end", iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=("evenrow",))
		else:
			my_tree.insert(parent='', index="end", iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=("oddrow",))

		count += 1

	conn.commit()
	conn.close()

def Select(e):
	TextID.delete(0, END)
	TextName.delete(0, END)
	TextGrade.delete(0, END)
	TextSection.delete(0, END)
	TextRollNo.delete(0, END)
	TextAge.delete(0, END)
	TextGender.delete(0, END)
	TextParentsName.delete(0, END)
	TextParentsNo.delete(0, END)
	TextAddress.delete(0, END)

	selected = my_tree.focus()
	values = my_tree.item(selected, 'values')

	TextID.insert(0, values[0])
	TextName.insert(0, values[1])
	TextGrade.insert(0, values[2])
	TextSection.insert(0, values[3])
	TextRollNo.insert(0, values[4])
	TextAge.insert(0, values[5])
	TextGender.insert(0, values[6])
	TextParentsName.insert(0, values[7])
	TextParentsNo.insert(0, values[8])
	TextAddress.insert(0, values[9])


def clearTextBox():
	TextID.delete(0, END)
	TextName.delete(0, END)
	TextGrade.delete(0, END)
	TextSection.delete(0, END)
	TextRollNo.delete(0, END)
	TextAge.delete(0, END)
	TextGender.delete(0, END)
	TextParentsName.delete(0, END)
	TextParentsNo.delete(0, END)
	TextAddress.delete(0, END)

def delete():
	x = my_tree.selection()[0]
	my_tree.delete(x)

	conn = sqlite3.connect("StudentData.db")
	c = conn.cursor()

	c.execute("DELETE FROM student WHERE oid=" + TextID.get())

	conn.commit()
	conn.close()

	clearTextBox()

	messagebox.showinfo("Deleted !", "Your record has been deleted")

def deleteAll():
	for record in my_tree.get_children():
		my_tree.delete(record)

def update():
	# Grab the record number
	selected = my_tree.focus()
	# Update record
	my_tree.item(selected, text="", values=(TextID.get(), TextName.get(), TextGrade.get(), TextSection.get(), TextRollNo.get(), TextAge.get(), TextGender.get(), TextParentsName.get(), TextParentsNo.get(), TextAddress.get(),))

	conn = sqlite3.connect("StudentData.db")
	c = conn.cursor()

	c.execute("""UPDATE student SET
			Name = :NAME,
			Grade = GRADE,
			Section = SECTION,
			RollNo = ROLLNO,
			Age = AGE,
			Gender = GENDER,
			ParentsName = PARENTSNAME,
			ParentsNo = PARENTSNO,
			Address = ADDRESS

			WHERE oid = :oid""",
			{
				'oid' : TextID.get(),
				'NAME': TextName.get(),
				'GRADE': TextGrade.get(),
				'SECTION': TextSection.get(),
				'ROLLNO': TextRollNo.get(),
				'AGE': TextAge.get(),
				'GENDER': TextGender.get(),
				'PARENTSNAME': TextParentsName.get(),
				'PARENTSNO': TextParentsNo.get(),
				'ADDRESS': TextAddress.get()
			}
		)

	conn.commit()
	conn.close()

	TextID.delete(0, END)
	TextName.delete(0, END)
	TextGrade.delete(0, END)
	TextSection.delete(0, END)
	TextRollNo.delete(0, END)
	TextAge.delete(0, END)
	TextGender.delete(0, END)
	TextParentsName.delete(0, END)
	TextParentsNo.delete(0, END)
	TextAddress.delete(0, END)

def addRecord():
	conn = sqlite3.connect("StudentData.db")
	c = conn.cursor()

	c.execute("INSERT INTO student VALUES (:id, :name, :grade, :section, :rollno, :age, :gender, :parentsname, :parentsno, :address)",
			{
				'id' : TextID.get(),
				'name': TextName.get(),
				'grade': TextGrade.get(),
				'section': TextSection.get(),
				'rollno': TextRollNo.get(),
				'age': TextAge.get(),
				'gender': TextGender.get(),
				'parentsname': TextParentsName.get(),
				'parentsno': TextParentsNo.get(),
				'address': TextAddress.get()
			}
		)

	conn.commit()
	conn.close()

	TextID.delete(0, END)
	TextName.delete(0, END)
	TextGrade.delete(0, END)
	TextSection.delete(0, END)
	TextRollNo.delete(0, END)
	TextAge.delete(0, END)
	TextGender.delete(0, END)
	TextParentsName.delete(0, END)
	TextParentsNo.delete(0, END)
	TextAddress.delete(0, END)

	my_tree.delete(*my_tree.get_children())

	query_our_database()


data_frame = LabelFrame(root, text="Record Data")
data_frame.pack(fill="x", padx=20, expand='yes')

IDLabel = Label(data_frame, text="ID")
TextID = Entry(data_frame)

NameLabel = Label(data_frame, text="Name")
NameLabel.grid(row=0, column=0, pady=10, padx=10)
TextName = Entry(data_frame)
TextName.grid(row=0, column=1, pady=10, padx=10)

GradeLabel = Label(data_frame, text="Grade")
GradeLabel.grid(row=0, column=2, pady=10, padx=10)
TextGrade = Entry(data_frame)
TextGrade.grid(row=0, column=3, pady=10, padx=10)

SectionLabel = Label(data_frame, text="Section")
SectionLabel.grid(row=0, column=4, pady=10, padx=10)
TextSection = Entry(data_frame)
TextSection.grid(row=0, column=5, pady=10, padx=10)

RollNoLabel = Label(data_frame, text="RollNo")
RollNoLabel.grid(row=0, column=6, pady=10, padx=10)
TextRollNo = Entry(data_frame)
TextRollNo.grid(row=0, column=7, pady=10, padx=10)

AgeLabel = Label(data_frame, text="Age")
AgeLabel.grid(row=0, column=8, pady=10, padx=10)
TextAge = Entry(data_frame)
TextAge.grid(row=0, column=9, pady=10, padx=10)

GenderLabel = Label(data_frame, text="Gender")
GenderLabel.grid(row=1, column=0, pady=10, padx=10)
TextGender = Entry(data_frame)
TextGender.grid(row=1, column=1, pady=10, padx=10)

ParentsNameLabel = Label(data_frame, text="ParentsName")
ParentsNameLabel.grid(row=1, column=2, pady=10, padx=10)
TextParentsName = Entry(data_frame)
TextParentsName.grid(row=1, column=3, pady=10, padx=10)

ParentsNoLabel = Label(data_frame, text="ParentsNo")
ParentsNoLabel.grid(row=1, column=4, pady=10, padx=10)
TextParentsNo = Entry(data_frame)
TextParentsNo.grid(row=1, column=5, pady=10, padx=10)

AddressLabel = Label(data_frame, text="Address")
AddressLabel.grid(row=1, column=6, pady=10, padx=10)
TextAddress = Entry(data_frame)
TextAddress.grid(row=1, column=7, pady=10, padx=10)

button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand='yes', padx=20)


add_button = Button(button_frame, text="Add Record", width=13, command=addRecord)
add_button.grid(row=0, column=0, pady=10, padx=10)

delete_button = Button(button_frame, text="Delete Record", width=13, command=delete)
delete_button.grid(row=0, column=1, pady=10, padx=10)

delete_all_button = Button(button_frame, text="Delete all Record", width=13, command=deleteAll)
delete_all_button.grid(row=0, column=2, pady=10, padx=10)

update_button = Button(button_frame, text="Update Record", width=13, command=update)
update_button.grid(row=0, column=3, pady=10, padx=10)

clear_all_text_box_button = Button(button_frame, text="Clear all text box", width=13, command=clearTextBox)
clear_all_text_box_button.grid(row=0, column=4, pady=10, padx=10)

my_tree.bind("<<TreeviewSelect>>", Select)

query_our_database()

root.mainloop()