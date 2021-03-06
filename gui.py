#! /usr/bin/env python
__author__ = 'Uyuni'
import Tkinter
import ttk
import re_notation
import regex_to_nfa
import tkMessageBox
import unittest
import tkFont
from StringIO import StringIO
from tests import test_re_notation
from tests import test_regex_to_nfa


class GUI(Tkinter.Frame):
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.init_gui_grid()
        self.center_window()
        self.parent.resizable(0, 0)


    def init_gui_grid(self):
        self.parent.title("Fundamentos de la computacion")
        self.style = ttk.Style().configure("TButton", padding=(0, 5, 0, 5))
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=3)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        # First regex label
        self.first_regex_label = Tkinter.Label(self)
        self.first_regex_label["text"] = "1ra Expresion regular"
        self.first_regex_label.grid(row=0, column=0)

        # First regex text field
        self.first_regex = Tkinter.Entry(self)
        self.first_regex["text"] = ""
        self.first_regex.insert(0, "")
        self.first_regex["width"] = 60
        self.first_regex.grid(row=0, column=1, sticky=Tkinter.W)

        # Second regex label
        self.second_regex_label = Tkinter.Label(self)
        self.second_regex_label["text"] = "2da Expresion regular"
        self.second_regex_label.grid(row=1, column=0)

        # Second regex text field
        self.second_regex = Tkinter.Entry(self)
        self.second_regex["text"] = ""
        self.second_regex.insert(0, "")
        self.second_regex["width"] = 60
        self.second_regex.grid(row=1, column=1, sticky=Tkinter.W)

        self.clean_button = Tkinter.Button(self)
        self.clean_button["text"] = "Borrar campos"
        self.clean_button.grid(row=0, column=2, rowspan=2, columnspan=2)

        # Regex acceptance label
        self.acceptanceStr = "Si reconocen el mismo lenguaje"
        self.rejectStr = "No reconocen el mismo lenguaje"
        self.resultFont = tkFont.Font(family="Helvetica", size=24, weight="bold")
        self.resultStr = "                                           "

        self.string_var = Tkinter.StringVar()
        self.regex_cmp_label = Tkinter.Label(self, textvariable=self.string_var, fg="blue", font=self.resultFont)
        self.string_var.set(self.resultStr)
        self.regex_cmp_label.grid(row=2, column=0, columnspan=3, sticky=Tkinter.W)

        myfont = tkFont.Font(family="Helvetica", size=14)
        self.details_str = Tkinter.StringVar()
        self.details_label = Tkinter.Label(self, textvariable=self.details_str, font=myfont)
        self.details_label.grid(row=3, column=0, rowspan=2, columnspan=2, sticky=Tkinter.W)

        # Boton comparar
        self.compare_button = Tkinter.Button(self)
        self.compare_button["text"] = "Comparar"
        self.compare_button["fg"] = "red"
        self.compare_button.grid(row=6, column=2)

        # Quit button
        self.quit_button = Tkinter.Button(self)
        self.quit_button["text"] = "Salir",
        self.quit_button["command"] = self.quit
        self.quit_button.grid(row=6, column=3)

        # Run tests button
        self.run_test_button = Tkinter.Button(self)
        self.run_test_button["text"] = "Test",
        self.run_test_button.grid(row=6, column=0)

        self.grid()

    def center_window(self):
        # We get the results we want but the window appears
        # for a moment in the wrong position
        self.parent.update()
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw / 2) - self.parent.winfo_width() / 2
        y = (sh / 2) - self.parent.winfo_height() / 2
        self.parent.geometry('+%d+%d' % (x, y))


class Controller():
    def __init__(self):
        self.root = Tkinter.Tk()
        self.gui = GUI(parent=self.root)
        self.binding()
        self.gui.mainloop()

    def binding(self):
        self.gui.compare_button["command"] = self.compare
        self.gui.run_test_button["command"] = self.run_test
        self.gui.clean_button["command"] = self.clean_fields
        self.root.bind('<Return>', lambda f: self.compare())

    def clean_fields(self):
        self.gui.string_var.set("")
        self.gui.details_str.set("")
        self.gui.regex_cmp_label["fg"] = "blue"
        self.gui.first_regex.delete(0, Tkinter.END)
        self.gui.second_regex.delete(0, Tkinter.END)

    def compare(self):
        # Model is actually called from here
        first_regex = self.gui.first_regex.get().strip()
        second_regex = self.gui.second_regex.get().strip()

        print "--------------------------------------------"
        print "Regular expressions received from the user:"
        print first_regex
        print second_regex

        try:
            regex1 = re_notation.infix_to_prefix(first_regex)
            regex2 = re_notation.infix_to_prefix(second_regex)

            print "--------------------------------------------"
            print "Converted regular expressions to prefix notation:"
            print regex1
            print regex2

            first_dfa = regex_to_nfa.build_dfa(regex1)
            second_dfa = regex_to_nfa.build_dfa(regex2)

            result, diff_string = regex_to_nfa.compare_dfas(first_dfa, second_dfa)
            print "--------------------------------------------"
            print "Do the regular expressions recognize the same language?"
            print result

            print "--------------------------------------------"
            if result:
                self.gui.details_str.set("")
                self.gui.string_var.set(self.gui.acceptanceStr)
                self.gui.regex_cmp_label["fg"] = "blue"
            else:
                self.gui.string_var.set(self.gui.rejectStr)
                self.gui.regex_cmp_label["fg"] = "red"
                self.gui.details_str.set(diff_string)
        except Exception as e:
            self.gui.string_var.set("Error al procesar las expresiones regulares.")
            self.gui.regex_cmp_label["fg"] = "red"
            self.gui.details_str.set(e.message)


    def run_test(self):
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        re_notation_test_results = runner.run(unittest.makeSuite(test_re_notation.TestReNotation))

        stream.seek(0)
        print stream.read()
        stream.seek(0)

        # Commented the next lines because it hangs
        regex_to_nfa_test_results = runner.run(unittest.makeSuite(test_regex_to_nfa.TestRegexToNfa))
        stream.seek(0)
        print stream.read()
        stream.seek(0)


def main():
    controller = Controller()


if __name__ == '__main__':
    main()