import tkinter as tk

C = {
    "bg": "#F4F9FD",
    "header": "#1565C0",
    "header_txt": "#FFFFFF",
    "sub_txt": "#90CAF9"
}

class FlowTreeUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("FlowTree")
        self.geometry("1200x700")
        self.configure(bg=C["bg"])

        self.build_ui()

    def build_ui(self):

        header = tk.Frame(self,bg=C["header"],height=60)
        header.pack(fill="x")

        header.pack_propagate(False)

        title = tk.Label(header,text="FlowTree",bg=C["header"],fg=C["header_txt"],font=("Segoe UI", 18, "bold"))
        title.pack(side="left", padx=20)

        subtitle = tk.Label(header,text="Visualizador de Árboles",bg=C["header"],fg=C["sub_txt"],font=("Segoe UI", 10))
        subtitle.pack(side="left")

if __name__ == "__main__":
    app = FlowTreeUI()
    app.mainloop()