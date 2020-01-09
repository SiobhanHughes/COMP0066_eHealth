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
            for i in range(len(titles)):
                tk.Label(self.parent, text=titles[i]).grid(row=0, column=i)
                for i in range(len(rows)):
                    for j in range(len(titles)):
                        tk.Label(self.parent, text=rows[i][j]).grid(row=i+1, column=j)
                
if __name__ == '__main__':
    root = tk.Tk()
    titles = ['Patient id','Patient first name', 'Patient last name', 'email', 'DOB', 'NHSno', 'active' ]
    rows = [(1,'Nicola', 'Hughes', 'nhughes@gmail.com', '1984-12-14', 'NHS001', 'yes'), (3, 'Nicola', 'Hughes', 'nhughes@gmail.com', '1984-12-14', 'NHS001', 'yes')]
    Search_results(root, titles, rows)   
    root.mainloop()     
        
        
        
    