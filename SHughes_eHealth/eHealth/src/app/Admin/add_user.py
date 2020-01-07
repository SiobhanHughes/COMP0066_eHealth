#Help with loop to create multiple widgets
#https://stackoverflow.com/questions/22916622/how-to-store-values-from-an-entry-widget-for-loop-in-tkinter


import tkinter as tk

class Add_info(tk.Frame):
    def __init__(self, parent, titles, *args, **kwargs):
        self.parent = parent
        self.titles = titles
        self.create_widgets(self.titles)
    
    def create_widgets(self, titles):
        self.entries = []
        for i in range(len(titles)):
            title = titles[i]
            self.labelframe = tk.LabelFrame(self.parent, text='Add user to eHealth system')
            self.labelframe.pack(fill="both", expand=True)
    
            self.label = tk.Label(self.labelframe, text=title)
            self.label.pack(expand=True, fill='both')
    
            self.entry = tk.Entry(self.labelframe)
            self.entry.pack()
            self.entries.append(self.entry)
        
        self.label = tk.Label(self.labelframe)
        self.label.pack(expand=True, fill='both')
        self.label = tk.Label(self.labelframe, text='Save all details', fg='blue')
        self.label.pack(expand=True, fill='both')
        self.button = tk.Button(self.labelframe, text="Save", command=self.get_input, fg='blue')
        self.button.pack()

    def get_input(self):
        info = []
        for entry in self.entries:
            info.append(entry.get().strip())
        print(info)
        self.save()
    
    def save(self):
        for widget in self.labelframe.winfo_children():
            widget.destroy()
    
        
if __name__ == '__main__':
    root = tk.Tk()
    titles = ['GP first name', 'GP last name', 'GP email', 'Address: street', 'Address: city', 'Address: postcode', 'Telephone number']
    Add_info(root, titles)
    root.mainloop()