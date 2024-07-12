import sys
import time
import requests
import threading
import logger_configs
from threading import Event
import tkinter as tk
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font
from user import (
    get_instances, 
    get_connection_status, 
    set_connection_status
)
from emulators.bluestacks import (
    get_bluestacks_windows, 
    get_adb_port_for_window
)
from settings import RUN_LOCAL
from scripts.script_handler import (
    stop,
    start,
    pause,
    script_exists,
    is_script_paused,
    remove_temp_model,
    get_available_scripts,
    get_script_container, 
    get_script_version,
    remove_script_container,
    remove_all_temp_models,
    stop_all_scripts,
    show_paint
)
from emulators.adb_handler import close_adb_connection
from conn.client import request


logger = logger_configs.get_bot_logger(__name__)
ctk.set_appearance_mode('dark')

class BotInstance:

    def __init__(self, id: int, parent_frame: ctk.CTkFrame) -> None:
        self.id = id
        self.frame = ctk.CTkFrame(parent_frame)

        # Fiery theme colors
        bg_color = '#FF7F50'  # Coral
        fg_color = '#FFD700'  # Gold
        text_color = 'black'
        button_fg_color = '#FFA500'  # Orange
        button_hover_color = '#FF8C00'  # DarkOrange
        entry_bg_color = '#FFA500'  # Orange
        entry_text_color = 'black'
        dropdown_bg_color = '#FF7F50'  # Coral
        dropdown_text_color = 'black'

        self.window_select = ctk.CTkOptionMenu(
            self.frame, 
            values=list(get_bluestacks_windows().keys()), 
            fg_color=dropdown_bg_color, 
            text_color=dropdown_text_color, 
            dropdown_fg_color=fg_color, 
            dropdown_text_color=dropdown_text_color
        )
        self.window_select.pack(side='left', padx=(10, 0), pady=10)
        
        self.script_select = ctk.CTkOptionMenu(
            self.frame, 
            values=get_available_scripts(), 
            fg_color=dropdown_bg_color, 
            text_color=dropdown_text_color, 
            dropdown_fg_color=fg_color, 
            dropdown_text_color=dropdown_text_color
        )
        self.script_select.pack(side='left', padx=(10, 0), pady=10)

        self.pin_field = ctk.CTkEntry(
            self.frame, 
            placeholder_text='PIN...', 
            width=70, 
            show="*", 
            fg_color=entry_bg_color, 
            text_color='black',
            placeholder_text_color='black'
        )
        self.pin_field.pack(side='left', padx=(10, 0), pady=10)

        self.start_button = ctk.CTkButton(
            self.frame, 
            width=70, 
            text='Start', 
            command=self.start_script, 
            fg_color=button_fg_color, 
            text_color=text_color, 
            hover_color=button_hover_color, 
            border_color='black', 
            border_width=1
        )
        self.start_button.pack(side='left', padx=(10, 0), pady=10)

        self.pause_button = ctk.CTkButton(
            self.frame, 
            width=70, 
            text='Pause', 
            command=self.pause_script, 
            fg_color='#FFD700',  # Gold
            text_color=text_color, 
            hover_color='#FFC107',  # Amber
            border_color='black', 
            border_width=1
        )
        self.pause_button.pack(side='left', padx=(10, 0), pady=10)

        self.stop_button = ctk.CTkButton(
            self.frame, 
            width=70, 
            text='Stop', 
            command=self.stop_script, 
            fg_color='#FF4500',  # OrangeRed
            text_color=text_color, 
            hover_color='#FF6347',  # Tomato
            border_color='black', 
            border_width=1
        )
        self.stop_button.pack(side='left', padx=(10, 0), pady=10)

        self.view_screen = ctk.CTkButton(
            self.frame, 
            width=200, 
            text='View', 
            command=self.view_more, 
            fg_color=button_fg_color, 
            text_color=text_color, 
            hover_color=button_hover_color, 
            border_color='black', 
            border_width=1
        )
        self.view_screen.pack(side='right', padx=(10, 10), pady=10)

        self.frame.pack(padx=10, pady=10, expand=True, fill='both')
        self.frame.configure(border_color='black', border_width=1)

        self.pause_button.configure(state='disabled')
        self.stop_button.configure(state='disabled')

        self.frame.after(1000, self.update_instance_names)
        # self.id = id
        # self.frame = ctk.CTkFrame(parent_frame)

        # self.window_select = ctk.CTkOptionMenu(self.frame, values=list(get_bluestacks_windows().keys()), fg_color='#F2CDA3', text_color='black', dropdown_fg_color='white', dropdown_text_color='black')
        # self.window_select.pack(side='left', padx=(10, 0), pady=10)
        
        # self.script_select = ctk.CTkOptionMenu(self.frame, values=get_available_scripts(), fg_color='#F2CDA3', text_color='black')
        # self.script_select.pack(side='left', padx=(10, 0), pady=10)

        # self.pin_field = ctk.CTkEntry(self.frame, placeholder_text='Bank PIN...', width=70, show="*")
        # self.pin_field.pack(side='left', padx=(10,0), pady=10)

        # self.start_button = ctk.CTkButton(self.frame, width=70, text='Start', command=self.start_script)
        # self.start_button.configure(fg_color='green', text_color='black', hover_color='#02640f', border_color='black', border_width=1)
        # self.start_button.pack(side='left', padx=(10, 0), pady=10)

        # self.pause_button = ctk.CTkButton(self.frame, width=70, text='Pause', command=self.pause_script)
        # self.pause_button.configure(fg_color='#ffff00', text_color='black', hover_color='#ffea00', border_color='black', border_width=1)
        # self.pause_button.pack(side='left', padx=(10, 0), pady=10)

        # self.stop_button = ctk.CTkButton(self.frame, width=70, text='Stop', command=self.stop_script)
        # self.stop_button.configure(fg_color='red', text_color='black', hover_color='#cd0000', border_color='black', border_width=1)
        # self.stop_button.pack(side='left', padx=(10, 0), pady=10)

        # view_screen = ctk.CTkButton(self.frame, width=200, text='View', command=self.view_more)
        # view_screen.pack(side='right', padx=(10, 10), pady=10)

        # self.frame.pack(padx=10, pady=10, expand=True, fill='both')
        # self.frame.configure(border_color='black', border_width=1)

        # self.pause_button.configure(state='disabled')
        # self.stop_button.configure(state='disabled')

        # self.frame.after(1000, self.update_instance_names)

    def disable(self) -> None:
        logger.info(f'Disabling all widgets for bot instance: {self.id}')
        for widget in self.frame.winfo_children():
            try:
                widget.configure(state="disabled")
            except ctk.TkError:
                ...

    def start_script(self) -> None:
        need_to_wait = False
        window_name = self.window_select.get()
        script_name = self.script_select.get()
        adb_port = get_adb_port_for_window(window_name)
        bank_pin = self.pin_field.get()

        def set_buttons() -> None:
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')
            self.stop_button.configure(state='normal')
            self.script_select.configure(state='disabled')
            self.window_select.configure(state='disabled')

        if RUN_LOCAL:
            if len(bank_pin) > 4:
                logger.warning('Bank PIN cannot be longer than 4 digits.')
                messagebox.showwarning(title='Warning!', message='Bank PIN cannot be longer than 4 digits.')
                return
            
            if not bank_pin.isdigit() and bank_pin != '':
                logger.warning('Bank PIN must only contain numbers.')
                messagebox.showwarning(title='Warning!', message='Bank PIN must only contain numbers.')
                return

            if start(self.id, script_name, adb_port, window_name, self, bank_pin):
                logger.info(f'Starting local script: {script_name}')
                set_buttons()
        else:
            if len(bank_pin) > 4:
                logger.warning('Bank PIN cannot be longer than 4 digits.')
                messagebox.showwarning(title='Warning!', message='Bank PIN cannot be longer than 4 digits.')
                return
            
            if not bank_pin.isdigit() and bank_pin != '':
                logger.warning('Bank PIN must only contain numbers.')
                messagebox.showwarning(title='Warning!', message='Bank PIN must only contain numbers.')
                return

            if script_exists(script_name):
                container = get_script_container(script_name)
                client_version = container.version
                server_version = get_script_version(script_name)
                if client_version < server_version:
                    logger.info(f'Script: {script_name} is outdated, removing models, temaplates, and attempting to update/start.')
                    remove_temp_model(script_name)
                    remove_script_container(script_name)
                    need_to_wait = True
                else:
                    if start(self.id, script_name, adb_port, window_name, self.frame, bank_pin):
                        logger.info(f'Starting remote script: {script_name}')
                        set_buttons()
                        return
            else:
                need_to_wait = True

            if need_to_wait:
                request(event_name='request_script', script_name=script_name)
    
                def wait_and_start() -> None:
                    while not script_exists(script_name):
                        time.sleep(1)
                    if start(self.id, script_name, adb_port, window_name, self.frame, bank_pin):
                        logger.info(f'Update complete for script: {script_name}, script started.')
                        set_buttons()

                thread = threading.Thread(target=wait_and_start)
                thread.start()
                
    def pause_script(self) -> None:
        pause(self.id)
        is_paused = is_script_paused(self.id)
        button_text = 'Resume' if is_paused else 'Pause'
        self.pause_button.configure(text=button_text)

    def stop_script(self) -> None:
        stop(self.id)
        close_adb_connection(self.window_select.get())
        self.start_button.configure(state='normal')
        self.pause_button.configure(state='disabled')
        self.stop_button.configure(state='disabled')
        self.script_select.configure(state='normal')
        self.window_select.configure(state='normal')

    def view_more(self) -> None:
        print(f'View # {self.id}')
        show_paint(self.id)

    def update_instance_names(self) -> None:
        current_instances = list(self.window_select._values)
        updated_instances = list(get_bluestacks_windows().keys())
        if current_instances != updated_instances:
            self.window_select.configure(values=updated_instances)
        self.frame.after(1000, self.update_instance_names)

class MainGUI:
    def __init__(self) -> None:
        self.failed_connection_attemps = 0
        self.instance_frames = {}
        self.num_instances = get_instances()
        self.app = ctk.CTk()
        self.create_ui()

    def on_close(self) -> None:
        # if messagebox.askokcancel("Quit", "Do you want to exit PyschoBot?"):
        #     print("Closing application.")
        #     self.app.quit()
        #     self.app.destroy()
        sys.exit(0)

    def monitor_version(self) -> None:
        ...
        # client.send_message('check_version', {'version': 1.0})
        # self.app.after(1000, self.monitor_version)

    def check_internet_connection(self) -> None:
        try:
            request = requests.get('https://www.google.com')
            status_code = request.status_code
            if status_code == 200:
                self.failed_connection_attemps = 0
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            self.failed_connection_attemps += 1
            logger.warning('Internet connection lost, attemping to reconnect.')
            if self.failed_connection_attemps > 2:
                set_connection_status(False)
        finally:
            if not get_connection_status():
                logger.warning('Connection has been lost, disabling bot.')
                stop_all_scripts()
                remove_all_temp_models()
                messagebox.showerror(title='Connection Error', message='Please check your internet connection, restart the bot to continue!')
                for _, instance in self.instance_frames.items():
                    instance.disable()
            else:
                self.app.after(3000, self.check_internet_connection)

    def create_ui(self) -> None:
        self.app.title('PsychoBot')
        self.set_window_position(850, 745)
        self.create_menu_bar()
        self.create_frames()
        self.create_tabs()
        self.create_bot_instances()
        # self.app.protocol("WM_DELETE_WINDOW", self.on_close)
        self.app.resizable(False, False)
        self.app.after(3000, self.check_internet_connection)
        # self.app.after(1000, self.monitor_version)
        self.app.mainloop()

    def set_window_position(self, width, height):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

    def create_menu_bar(self) -> None:
        menu_bar = tk.Menu(self.app)
        self.app.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.app.quit)
        #
        edit_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        #
        help_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Discord')

    def create_frames(self) -> None:
        self.top_frame = ctk.CTkFrame(self.app, corner_radius=15, height=55)
        self.top_frame.pack(side='top', fill='x', padx=10, pady=(10, 0))
        self.top_frame.configure(border_color='black', border_width=1)
        #
        # news = News(self.top_frame)
        # self.news_label = ctk.CTkLabel(self.top_frame, text=f'News: Savi is a fuckin fag...', font=('Century Gothic', 14, 'bold'))
        # self.news_label.pack(side='left', fill='x', padx=10, pady=(5, 5))
        #
        self.center_frame = ctk.CTkFrame(self.app, corner_radius=15)
        self.center_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.center_frame.configure(border_color='black', border_width=1)

    def create_tabs(self) -> None:
        style = ttk.Style()
        style.configure("TNotebook.Tab", foreground="black", background="lightgray", padding=[5, 5], font=('Century Gothic', 10))    
        notebook = ttk.Notebook(self.center_frame, style="Rounded.TNotebook")
        notebook.pack(expand=True, fill='both')
        self.home_tab = ctk.CTkFrame(notebook)
        # notebook.add(self.home_tab, text='Home')
        # notebook.select(self.home_tab)
        self.bot_tab = ctk.CTkFrame(notebook)
        notebook.add(self.bot_tab, text='Bots')
        self.bot_tab_frame = ctk.CTkFrame(self.bot_tab)
        self.bot_tab_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.bot_tab_frame.configure(border_color='black', border_width=1)
        # self.settings_tab = ctk.CTkFrame(notebook)
        # notebook.add(self.settings_tab, text='Settings')

    def create_bot_instances(self) -> None:
        self.instance_frames = {id: BotInstance(id, self.bot_tab_frame) for id in range(self.num_instances)}