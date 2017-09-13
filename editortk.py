try:
    import tkinter as tk
except:
    import Tkinter as tk

try:
    import tkMessageBox as pop_up
except:
    import tkinter.tkMessageBox as pop_up

import time

EMPTY_TITLE_ERROR_MESSAGE_SAVE = "Please write the name of the file you want to save in the given field."
EMPTY_TITLE_ERROR_MESSAGE_OPEN = "Please write the name of the file you want to open in the given field."
FILE_NOT_FOUND_ERROR_MESSAGE = "No file with the given title was found, remember that this text editor can only read files in its directory."
SAVING_SUCCESS_MESSAGE = "Your text is now stored in the {filename} file"
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Please be sure that the file you want to open exists and that it is in the same folder of this editor."

class mywindow():
    def __init__(self, root):
        top = tk.Frame(root)
        temp = tk.Label(root, text="Title:")
        temp.pack(in_=top, side=tk.LEFT)

        file_title = tk.Entry(root)
        file_title.insert(0, "default")
        file_title.pack(in_=top, side=tk.RIGHT)

        top.pack()

        main_text = tk.Text(root)
        main_text.pack()

        menubar = tk.Menu(root)
        menubar.add_command(label="Open", command=self._open)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label="Add signature", command=self.add_signature)
        menubar.add_command(label="Add date", command=self.add_date)
        menubar.add_command(label="Run", command=self.run_code)

        root.config(menu=menubar)
        self.file_title = file_title
        self.main_text = main_text
        self.top = top
        self._open()

    def _open(self):
        if not self.file_title.get():
            pop_up.showerror("Title is empty.", EMPTY_TITLE_ERROR_MESSAGE_OPEN)
            return 1

        if ".txt" not in self.file_title.get():
            filename = self.file_title.get() + ".txt"

        try:
            with open(filename) as f:
                self.main_text.delete("1.0", tk.END)
                self.main_text.insert(tk.INSERT, f.read(), "a")
        except IOError:
            pop_up.showerror("File not found.", FILE_NOT_FOUND_ERROR_MESSAGE)


    def save(self):
        if not self.file_title.get():
            pop_up.showerror("No title.", EMPTY_TITLE_ERROR_MESSAGE_SAVE)
            return 1

        if ".txt" not in self.file_title.get():
            filename = self.file_title.get() + ".txt"

        with open(filename, "w+") as f:
            f.write(self.main_text.get(1.0, tk.END))
        pop_up.showinfo(
            "File saved succesfully.",
            SAVING_SUCCESS_MESSAGE.format(
                filename=filename))
    def run_code(self):
        data = self.main_text.get(1.0, tk.END)
        exec(data)


    def add_date(self):
        full_date = time.localtime()
        day = str(full_date.tm_mday)
        month = str(full_date.tm_mon)
        year = str(full_date.tm_year)
        date = "\n" + day + '/' + month + '/' + year
        self.main_text.insert(tk.INSERT, date, "a")

    def add_signature(self):
        try:
            with open("signature.txt") as f:
                self.main_text.insert(tk.INSERT, "\n" + f.read(), "a")
        except IOError:
            MESSAGE = SIGNATURE_TXT_NOT_FOUND_MESSAGE
            pop_up.showerror("\"signature.txt\" not found.", MESSAGE)

root = tk.Tk()

mywin  = mywindow(root)

root.bind("<F5>", lambda event: mywin.run_code())

tk.mainloop()
