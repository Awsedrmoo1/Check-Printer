import tkinter as tk

class NumberBox(tk.Frame):
    def __init__(chknum, master=None, default_value=1):
        super().__init__(master)
        chknum.value = default_value



        # Create entry to type in value
        chknum.entry = tk.Entry(chknum, width=6)
        chknum.entry.insert(0, f"{chknum.value:06d}")
        chknum.entry.pack(side=tk.LEFT)

        # Create buttons to increment/decrement value
        chknum.inc_button = tk.Button(chknum, text="+", command=chknum.increment)
        chknum.dec_button = tk.Button(chknum, text="-", command=chknum.decrement)
        chknum.inc_button.pack(side=tk.RIGHT, padx=(0, 5))
        chknum.dec_button.pack(side=tk.LEFT, padx=(5, 0))

        # Bind the return key to update the value
        chknum.entry.bind("<Return>", chknum.update_from_entry)
        

    def increment(chknum):
        chknum.value += 1
        chknum.update_display()

    def decrement(chknum):
        if chknum.value > 1:
            chknum.value -= 1
            chknum.update_display()

    def update_display(chknum):
        chknum.entry.delete(0, tk.END)
        chknum.entry.insert(0, f"{chknum.value:06d}")

    def update_from_entry(chknum, event):
        try:
            new_value = int(chknum.entry.get())
            if new_value > 0:
                chknum.value = new_value
                chknum.update_display()
        except ValueError:
            pass
    def get_value(chknum):
        return chknum.value



'''root = tk.Tk()
root.title("Number Box")

box = NumberBox(root, default_value=1)
box.pack()

root.mainloop()
'''