import tkinter as tk

class Main(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        
    def configura_titulo(self, titulo:str) -> None:
        self.title(titulo)