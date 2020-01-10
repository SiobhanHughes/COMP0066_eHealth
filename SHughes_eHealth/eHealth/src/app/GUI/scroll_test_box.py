#scrolled text box implemetation taken from:
#https://stackoverflow.com/questions/13832720/how-to-attach-a-scrollbar-to-a-text-widget/13833338

import tkinter
import tkinter.scrolledtext as scrolledtext

main_window = tkinter.Tk()

txt = scrolledtext.ScrolledText(main_window, undo=True)
txt['font'] = ('consolas', '12')
txt.pack(expand=True, fill='both')

main_window.mainloop()