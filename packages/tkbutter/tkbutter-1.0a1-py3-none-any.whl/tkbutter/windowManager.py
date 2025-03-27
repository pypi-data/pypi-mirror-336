
from ast import Lambda
from tkinter import *
from tkinter import font
import tkinter
from tkinter.font import *
from typing import Any, Callable

#윈도우를 만들 때 복잡한 과정들을 메소드화하는 클래스를 만든다. 그게 windowManager
class WindowManager:
    def __init__(self, title: str="Do you want some BUTTER?", resizing_x: bool=True, resizing_y: bool=True):
        self.__window = Tk()
        self.__window.title(title)
        self.__window.resizable(width=resizing_x, height=resizing_y)
        self.__widget_list: list[tkinter.Widget]= []
        self.__frame_list = [self.__window]
        self.__font_list = [Font()]



    def get_window():
        return 0



    def create_font(self, family: str="TkDefaultFont", size: int=16, weight: str="normal", slant: str="roman", underline: bool=False, overstrike: bool=False):
        font_number = len(self.__font_list)
        self.__font_list.append(Font(family=family, size=size, weight=weight, slant=slant, underline=underline, overstrike=overstrike))
        return font_number



    #위젯 매니저
    def create_label(self, frame_number: int=0, text: str="Do you want some BUTTER?", font_number: int=0):
        wizet_number = len(self.__widget_list)
        self.__widget_list.append(Label(self.__frame_list[frame_number], text=text, font=self.__font_list[font_number]))
        return wizet_number

    def create_button(self, frame_number, text: str="Do you want some BUTTER?", commend: Callable[..., Any]=print("Do you want some BUTTER?"), font_number: int=0, width: int=0, hight: int=0):
        wizet_number = len(self.__widget_list)
        self.__widget_list.append(Button(self.__frame_list[frame_number], text=text, command=commend, font=self.__font_list[font_number], width=width, hight=hight))
        return wizet_number



    #pack and grid
    def pack_widget(self, wizet: int=0, side: str="Center", padx: int=0, pady: int=0):
        self.__widget_list[wizet].pack(side=side, padx=padx, pady=pady)

    def grid_widget(self, widget: int=0, row: int=0, column: int=0, rowspan: int=1, columnspan: int=1, padx: int=0, pady: int=0):
        self.__widget_list[widget].grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady)



    def set_size(self, geometry: str):
        self.__window.geometry(geometry)

    def main_loop_window(self):
        self.__window.mainloop()