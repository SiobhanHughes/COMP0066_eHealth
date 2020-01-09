#============================IMPORT============================================

import tkinter as tk


#============================Search results interface======================

class Search_results:
    def __init__(self, parent, titles, rows, *args, **kwargs):
        self.parent = parent
        self.titles = titles
        self.rows = rows
        self.display_result(self.titles, self.rows)
        
    def display_result(self, titles, rows):
        for x in range(len(rows)):
            self.labelframe = tk.LabelFrame(self.parent)
            self.labelframe.pack(fill="both", expand=True)
            for i in range(len(titles)):
                tk.Label(self.labelframe, text=titles[i]).grid(row=0, column=i)
                for j in range(len(titles)):
                    tk.Label(self.labelframe, text=rows[x][j]).grid(row=1, column=j)
                
if __name__ == '__main__':
    root = tk.Tk()
    titles = ['Patient id','Patient first name', 'Patient last name', 'email', 'DOB', 'NHSno', 'active' ]
    rows = [(1,'Nicola', 'Hughes', 'nhughes@gmail.com', '1984-12-14', 'NHS001', 'yes'), (3, 'Nicola', 'Hughes', 'nhughes@gmail.com', '1984-12-14', 'NHS001', 'yes')]
    Search_results(root, titles, rows)   
    root.mainloop()     
        
        
        
    