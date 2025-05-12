import tkinter as tk

root = tk.Tk()
root.title("Teste Tkinter")
root.geometry("300x100")

label = tk.Label(root, text="Se você está vendo esta janela, o Tkinter está funcionando!")
label.pack(pady=20)

root.mainloop() 