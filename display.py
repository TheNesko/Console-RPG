from imports import *

class Color:
    TEXT_COLOR = "green"
    HIGHLIGHT_COLOR = "dark_green"
    UNAVALIBLE = "grey37"
    PANEL_COLOR = "white"
    GO_BACK_COLOR = "dark_orange"
    DANGER_COLOR = "red"
    NEW_SAVE_FILE = "bright_blue"

layout = Layout()
layout.split_column(
Layout(name='MainTop',ratio=2,visible=False),
Layout(name='MainBottom',ratio=6)
)
layout['MainBottom'].split_column(
Layout(name='Game',ratio=2),
Layout(name='Map',ratio=6,visible=False)
)
layout['Game'].split_row(
Layout(name='Left',ratio=1),
Layout(name='Right',ratio=1)
)
layout["Left"].split_column(
Layout(name='TopL',ratio=2),
Layout(name='BottomL',ratio=6)
)
layout["Right"].split_column(
Layout(name='TopR',ratio=2),
Layout(name='BottomR',ratio=6)
)

class Display:
    @staticmethod
    def window(Title:str="Window",Colums:int=80,Lines:int=30):
        system('mode con: cols=%i lines=%i' %(Colums,Lines))
        system("title %s" % Title)
    
    @staticmethod
    def set_window_size(Colums:int=80,Lines:int=30):
        system('mode con: cols=%i lines=%i' %(Colums,Lines))
    
    @staticmethod
    def disable_quickedit():
        '''Disable quickedit mode on Windows terminal. quickedit prevents script to
        run without user pressing keys..'''
        if not os.name == 'posix':
            try:
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                device = r'\\.\CONIN$'
                with open(device, 'r') as con:
                    hCon = msvcrt.get_osfhandle(con.fileno())
                    kernel32.SetConsoleMode(hCon, 0x0080)
            except Exception as e:
                print('Cannot disable QuickEdit mode! ' + str(e))

    @staticmethod
    def disable_window_resize():
        # get the handle of the window you want to disable resizing for
        hwnd = win32gui.FindWindow(None, 'Rpg game')
        # get the current window style
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        # disable the resizable flag in the window style
        style &= ~win32con.WS_THICKFRAME
        # update the window style
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
        # force the window to redraw with the new style
        win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE |
                            win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)

    @staticmethod
    def update_layout(layout_name: str,
                      content="",
                      title: str=None,
                      ratio: int=None,
                      visible: bool=True,
                      border=box.MINIMAL):
        layout[layout_name].update(Panel(content,title=title,style=Color.PANEL_COLOR,box=border))
        if ratio != None: layout[layout_name].ratio = ratio
        layout[layout_name].visible = visible

    @staticmethod
    def toggle_visible(layout_name: str,
                       visible: bool=None):
        if visible == None: layout[layout_name].visible = not layout[layout_name].visible
        else: layout[layout_name].visible = visible

    @staticmethod
    def options_to_text(options,
                        target=0):
        text = Text(justify="left")
        for index, name in enumerate(options):
            if index == len(options)-1 and target == index:
                text.append(f">{index+1}.{name}\n", f"u {Color.GO_BACK_COLOR}")
            elif index == target:
                text.append(f">{index+1}.{name}\n", f"u {Color.HIGHLIGHT_COLOR}")
            else:
                text.append(f"{index+1}.{name}\n", Color.TEXT_COLOR)
        return text


class Ascii:
    @staticmethod
    def game_name(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('____ ___  ____    ____ ____ _  _ ____ \n',style=f'{Style}')
        text.append('|__/ |__] | __    | __ |__| |\/| |___ \n',style=f'{Style}')
        text.append('|  \ |    |__]    |__] |  | |  | |___ \n',style=f'{Style}')
        return text

    @staticmethod
    def new_game(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('_  _ ____ _   _  ____ ____ _  _ ____ \n',style=f'{Style}')
        text.append('|\ | |___ | _ |  | __ |__| |\/| |___ \n',style=f'{Style}')
        text.append('| \| |___ |/ \|  |__] |  | |  | |___ \n',style=f'{Style}')
        return text
    
    @staticmethod
    def credits(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('___ ____ ____ ___  _ ___ ____  \n',style=f'{Style}')
        text.append('|   |__/ |___ |  \ |  |  [___  \n',style=f'{Style}')
        text.append('|__ |  \ |___ |__/ |  |  ___]  \n',style=f'{Style}')
        return text
    
    @staticmethod
    def load(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('_   ____ ____ ___   \n',style=f'{Style}')
        text.append(' |   |  | |__| |  \ \n',style=f'{Style}')
        text.append(' |__ |__| |  | |__/ \n',style=f'{Style}')
        return text
    
    @staticmethod
    def back(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append(' ___  ____ ___ _  _\n',style=f'{Style}')
        text.append('|__\ |__| |   |_/ \n',style=f'{Style}')
        text.append('|__/ |  | |__ | \ \n',style=f'{Style}')
        return text
