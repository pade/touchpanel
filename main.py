# -*- coding: UTF-8 -*-

'''
Created on 27 janv. 2017

@author: dassierp
'''

import kivy
kivy.require('1.9.1')

from kivy.uix.slider import Slider
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty

from kivy.uix.button import Button

class TouchPanelButton(Button):
    index = NumericProperty(0)
    isset = BooleanProperty(False)
    background_color_normal = ListProperty([1, 1, 1, 0.5])
    background_color_down = ListProperty([1, 1, 1, 1])
    
    def __init__(self, color, **kwargs):
        super(TouchPanelButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color_normal = color + [0.5]
        self.background_color_down = color + [1]
        self.background_color = self.background_color_normal
    
    def on_press(self):
        self.isset = not self.isset
        if self.isset:
            self.background_color = self.background_color_down
        else:
            self.background_color = self.background_color_normal

            
class TouchPanelSlider(Slider):
    index = NumericProperty(0)
    activate = BooleanProperty(True)
    

class TouchPanelMain(BoxLayout):
    '''
    Main windows
    '''
    app = ObjectProperty(None)
    menu_layout = ObjectProperty(None)
    button_layout = ObjectProperty(None)
    slider_layout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(TouchPanelMain, self).__init__(**kwargs)
        
        color_list = [[1,0,0], [0,0,1], [0,1,0], [1,1,0], [1,0,1], [0,1,1]]
        i=0
        for color in color_list:
            btn = TouchPanelButton(color=color, index=i)
            i = i+1
            self.button_layout.add_widget(btn)

        for i in range(6):
            sld = TouchPanelSlider(index=i)
            self.slider_layout.add_widget(sld)
            
    
class TouchPanelApp(App):
    def build(self):
        return TouchPanelMain(app=self)


if __name__ == '__main__':
    TouchPanelApp().run()