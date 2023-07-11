import tkinter as tk

window = tk.Tk()

for i in range(3): # rows
    window.columnconfigure(i, weight=1, minsize=75) # enables responsive column
    window.rowconfigure(i, weight=1, minsize=50) # enables responsive row
    
    for j in range(3): # columns
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()

window.mainloop()
