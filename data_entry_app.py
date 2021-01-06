# testing github
# testing github again
# The program must:
# * allow all relevant, valid data to be entered, as per the field chart
# * append entered data to a CSV file
#   - The CSV file must have a filename
#     of abq_data_record_CURRENTDATE.csv, where
#     CURRENTDATE is the date of the checks in
#     ISO format (Year-month-day)
#   - The CSV file must have all the fields as per the chart
# * enforce correct datatypes per field
# The program should try, whenever possible, to:
# * enforce reasonable limits on data entered
# * Auto-fill data
# * Suggest likely correct values
# * Provide a smooth and efficient workflow

# |Field       | Datatype | Units| Range        |Descripton           |
# +============+==========+======+==============+=====================+
# |Date        |Date      |      |              |Date of record       |
# +------------+----------+------+--------------+---------------------+
# |Time        |Time      |      |8, 12, 16, 20 |Time period          |
# +------------+----------+------+--------------+---------------------+
# |Lab         |String    |      | A - E        |Lab ID               |
# +------------+----------+------+--------------+---------------------+
# |Technician  |String    |      |              |Technician name      |
# +------------+----------+------+--------------+---------------------+
# |Plot        |Int       |      | 1 - 20       |Plot ID              |
# +------------+----------+------+--------------+---------------------+
# |Seed        |String    |      |              |Seed sample ID       |
# |sample      |          |      |              |                     |
# +------------+----------+------+--------------+---------------------+
# |Fault       |Bool      |      |              |Fault on sensor      |
# +------------+----------+------+--------------+---------------------+
# |Light       |Decimal   |klx   | 0 - 100      |Light at plot        |
# +------------+----------+------+--------------+---------------------+
# |Humidity    |Decimal   |g/m³  | 0.5 - 52.0   |Abs humidity at plot |
# +------------+----------+------+--------------+---------------------+
# |Temperature |Decimal   |°C    | 4 - 40       |Temperature at plot  |
# +------------+----------+------+--------------+---------------------+
# |Blossoms    |Int       |      | 0 - 1000     |# blossoms in plot   |
# +------------+----------+------+--------------+---------------------+
# |Fruit       |Int       |      | 0 - 1000     |# fruits in plot     |
# +------------+----------+------+--------------+---------------------+
# |Plants      |Int       |      | 0 - 20       |# plants in plot     |
# +------------+----------+------+--------------+---------------------+
# |Max height  |Decimal   |cm    | 0 - 1000     |Ht of tallest plant  |
# +------------+----------+------+--------------+---------------------+
# |Min height  |Decimal   |cm    | 0 - 1000     |Ht of shortest plant |
# +------------+----------+------+--------------+---------------------+
# |Median      |Decimal   |cm    | 0 - 1000     |Median ht of plants  |
# |height      |          |      |              |                     |
# +------------+----------+------+--------------+---------------------+
# |Notes       |String    |      |              |Miscellaneous notes  |
# +------------+----------+------+--------------+---------------------+


from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk



# class DataView:
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#
#         blossoms = str()
#         date = str()
#         fault = bool()
#         fruit = str()
#         blossoms_entry = tk.Spinbox(parent, from_=0, to=1000, increment=1, textvariable=blossoms)
#
#         date_entry = ttk.Entry(parent, textvariable=date)
#
#         fault_entry=ttk.Checkbutton(parent, text="Fault", variable=fault, onvalue=1, offvalue=0, height=5, width=20)
#
#         fruit_entry = tk.Spinbox(parent, from_=0, to=1000, increment=1, textvariable=fruit)
#
#         blossoms_entry.pack()
#         date_entry.pack()
#         fault_entry.pack()
#         fruit_entry.pack()
#
#
# class MyApplication(tk.Tk):
#     """A friendly little module"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.title("AgriLabs")
#         self.geometry("800x600")
#         self.resizable(width=False, height=False)
#
#         DataView(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
#         self.columnconfigure(0, weight=1)





class LabelInput(tk.Frame):

    def __init__(self, parent, label='', input_class=ttk.Entry, input_var=None, input_args=None, label_args=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W +tk.E))
            input_args["textvariable"] = input_var

        self.input=input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) ==tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except(TypeError, tk.TclError):
            # happens when numeric fields are empty
            return''

    def set(self, value, *args, **kwargs):
        if type(self.variable) ==tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input)==tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)

        else:
    #input must be an entry type widget with no variable
            self.input.delete(0, tk.END) 
            self.input.insert(0, value)

class DataRecordForm(tk.Frame):
#     input form from widgets
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.inputs = {}

        recordinfo = tk.LabelFrame(self, text="Record Information")
        self.inputs['date']=LabelInput(recordinfo, "Date", input_var=tk.StringVar())
        self.inputs['date'].grid(row=0, column=0)

        self.inputs['Time'] = LabelInput(recordinfo, "Time", input_class=ttk.Combobox, input_var=tk.StringVar(), input_args={"values": ["8:00", "12:00", "16:00", "20:00"]})
        self.inputs['Time'].grid(row=0, column=1)

        self.inputs['Technician']=LabelInput(recordinfo, "Technician", input_var=tk.StringVar())
        self.inputs['Technician'].grid(row=0, column=2)

        # line 2


        self.inputs['Lab'] = LabelInput(recordinfo, "Lab",
                                        input_class=ttk.Combobox, input_var=tk.StringVar(),
                                        input_args={"values": ["A", "B", "C", "D", "E"]})
        self.inputs['Lab'].grid(row=1, column=0)

        self.inputs['Plot'] = LabelInput(recordinfo, "Plot",
                                         input_class=ttk.Combobox, input_var=tk.IntVar(),
                                         input_args={"values": list(range(1, 21))})
        self.inputs['Plot'].grid(row=1, column=1)

        self.inputs['Seed sample'] = LabelInput(
            recordinfo, "Seed sample", input_var=tk.StringVar())
        self.inputs['Seed sample'].grid(row=1, column=2)

        recordinfo.grid(row=0, column=0, sticky=tk.W + tk.E)

        # Environment Data

        environmentsinfo = tk.LabelFrame(self, text='Environment Info')
        self.inputs['Humidity'] = LabelInput(environmentsinfo, "Humidity (g/m2)", input_class=tk.Spinbox, input_var=tk.DoubleVar(), input_args={"from_": 0.5, "to": 52.0, "increment": .01})
        self.inputs['Humidity'].grid(row=0, column=0)

        self.inputs['Equipment Fault'] = LabelInput(
            environmentsinfo, "Equipment Fault",
            input_class=ttk.Checkbutton,
            input_var=tk.BooleanVar()
        )
        self.inputs['Equipment Fault'].grid(
            row=1, column=0, columnspan=3
        )

        plantinfo = tk.LabelFrame(self, text="Plant Data")

        self.inputs['Plants'] = LabelInput(
            plantinfo, "Plants",
            input_class=tk.Spinbox,
            input_var=tk.IntVar(),
            input_args={"from_": 0, "to": 20})
        self.inputs['Plants'].grid(row=0, column=1)

        self.inputs['Blossoms'] = LabelInput(
            plantinfo, "Blossoms",
            input_class=tk.Spinbox,
            input_var=tk.IntVar(),
            input_args={"from_": 0, "to": 1000})
        self.inputs['Blossoms'].grid(row=0, column=2)

        environmentsinfo.grid(row=2, column=0, sticky=tk.W + tk.E)
        plantinfo.grid(row=3, column=0, stick=tk.W + tk.E)

        # notes section

        self.inputs['Notes'] = LabelInput(self,
             "Notes",
             input_class=tk.Text,
             input_args={"width":75, "height": 10}
        )

        self.inputs['Notes'].grid(sticky="w", row=4, column=0)

    def get(self):
        data={}
        for key, widget in self.inputs.items():
            data[key] =widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')

        self.reset()

class ValidateMixin:

    # Add validation input functionality to an input widget

    def __init__(self, *args, error_var=None, **kwargs):
        self.error  = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.config(
            validate='all',
            validatecommand=(vcmd, '%P', '&s', 'S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '&s', 'S', '%V', '%i', '%d')
        )

    def _toggle_error(self, on=False):
        self.config(foreground=('red' if  on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        self._toggle_error(False)
        self.error.set('')
        valid = True
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(proposed=proposed, current=current, char=char, event=event, index=index,action=action)
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, ** kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(proposed=proposed, current=current, char=char, event=event, index=index,action=action)

    def _focusout_invalid(self, **kwargs):
        self._toggle_error(True)

    def _key_validate(self, **kwargs):
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid

class RequiredEntry(ValidateMixin, ttk.Entry)

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is requried')
        return valid

class DateEntry(ValidateMixin, ttk.Entry)

    def _key_validate(self, action, index, char, **kwargs):
        valid = True

        if action == '0':
            valid = True
        elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
            valid=char.isdigit()
        elif index in ('4', '7'):
            valid = char == '-'
        else:
            valid=False
        return valid

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            self.error.set('A value is requried')
            valid = False
        try:
            datetime.strptime(self.get(), %Y-%m-%d)
        except ValueError:
            self.error.set('Invalid date')
            valid =False
        return valid

 
        

        
class Application(tk.Tk):
    #     Application root window

    def on_save(self):
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        newfile = not os.path.exists(filename)

        data = self.recordform.get()

        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.records_saved = 0
        self.records_saved +=  1
        self.status.set(
            "{} records saved this session".format(self.records_saved)
        )

        self.recordform.reset()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("ABQ Data Entry Application")
        self.resizable(width=False, height=False)

        ttk.Label(
            self,
            text="ABQ Data Entry Application",
            font=("TkDefaultFont", 16)
        ).grid(row=0)


        self.recordform=DataRecordForm(self)
        self.recordform.grid(row=1, padx=10)

        ttk.Style().configure("TButton", padding=6, relief="flat",
                              background="red")
        self.savebutton =ttk.Button(self, text='Save', command=self.on_save)
        self.savebutton.grid(sticky=tk.W, row=2, padx=10)

        # status bar

        self.status=tk.StringVar()
        self.statusbar=ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
      


if __name__ == '__main__':
     app = Application()
     app.mainloop()
















