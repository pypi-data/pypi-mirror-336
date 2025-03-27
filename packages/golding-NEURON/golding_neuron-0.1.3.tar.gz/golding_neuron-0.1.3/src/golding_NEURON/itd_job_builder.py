
import glob
import logging.handlers
from .fileaccess import get_package_path
from .itd_job import ITDJob, run_tasks
from .nsg_portal import NSGWindow
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import os
import numpy as np
from tkinter import scrolledtext
import logging
import dill
import threading
import tkinter as tk
import tkinter.ttk as ttk
from shutil import copytree, copyfile, make_archive, rmtree
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Based on
#   https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, parent, *args, **kw):
        
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)

    def create(self):
        self.interior_id = self.canvas.create_window(
            0, 0, window=self.interior, anchor=tk.NW, tags="self.interior"
        )


class ITDBuildGUI(tk.Tk):

    job_file_dir = get_package_path("itd_job_builder/job_files")
    temp_dir = os.path.join(job_file_dir, "temp_archive")
    temp_subdir = os.path.join(temp_dir, "sub")
    iterables = {}

    def __init__(self):
        super().__init__()
        # self.minsize()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.title(os.getcwd())
        self.geometry(f"{screen_width-20}x{screen_height-50}+{10}+0")
        self.minsize(600, 300)
        self.maxsize(screen_width - 20, screen_height - 50)
        self.section_locs = {
            "Excitation": (1, 0),
            "Inhibition": (2, 0),
            "Axon": (3, 0),
            "Cells": (1, 1),
            "ITD": (2, 1),
            "Send": (3, 1),
        }
        # self.grid_propagate(False)
        self.create_grid()

        self.cell_files = glob.glob(get_package_path("cells") + "/*.asc")
        self.cell_names = [Path(f).stem for f in self.cell_files]
        # self.after(10000)
        self.create_label("IΤD Test", self.subframes[self.section_locs["ITD"]])

        # Listbox

        # self.create_menubar()
        self.create_listbox(
            "Cells",
            "selected_cells",
            self.cell_names,
            parent=self.subframes[self.section_locs["Cells"]],
            reveal_cat="Cells",
        )

        # Checkboxes
        self.checkbox_vars = {}
        self.create_checkbox(
            "Attach axon",
            "axon",
            parent=self.subframes[self.section_locs["Axon"]],
            reveal_cat="Axon",
        )
        self.create_checkbox(
            "Inhibition",
            "inhibition",
            parent=self.subframes[self.section_locs["Inhibition"]],
            reveal_cat="Inhibition",
        )
        self.create_checkbox(
            "Excitation",
            "excitation",
            parent=self.subframes[self.section_locs["Excitation"]],
            reveal_cat="Excitation",
        )
        trace_box = self.create_checkbox(
            "Output traces",
            "traces",
            parent=self.subframes[self.section_locs["Send"]],
            reveal_cat="Send",
            pack=False,
        )
        trace_box.grid(row=0, column=0, columnspan=2)

        # Spinboxes
        self.spinbox_vars = {}

        self.create_total_spinbox(
            "ITD range",
            "itd_range",
            0,
            5,
            increment=0.1,
            default=2,
            parent=self.subframes[self.section_locs["ITD"]],
            reveal_cat="ITD",
        )
        self.create_total_spinbox(
            "ITD step",
            "itd_step",
            0,
            1,
            increment=0.005,
            default=0.01,
            parent=self.subframes[self.section_locs["ITD"]],
            reveal_cat="ITD",
        )
        self.create_total_spinbox(
            "Number of trials",
            "itd_trials",
            0,
            1000,
            increment=1,
            default=400,
            parent=self.subframes[self.section_locs["ITD"]],
            reveal_cat="ITD",
        )
        self.create_checkbox(
            "Threshold options",
            "threshold_bool",
            parent=self.subframes[self.section_locs["ITD"]],
            reveal_cat="Threshold",
        )

        self.advanced_widget_args = {
            "spinbox": {
                "Number of synapses per group": {
                    "var_label": "Number of synapses per group",
                    "var_name": "numsyn",
                    "from_": 0,
                    "to": 20,
                    "increment": 1,
                    "default": 4,
                    "parent": self.subframes[self.section_locs["Excitation"]],
                    "reveal_cat": "Excitation",
                    "iterable": True,
                },
                "Synapse space": {
                    "var_label": "Synapse space",
                    "var_name": "synspace",
                    "from_": 0,
                    "to": 20,
                    "increment": 1,
                    "default": 7,
                    "parent": self.subframes[self.section_locs["Excitation"]],
                    "reveal_cat": "Excitation",
                    "iterable": True,
                },
                "Simultaneous": {
                    "var_label": "Number of syn. fibers",
                    "var_name": "numfiber",
                    "from_": 0,
                    "to": 10,
                    "increment": 1,
                    "default": 2,
                    "parent": self.subframes[self.section_locs["Excitation"]],
                    "reveal_cat": "Excitation",
                    "iterable": True,
                },
                "Excitatory fiber conductance": {
                    "var_label": "Excitatory fiber conductance",
                    "var_name": "exc_fiber_gmax",
                    "from_": 0,
                    "to": 0.1,
                    "increment": 0.005,
                    "default": 0.015,
                    "parent": self.subframes[self.section_locs["Excitation"]],
                    "reveal_cat": "Excitation",
                    "iterable": True,
                },
                "Threshold": {
                    "var_label": "Threshold",
                    "var_name": "threshold",
                    "from_": -100,
                    "to": 100,
                    "increment": 1,
                    "default": 25,
                    "parent": self.subframes[self.section_locs["ITD"]],
                    "reveal_cat": "Threshold",
                },
                "Inhibitory fiber gmax": {
                    "var_label": "Inhibitory fiber gmax",
                    "var_name": "inh_fiber_gmax",
                    "from_": 0,
                    "to": 1,
                    "increment": 0.001,
                    "default": 0.022,
                    "parent": self.subframes[self.section_locs["Inhibition"]],
                    "reveal_cat": "Inhibition",
                    "iterable": True,
                },
                "Inhibitory timing": {
                    "var_label": "Inhibitory timing",
                    "var_name": "inh_timing",
                    "from_": 0,
                    "to": 20,
                    "increment": 0.01,
                    "default": -0.32,
                    "parent": self.subframes[self.section_locs["Inhibition"]],
                    "reveal_cat": "Inhibition",
                    "iterable": True,
                },
                "Axon speed": {
                    "var_label": "Axon speed",
                    "var_name": "axonspeed",
                    "from_": 0,
                    "to": 5,
                    "increment": 0.25,
                    "default": 1,
                    "parent": self.subframes[self.section_locs["Axon"]],
                    "reveal_cat": "Axon",
                    "iterable": True,
                },
            },
            "checkbox": {
                "Absolute threshold": {
                    "label": "Absolute threshold",
                    "var_name": "absolute_threshold",
                    "default": False,
                    "parent": self.subframes[self.section_locs["ITD"]],
                    "reveal_cat": "Threshold",
                    "reveal": False,
                },
            },
        }
        self.create_advanced_widgets(self.advanced_widget_args)
        # Run button
        self.subframes[self.section_locs["Send"]].columnconfigure(0, weight=1)
        self.subframes[self.section_locs["Send"]].columnconfigure(1, weight=1)
        self.run_button = ttk.Button(
            self.subframes[self.section_locs["Send"]],
            text="Run local",
            command=self.run_procedure,
        )
        self.run_button.grid(column=0, row=2, columnspan=2, sticky=tk.EW)

        self.job_file_button = ttk.Button(
            self.subframes[self.section_locs["Send"]],
            text="Create job file",
            command=self.create_job,
        )
        self.job_file_button.grid(column=0, row=1, sticky=tk.EW)
        self.send_button = ttk.Button(
            self.subframes[self.section_locs["Send"]],
            text="Send job",
            command=self.send,
            state=tk.DISABLED,
        )
        self.send_button.grid(column=1, row=1, sticky=tk.EW)
        self.name_entry = self.create_name_entry("Name", parent=self.subframes[0, 0])
        self.textbox = self.create_textbox("Output", parent=self.subframes[0, 1])
        self.update_frames()

    def create_name_entry(self, label, parent=None):

        name_entered = tk.StringVar(value=label)
        entry = ttk.Entry(parent, textvariable=name_entered)
        entry.pack(pady=10, padx=10, anchor=tk.CENTER, fill=tk.X)
        self.name_entered = name_entered
        return entry

    def create_textbox(self, label, parent=None):
        text_widget = scrolledtext.ScrolledText(parent)
        text_widget.pack(pady=10, padx=10, anchor=tk.CENTER, fill=tk.BOTH)
        text_widget.mark_set(tk.INSERT, tk.END)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.INSERT, label)
        text_widget.configure(state="disabled")
        return text_widget

    def update_textbox(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete(1.0, tk.END)
        textbox.insert(tk.INSERT, text)
        textbox.configure(state="disabled")

    def create_label(self, text, parent):
        label = ttk.Label(parent, text=text)
        label.pack(side=tk.TOP)
        return label

    def create_grid(self, rows=4, columns=2):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid = ttk.Frame(self, relief=tk.RAISED, padding=5)
        self.grid.grid(row=0, column=0, sticky="nsew")
        self.subgrids = np.empty((rows, columns), dtype=object)
        self.subframes = np.empty((rows, columns), dtype=object)
        self.super_subframes = np.empty((rows, columns), dtype=object)
        for i in range(rows):
            self.grid.rowconfigure(i, weight=1, minsize=200)
        for i in range(columns):
            if i == 0:
                self.grid.columnconfigure(i, weight=1, minsize=750)
            else:
                self.grid.columnconfigure(i, weight=1, minsize=400)
        for i in range(rows):
            for j in range(columns):
                self.subgrids[i, j] = ttk.Frame(self.grid, padding=5, relief=tk.RAISED)
                self.subgrids[i, j].grid(row=i, column=j, sticky="nsew")
                self.super_subframes[i, j] = VerticalScrolledFrame(self.subgrids[i, j])
                self.subframes[i, j] = self.super_subframes[i, j].interior
                self.super_subframes[i, j].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_frames(self):
        for super_subframe in self.super_subframes.flatten():
            super_subframe.create()

    def create_advanced_widgets(self, advanced_widget_args):
        self.advanced_widgets = {
            "Excitation": [],
            "Inhibition": [],
            "Axon": [],
            "Send": [],
            "ITD": [],
            "Threshold": [],
        }
        for type_name, type_ in advanced_widget_args.items():
            # print(type_name),
            func = None
            if type_name == "spinbox":
                func = lambda widget_args: self.create_total_spinbox(**widget_args)
            elif type_name == "checkbox":
                func = lambda widget_args: self.create_checkbox(**widget_args)
            elif type_name == "radiobuttons":
                func = lambda widget_args: self.create_radiobuttons(**widget_args)
            elif type_name == "listbox":
                func = lambda widget_args: self.create_listbox(**widget_args)

            for widget_key, widget_args in type_.items():
                # print(widget_args["reveal_cat"])
                widget_in_cat = func(widget_args)
                widget_in_cat.pack_forget()
                self.advanced_widgets[widget_args["reveal_cat"]].append(widget_in_cat)

    def create_menubar(self):
        self.option_add("*tearOff", tk.FALSE)
        menubar = tk.Menu(self)
        self["menu"] = menubar
        menu_options = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_options, label="Options")
        self.advanced_option_state = tk.BooleanVar(value=False)
        menu_options.add_checkbutton(
            label="Advanced",
            command=self.update_advanced_view,
            onvalue=True,
            offvalue=False,
            variable=self.advanced_option_state,
        )
        return menubar

    def reveal_advanced(self, val, category):
        if val.get():
            for widget in self.advanced_widgets[category]:
                widget.pack(padx=1, pady=1, fill=tk.X, anchor=tk.CENTER)
        else:
            for widget in self.advanced_widgets[category]:
                widget.pack_forget()
        # self.update_frames()



    def create_listbox(self, label, var_name, values, parent=None, reveal_cat=None):
        choicesvar = tk.StringVar(value=values)
        listbox = tk.Listbox(
            parent,
            listvariable=choicesvar,
            selectmode=tk.EXTENDED,
            justify=tk.CENTER,
        )
        listbox.bind("<<ListboxSelect>>", lambda e: self.on_cell_select(e))
        listbox.pack(pady=1, padx=1, anchor=tk.CENTER, fill=tk.BOTH, expand=True)
        return listbox

    def on_cell_select(self, event):
        # print("Selected cells:", event.widget.curselection())
        self.cell_selection = event.widget.curselection()

    def create_checkbox(
        self,
        label,
        var_name,
        default=False,
        parent=None,
        pack=True,
        reveal_cat=None,
        command=None,
        reveal=True,
    ):
        var = tk.BooleanVar(value=default)
        if reveal_cat is not None and reveal:
            checkbox = ttk.Checkbutton(
                parent,
                text=label,
                variable=var,
                command=lambda: self.reveal_advanced(var, reveal_cat),
            )
        elif command is not None:
            checkbox = ttk.Checkbutton(
                parent, text=label, variable=var, command=command
            )
        else:
            checkbox = ttk.Checkbutton(parent, text=label, variable=var)
        if pack:
            checkbox.pack(padx=1, pady=1, anchor=tk.CENTER)
        self.checkbox_vars[var_name] = var
        return checkbox

    def create_radiobuttons(
        self,
        major_label,
        minor_labels,
        var_name,
        default=False,
        parent=None,
        reveal_cat=None,
    ):
        var = tk.BooleanVar()
        frame = ttk.Frame(parent)
        frame.pack(pady=1, padx=1, anchor=tk.CENTER)
        label_string = tk.StringVar(value=major_label)
        label = ttk.Label(frame, textvariable=label_string)
        label.pack(side=tk.TOP, padx=1)
        for minor_label in minor_labels:
            radiobutton = ttk.Radiobutton(frame, text=minor_label, variable=var)
            radiobutton.pack(padx=1, pady=1, side=tk.LEFT)
        self.radiobutton_vars[var_name] = var
        return frame

    def create_spinbox_frame(self, parent):
        frame = ttk.Frame(parent, borderwidth=1)
        frame.pack(pady=1, padx=1, anchor=tk.E, fill=tk.BOTH)
        frame.grid_columnconfigure(0, weight=1, uniform="spinbox")
        frame.grid_columnconfigure(1, weight=1, uniform="spinbox")
        frame.grid_columnconfigure(2, weight=1, uniform="spinbox")
        return frame

    def create_spinbox_label(self, frame, var_label, pos=(1, 0), **kwargs):
        label_string = tk.StringVar(value=var_label)
        label = ttk.Label(
            frame, background="white", text=label_string.get(), width=30, **kwargs
        )
        label.grid(row=pos[0], column=pos[1], padx=1, pady=1, sticky=tk.NSEW)
        return label

    def create_spinbox_widget(
        self, from_, to, increment, frame, default=0.0, pos=(1, 1)
    ):
        var = tk.DoubleVar(value=default)
        spinbox = ttk.Spinbox(
            frame,
            textvariable=var,
            from_=from_,
            to=to,
            increment=increment,
            width=10,
            justify=tk.CENTER,
        )
        row, col = pos
        spinbox.grid(
            column=col,
            row=row,
            padx=1,
            pady=1,
            sticky=tk.EW,
        )
        return spinbox, var

    def create_total_spinbox(
        self,
        var_label,
        var_name,
        from_,
        to,
        increment,
        default,
        parent,
        reveal_cat,
        iterable=False,
    ):
        frame = self.create_spinbox_frame(parent)
        label = self.create_spinbox_label(
            frame, var_label, justify=tk.RIGHT, pos=(0, 0)
        )
        spinbox, var = self.create_spinbox_widget(
            from_, to, increment, frame, default, pos=(0, 1)
        )
        if iterable:
            check = self.create_checkbox(
                "Iterate",
                f"{var_name}_iterable",
                parent=frame,
                pack=False,
                command=lambda: self.check_iteration(
                    var_name, reveal_cat, frame, spinbox, default, increment, from_, to
                ),
            )
            check.grid(row=0, column=2)

        self.spinbox_vars[f"{var_name}_base"] = var
        return frame

    def forget_widget(self, widget):
        try:
            widget.grid_forget()
            # print("Grid forget")
        except:
            try:
                widget.pack_forget()
                # print("Pack forget")
            except Exception:
                "Widget not found"

    def unforget_widget(self, widget, loc=None):
        try:
            widget.grid(
                row=loc[0],
                column=loc[1],
                padx=1,
                pady=1,
                sticky=tk.EW,
            )
        except:
            try:
                widget.pack()
            except Exception:
                "Widget not found"

    def check_iteration(
        self, var_name, reveal_cat, parent, basic_spinbox, default, increment, from_, to
    ):
        if self.checkbox_vars[f"{var_name}_iterable"].get():
            # self.forget_widgets(basic_spinbox)
            self.create_iteration(
                var_name,
                reveal_cat,
                parent,
                basic_spinbox,
                default,
                increment,
                from_,
                to,
            )

        else:
            for widget in self.iterables[var_name]["spinboxes"]:
                self.forget_widget(widget)
            for widget in self.iterables[var_name]["labels"]:
                self.forget_widget(widget)
            self.unforget_widget(basic_spinbox, loc=(0, 1))

    def create_iteration(
        self, var_name, reveal_cat, parent, basic_spinbox, default, increment, from_, to
    ):
        self.forget_widget(basic_spinbox)
        self.iterables[var_name] = {}
        iterable_labels = [
            self.create_spinbox_label(
                parent,
                "From",
                pos=(4, 0),
                anchor=tk.CENTER,
            ),
            self.create_spinbox_label(
                parent,
                "To",
                pos=(4, 1),
                anchor=tk.CENTER,
            ),
            self.create_spinbox_label(
                parent,
                "Increment",
                pos=(4, 2),
                anchor=tk.CENTER,
            ),
        ]
        iterables = [
            self.create_spinbox_widget(
                from_,
                to,
                increment=increment,
                default=default,
                frame=parent,
                pos=(3, 0),
            ),
            self.create_spinbox_widget(
                from_,
                to,
                increment=increment,
                default=default + increment,
                frame=parent,
                pos=(3, 1),
            ),
            self.create_spinbox_widget(
                increment * 0.1,
                increment * 10,
                increment=increment,
                default=increment,
                frame=parent,
                pos=(3, 2),
            ),
        ]
        self.iterables[var_name]["spinboxes"] = [x[0] for x in iterables]
        self.iterables[var_name]["labels"] = iterable_labels
        self.iterables[var_name]["values"] = [x[1] for x in iterables]

    def get_simulation_values(self):
        checkbox_values = {
            k: v.get() for k, v in self.checkbox_vars.items() if "iterable" not in k
        }
        active_iterable_keys = [
            k for k, v in self.checkbox_vars.items() if "iterable" in k and v.get()
        ]
        spinbox_values = {
            "_".join(k.split("_")[:-1]): v.get() for k, v in self.spinbox_vars.items()
        }
        listbox_values = self.cell_selection
        logger.info(f"Arguments with iterated values:{active_iterable_keys}")
        iterables = {}
        for key in active_iterable_keys:
            tagless_key = "_".join(key.split("_")[:-1])
            iterables[tagless_key] = [
                v.get() for v in self.iterables[tagless_key]["values"]
            ]
        # Call the itd_test function with the collected values
        # itd_test(**checkbox_values, **spinbox_values)
        filenames = [self.cell_names[i] for i in listbox_values]
        itd_tester = ITDJob(
            filenames=filenames,
            iterables=iterables,
            **checkbox_values,
            **spinbox_values,
        )
        return itd_tester

    def create_job(self, dilled=True):
        day = datetime.datetime.now().strftime('%y%m%d')
        namedate = f"{self.name_entered.get()}_{day}"
        itd_tester = self.get_simulation_values()
        if dilled:
            serialized = dill.dumps(itd_tester)
            try:
                try:os.mkdir(
                    os.path.join(get_package_path("itd_job_builder/job_files"),namedate)
                )
                except:
                    logger.info("Job folder already exists")
                with open(os.path.join(get_package_path("itd_job_builder"),"job_files",namedate,f"{namedate}.pkl"), "wb") as f:
                    f.write(serialized)
            except Exception as e:
                logger.error(f"Error serializing job file", exc_info=e)
        self.send_button["state"] = tk.NORMAL
        logger.info("Procedure created")
        return itd_tester

    def run_procedure(self, itd_tester=None):
        logger.info("Running procedure")
        if itd_tester is None:
            itd_tester = self.create_job()
        iterables = itd_tester.iterables
        logger.info(f"it_dict:{iterables}")
        tasks = itd_tester.generate_tasks()
        run_tasks(tasks, iterables, job_name=self.name_entered.get())
        # threading.Thread(target=itd_job.run_tasks, args=(tasks,iterables)).start()

    def open_send_window(self):
        self.send_window = NSGWindow()

    def open_send_window_bg(self):
        threading.Thread(target=self.open_send_window).start()

    def send(self):
        self.create_job()
        self.create_archive()
        
    def create_archive(self):
        day = datetime.datetime.now().strftime('%y%m%d')
        namedate = f"{self.name_entered.get()}_{day}"
        
        itd_tester = self.create_job()
        os.makedirs(
            os.path.join(self.job_file_dir,namedate), exist_ok=True
        )
        
        copytree(
            os.path.join(get_package_path("itd_job_builder"),"itd_job"),
            self.temp_subdir,
            dirs_exist_ok=True,
        )
        copyfile(
            os.path.join(get_package_path("itd_job_builder"),"job_files",namedate,f"{namedate}.pkl"),
            os.path.join(self.temp_subdir,f"{namedate}.pkl")
        )
        copyfile(
            os.path.join(get_package_path(),"itd_job.py"),
            os.path.join(self.temp_subdir,"itd_job.py")
        )
        make_archive(os.path.join(self.job_file_dir,namedate, namedate), "zip", self.temp_dir)
        rmtree(self.temp_dir)

        logger.info("Archive created")
def main():
    logger.info("Starting ITD job builder")
    app = ITDBuildGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
