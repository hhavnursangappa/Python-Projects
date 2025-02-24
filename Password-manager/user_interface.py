# Import necessary modules
import sys
import random
import pyperclip
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from functools import partial
from sql_setup import Database

db = Database()  # Instantiate the database object

class UserInterface:
    """Class definition for the first window that appears when the application is booted."""
    def __init__(self):
        """Constructor for the User Interface class."""

        self.root = tk.Tk()
        self.root.title("Hello User")
        self.root.protocol("WM_DELETE_WINDOW", self.close_all_windows)
        self.root.iconbitmap(".\\icons\\key_icon.ico")
        self.all_entries = []
        self.checkbox_list = []
        self.chk_var_list = []

        top_frame = tk.Frame(self.root)
        top_frame.pack(side='top')

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side='top')

        welcome_label = tk.Label(top_frame, text="Welcome to your Password manager")
        welcome_label.pack(side='top', padx=5, pady=5)

        login_btn = tk.Button(bottom_frame, text="Login", width=10, command=self.login_window)
        login_btn.pack(side='left', padx=5, pady=5)

        m_data = db.is_master_data()
        if not m_data:
            create_btn = tk.Button(bottom_frame, text="Create Vault", width=10, command=self.create_password_window)
            create_btn.pack(side='left', padx=5, pady=5)

        self.center_position_window(self.root)

        self.root.mainloop()


    def login_window(self):
        """Function callback for the 'Login' button on the boot up window."""
        self.login_win = tk.Toplevel()
        self.login_win.title("Vault Login")
        self.login_win.grab_set()

        frame = tk.Frame(self.login_win)
        frame.pack(side='top')

        prompt_label = tk.Label(frame, text="Enter master password to login")
        prompt_label.pack(side='top', padx=5, pady=5)

        self.pass_field = tk.Entry(frame, show='*', width=15)
        self.pass_field.pack(side='top', padx=5, pady=5)

        login_btn = tk.Button(frame, text="Login", width=10, command=self.login_password_vault)
        login_btn.pack(side='top', padx=5, pady=5)
        self.login_win.bind('<Return>', self.login_btn_command)  # TODO: Bind the return event to all respective button function calls

        self.center_position_window(self.login_win)


    def login_password_vault(self):
        """Function callback for the 'Login' button on the 'Vault Login' window."""
        m_data = db.is_master_data()
        if m_data:
            m_pwd = db.return_master_password()
            pass_key = str(self.pass_field.get())
            user_can_login = False
            attempt = 0

            while not user_can_login:
                if pass_key != m_pwd:
                    if attempt < 3:
                        pass_key = simpledialog.askstring(title="Login Failed", prompt=f"Wrong password. Attempts left: {3 - attempt}. \nPlease try again: ", show='*')
                        if pass_key is not None:
                            attempt += 1
                        else:
                            self.login_win.destroy()
                            break
                    else:
                        messagebox.showinfo("Login Failed", "You have exhausted your attempts. \nThe application is going to terminate now.")
                        self.close_all_windows()
                else:
                    user_can_login = True

            if user_can_login:
                self.login_win.withdraw()
                self.root.withdraw()
                messagebox.showinfo("Login Successful", "You have successfully logged in")
                self.show_password_table()

        else:
            messagebox.showwarning("Login Failed", "You have not yet created a vault. Create one by entering the master password")
            self.login_win.destroy()
            self.create_password_window()


    def create_password_window(self):
        """Function to create a password vault if the entered master password does not exist."""
        self.pass_win = tk.Toplevel()
        self.pass_win.title("Create Vault")
        self.pass_win.grab_set()
        self.pass_win.protocol("WM_DELETE_WINDOW", self.close_all_windows)
        self.pass_win.bind('<Return>', self.create_btn_command)

        frame = tk.Frame(self.pass_win)
        frame.pack(side='top')

        prompt_label = tk.Label(frame, text="Enter master password")
        prompt_label.pack(side='top', padx=5, pady=5)

        self.pass_field = tk.Entry(frame, show='*', width=15)
        self.pass_field.pack(side='top', padx=5, pady=5)

        create_btn = tk.Button(frame, text="Create", width=10, command=self.create_password_vault)
        create_btn.pack(side='top', padx=5, pady=5)

        self.pass_win.update()
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.pass_win.winfo_reqheight()

        self.pass_win.geometry(f"{windowWidth}x{windowHeight}")

        positionX = int((self.root.winfo_screenwidth() / 2) - (windowWidth / 2))
        positionY = int((self.root.winfo_screenheight() / 2) - (windowHeight / 2))

        self.pass_win.geometry("+{}+{}".format(positionX, positionY))
        self.pass_win.resizable(False, False)


    def create_password_vault(self):
        """Function callback for the 'Create' button on the 'Create Vault' window."""
        db.remove_all_values()
        db.create_master_password_table(self.pass_field.get())
        messagebox.showinfo("Vault creation successful", "A Vault has been successfully created for you")
        self.pass_win.destroy()
        self.show_password_table()


    def show_password_table(self):
        """Function to show the password table after entering the master password / creating a new vault."""
        self.root.withdraw()
        try:
            self.login_win.destroy()
        except AttributeError:
            self.pass_win.destroy()

        self.pass_table_win = tk.Toplevel()
        self.pass_table_win.title("Password Manager")
        self.pass_table_win.protocol("WM_DELETE_WINDOW", self.close_all_windows)

        top_frame = tk.Frame(self.pass_table_win)
        top_frame.pack(side='top', fill='both')

        top_left_frame = tk.Frame(master=top_frame)
        top_left_frame.pack(side='left', pady=0)

        bottom_frame = tk.Frame(self.pass_table_win)
        bottom_frame.pack(side='top')

        # Create scrollbar
        pass_table_scroll = tk.Scrollbar(master=top_frame, orient=tk.VERTICAL)
        pass_table_scroll.pack(side='right', fill='y')

        # Create tree view
        cols = ('SL.NO.', 'WEBSITE', 'USERNAME', 'PASSWORD')
        self.password_table = ttk.Treeview(master=top_left_frame, columns=cols, padding=0, show='headings', selectmode='browse',
                                           yscrollcommand=pass_table_scroll.set, height=3)
        self.password_table.pack(side='top', anchor='nw', padx=5)
        self.password_table.column("SL.NO.", width=45, anchor='center')
        self.password_table.column("WEBSITE", anchor='center')
        self.password_table.column("USERNAME", anchor='center')
        self.password_table.column("PASSWORD", anchor='center')
        self.password_table.update()

        pass_table_scroll.configure(command=self.password_table.yview)
        self.password_table.configure(yscrollcommand=pass_table_scroll.set)
        self.pass_table_win.update()

        # Bind the left and right click actions to functions
        self.password_table.bind('<ButtonRelease-1>', self.return_entry_id)
        self.password_table.bind('<Button-3>', self.create_right_click_menu)

        # Insert headings in to the tree view widget
        for col in cols:
            self.password_table.heading(col, text=col)

        # Adjust the row height tree view widget
        style = ttk.Style(top_left_frame)
        style.configure('Treeview', rowheight=25)

        self.update_password_table()
        self.pass_table_win.update()

        # Assign alternating colors to rows of the table
        self.password_table.tag_configure('odd_row', background='#cfd1d4')
        self.password_table.tag_configure('even_row', background='white')

        # Add the buttons
        self.show_pass_btn = tk.Button(master=bottom_frame, text="Show passwords",  width=15, command=self.show_or_hide_passwords)
        self.show_pass_btn.grid(row=0, column=0, padx=5, pady=5)

        add_entry_btn = tk.Button(bottom_frame, text="Add credentials", width=15, command=self.add_credentials_window)
        add_entry_btn.grid(row=0, column=1, padx=5, pady=5)

        change_mas_pwd_btn = tk.Button(bottom_frame, text="Change master key", width=15, command=self.change_master_password_window)
        change_mas_pwd_btn.grid(row=0, column=2, padx=5, pady=5)

        delete_all_btn = tk.Button(bottom_frame, text="Delete all", width=15, command=self.delete_all_credentials)
        delete_all_btn.grid(row=1, column=0, padx=5, pady=5)

        logout_btn = tk.Button(bottom_frame, text="Logout", width=15, command=self.logout)
        logout_btn.grid(row=1, column=1, padx=5, pady=5)

        self.pass_table_win.update()
        self.center_position_window(self.pass_table_win)


    def update_password_table(self, mask=None):
        """Function callback to update the password table."""
        values_to_insert = db.return_all_values()
        self.all_entries = values_to_insert
        tags = 'odd_row'
        color = '#cfd1d4'
        iid = 0

        for idx, val in enumerate(values_to_insert):
            iid += 1
            if mask or (mask is None):
                self.password_table.insert("", "end", iid=str(iid), values=(val[0], val[1], val[2], '*' * len(val[3])), tags=(tags, ))
            else:
                self.password_table.insert("", "end", iid=str(iid), values=(val[0], val[1], val[2], val[3]), tags=(tags, ))
            tags = 'even_row' if tags == 'odd_row' else 'odd_row'
            self.pass_table_win.update()


    def create_right_click_menu(self, event):
        """Function to create the right-click menu when right-clicked on the table entries."""
        row = self.password_table.identify_row(event.y)
        self.password_table.selection_set(row)
        column = self.password_table.identify_column(event.x)
        # self.update_or_delete = self.password_table.item(row)['values']
        menu = tk.Menu(self.pass_table_win, tearoff=0)
        menu.add_command(label='Update', command=lambda: self.update_credentials_window(row))
        menu.add_command(label='Delete', command=lambda: self.delete_credentials(row))
        menu.add_command(label='Copy', command=lambda: self.copy_data(row, column))
        menu.tk_popup(event.x_root, event.y_root)

    def copy_data(self, row, column):
        """Function callback for the 'Copy' option in the right-click context menu."""
        column = int(column[-1]) - 1
        row = int(row[-1]) - 1
        text_to_copy = self.all_entries[int(row)][column]
        pyperclip.copy(str(text_to_copy))


    def return_entry_id(self, event):
        """Function binded to the left mouse click event."""
        self.password_table.focus()


    def update_credentials_window(self, row):
        """Function callback for the 'Update' option in the right-click context menu."""
        idx = int(row[-1]) - 1
        entry = self.all_entries[idx]

        self.update_cred_win = tk.Toplevel()
        self.update_cred_win.bind('<Return>', lambda: self.update_btn_command(idx))

        update_web_label = tk.Label(self.update_cred_win, text="Updated website")
        update_web_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.update_web_field = tk.Entry(self.update_cred_win)
        self.update_web_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.update_web_field.insert(0, entry[1])

        update_user_label = tk.Label(self.update_cred_win, text="Updated username")
        update_user_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.update_user_field = tk.Entry(self.update_cred_win)
        self.update_user_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.update_user_field.insert(0, entry[2])

        update_pass_label = tk.Label(self.update_cred_win, text="Updated password")
        update_pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.update_pass_field = tk.Entry(self.update_cred_win)
        self.update_pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.update_pass_field.insert(0, entry[3])

        update_btn = tk.Button(self.update_cred_win, text='Update', command=lambda: self.update_credentials(idx))
        update_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.update_cred_win, text='Cancel', command=lambda: self.update_cred_win.destroy())
        cancel_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.center_position_window(self.update_cred_win)


    def update_credentials(self, idx):
        """Function callback for the 'Update' button on the 'Update Credentials' window."""
        entry_to_update = self.all_entries[idx]
        res = db.update_credentials(sl_num=entry_to_update[0], new_web=self.update_web_field.get(),
                                    new_user=self.update_user_field.get(), new_pass=self.update_pass_field.get())
        if res:
            messagebox.showinfo("Credentials updated", "Your credentials have been updated")
            self.update_cred_win.destroy()
            self.refresh_password_table()
        else:
            messagebox.showwarning("Credentials update failed", "Your credentials couldn't be updated")
        self.pass_table_win.wait_window()


    def delete_credentials(self, row):
        """Function callback for the 'Delete' option in the right-click context menu."""
        idx = int(row[-1]) - 1
        entry_to_delete = self.all_entries[idx]
        ans = messagebox.askyesnocancel("Delete Entry", "Are you sure you want to delete the entry:\n [ " + ', '.join(entry_to_delete[1:]) + " ]?")
        if ans:
            sl_no_to_remove = entry_to_delete[0]
            res = db.remove_values(sl_no_to_remove)
            if res:
                messagebox.showinfo("Credential Deleted", "The entry [ " + ', '.join(entry_to_delete[1:]) + " ] has been successfully deleted.")
                self.refresh_password_table()
                self.pass_table_win.wait_window()
            else:
                messagebox.showwarning("Credential Delete Failed", "The entry [ " + ', '.join(entry_to_delete[1:]) + " ] couldn't be deleted.")
                self.pass_table_win.wait_window()
        else:
            self.pass_table_win.wait_window()


    def add_credentials_window(self):
        """Function callback for the 'Add Credentials' button on the 'Password Manager' window."""
        self.cred_win = tk.Toplevel()
        self.cred_win.title("Add Credentials")
        self.cred_win.title = 'Add a new entry'
        self.cred_win.bind('<Return>', self.add_btn_command)

        web_label = tk.Label(self.cred_win, text="Enter the website")
        web_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.web_field = tk.Entry(self.cred_win)
        self.web_field.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        user_label = tk.Label(self.cred_win, text="Enter the username")
        user_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.user_field = tk.Entry(self.cred_win)
        self.user_field.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        pass_label = tk.Label(self.cred_win, text="Enter the password")  # TODO: Insert the parameter show='*'
        pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.pass_field = tk.Entry(self.cred_win)
        self.pass_field.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        add_btn = tk.Button(self.cred_win, text='Add', command=self.add_credentials)
        add_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        gen_pass_btn = tk.Button(self.cred_win, text='Generate Password', command=self.generate_password)
        gen_pass_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.cred_win, text='Cancel', command=lambda: self.cred_win.destroy())
        cancel_btn.grid(row=3, column=2, padx=5, pady=5, sticky='ew')

        self.center_position_window(self.cred_win)


    def add_credentials(self):
        """Function callback for the 'Add' button on the 'Add Credentials' window."""
        self.cred_win.withdraw()

        web = str(self.web_field.get())
        username = str(self.user_field.get())
        password = str(self.pass_field.get())

        table_exists = db.is_password_table()
        if table_exists:
            sl_no = db.return_serial_number()
        else:
            sl_no = 1

        db.create_pwd_table(sl_no, web, username, password)
        messagebox.showinfo("Added Credentials", "The password has been successfully added to the vault")
        self.refresh_password_table()
        self.pass_table_win.wait_window()


    def generate_password(self):
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

        self.pass_field.delete('0', tk.END)
        self.pass_field.insert('0', string=password)

    def delete_all_credentials(self):
        """Function callback for the 'Delete all' button on the 'Password Manager' window."""
        ans = messagebox.askyesnocancel("Delete all credentials", "Are you sure you want to delete all credentials and clear the vault?")
        if ans:
            db.remove_all_values()
            self.refresh_password_table()
        else:
            self.pass_table_win.wait_window()

    def refresh_password_table(self):
        """Function to refresh / reload the password table after changes have been made to the entries."""
        self.password_table.delete(*self.password_table.get_children())
        self.update_password_table()
        if self.show_pass_btn.cget('text') == "Hide passwords":
            self.show_pass_btn.configure(text="Show passwords")

    def change_master_password_window(self):
        """Function callback for the 'Change master key' button on the 'Password Manager' window."""
        self.chng_master_pwd_win = tk.Toplevel()
        self.chng_master_pwd_win.title = "Change the master password"
        self.chng_master_pwd_win.bind('<Return>', self.change_pass_btn_command)

        curr_pass_label = tk.Label(master=self.chng_master_pwd_win, text="Enter the current master password")
        curr_pass_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.curr_pass_field = tk.Entry(self.chng_master_pwd_win)  # TODO: Pass the parameter show='*'
        self.curr_pass_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        new_pass_label = tk.Label(master=self.chng_master_pwd_win, text="Enter the new master password")
        new_pass_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.new_pass_field = tk.Entry(self.chng_master_pwd_win)  # TODO: Pass the parameter show='*'
        self.new_pass_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        conf_pass_label = tk.Label(master=self.chng_master_pwd_win, text="Confirm the new master password")
        conf_pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.conf_pass_field = tk.Entry(self.chng_master_pwd_win)  # TODO: Pass the parameter show='*'
        self.conf_pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        change_pass_btn = tk.Button(self.chng_master_pwd_win, text='Change Master Password', command=self.change_master_password)
        change_pass_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.chng_master_pwd_win, text='Cancel', command=lambda: self.chng_master_pwd_win.destroy())
        cancel_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.center_position_window(self.chng_master_pwd_win)

    def change_master_password(self):
        """Function callback for the 'Change Master Password' button on the 'Change the master password' window."""
        curr_m_pwd = str(self.curr_pass_field.get())
        new_m_pwd = str(self.new_pass_field.get())
        conf_m_pwd = str(self.conf_pass_field.get())
        m_pwd = db.return_master_password()
        if curr_m_pwd == m_pwd:
            if conf_m_pwd == new_m_pwd:
                if new_m_pwd != curr_m_pwd:
                    res = db.update_master_pwd(new_m_pwd)
                    if res:
                        messagebox.showinfo("Change master password", "Master password changed successfully !")
                        self.chng_master_pwd_win.destroy()
                    else:
                        messagebox.showwarning("Change master password", "There was a problem changing the password.")
                        self.chng_master_pwd_win.wait_window()
                else:
                    messagebox.showwarning("Change master password", "The old and the new password cannot be same. \nPlease enter a unique password")
                    self.chng_master_pwd_win.wait_window()
            else:
                messagebox.showwarning("Change master password", "The confirmed password doesnt match the new password. Please check")
                self.chng_master_pwd_win.wait_window()
        else:
            messagebox.showwarning("Change master password", "Please enter the current master password correctly\n")
            self.chng_master_pwd_win.wait_window()

    def show_or_hide_passwords(self):
        """Function callback for the 'Show Passwords' button on the 'Password Manager' window."""
        text = self.show_pass_btn.cget("text")
        self.password_table.delete(*self.password_table.get_children())

        if text == "Show passwords":
            self.update_password_table(mask=False)
            self.show_pass_btn.configure(text="Hide passwords")
        elif text == "Hide passwords":
            self.update_password_table(mask=True)
            self.show_pass_btn.configure(text="Show passwords")


    def logout(self):
        """Function callback for the 'Logout' button on the 'Password Manager' window."""
        ans = messagebox.askyesnocancel('Logout', 'Are you sure you want to log out of the vault')
        if ans:
            self.close_all_windows()
            messagebox.showinfo('Logout', 'Goodbye! Have a nice day ahead')
        else:
            self.pass_table_win.wait_window()


    def center_position_window(self, window):
        """Function to center a given window on the main screen."""
        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()

        positionX = int((window.winfo_screenwidth() / 2) - (windowWidth / 2))
        positionY = int((window.winfo_screenheight() / 2) - (windowHeight / 2))

        window.geometry(f"+{positionX}+{positionY}")
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
    def login_btn_command(self, event):
        self.login_password_vault()


    def create_btn_command(self, event):
        self.create_password_vault()


    def update_btn_command(self, event, idx):
        self.update_credentials(idx)


    def add_btn_command(self, event):
        self.add_credentials()


    def change_pass_btn_command(self, event):
        self.change_master_password()


# Main Function
if __name__ == '__main__':
    ui = UserInterface()
