import ctypes
from contextlib import suppress
import tkinter as tk
from tkinter import ttk, StringVar, PhotoImage, Scrollbar, Tk, Frame, Label, Button, Entry
import os
from tkinter import filedialog
import re
import struct

from pytqs.utils import icon


ctypes.windll.shcore.SetProcessDpiAwareness(2)

TQSBUILD_CONCRETE = 0
TQSBUILD_PRECAST = 1
TQSBUILD_ALVEST = 2
TQSBUILD_CONCRETEWALL = 3

TREESELECTION_ALL = 0
TREESELECTION_NOTBUILDINGS = 1

TQSFLOOR_CONCRETE = 0
TQSFLOOR_PRECAST = 1
TQSFLOOR_ALVEST = 2
TQSFLOOR_CONCRETEWALL = 3

TQSFLOOR_FUN = 1   # Fundação
TQSFLOOR_SUB = 2   # Subsolo
TQSFLOOR_TER = 3   # Térreo
TQSFLOOR_MEZ = 4   # Mezzanino
TQSFLOOR_TRN = 5   # Transição
TQSFLOOR_PRI = 6   # Primeiro
TQSFLOOR_TIP = 7   # Tipo
TQSFLOOR_COB = 8   # Cobertura
TQSFLOOR_ATI = 9   # Ático
TQSFLOOR_DUP = 10  # Duplex
TQSFLOOR_TRI = 11  # Triplex

folder_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAd0lEQVQ4jcVTWwrAIAzLhufqdjVv1vZiHfHDIXMP5ocBCSpJU6xLRAQGsI6IieTuUN0uF/tuEJF3h5wRZsZGGj7Pn5FoIrLB3RoGrCRT7RdmwpL8LsEXprYY/BGTueYmqAYjCRZuenPwBr5CnYO5LRSXAUz+jQAOEHuqWL76r+QAAAAASUVORK5CYII="
conc_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAWElEQVQ4jWP8////fwYsgJGxFUXw//9qbMoYmLCKImnCpREGMFyAbjM2Q5EBCzGK8BmO1QBCrhh1wbBzATglkmIjukVwFxBK87hcAzeAXFfgzM5EAQYGBgDqXjK4fqF0TQAAAABJRU5ErkJggg=="
alv_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAVklEQVQ4jWP8////fwYKACMDQwtBA/7/r2ZgZGzFKscCIqYx1ODUnMXQAmdjU8dEifMZqOEF6gYiPptwuYgFFjCEAgsG0NVRNxDJ8cJoShzwlMjAwAAAr+Q8VYuo15UAAAAASUVORK5CYII="
preo_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAhklEQVQ4jc2R3QqAIAxGZ/lc4nsFikLvJb5XLHZhSG626KZz588O2zeDiAgfsFRqzD4YEDf2/o5t55SO6ynGFbj7qYAIIUDOefjkvdcJJEopouxRwI3jnNMJKMiGFKgo6At6kUogbaRRa5UFLSSak9uIqoMZ/UZeC7hx1AIpyOVNBz8UAMAJbZgrNEuSJycAAAAASUVORK5CYII="
parcon_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAxElEQVQ4jY2T0QqDMAxFr913Dftfe5DC9l+VfZd0JHBLjGldXoox9/S0IoB3K6U0u87KzyUAyDmjlAPb9tB1WT6ISvqc2/enPiug1noLsWFZJSPVDWYQG5aSVWY7QMLSHEFsuLUXmDkZkMwXcka7ow3bTLI0GaCeBfnw0ICD6/rtPQ76uhjws/gdLHxq4CF3BrwXBVCZkH8MeNzEy4kgkQENmVODCMKdrYEPd8AIYg2i8AkQQbyBDytYfslLM/gbozAA/AAGK+IJCFNXZQAAAABJRU5ErkJggg=="
pav_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAX0lEQVQ4jWP8////fwYKACMDQwtFBjCADIABZDYugK6eBd04RsZWkqzH8ML//9X4NaBZwISsiZBmbGqZSHIvFjBqABWiEWwATBOxiQhZPUZKJMsFRFmLy0CKsjMDAwMAVzxe6g2dMM8AAAAASUVORK5CYII="


class TQSFloor():
    def __init__(self, name: str, project_number: int, repetitions: int, project_class: int, height: float):
        self.name = name
        self.project_number = project_number
        self.repetitions = repetitions
        self.project_class = project_class
        self.height = height
    
    def __repr__(self) -> str:
        return f"TQSFloor[{self.project_number}, {self.name}, {self.repetitions}x, {self.project_class}, {self.height}m]"


class TQSProject():
    def __init__(self, project_path: str):
        self.path = project_path
        self.bde_file = f"{project_path}/EDIFICIO.BDE"
        self.bde_content = open(self.bde_file, 'rb').read()
        self.name = os.path.basename(project_path)
        self.directory = os.path.dirname(project_path)
        self.project_type = self.get_project_type()
        self.floor_names = self.get_floor_names()
        self.floors = self.get_floors()
        self.code = self.get_code()
        self._subfolders = None

    @property
    def subfolders(self):
        if self._subfolders is None:
            self._subfolders = self.get_subfolders()

        return self._subfolders
        
    def get_project_type(self) -> int:
        content = open(self.bde_file, 'rb').read()
        typ = content.partition(b'\xCD\xCC\x4C\x3F\x09')[2][11]
        is_pre = content.partition(b'\x13\x9E\xA8\x97')[2][336]
        if typ == 0:
            return 1 if is_pre else 0
        return typ + 1

    def get_subfolders(self) -> list[str]:
        def string_between(string: str, start: str, end: str) -> str:
            return string.partition(start)[2].split(end)[0]
        
        def decode_folder_string(data: bytes) -> list[str]:
            folders = []
            while data:
                num_char = int(data[0])
                folders.append(str(data[4:3+num_char], "cp1252"))
                data = data[4+num_char:]
                if len(folders) >= 8:
                    break
            return folders

        def split_first_list(content: bytes, project_name: str) -> list[str]:
            if b'\x00\x39\x40' in content:
                data = string_between(content, b'\xFC\x07\x00\x00\x36', b'\x00\x39\x40')
            else:
                data = string_between(content, b'\xFC\x07\x00\x00\x36', b'\x66\x66\x66\x66\x66\x66\xF6\x3F')
            data = data.partition(str.encode(project_name, encoding="cp1252"))[2].partition(b'\x01')[2][19:]
            return decode_folder_string(data)

        def split_second_list(content) -> list[str]:
            data = string_between(content, b'\x40\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01', b'\x80')[126:].partition(b'\x01')[2][4:]
            return decode_folder_string(data)

        return [folder for folder in (split_first_list(self.bde_content, self.name) + split_second_list(self.bde_content)) if folder]
    
    def get_code(self) -> str:
        if self.project_type in [0, 1]:
            if str.encode("NB1-78", encoding="cp1252") in self.bde_content:
                return "NB1-78"
            elif str.encode("NBR-6118-2003", encoding="cp1252") in self.bde_content:
                return "NBR-6118:2003"
            elif str.encode("NBR-6118-2014", encoding="cp1252") in self.bde_content:
                return "NBR-6118:2014"
            elif str.encode("CIRSOC-2005", encoding="cp1252") in self.bde_content:
                return "CIRSOC-2005"
            elif str.encode("ACI-318-05", encoding="cp1252") in self.bde_content:
                return "ACI-318-05"
            elif str.encode("ACI-318-14", encoding="cp1252") in self.bde_content:
                return "ACI-318-14"
        elif self.project_type == 2:
            code_number = self.bde_content.partition(b'\x7B\x14\xAE\x47\xE1\x7A\x94\x3F\x33\x33\x33\x33\x33\x33\xF3\x3F')[2][92]
            if code_number == 0:
                return "NBR-10837:1989"
            elif code_number == 1:
                return "NBR-15961-1:2011"
            elif code_number == 2:
                return "NBR-15812-1:2010"
            elif code_number == 3:
                return "NBR-16868-1:2020"
        elif self.project_type == 3:
            return "NBR-16055:2012"

        return "Norma indefinida"
    
    def get_floor_names(self) -> list[str]:
        data = self.bde_content.partition(b'\xFC\x07\x00\x00\x36')[2].partition(b'\xFC\x07\x00\x00\x36')[2].split(b'\x00\x39\x40')[0].partition(str.encode(self.name, encoding="cp1252"))[0]
        return [str(folder, "cp1252") for folder in filter(lambda a: len(a) != 1 or a >= b'\x30', [s for s in data[511:-5].split(b'\x00') if s])]
    
    def get_floors(self) -> list[TQSFloor]:
        content = self.bde_content.partition(b'\xCD\xCC\x4C\x3F\x09')[2]
        return [TQSFloor(floor, content[229+i*1850], content[625+i*1850], content[631+i*1850], round((struct.unpack('!f', content[627+i*1850:631+i*1850][::-1])[0]), 3)) for i, floor in enumerate(self.floor_names)]
    
    def get_alvest_block_specs(self) -> list[tuple[float, float, float]]:
        if self.project_type != 2:
            return None
        instalv_text = open(f"{self.path}\\INSTALV.DAT", "r").read()
        material_string_section = re.search(r'\s+\d+\s+Quantidade de fbks\/fps na tabela(.+)\d+\s+Material\spré-estabelecido:', instalv_text, re.S)[1]
        material_rows = [list(filter(None, striped_row.split(" "))) for row in material_string_section.split("\n") if (striped_row := row.strip())]

        return [(float(i[0]), float(i[1]), float(i[6])) for i in material_rows]
    
    def get_alvest_load_reduction(self) -> bool:
        if self.project_type != 2:
            return False
        
        carrpor_text = open(f"{self.path}\\ESPACIAL\\CARRPOR.DAT", "r").read()
        return int(re.search(r'(\d+)\s+\/\/\sNúmero\sde\scasos\sordenados', carrpor_text, re.M)[1]) == 9
    
    def get_alvest_grout_specific_weight(self) -> float:
        if self.project_type != 2:
            return None
        instalv_text = open(f"{self.path}\\INSTALV.DAT", "r").read()
        return float(re.search(r'^\s*(\d+.?\d*)\s+Peso específico graute', instalv_text, re.M)[1])
    
    def get_alvest_wind_transfer(self) -> int:
        if self.project_type != 2:
            return None
        instalv_text = open(f"{self.path}\\INSTALV.DAT", "r").read()
        return int(re.search(r'^\s*(\d+)\s+Transf\. carregs de Ventos', instalv_text, re.M)[1])


class BuildingTreeApp:
    def __init__(self, tqs_path: str, list_pavs: bool, list_subfolders: bool, building_filter: list[int], selection_mode: int, building_code_filter: list[str] = None, master = None):
        self.tqs_path = tqs_path
        self.list_pavs = list_pavs
        self.list_subfolders = list_subfolders
        self.building_filter = building_filter
        self.building_code_filter = building_code_filter
        self.selection_mode = selection_mode

        # Ícones
        self.master = master or Tk()
        self.master.wm_withdraw()
        self.selected_folder = StringVar()

        self.img_folder = PhotoImage(data=folder_png_b64, width=20, height=16)
        self.img_conc = PhotoImage(data=conc_png_b64, width=20, height=16)
        self.img_alvest = PhotoImage(data=alv_png_b64, width=20, height=16)
        self.img_preo = PhotoImage(data=preo_png_b64, width=20, height=16)
        self.img_parcon = PhotoImage(data=parcon_png_b64, width=20, height=16)
        self.img_floor = PhotoImage(data=pav_png_b64, width=20, height=16)

        # Configuração da janela e posicionamento ao centro da tela
        self.master.title('Árvore de Edifícios TQS')
        self.master.wm_iconbitmap(icon())
        win_width = 700
        win_height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int((screen_width / 2) - (win_width / 2))
        center_y = int((screen_height / 2) - (win_height / 2))
        self.master.geometry(f'{win_width}x{win_height}+{center_x}+{center_y}')
        self.master.resizable(False, False)
        self.master.attributes('-topmost', True)
        
        #frame_top
        frame_top = Frame(self.master)
        frame_top.columnconfigure(0, weight=1)
        frame_top.columnconfigure(0, weight=3)
        frame_top.columnconfigure(0, weight=1)
        frame_top.columnconfigure(0, weight=1)
       
        # Label 'Pasta Raiz'
        Label(frame_top,text='Pasta Raiz:').grid(row=0, column=0, sticky='w', pady=5)
       
        # Entry 'Caminho'
        self.tqs_path_entry = Entry(frame_top, width=30)
        self.tqs_path_entry.insert(0, self.tqs_path)
        self.tqs_path_entry.grid(row=0, column=1, sticky='w',padx=5,pady=5)
        self.tqs_path_entry.focus()

        update_button = Button(frame_top, text='Atualizar', command=self.update_tree, width=10)
        update_button.grid(row=0, column=2, sticky='w',padx=3,pady=5)

        find_button = Button(frame_top, text='Encontra Pasta', command=self.find_folder, width=14)
        find_button.grid(row=0, column=3, sticky='w',pady=5)
        
        frame_top.pack()

        s = ttk.Style()
        s.configure('Treeview', rowheight=28)

        # Árvore de Edifícios
        tree_frame = Frame(self.master)
        self.tree = ttk.Treeview(tree_frame, show='tree', selectmode="browse")
        ybar = Scrollbar(tree_frame,orient=tk.VERTICAL, command=self.tree.yview)
        self.update_tree()
        self.tree.configure(yscroll=ybar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        ybar.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        tree_frame.pack(fill='both',expand=True,padx=5,pady=5)

        # frame_bottom
        frame_bottom = Frame(self.master)
        Label(frame_bottom,text='Seleção Atual:').pack(side='left', fill='x', expand=False)
        
        # Entry não editável de projeto selecionado
        self.selected_project_entry = Entry(frame_bottom, width=50, state='disabled', textvariable=self.selected_folder)
        self.selected_project_entry.pack(side='right',fill='x',expand=True)
        frame_bottom.pack()

        # Botão Ok
        close_button = Button(self.master,text='Selecionar', command=self.finish_selection, width=10)
        close_button.pack(side=tk.BOTTOM,padx=5,pady=5)
        
        # Variável de saída
        self.output = None

        self.master.wm_deiconify()
        self.master.wait_window()


    
    def _get_tqs_folders(self, path: str) -> list[TQSProject]:
        all_folders = []
        for root, dirs, files in os.walk(path):
            all_folders.extend(os.path.join(root, dir) for dir in dirs)
        tqs_buildings = [TQSProject(dir) for dir in all_folders if os.path.exists(os.path.join(dir, 'EDIFICIO.BDE'))]
    
        return [project for project in tqs_buildings if (not self.building_filter or project.project_type in self.building_filter) and 
                                                        (not self.building_code_filter or project.code in self.building_code_filter)]

    def project_type_image(self, project: TQSProject):
        try:
            return [self.img_conc, self.img_preo, self.img_alvest, self.img_parcon][project.project_type]
        except Exception:
            return self.img_conc
        
    def list_tqs_subfolders(self, projects: list[TQSProject]):
        for project in projects:
            for subfolder in project.subfolders:
                self.tree.insert(project.path, "end", os.path.join(project.path, subfolder), text=subfolder, image=self.img_folder)

    def list_tqs_floors(self, projects: list[TQSProject]):
        for project in projects:
            for floor in reversed(project.floor_names):
                self.tree.insert(project.path, "end", os.path.join(project.path, floor), text=floor, image=self.img_floor)


    def on_select(self, event):
        """Seleciona um projeto TQS"""
        with suppress(IndexError):
            parent = self.tree.parent(self.tree.selection()[0])
            if parent and (self.selection_mode == TREESELECTION_ALL or (self.selection_mode == TREESELECTION_NOTBUILDINGS and (parent != self.tqs_path))):
                self.selected_folder.set(os.path.basename(self.tree.selection()[0]))
            else:
                self.selected_folder.set("")
    
    def finish_selection(self):
        try:
            self.output = self.tree.selection()[0] if self.selected_folder.get() else None
        except IndexError:
            self.output = None
        self.master.destroy()


    def update_tree(self):
        """Atualiza a árvore de edifícios"""
        self.tqs_path = self.tqs_path_entry.get()
        self.tqs_path = os.path.normpath(self.tqs_path)

        # Lista todos os projetos TQS
        projects = self._get_tqs_folders(self.tqs_path)
        
        # Limpa a árvore
        self.tree.delete(*self.tree.get_children())

        # Adiciona os projetos TQS na árvore
        # Insere a pasta raiz
        self.tree.insert('', 'end', iid=self.tqs_path, text=self.tqs_path, open=True)
        # Insere os projetos TQS
        path_depth = len(self.tqs_path.split(os.path.sep))
        for project in projects:
            project_split = project.path.split(os.path.sep)
            project_depth = len(project_split)
            for i in range(project_depth):
                if i < path_depth:
                    continue
                current_folder = '\\'
                current_folder = current_folder.join(project_split[:i])
                if self.tree.exists(current_folder):
                    continue
                else:
                    self.tree.insert(os.path.dirname(current_folder),
                    'end',
                    current_folder,
                    text=os.path.basename(current_folder),
                    image=self.img_folder)

            self.tree.insert(project.directory,'end', project.path, text=project.name, image=self.project_type_image(project))
        
        if self.list_subfolders:
            self.list_tqs_subfolders(projects)

        if self.list_pavs:
            self.list_tqs_floors(projects)


    def is_tqs_project(self, project):
        """Verifica se o projeto é um projeto TQS"""
        return os.path.exists(os.path.join(project,'EDIFICIO.BDE'))


    def find_folder(self):
        """Selecione uma pasta de projeto TQS"""
        if projeto := filedialog.askdirectory(mustexist = True, title = "Selecione a pasta de projetos TQS", initialdir = self.tqs_path):
            projeto = os.path.normpath(projeto)
            self.tqs_path_entry.delete(0, tk.END)
            self.tqs_path_entry.insert(0, projeto)
            self.update_tree()

def building_tree(initialdir:str = r'C:\TQS' if os.path.exists(r'C:\TQS') else '', list_pavs:bool = True, list_subfolders:bool = True, building_filter:list[int] = None, selection_mode: int = TREESELECTION_ALL, building_code_filter: list[str] = None, master=None):
    building_tree_app = BuildingTreeApp(initialdir, list_pavs, list_subfolders, building_filter, selection_mode, building_code_filter, master)
    return building_tree_app.output

def building_tree_project(initialdir:str = r'C:\TQS' if os.path.exists(r'C:\TQS') else '', building_filter:list[int] = None, selection_mode: int = TREESELECTION_ALL, building_code_filter: list[str] = None, master=None):
    building_path = BuildingTreeApp(initialdir, False, False, building_filter, selection_mode, building_code_filter, master).output
    return TQSProject(building_path) if building_path else None

if __name__ == "__main__":
    print(building_tree())
