# !/usr/local/bin/python3
# ADD comments
# ADD log file support
from .fileaccess import get_package_path
import datetime
import subprocess
import os
import shutil
import time
import tkinter.scrolledtext
import numpy as np
import tkinter
import tkinter.filedialog
import pickle
import tkinter.ttk
import logging

# BUG job upload needs restart to see new jobs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NSGWindow:
    URL = "https://nsgr.sdsc.edu:8443/cipresrest/v1"
    USER = "jared"
    PASSWORD = "Finniggy1319!"
    KEY = "MSODM-3491DEF83CF34CF9BBB455E487619054"
    TOOL = "NEURON_EXPANSE"

    def __init__(self):
        try:
            with open("jobs.pickle", "rb") as handle:
                loaded_jobs = pickle.load(handle)
                self.job_dict = loaded_jobs
        except:
            self.job_dict = {}
        self.refresh_jobs()
        self.window = tkinter.Tk()
        self.window.resizable(True, True)
        self.window.grid_rowconfigure(0, weight=1)
        for col in range(3):
            self.window.grid_columnconfigure(col, weight=1)
        # self.window.configure(background="#d2d7e7")
        self.window.title("NSG Job Submission")
        self.clicked = tkinter.StringVar()
        self.clicked.set("Select submitted job")
        # getting screen width and height of display
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))

        # setting tkinter window size

        self.job_message = tkinter.scrolledtext.ScrolledText(
            self.window,
            wrap=tkinter.NONE,
            bg="#283618",
            width=int(width / 7),
            height=int(height / 7),
        )

        # self.job_message.place(x=0, y=0, relwidth=1, relheight=1)

        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.delete(1.0, tkinter.END)
        longhorn_art = open(f"{get_package_path()}/longhorn/longhorn.txt", "r").readlines()
        longhorn_center = ""
        for line in longhorn_art:
            longhorn_center += line.strip().center(int(width / 7)) + "\n"

        self.job_message.insert(tkinter.INSERT, longhorn_center)
        self.job_message.configure(state="disabled")
        self.job_message.grid(column=0, row=0, columnspan=3, sticky=tkinter.NSEW)

        self.file_url_dict = {}
        self.job_info_button = tkinter.Button(
            self.window,
            text="Get job info",
            command=self.view_job_info,
            state="disabled",
        )
        self.job_info_button.grid(column=1, row=2, sticky=tkinter.EW)
        self.name_entered = tkinter.StringVar()
        self.name_entered.set("Name")
        self.name_entry = tkinter.Entry(
            self.window, textvariable=self.name_entered, state=tkinter.DISABLED
        )
        self.name_entry.grid(column=0, row=3, sticky=tkinter.EW)
        self.runtime_text = tkinter.Label(self.window, text="Runtime (hrs)")
        self.runtime_text.grid(column=0, row=5, sticky=tkinter.EW)
        self.runtime_slider = tkinter.Scale(
            self.window, from_=1, to=30, orient=tkinter.HORIZONTAL, length=250
        )
        self.runtime_slider.grid(column=0, row=4, sticky=tkinter.EW)
        self.delete_button = tkinter.Button(self.window,
            text="Delete job", command=self.delete_job, state="disabled"
        )
        self.delete_button.grid(column=1, row=3, padx=5, sticky=tkinter.EW)
        self.make_file_widgets()
        logger.info("main window initialized")
        upload_button = tkinter.Button(
            self.window,
            text="Select job directory",
            width=25,
            command=self.file_button_click,
        )
        upload_button.grid(column=0, row=1, sticky=tkinter.EW)

        send_button = tkinter.Button(
            self.window,
            text="Submit job",
            width=25,
            command=self.submit_job,
        )

        send_button.grid(column=0, row=2, sticky=tkinter.EW)

        # photo = ImageTk.PhotoImage(Image.open("UT_LONGHORN.png"))
        # # Resizing image to fit on button
        # longhorn_can = tkinter.Canvas(self.window, height=50, width=50)
        # longhorn_can.grid(
        #     column=2,
        #     row=4,
        #     sticky=tkinter.EW,
        # )
        # longhorn_button = longhorn_can.create_image(200, 25, image=photo)
        # longhorn_can.tag_bind(longhorn_button, "<Button-1>", self.check_state)

        drop = tkinter.OptionMenu(
            self.window,
            self.clicked,
            *self.dropdown_jobs,
            command=self.dropdown_command,
        )
        drop.config(width=50)
        drop.grid(column=1, row=1, sticky=tkinter.EW)


        # job_workdir_button = tkinter.Button(
        #     nsg_window.window,
        #     text="get working directory",
        #     command=nsg_window.get_workdir,
        #     width=25,
        # )
        # job_workdir_button.grid(padx=5, pady=15, side=tkinter.BOTTOM)
        refresh_jobs_button = tkinter.Button(
            self.window,
            text="Refresh jobs",
            borderwidth=1,
            command=self.refresh_jobs,
        )
        refresh_jobs_button.grid(column=1, row=4, padx=5, sticky=tkinter.EW)





    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def make_loading_window(self, name):
        self.loading_window = tkinter.Tk()
        self.loading_window.withdraw()
        self.loading_window.title(name)
        self.loading_window.geometry("200x50")
        self.center_window(self.loading_window)
        self.loading_window.resizable(False, False)
        self.progress = tkinter.ttk.Progressbar(
            self.loading_window, orient=tkinter.HORIZONTAL, length=175
        )
        self.progress.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.loading_window.wm_deiconify()

    def destroy_loading_window(self):
        self.loading_window.destroy()

    def increment_loading_window(self, inc):
        self.progress.step(inc)
        self.progress.update()

    def list_files_and_enable_button(self, selection=None):
        self.job_info_button.configure(state="normal")
        self.delete_button.configure(state="normal")
        job_id = self.job_dict[selection]
        logger.info(f"job {selection} selected")
        self.list_files(job_id)
        logger.info(f"files for job {selection} listed")

    def file_button_click(self):
        self.directory_path = tkinter.filedialog.askdirectory(
            initialdir="/Volumes/oj hardrive/goldingLabMSO/Jared"
        )
        self.archive()
        self.job_message.configure(state="normal")
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.insert(tkinter.INSERT, f"{self.directory_name}.zip created")
        self.job_message.configure(state="disabled")
        self.name_entry.configure(state=tkinter.NORMAL)

    def archive(self):
        self.directory_name = os.path.basename(self.directory_path)
        # try:
        #     shutil.rmtree(f"{self.directory_path}/sub/golding_NEURON")
        # except:
        #     pass
        # shutil.copytree(
        #     ".././golding_NEURON", f"{self.directory_path}/sub/golding_NEURON"
        # )
        day = datetime.datetime.now().strftime('%y%m%d')
        self.zipfile_name = f"{self.directory_name}{day}"
        try:
            os.mkdir("NSG Archive")
        except:
            pass
        shutil.make_archive(
            f"NSG Archive/{self.zipfile_name}",
            "zip",
            root_dir=self.directory_path,
        )
        # shutil.rmtree(f"{self.directory_path}/sub/golding_NEURON")
        logger.info(f"{self.directory_name}{day} archived")
    def submit_job(self):
        if not hasattr(self, "directory_path"):
            self.job_message.mark_set(tkinter.INSERT, tkinter.END)
            self.job_message.configure(state="normal")
            self.job_message.delete(1.0, tkinter.END)
            self.job_message.insert(
                tkinter.INSERT, "must choose directory for job submission"
            )
            self.job_message.configure(state="disabled")
            return
        else:
            self.RUNTIME = self.runtime_slider.get()
            self.name_entered = self.name_entry.get()
            params = {
                "Client Job ID": self.name_entered,
                "Tool": self.TOOL,
                "Runtime": self.RUNTIME,
                "Archive filename": self.zipfile_name,
                "Input filename": self.directory_name,
            }
            logger.info(f"Job submitted\n {', '.join(f'{key}: {value}' for key, value in params.items())}")
            logger.info(params)
            output = subprocess.run(
                f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER} -F tool={self.TOOL} -F input.infile_=@'./NSG Archive/{self.zipfile_name}.zip' -F metadata.statusEmail=true -F metadata.clientJobId={self.name_entered}  -F vparam.runtime_={self.RUNTIME}  -F vparam.filename_={self.directory_name}.py -F vparam.pythonoption_=1 -F vparam.tasks_per_node_=128 -F vparam.number_cores_=128 -F vparam.number_gbmemorypernode_=240",
                capture_output=True,
                text=True,
                shell=True,
                check=True,
            ).stdout

            self.output = output
            self.job_message.configure(state="normal")
            self.job_message.delete(1.0, tkinter.END)
            self.job_message.mark_set(tkinter.INSERT, tkinter.END)
            self.job_message.insert(tkinter.INSERT, output)
            self.job_message.configure(state="disabled")

    # FIXME certain jobs aren't stored into dict
    def list_jobs(self):
        self.make_loading_window("Listing jobs")
        if hasattr(self, "job_dict"):
            previous_job_dict = self.job_dict
            print("got previous")
        else:
            previous_job_dict = {}
        try:
            print(time.time())
            job_list = subprocess.run(
                f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER}",
                capture_output=True,
                text=True,
                shell=True,
                check=True,
            ).stdout

        except:
            job_list = ""
        job_list_np = np.array(job_list.splitlines())
        jobs = []
        urls = []
        for line in job_list_np:
            if line.find("title") != -1:
                urls.append(line)
        for url in urls:
            first_pass = url.split(">")[1]
            second_pass = first_pass.split("<")[0]
            jobs.append(second_pass)
        job_dict = {}
        previous_job_ids = list(previous_job_dict.values())
        # print(previous_job_ids)
        previous_job_names = list(previous_job_dict.keys())
        self.job_count = len(jobs[1:])
        print(self.job_count)
        jobs_loaded = 0
        
        if len(jobs) > 10:
            jobs_to_query = jobs[-10:]
        else:
            jobs_to_query = jobs[1:]
        inc = 99 / len(jobs_to_query)
        for job_ind, job in enumerate(jobs_to_query):
            self.increment_loading_window(inc)
            if job in previous_job_ids:
                job_dict[previous_job_names[previous_job_ids.index(job)]] = job
                continue
            else:
                print("not skipped", job)
            status = subprocess.run(
                f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER}/{job}",
                capture_output=True,
                text=True,
                shell=True,
                check=True,
            ).stdout
            status_list = np.array(status.splitlines())
            for idx, line in enumerate(status_list):
                if line.find("clientJobId") != -1:
                    nickname_line = status_list[idx + 1]
                    first_pass = nickname_line.split(">")[1]
                    client_id = first_pass.split("<")[0]
                if line.find("dateSubmitted") != -1:
                    date_line = line
                    date_hyph = date_line.split(">")[1].split("T")[0]
                    yr = int(date_hyph.split("-")[0])
                    mo = int(date_hyph.split("-")[1])
                    day = int(date_hyph.split("-")[2])
                    date = datetime.date(yr, mo, day)
                    date_str = date.strftime("%y%m%d")
            if f"{client_id}_{date_str}" in list(job_dict.keys()):
                job_num = sum(
                    f"{client_id}_{date_str}" in job for job in list(job_dict.keys())
                )
                job_dict[f"{client_id}_{date_str}_{job_num}"] = job
            else:
                job_dict[f"{client_id}_{date_str}"] = job
        self.destroy_loading_window()
        jobs = jobs[1:]
        with open(os.path.join(get_package_path("nsg_portal"),"jobs.pickle"), "wb") as handle:
            pickle.dump(job_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return job_dict

    def list_files(self, selection=None):
        try:
            self.file_drop.grid_forget()
            self.download_button.grid_forget()
        except:
            pass
        self.selected_job = selection
        file_list = subprocess.run(
            f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER}/{self.selected_job}/output",
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        ).stdout
        file_list_np = np.array(file_list.splitlines())
        jobs = []
        untrimmed_urls = []
        untrimmed_filenames = []
        urls = []
        filenames = []
        file_url_dict = {}
        for line in file_list_np:
            if line.find("url") != -1:
                untrimmed_urls.append(line)
            if line.find("title") != -1:
                untrimmed_filenames.append(line)
        if len(untrimmed_filenames) < 1:
            file_list = subprocess.run(
                f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER}/{self.selected_job}/workingdir",
                capture_output=True,
                text=True,
                shell=True,
                check=True,
            ).stdout
            file_list_np = np.array(file_list.splitlines())
            jobs = []
            untrimmed_urls = []
            untrimmed_filenames = []
            urls = []
            filenames = []
            file_url_dict = {}
            for line in file_list_np:
                if line.find("url") != -1:
                    untrimmed_urls.append(line)
                if line.find("title") != -1:
                    untrimmed_filenames.append(line)

        for url in untrimmed_urls:
            trimmed_start = url.split(">")[1]
            trimmed = trimmed_start.split("<")[0]
            urls.append(trimmed)
        for filename in untrimmed_filenames:
            trimmed_start = filename.split(">")[1]
            trimmed = trimmed_start.split("<")[0]
            filenames.append(trimmed)

        for url, filename in zip(urls, filenames):
            file_url_dict[filename] = url
        self.file_url_dict = file_url_dict
        self.make_file_widgets()

    def make_file_widgets(self):
        try:
            if len(self.file_url_dict) < 1:
                values = ["Job not loaded"]
            else:
                values = list(self.file_url_dict.keys())

            self.file_clicked = tkinter.StringVar()
            self.file_clicked.set("Select file")

            self.file_drop = tkinter.OptionMenu(
                self.window,
                self.file_clicked,
                *values,
            )

            self.file_drop.config(width=25)
            self.file_drop.grid(column=2, row=1, sticky=tkinter.EW)

            self.download_button = tkinter.Button(
                self.window, text="Download", command=self.download_file
            )
            self.download_button.grid(column=2, row=2, sticky=tkinter.EW)
            if "Job not loaded" in values:
                self.file_drop.configure(state="disabled")
                self.download_button.configure(state="disabled")
        except:
            pass

    def get_job_info(self) -> None:

        self.job_handle = self.job_dict[self.clicked.get()]
        try:
            job_status = subprocess.run(
                f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER}/{self.job_handle}",
                capture_output=True,
                text=True,
                shell=True,
                check=True,
            ).stdout
        except:
            job_status = ""

        return job_status

    def view_job_info(self):
        s = self.get_job_info()
        self.job_message.configure(state="normal")
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.insert(tkinter.INSERT, s)
        self.job_message.configure(state="disabled")
        logger.info(f"job info for {self.clicked.get()} displayed")

    def download_file(self):
        file_key = self.file_clicked.get()
        try:
            os.remove(f"{os.getcwd()}/NSG Downloads/{self.clicked.get()}/{file_key}")
        except:
            Exception("file couldn't be removed")
        file_url = self.file_url_dict[file_key]

        file_download_output = subprocess.run(
            f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} -O -J {file_url} --output-dir 'NSG Downloads/{self.clicked.get()}' --create-dirs",
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        ).stdout

        self.job_message.configure(state="normal")
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.insert(tkinter.INSERT, f"{file_key} downloaded \n")
        self.job_message.configure(state="disabled")
        logger.info(f"{file_key} downloaded from {self.clicked.get()}")

    def get_workdir(self):
        self.job_handle = self.job_dict[self.clicked.get()]
        workdir = subprocess.run(
            f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} {self.URL}/job/{self.USER}/{self.job_handle}/workingdir",
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        ).stdout
        self.job_message.configure(state="normal")
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.insert(tkinter.INSERT, workdir)
        self.job_message.configure(state="disabled")

    def refresh_jobs(self):
        try:
            self.drop.grid_forget()
        except:
            pass
        self.job_dict = self.list_jobs()
        self.job_list = list(self.job_dict.keys())
        disable_dropdown = False
        self.dropdown_command = None
        self.dropdown_jobs = ["No jobs available"]
        if len(self.job_list) == 0:
            self.dropdown_jobs = ["No jobs available"]
            self.dropdown_command = None
        elif len(self.job_list) > 10:
            self.dropdown_jobs = self.job_list[-10:]
            self.dropdown_command = self.list_files_and_enable_button
        else:
            self.dropdown_jobs = self.job_list
            self.dropdown_command = self.list_files_and_enable_button
        logger.info("jobs refreshed")

    def delete_job(self):
        self.job_handle = self.job_dict[self.clicked.get()]
        file_delete_output = subprocess.run(
            f"curl -u {self.USER}:{self.PASSWORD} -H cipres-appkey:{self.KEY} -X DELETE {self.URL}/job/{self.USER}/{self.job_handle}",
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        ).stdout
        self.drop.configure(text="Submitted jobs")
        self.refresh_jobs()
        self.job_message.configure(state="normal")
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.insert(tkinter.INSERT, f"{self.job_handle} deleted \n")
        self.job_message.configure(state="disabled")
        logger.info(f"{self.clicked.get()} deleted")
    def mark(self, direction=None):

        if self.state == "snake":
            spot = tkinter.INSERT
        else:
            spot = tkinter.CURRENT
        self.job_message.configure(state="normal")
        if direction == "up":
            spot = tkinter.INSERT + "- 1 line"
        if direction == "down":
            spot = tkinter.INSERT + "+ 1 line"
        if direction == "left":
            spot = tkinter.INSERT + "- 2 char"
        if direction == "right":
            spot = tkinter.INSERT + "+ 2 char"
        self.job_message.delete(spot + "-1 char", spot)
        self.job_message.insert(spot, "*")
        self.job_message.mark_set(tkinter.INSERT, spot)
        self.job_message.update()
        self.job_message.configure(state="disabled")

    def draw(self):
        self.job_message.configure(state="normal")
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.focus()
        filler = ""
        for line in range(self.job_message["height"]):
            for char in range(self.job_message["width"]):
                filler += " "
            filler += "\n"
        self.job_message.insert(tkinter.INSERT, filler)
        self.job_message.bind("<space>", lambda event: self.mark())
        self.job_message.configure(state="disabled")

    def snake(self):
        self.job_message.configure(state="normal")
        self.job_message.delete(1.0, tkinter.END)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.focus()
        filler = ""
        for line in range(self.job_message["height"]):
            for char in range(self.job_message["width"]):
                filler += " "
            filler += "\n"
        self.job_message.insert(tkinter.INSERT, filler)
        self.job_message.mark_set(tkinter.INSERT, tkinter.END)
        self.job_message.bind("w", lambda event: self.mark(direction="up"))
        self.job_message.bind("a", lambda event: self.mark(direction="left"))
        self.job_message.bind("s", lambda event: self.mark(direction="down"))
        self.job_message.bind("d", lambda event: self.mark(direction="right"))
        self.job_message.configure(state="disabled")

    def check_state(self, event):
        try:
            if self.state == None:
                self.state = "draw"
                self.draw()
            elif self.state == "draw":
                self.state = "snake"
                self.snake()
            elif self.state == "snake":
                self.state = None
                self.job_message.configure(state="normal")
                self.job_message.delete(1.0, tkinter.END)
                self.job_message.mark_set(tkinter.INSERT, tkinter.END)
                self.job_message.configure(state="disabled")
                self.job_message.unbind(
                    "w",
                )
                self.job_message.unbind(
                    "a",
                )
                self.job_message.unbind(
                    "s",
                )
                self.job_message.unbind("d")
        except:
            self.state = "draw"
            self.draw()
def main():
    logger.info("Creating NSG portal")
    app = NSGWindow()
    app.window.mainloop()
if __name__ == "__main__":
    main()

