from __future__ import annotations
from tkinter import filedialog, Tk
from TQS.TQSJan import Window
from TQS.TQSEag import Eag, EAG_RUBLINEAR, EAG_RUBNAO, EAG_RUBRET_NAOPREEN 
from TQS import TQSEag
from tempfile import NamedTemporaryFile
from base64 import b64decode

from pytqs.drawning import TQSDrawning, TQSElementList, Line

def hex_to_rgb(hex_string: str):
  return tuple(int(hex_string.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

def icon() -> str:
    iconb64 = \
        '''
        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
        '''
    with NamedTemporaryFile(suffix=".ico", delete=False) as tmp:
        icondata = b64decode(iconb64)
        tmp.write(icondata)
    return tmp.name

def get_file_path (title: str, filetypes: list, initialdir: str ="") -> str:
    """
    Retorna o caminho para um arquivo.

    Abre uma janela do tkinter pedindo para o usuário selecionar um arquivo.

    Args:
        title (str) : Título da janela tkinter.
        filetypes (list) : Lista de formatos de arquivo aceitos. Ex:[("Arquivo PDF", "*.pdf"), ("Arquivo Word", "*.docx")]
        initialdir (str) : Diretório inicial.

    Returns:
        Caminho do arquivo selecionado.
    """
    window = Tk()
    window.withdraw()
    window.wm_iconbitmap(icon())
    window.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(parent=window, initialdir=initialdir, title=title, filetypes=filetypes)
    window.destroy()

    return file_path

def select(tqsjan: Window, msg, selection_type= TQSEag.EAG_INORM) -> TQSElementList:
    eag = Eag.GetEag()
    eag.exec.Command("ID_ORTOGONAL")
    eag.exec.Command("ID_ORTOGONAL")
    addr, x, y, np, istat = eag.locate.Select(tqsjan, msg, selection_type)
    return TQSDrawning(dwg = tqsjan.dwg).filter({"addr": [addr]}) if istat == 0 else TQSElementList()

def select_multiple(tqsjan: Window, msg: str, selection_type= TQSEag.EAG_INORM) -> TQSElementList:
    eag = Eag.GetEag()
    eag.exec.Command("ID_ORTOGONAL")
    eag.exec.Command("ID_ORTOGONAL")
    eag.locate.Select(tqsjan, msg, selection_type)
    if eag.locate.BeginSelection(tqsjan) == 1:
        return TQSElementList()
    element_list = []
    while (element := eag.locate.NextSelection(tqsjan)):
        element_list.append(element)
    return TQSDrawning(dwg = tqsjan.dwg).filter({"addr": element_list})

def get_vector(tqsjan: Window, msg1: str = "Selecione o primeiro ponto: ", msg2: str = "Selecione o segundo ponto: ", rubber_line: bool = True) -> Line:
    eag = Eag.GetEag()
    _, x1, y1 = eag.locate.GetPoint(tqsjan, msg1)
    _, x2, y2 = eag.locate.GetSecondPoint(tqsjan, x1, y1, EAG_RUBLINEAR if rubber_line else EAG_RUBNAO, EAG_RUBRET_NAOPREEN, msg2)

    return Line(x1, y1, x2, y2)


# def select_multiple(tqsjan: Window, msg, selection_type= TQSEag.EAG_INORM) -> TQSElementList:
#     try:
#         selected_building = subprocess.check_output(f"py {__file__} {initialdir} {list_pavs} {list_subfolders} {building_filter} {selection_mode}", shell=True)
#     except subprocess.CalledProcessError as e:
#         selected_building = e.output
    
#     try:
#         selected_building = str(selected_building, "utf8")
#     except UnicodeDecodeError:
#         selected_building = str(selected_building, "cp1252")

#     try:
#         return literal_eval(selected_building)
#     except Exception:
#         return selected_building

# if __name__ == "__main__":
#     print(app.output, end="")