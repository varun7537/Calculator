import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext

class CalculatorClient:
    def __init__(self, master):
        self.master = master
        master.title("Scientific Calculator")
        master.resizable(False, False)

        self.theme = "light"
        self.history = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 65432))

        self.entry = tk.Entry(master, width=30, font=('Arial', 20), borderwidth=5, relief="ridge", justify="right")
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        self.history_box = scrolledtext.ScrolledText(master, width=40, height=6, font=('Arial', 12), state='disabled')
        self.history_box.grid(row=1, column=0, columnspan=5, padx=10, pady=(0, 10))

        buttons = [
            '7', '8', '9', '/', 'sqrt(',
            '4', '5', '6', '*', 'log(',
            '1', '2', '3', '-', 'sin(',
            '0', '.', '(', ')', 'cos(',
            'exp(', 'tan(', '+', '^', 'C'
        ]

        row = 2
        col = 0

        for button in buttons:
            action = lambda x=button: self.button_click(x)
            b = tk.Button(master, text=button, width=5, height=2, font=('Arial', 14),
                        command=action, relief="raised")
            b.grid(row=row, column=col, padx=3, pady=3)
            col += 1
            if col > 4:
                col = 0
                row += 1

        equals = tk.Button(master, text='=', width=25, height=2, font=('Arial', 14), bg='lightgreen', command=self.calculate)
        equals.grid(row=row, column=0, columnspan=5, padx=5, pady=5)

        theme_button = tk.Button(master, text="Toggle Theme", command=self.toggle_theme)
        theme_button.grid(row=row+1, column=0, columnspan=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.close_connection)

        self.update_theme()

    def button_click(self, value):
        if value == 'C':
            self.entry.delete(0, tk.END)
        else:
            current = self.entry.get()
            if value == '^':
                value = '**'
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current + value)

    def calculate(self):
        expression = self.entry.get()
        if not expression.strip():
            return
        self.socket.sendall(expression.encode())
        if expression.lower() == 'exit':
            self.close_connection()
        else:
            data = self.socket.recv(1024).decode()
            result_line = f"{expression} = {data}"
            self.history.append(result_line)
            self.update_history_box()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, data)

    def update_history_box(self):
        self.history_box.config(state='normal')
        self.history_box.delete(1.0, tk.END)
        for line in self.history[-10:]: 
            self.history_box.insert(tk.END, line + '\n')
        self.history_box.config(state='disabled')

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.update_theme()

    def update_theme(self):
        if self.theme == "light":
            bg = "white"
            fg = "black"
            entry_bg = "white"
            history_bg = "#f8f8f8"
        else:
            bg = "#2e2e2e"
            fg = "white"
            entry_bg = "#3e3e3e"
            history_bg = "#444444"

        self.master.configure(bg=bg)
        self.entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        self.history_box.configure(bg=history_bg, fg=fg)

        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                if widget['text'] == '=':
                    widget.configure(bg='lightgreen' if self.theme == 'light' else '#3cba54', fg='black')
                elif widget['text'] == 'Toggle Theme':
                    widget.configure(bg='#cccccc' if self.theme == 'light' else '#555555', fg=fg)
                else:
                    widget.configure(bg='#f0f0f0' if self.theme == 'light' else '#444444', fg=fg)

    def close_connection(self):
        try:
            self.socket.sendall(b'exit')
        except:
            pass
        self.socket.close()
        self.master.destroy()

root = tk.Tk()
client = CalculatorClient(root)
root.mainloop()
