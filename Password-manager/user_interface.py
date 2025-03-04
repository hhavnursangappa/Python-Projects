# Import necessary modules
import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import ttkbootstrap as btk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from PIL import ImageTk, Image

import sys
import subprocess
import markdown
import random
import pyperclip
from functools import partial

from sql_setup import Database

db = Database()  # Instantiate the database object


class UserInterface:
	"""Class definition for the first window that appears when the application is booted."""

	def __init__(self):
		"""Constructor for the User Interface class."""

		self.root = btk.Window(themename="cyborg")
		self.root.title("Welcome")
		self.root.protocol("WM_DELETE_WINDOW", self.close_all_windows)
		self.root.iconbitmap(".\\icons\\key_icon.ico")
		self.root.geometry("1200x650")
		self.root.bind('<Return>', self.command_login_password_vault)
		self.root.option_add('*font', 'Consolas 12')
		self.root.option_add('*Dialog.msg.font', 'Consolas 12')

		logo = Image.open("images/password_manager.png")
		logo = ImageTk.PhotoImage(logo)

		self.all_entries = []
		self.checkbox_list = []
		self.check_var_list = []

		left_frame = tk.Frame(self.root)
		left_frame.pack(side='left')

		logo_image = Image.open("images/password_manager.png").resize((610, 650))
		logo_image = ImageTk.PhotoImage(logo_image)

		logo_label = tk.Label(left_frame, image=logo_image)
		logo_label.pack(side='top', fill=BOTH, expand=True)

		right_frame = tk.Frame(self.root)
		right_frame.pack(side='right')

		right_top_frame = tk.Frame(self.root)
		right_top_frame.pack(side='top')

		welcome_label = tk.Label(right_top_frame, text="Welcome to your \nPassword manager !", font=('Constantia', 26))
		welcome_label.pack(side='top', padx=5, pady=25)

		description_label = tk.Label(right_top_frame, text="\nYour personal vault to manage all your \npasswords in one place.\n\nOne password to remember them all !!!",
									font=('Constantia', 16))
		description_label.pack(side='top', padx=5, pady=5)

		prompt_label = tk.Label(right_top_frame, text="\nEnter Master Password:", justify="left", font=('Constantia', 14))
		prompt_label.pack(side='top', padx=15, pady=5, anchor="w")

		self.login_password_field = tk.Entry(right_top_frame, width=450, font=('Constantia', 14), show=u'•')
		self.login_password_field.pack(side='top', padx=15, pady=5)

		right_bottom_frame = tk.Frame(self.root)
		right_bottom_frame.pack(side='top')

		login_button = tk.Button(right_bottom_frame, text="Login", width=12, font=('Constantia', 14), command=partial(self.command_login_password_vault, None))
		login_button.pack(side='left', padx=5, pady=35)

		self.master_data_empty = db.sql_is_master_table_empty()
		if self.master_data_empty:
			create_btn = tk.Button(right_bottom_frame, text="Create Vault", width=15, font=('Constantia', 14), command=self.open_create_vault_window)
			create_btn.pack(side='left', padx=5, pady=35)

		self.center_position_window(self.root)

		self.root.mainloop()

	def open_vault_login_window(self):
		"""Function callback for the 'Login' button on the boot up window."""

		self.login_window = tk.Toplevel()
		self.login_window.iconbitmap(".\\icons\\key_icon.ico")
		self.login_window.title("Vault Login")
		self.login_window.geometry("600x400")
		self.login_window.grab_set()
		self.login_window.bind('<Return>', self.command_login_password_vault)

		frame = tk.Frame(self.login_window)
		frame.pack(side='top')

		prompt_label = tk.Label(frame, text="Enter master password to login", font=('Constantia', 14))
		prompt_label.pack(side='top', padx=5, pady=5)

		# self.login_password_field = tk.Entry(frame, show='*', width=15)
		# self.login_password_field.pack(side='top', padx=5, pady=5)

		login_button = tk.Button(frame, text="Login", width=10, command=partial(self.command_login_password_vault, None))
		login_button.pack(side='top', padx=5, pady=5)

		self.center_position_window(self.login_window)

	def command_login_password_vault(self, _):
		"""Function callback for the 'Login' button on the 'Vault Login' window."""

		# self.master_data_empty = db.sql_is_master_table_empty()
		if not self.master_data_empty:
			master_pwd = db.sql_return_master_password()
			read_pwd = str(self.login_password_field.get())
			user_can_login = False
			attempt = 0

			while not user_can_login:
				if read_pwd != master_pwd:
					if attempt < 3:
						read_pwd = simpledialog.askstring(title="Login Failed", prompt=f"Wrong password. Attempts left: {3 - attempt}. \nPlease try again: ", show=u'•')
						if read_pwd is not None:
							attempt += 1
						else:
							self.login_window.destroy()
							break
					else:
						messagebox.showinfo(title="Login Failed", message="You have exhausted your attempts. \nThe application is going to terminate now.")
						self.close_all_windows()
				else:
					user_can_login = True

			if user_can_login:
				self.root.withdraw()
				messagebox.showinfo(title="Login Successful", message="You have successfully logged in", parent=self.root)
				self.function_show_password_table()

		else:
			messagebox.showwarning("Login Failed", "You have not yet created a vault. Create one by entering the master password")
			self.open_create_vault_window()

	def open_create_vault_window(self):
		"""Function to create a password vault if the entered master password does not exist."""

		self.create_master_password_window = tk.Toplevel()
		self.create_master_password_window.iconbitmap(".\\icons\\key_icon.ico")
		self.create_master_password_window.title("Create New Vault")
		self.create_master_password_window.geometry("600x280")
		self.create_master_password_window.grab_set()
		self.create_master_password_window.focus()
		self.create_master_password_window.protocol("WM_DELETE_WINDOW", self.close_all_windows)
		self.create_master_password_window.bind('<Return>', self.command_create_password_vault)

		frame = tk.Frame(self.create_master_password_window)
		frame.pack(side='top')

		prompt_label = tk.Label(frame, text="\nEnter master password for the new vault", font=('Constantia', 14), justify="left")
		prompt_label.pack(side='top', padx=5, pady=5, anchor="w")

		self.create_master_password_field = tk.Entry(frame, show=u'•', width=30, font=('Constantia', 14), background="#fff")
		self.create_master_password_field.pack(side='top', padx=5, pady=15)

		create_btn = tk.Button(frame, text="Create", width=10, font=('Constantia', 14), command=partial(self.command_create_password_vault, None))
		create_btn.pack(side='top', padx=5, pady=15)

		self.create_master_password_window.update()
		self.center_position_window(self.create_master_password_window)

	def command_create_password_vault(self, _):
		"""Function callback for the 'Create' button on the 'Create Vault' window."""

		db.sql_remove_all_values()
		db.sql_create_master_password_table(self.create_master_password_field.get())
		messagebox.showinfo("Vault creation successful", "A Vault has been successfully created for you")
		self.create_master_password_window.destroy()
		self.function_show_password_table()

	def function_show_password_table(self):
		"""Function to show the password table after entering the master password / creating a new vault."""

		self.root.withdraw()
		try:
			self.create_master_password_window.destroy()
		except AttributeError:
			pass

		self.password_table_window = tk.Toplevel()
		self.password_table_window.iconbitmap(".\\icons\\key_icon.ico")
		self.password_table_window.title("Password Manager")
		self.password_table_window.geometry("1200x650")
		self.password_table_window.focus()
		self.password_table_window.protocol("WM_DELETE_WINDOW", self.close_all_windows)

		top_frame = ScrolledFrame(master=self.password_table_window, height=400)
		top_frame.pack(side='top', padx=(20, 20), pady=(20, 20), fill=tk.BOTH)

		bottom_frame = tk.Frame(self.password_table_window)
		bottom_frame.pack(side='top')

		# Define columns in the TreeView
		column_headings = ('SL.NO.', 'WEBSITE', 'USERNAME', 'PASSWORD')
		self.password_table = ttk.Treeview(master=top_frame, columns=column_headings, padding=0, show='headings', selectmode='browse', height=14)
		self.password_table.pack(side='top', anchor='nw', fill=tk.BOTH)

		# Format columns in the tree view
		self.password_table.column("SL.NO.", width=100, anchor='center', stretch=NO)
		self.password_table.column("WEBSITE", anchor='center')
		self.password_table.column("USERNAME", anchor='center')
		self.password_table.column("PASSWORD", anchor='center')
		self.password_table.update()

		# Bind the left and right click actions to functions
		self.password_table.bind('<ButtonRelease-1>', self.password_table_focus)
		self.password_table.bind('<Button-3>', self.create_right_click_menu)

		# Insert headings in to the tree view widget
		for heading in column_headings:
			self.password_table.heading(heading, text=heading)

		# Adjust the row height tree view widget
		row_style = ttk.Style()
		row_style.configure('Treeview', rowheight=45, font=('Consolas', 12))
		row_style.configure('Treeview.Heading', font=('Constantia', 14))
		row_style.map('Treeview', background=[('selected', '#ff79c6')])

		# Add the buttons
		self.show_passwords_button = tk.Button(master=bottom_frame, text="Show passwords", width=15, font=('Constantia', 12), command=self.command_show_or_hide_passwords)
		self.show_passwords_button.grid(row=0, column=0, padx=10, pady=(20, 10))

		add_credentials_button = tk.Button(bottom_frame, text="Add credentials", width=15, font=('Constantia', 12), command=self.open_add_credentials_window)
		add_credentials_button.grid(row=0, column=1, padx=10, pady=(20, 10))

		change_master_key_button = tk.Button(bottom_frame, text="Change Master Password", width=22, font=('Constantia', 12), command=self.open_change_master_password_window)
		change_master_key_button.grid(row=0, column=2, padx=10, pady=(20, 10))

		delete_all_button = tk.Button(bottom_frame, text="Delete all", width=15, font=('Constantia', 12), command=self.open_delete_all_credentials_window)
		delete_all_button.grid(row=1, column=0, padx=10, pady=10)

		logout_button = tk.Button(bottom_frame, text="Logout", width=15, font=('Constantia', 12), command=self.open_logout_window)
		logout_button.grid(row=1, column=1, padx=10, pady=10)

		logout_button = tk.Button(bottom_frame, text="Help", width=15, font=('Constantia', 12), command=self.open_help_documentation)
		logout_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

		self.function_update_password_table()

		# Assign alternating colors to rows of the table
		self.password_table.tag_configure('odd_row', background='#282a36')
		# self.password_table.tag_configure('even_row', background='white')

		self.password_table_window.update()
		self.center_position_window(self.password_table_window)

	def function_update_password_table(self, refresh=False, mask=True):
		"""Function callback to update the password table."""

		values_to_insert = db.sql_return_all_values()
		self.all_entries = values_to_insert
		tags = 'odd_row'
		row_id = 0

		if refresh:
			self.password_table.delete(*self.password_table.get_children())

		for idx, values in enumerate(values_to_insert):
			row_id += 1
			if mask or (mask is None):
				self.password_table.insert("", "end", iid=str(row_id), values=(values[0], values[1], values[2], '*' * len(values[3])), tags=(tags,))
				self.show_passwords_button.configure(text="Show passwords")
			else:
				self.password_table.insert("", "end", iid=str(row_id), values=(values[0], values[1], values[2], values[3]), tags=(tags,))
				self.show_passwords_button.configure(text="Hide passwords")
			tags = 'even_row' if tags == 'odd_row' else 'odd_row'
			self.password_table_window.update()

	def command_show_or_hide_passwords(self):
		"""Function callback for the 'Show Passwords' button on the 'Password Manager' window."""

		text = self.show_passwords_button.cget("text")
		self.password_table.delete(*self.password_table.get_children())

		if text == "Show passwords":
			self.function_update_password_table(mask=False)
			# self.show_passwords_button.configure(text="Hide passwords")
		elif text == "Hide passwords":
			self.function_update_password_table(mask=True)
			# self.show_passwords_button.configure(text="Show passwords")

	def open_add_credentials_window(self):
		"""Function callback for the 'Add Credentials' button on the 'Password Manager' window."""

		self.add_entry_window = tk.Toplevel()
		self.add_entry_window.iconbitmap(".\\icons\\key_icon.ico")
		self.add_entry_window.title("Add Credentials")
		self.add_entry_window.bind('<Return>', self.command_add_credentials)

		add_website_label = tk.Label(self.add_entry_window, text="Enter the website", font=('Constantia', 12))
		add_website_label.grid(row=0, column=0, padx=(20, 5), pady=(30, 10), sticky='w')

		self.add_website_field = tk.Entry(self.add_entry_window, font=('Constantia', 12))
		self.add_website_field.grid(row=0, column=1, columnspan=2, padx=(5, 20), pady=(30, 10), sticky='ew')

		add_username_label = tk.Label(self.add_entry_window, text="Enter the username", font=('Constantia', 12))
		add_username_label.grid(row=1, column=0, padx=(20, 5), pady=5, sticky='w')

		self.add_username_field = tk.Entry(self.add_entry_window, font=('Constantia', 12))
		self.add_username_field.grid(row=1, column=1, columnspan=2, padx=(5, 20), pady=5, sticky='ew')

		add_password_label = tk.Label(self.add_entry_window, text="Enter the password", font=('Constantia', 12))
		add_password_label.grid(row=2, column=0, padx=(20, 5), pady=10, sticky='w')

		self.add_password_field = tk.Entry(self.add_entry_window, font=('Constantia', 12))
		self.add_password_field.grid(row=2, column=1, columnspan=2, padx=(5, 20), pady=10, sticky='ew')

		add_button = tk.Button(self.add_entry_window, text='Add', font=('Constantia', 12), command=partial(self.command_add_credentials, None))
		add_button.grid(row=3, column=0, padx=(20, 5), pady=(20, 20), sticky='ew')

		generate_password_button = tk.Button(self.add_entry_window, text='Generate Password', width=20, font=('Constantia', 12), command=partial(self.command_generate_password, "add"))
		generate_password_button.grid(row=3, column=1, padx=5, pady=(20, 20), sticky='ew')

		cancel_button = tk.Button(self.add_entry_window, text='Cancel', width=10, font=('Constantia', 12), command=lambda: self.add_entry_window.destroy())
		cancel_button.grid(row=3, column=2, padx=(5, 20), pady=(20, 20), sticky='ew')

		self.center_position_window(self.add_entry_window)

	def command_add_credentials(self, _):
		"""Function callback for the 'Add' button on the 'Add Credentials' window."""
		self.add_entry_window.withdraw()

		web = str(self.add_website_field.get())
		username = str(self.add_username_field.get())
		password = str(self.add_password_field.get())

		table_exists = db.is_password_table()
		if table_exists:
			sl_no = db.sql_return_serial_number()
		else:
			sl_no = 1

		db.sql_create_password_table(sl_no=sl_no, website=web, username=username, password=password)
		messagebox.showinfo("Added Credentials", "The password has been successfully added to the vault")
		self.function_update_password_table(refresh=True)
		self.password_table_window.wait_window()

	def command_generate_password(self, field_type):
		"""Function callback for the 'Generate Password' button on the 'Add Credentials' window."""
		lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		spl_char = ['!', '§', '$', '%', '&', '/', '(', ')', '=', '?']

		num_lower_case = 4
		num_upper_case = 4
		num_numbers = 3
		num_spl_char = 3

		password = []

		# Random selection of lower case letters
		for ii in range(num_lower_case + 1):
			char = random.choice(lower_case)
			password.append(char)

		# Random selection of upper case letters
		for ii in range(num_upper_case + 1):
			char = random.choice(upper_case)
			password.append(char)

		# Random selection of numbers
		for ii in range(num_numbers + 1):
			char = random.choice(numbers)
			password.append(char)

		# Random selection of special characters
		for ii in range(num_spl_char + 1):
			char = random.choice(spl_char)
			password.append(char)

		# Shuffle the password
		random.shuffle(password)
		password = ''.join(password)

		if field_type == "add":
			self.add_password_field.delete('0', tk.END)
			self.add_password_field.insert('0', string=password)
		elif field_type == "update":
			self.update_password_field.delete('0', tk.END)
			self.update_password_field.insert('0', string=password)

	def open_change_master_password_window(self):
		"""Function callback for the 'Change Master Password' button on the 'Password Manager' window."""
		self.change_master_passkey_window = tk.Toplevel()
		self.change_master_passkey_window.iconbitmap(".\\icons\\key_icon.ico")
		self.change_master_passkey_window.title("Change the master password")
		self.change_master_passkey_window.bind('<Return>', self.command_change_master_password)

		current_password_label = tk.Label(master=self.change_master_passkey_window, text="Enter the current master password", font=('Constantia', 12))
		current_password_label.grid(row=0, column=0, padx=(20, 5), pady=(30, 10), sticky='w')

		self.current_pass_field = tk.Entry(self.change_master_passkey_window, font=('Constantia', 12))
		self.current_pass_field.grid(row=0, column=1, padx=(5, 20), pady=(30, 10), sticky='ew')

		new_password_label = tk.Label(master=self.change_master_passkey_window, text="Enter the new master password", font=('Constantia', 12))
		new_password_label.grid(row=1, column=0, padx=(20, 5), pady=5, sticky='w')

		self.new_password_field = tk.Entry(self.change_master_passkey_window, font=('Constantia', 12))
		self.new_password_field.grid(row=1, column=1, padx=(5, 20), pady=5, sticky='ew')

		confirm_password_label = tk.Label(master=self.change_master_passkey_window, text="Confirm the new master password", font=('Constantia', 12))
		confirm_password_label.grid(row=2, column=0,  padx=(20, 5), pady=10, sticky='e')

		self.confirm_password_field = tk.Entry(self.change_master_passkey_window, font=('Constantia', 12))
		self.confirm_password_field.grid(row=2, column=1, padx=(5, 20), pady=10, sticky='ew')

		change_password_button = tk.Button(self.change_master_passkey_window, text='Change Master Password', font=('Constantia', 12), command=partial(self.command_change_master_password, None))
		change_password_button.grid(row=3, column=0, padx=(20, 5), pady=(20, 20), sticky='ew')

		cancel_button = tk.Button(self.change_master_passkey_window, text='Cancel', font=('Constantia', 12), command=lambda: self.change_master_passkey_window.destroy())
		cancel_button.grid(row=3, column=1, padx=(5, 20), pady=(20, 20), sticky='ew')

		self.center_position_window(self.change_master_passkey_window)

	def command_change_master_password(self, _):
		"""Function callback for the 'Change Master Password' button on the 'Change the master password' window."""

		current_master_password = str(self.current_pass_field.get())
		new_master_password = str(self.new_password_field.get())
		confirm_master_pwd = str(self.confirm_password_field.get())
		master_password = db.sql_return_master_password()
		if current_master_password == master_password:
			if confirm_master_pwd == new_master_password:
				if new_master_password != current_master_password:
					res = db.sql_update_master_pwd(new_master_password)
					if res:
						messagebox.showinfo("Change master password", "Master password changed successfully !")
						self.change_master_passkey_window.destroy()
					else:
						messagebox.showwarning("Change master password", "There was a problem changing the password.")
						self.change_master_passkey_window.wait_window()
				else:
					messagebox.showwarning("Change master password", "The old and the new password cannot be same. \nPlease enter a unique password")
					self.change_master_passkey_window.wait_window()
			else:
				messagebox.showwarning("Change master password", "The confirmed password doesnt match the new password. Please check")
				self.change_master_passkey_window.wait_window()
		else:
			messagebox.showwarning("Change master password", "Please enter the current master password correctly\n")
			self.change_master_passkey_window.wait_window()

	def open_delete_all_credentials_window(self):
		"""Function callback for the 'Delete all' button on the 'Password Manager' window."""

		ans = messagebox.askyesnocancel("Delete all credentials", "Are you sure you want to delete all credentials and clear the vault?")
		if ans:
			db.sql_remove_all_values()
			self.function_update_password_table(refresh=True)
		else:
			self.password_table_window.wait_window()

	def open_logout_window(self):
		"""Function callback for the 'Logout' button on the 'Password Manager' window."""

		ans = messagebox.askyesnocancel('Logout', 'Are you sure you want to log out of the vault')
		if ans:
			self.close_all_windows()
			messagebox.showinfo('Logout', 'Goodbye! Have a nice day ahead')
		else:
			self.password_table_window.wait_window()

	@staticmethod
	def open_help_documentation():
		"""Function callback for the 'Help' button on the 'Password manager' window."""
		help_filename = "README.html"
		# for path, directory, file in os.walk('.'):
		# 	if file != help_filename:
		# 		with open('README.md', 'r', encoding='cp1252') as markdown_file:
		# 			markdown_string = markdown_file.read()
		# 			markdown_file.close()
		#
		# 		html_string = markdown.markdown(markdown_string)
		#
		# 		with open(help_filename, 'w') as html_file:
		# 			html_file.write(html_string)
		# 			html_file.close()
		# 	else:
		subprocess.popen("help_filename")

	def create_right_click_menu(self, event):
		"""Function to create the right-click menu when right-clicked on the table entries."""

		row = self.password_table.identify_row(event.y)
		self.password_table.selection_set(row)
		column = self.password_table.identify_column(event.x)
		# self.update_or_delete = self.password_table.item(row)['values']
		right_click_menu = tk.Menu(self.password_table_window, tearoff=0)
		right_click_menu.add_command(label='Update', command=lambda: self.open_update_credentials_window(row), font=('Constantia', 12))
		right_click_menu.add_command(label='Delete', command=lambda: self.open_delete_credentials(row), font=('Constantia', 12))
		right_click_menu.add_command(label='Copy', command=lambda: self.command_copy_credentials(row, column), font=('Constantia', 12))
		right_click_menu.tk_popup(event.x_root, event.y_root)

	def open_update_credentials_window(self, row):
		"""Function callback for the 'Update' option in the right-click context menu."""

		entry_idx = int(row[-1]) - 1
		entry = self.all_entries[entry_idx]

		self.update_credentials_window = tk.Toplevel()
		self.update_credentials_window.title = "Update Credentials"
		self.update_credentials_window.iconbitmap(".\\icons\\key_icon.ico")
		self.update_credentials_window.bind('<Return>', lambda: self.update_button_command(event=None, idx=entry_idx))

		update_website_label = tk.Label(self.update_credentials_window, text="Updated website")
		update_website_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

		self.update_website_field = tk.Entry(self.update_credentials_window)
		self.update_website_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
		self.update_website_field.insert(0, entry[1])

		update_user_label = tk.Label(self.update_credentials_window, text="Updated username")
		update_user_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

		self.update_user_field = tk.Entry(self.update_credentials_window)
		self.update_user_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
		self.update_user_field.insert(0, entry[2])

		update_password_label = tk.Label(self.update_credentials_window, text="Updated password")
		update_password_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

		self.update_password_field = tk.Entry(self.update_credentials_window)
		self.update_password_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
		self.update_password_field.insert(0, entry[3])

		update_button = tk.Button(self.update_credentials_window, text='Update', command=lambda: self.command_update_credentials(entry_idx))
		update_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

		generate_password_button = tk.Button(self.update_credentials_window, text='Generate New Password', command=partial(self.command_generate_password, "update"))
		generate_password_button.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

		cancel_button = tk.Button(self.update_credentials_window, text='Cancel', command=lambda: self.update_credentials_window.destroy())
		cancel_button.grid(row=3, column=2, padx=5, pady=5, sticky='ew')

		self.center_position_window(self.update_credentials_window)

	def command_update_credentials(self, idx):
		"""Function callback for the 'Update' button on the 'Update Credentials' window."""
		entry_to_update = self.all_entries[idx]
		res = db.sql_update_credentials(sl_num=entry_to_update[0], new_website=self.update_website_field.get(),
										new_username=self.update_user_field.get(), new_password=self.update_password_field.get())
		if res:
			messagebox.showinfo("Credentials updated", "Your credentials have been updated")
			self.update_credentials_window.destroy()
			self.function_update_password_table(refresh=True)
		else:
			messagebox.showwarning("Credentials update failed", "Your credentials couldn't be updated")
		self.password_table_window.wait_window()

	def open_delete_credentials(self, row):
		"""Function callback for the 'Delete' option in the right-click context menu."""

		entry_idx = int(row[-1]) - 1
		entry_to_delete = self.all_entries[entry_idx]
		ans = messagebox.askyesnocancel("Delete Entry", "Are you sure you want to delete the entry:\n [ " + ', '.join(entry_to_delete[1:]) + " ]?")
		if ans:
			sl_no_to_remove = entry_to_delete[0]
			res = db.sql_remove_values(sl_no_to_remove)
			if res:
				messagebox.showinfo("Credential Deleted", "The entry [ " + ', '.join(entry_to_delete[1:]) + " ] has been successfully deleted.")
				self.function_update_password_table(refresh=True)
				self.password_table_window.wait_window()
			else:
				messagebox.showwarning("Credential Delete Failed", "The entry [ " + ', '.join(entry_to_delete[1:]) + " ] couldn't be deleted.")
				self.password_table_window.wait_window()
		else:
			self.password_table_window.wait_window()

	def command_copy_credentials(self, row, column):
		"""Function callback for the 'Copy' option in the right-click context menu."""

		column = int(column[-1]) - 1
		row = int(row[-1]) - 1
		text_to_copy = self.all_entries[row][column]
		pyperclip.copy(str(text_to_copy))

	@staticmethod
	def center_position_window(window):
		"""Function to center a given window on the main screen."""
		window_width = window.winfo_reqwidth()
		window_height = window.winfo_reqheight()

		position_x = int((window.winfo_screenwidth() / 2) - (window_width / 2))
		position_y = int((window.winfo_screenheight() / 2) - (window_height / 2))

		window.geometry(f"+{position_x}+{position_y}")
		window.resizable(False, False)

	def close_all_windows(self):
		"""Function to close all windows after logout / after pressing the 'X' button."""
		for widget in self.root.winfo_children():
			if isinstance(widget, tk.Toplevel):
				widget.destroy()
		messagebox.showinfo('Exit', 'Goodbye! Have a nice day ahead')
		self.root.destroy()
		sys.exit()

	# List of Functions bound to the '<Return>' event
	def password_table_focus(self, event):
		"""Function bound to the left mouse click event."""
		self.password_table.focus()

	def update_button_command(self, event, idx):
		self.command_update_credentials(idx)


# Main Function
if __name__ == '__main__':
	ui = UserInterface()
