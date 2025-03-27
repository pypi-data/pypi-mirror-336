# coding: latin-1
#-----------------------------------------------------------------------------
#    TQSUTIL.PY        Utilidades TQS
#-----------------------------------------------------------------------------
import inspect
import tkinter.messagebox
import ctypes
import winreg
import sys
import os

#-----------------------------------------------------------------------------
#    Constantes auxiliares
#
PI         = 3.1415926535897932                   # Constante PI
RADGRAUS   = 180./PI                              # Conversão graus radianos
GRAUSRAD   = PI/180.                              # Conversão radianos graus
CHARSET    = "latin-1"                            #!NTR Caracteres usados nos fontes
MAXNCSTR   = 256                                  # Número máximo de caracteres de strings
                                                  # Limite dos strings recebidos das DLLs C++
#-----------------------------------------------------------------------------
#    Variáveis globais
#
__jmsgdll              = None                     # JMSGDLL.DLL
__pastaProgram         = ""                       # Pasta EXEC
__pastaSuporte         = ""                       # Pasta SUPORTE
__pastaUsuario         = ""                       # Pasta USUARIO
#-----------------------------------------------------------------------------
#   Verifica DLLs carregadas
#
def __VerifyDlls ():
    global             __jmsgdll
    if                 __jmsgdll != None:
        return
    __jmsgdll           = LoadDll ("JMSGDLL.DLL")

#-----------------------------------------------------------------------------
#   Verifica strings das pastas TQS Carregados
#
def __VerifyFolfers ():
    """
    Chamada necessária antes de LoadDll se nenhuma impressão foi feita com writef
    """
    global             __pastaProgram, __pastaSuporte, __pastaUsuario
    if                 len (__pastaProgram) > 0 and len (__pastaSuporte) > 0 and len (__pastaUsuario) > 0:
        return
    sKey               = "SOFTWARE\TQS"#!NTR
    hReg               = winreg.ConnectRegistry (None, winreg.HKEY_LOCAL_MACHINE)
    hKey               = winreg.OpenKey (hReg, sKey)
    __pastaProgram, itype = winreg.QueryValueEx (hKey, "Programas")#!NTR
    __pastaSuporte, itype = winreg.QueryValueEx (hKey, "Suporte")#!NTR
    __pastaUsuario, itype = winreg.QueryValueEx (hKey, "Usuario")#!NTR
    winreg.CloseKey    (hKey)
    winreg.CloseKey    (hReg)

#-----------------------------------------------------------------------------
#   Carrega e retorna handle para uma DLL
#
def LoadDll (libname):
    __VerifyFolfers    ()
    global             __pastaProgram
    nomearqdll         = __pastaProgram
    if                 __pastaProgram [len (__pastaProgram)-1] != '\\':
        nomearqdll     += "\\"
    nomearqdll         += libname
    hlib               = ctypes.windll.LoadLibrary (nomearqdll)
    if                 hlib == None:
        tkinter.messagebox.showerror(title="Biblioteca não encontrada", message=nomearqdll)
    return             hlib

#-----------------------------------------------------------------------------
#    Rotina de impressão de mensagens via JMSG.EXE
#
def writef (*args):
    """
    Faz impressão de mensagens em janela TQS com número variável de argumentos
    """
    __VerifyDlls       ()
    if                 __jmsgdll == None:
        return
    txt                 = ""
    for                 msg in args:
        txt             += str (msg)
    par                 = ctypes.c_char_p (txt.encode(CHARSET))
    __jmsgdll.writej     (par)
#-----------------------------------------------------------------------------
#    Rotina de debug igual a ASMLIB::DEBW
#
def DEBW ():
    """
    Em debug, imprime nome do arquivo e número da linha (ASMLIB::DEBW)
    """
    __VerifyDlls       ()
    caller             = inspect.getframeinfo (inspect.stack()[1][0])
    writef             ("[%s] [%d]" % (caller.filename, caller.lineno))
    return             0
#-----------------------------------------------------------------------------
#    Retorna pastas padrão TQS lidas do Registry
#
def ProgramsFolder ():
    """
    Retorna a pasta de programas TQS
    """
    __VerifyFolfers    ()
    return             (__pastaProgram)

def SupportFolder ():
    """
    Retorna a pasta de arquivos de suporte TQS
    """
    __VerifyFolfers    ()
    return             (__pastaSuporte)

def UserFolder ():
    """
    Retorna a pasta de arquivos de usuário TQS
    """
    __VerifyFolfers    ()
    return             (__pastaUsuario)
#-----------------------------------------------------------------------------
#    Mostra o resultado de uma exceção genérica
#
def ShowException (e):
    """
    Mostra o resultado genérico de uma exceção, inclusive linha de programa
    """
    __VerifyDlls       ()
    iprimeira          = 0
    classerro          = ""
    strerro            = ""
    frames             = inspect.trace()
    frames.reverse     ()
    for                fr in frames:
        caller         = inspect.getframeinfo (fr [0])
        writef         ("TQS Erro em [%s] [%s] [%d]" % 
                        (caller.filename, caller.function, caller.lineno))
        writef         (caller.code_context)
        writef         ("")
        classerro      = sys.exc_info()[0]
        strerro        = e
    writef             ("Classe      ", str (classerro))
    writef             ("Erro        ", str (e))
    raise

#-----------------------------------------------------------------------------
#    Executa programa na pasta TQS
#
def ExecTqs (command):
    """
    Executa um programa e seus parâmetros na pasta TQSW\EXEC
    """
    linhacmd    = ProgramsFolder () + "\\" + command
    os.system   (linhacmd)

