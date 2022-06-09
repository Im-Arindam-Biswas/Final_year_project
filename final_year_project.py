from curses import beep
from re import T
import datetime
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter import Button, ttk
from tkinter import simpledialog
from tkinter import filedialog
from playsound import playsound
import time

pomodoro_time = 25
short_time = 5
long_time = 15
#--------------------Main Class--------------------
class PomodoroTimer:

 

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("810x400")
        self.root.title("Pomodoro Timer Project")
        self.root.configure(bg='pink')

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 26),
                         background="#9ACD32", foreground="blue")
        self.s.configure("TButton", font=("Ubuntu", 16),
                         background="#9ACD32", foreground="red")
        self.s.configure("TLabel", foreground="red")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=40, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab4 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab5 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(
            self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(
            self.tab2, text="05:00", font=("Ubuntu", 48))
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(
            self.tab3, text="15:00", font=("Ubuntu", 48))
        self.long_break_timer_label.pack(pady=20)

        self.setting_label = ttk.Label(
            self.tab4, text="Click the button below to change the default time of pomodoro and breaks", font=("Ubuntu", 16))
        self.setting_label.pack(pady=20)

        self.setting_label = ttk.Label(
            self.tab5, text="Click the button below to view your pomodoro history", font=("Ubuntu", 16))
        self.setting_label.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")
        self.tabs.add(self.tab4, text="Settings")
        self.tabs.add(self.tab5, text="Logs")

        self.grid_layout = ttk.Frame(self.tab4)
        self.grid_layout.pack(pady=10)

        self.setting_button = ttk.Button(
            self.grid_layout, text="Settings", command=self.setting_butt)
        self.setting_button.grid(row=0, column=0)

        self.grid_layout = ttk.Frame(self.tab5)
        self.grid_layout.pack(pady=10)

        self.setting_button = ttk.Button(
            self.grid_layout, text="View Log", command=self.log_history)
        self.setting_button.grid(row=0, column=0)

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        self.start_button = ttk.Button(
            self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.skip_button = ttk.Button(
            self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(
            self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=2)

        self.pomodoro_counter_label = ttk.Label(
            self.grid_layout, text="Pomodoros: 0", font=("Ubuntu", 16))
        self.pomodoro_counter_label.grid(
            row=1, column=0, columnspan=3, pady=10)


        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.root.mainloop()


    #---------------start timer thread function defination-----------------
    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    #--------------------start timer function defination-------------------
    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1

        if timer_id == 1:
            full_seconds = 60*pomodoro_time
            playsound("pomodoro_started.mp3")
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1

            if not self.stopped:
                self.pomodoros += 1
                log_file = open("Pomodoro_log_history.txt", "a")
                log_file.write(str(datetime.datetime.now().strftime(
                    "%x"))+" "+str(datetime.datetime.now().strftime("%X"))+" ")
                log_file.write("____POMODORO COMPLETED SUCCESSFULLY___\n")
                log_file.close()
                playsound("pomodoro_ends.mp3")
                playsound("beep-06.mp3")
            if not self.stopped or self.skipped:
                self.pomodoro_counter_label.config(
                    text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros != 0 and self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                    self.start_timer()
                else:
                    self.tabs.select(1)
                self.start_timer()
        elif timer_id == 2:
            full_seconds = 60*short_time
            playsound("short_break_started.mp3")
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped:
                playsound("short_break_ends.mp3")
                playsound("beep-06.mp3")
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        elif timer_id == 3:
            full_seconds = 60 * long_time
            playsound("long_break_started.mp3")
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.configure(
                    text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped:
                playsound("long_break_ends.mp3")
                playsound("beep-06.mp3")
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid timer id")

        
    #--------------------Reset clock function defination--------------------
    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text=str(pomodoro_time)+":00")
        self.short_break_timer_label.config(text=str(short_time)+":00")
        self.long_break_timer_label.config(text=str(long_time)+":00")
        self.running = False

    #--------------------Skip clock function defination--------------------
    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomodoro_timer_label.config(text=str(pomodoro_time)+":00")
        elif current_tab == 1:
            self.short_break_timer_label.config(text=str(short_time)+":00")
        elif current_tab == 2:
            self.long_break_timer_label.config(text=str(long_time)+":00")
        self.stopped = True
        self.skipped = True

    #--------------------Settings button function defination--------------------
    def setting_butt(self):
        self.stopped = True
        print("setting button working")
        global pomodoro_time
        global short_time
        global long_time
        pomodoro_time = simpledialog.askinteger(
            "Settings", "Enter new time for pomodoro")
        short_time = simpledialog.askinteger(
            "Settings", "Enter new time Short Break")
        long_time = simpledialog.askinteger(
            "Settings", "Enter new time Long Break")
        self.tabs.select(0)
        self.pomodoro_timer_label.config(text=str(pomodoro_time)+":00")
        self.short_break_timer_label.config(text=str(short_time)+":00")
        self.long_break_timer_label.config(text=str(long_time)+":00")

    # -------------------Log history function defination-------------------
    def log_history(self):
        print("view log running")
        file = open("Pomodoro_log_history.txt", 'r')
        top = tk.Toplevel(self.root)
        top.geometry("750x250")
        top.title("Logs")
        tk.Label(top, text=str(file.read()), font=(
            'Mistral 10')).place(x=150, y=80)
        file.close()


PomodoroTimer()