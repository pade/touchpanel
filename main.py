# -*- coding: UTF-8 -*-

'''
Created on 27 janv. 2017

@author: dassierp
'''

import kivy
from kivy.uix.boxlayout import BoxLayout
kivy.require('1.9.1')

from kivy.uix.slider import Slider
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button


class TouchPanelButton(Button):
    index = NumericProperty(0)
    isset = BooleanProperty(False)
    
    def on_press(self):
        self.isset = not self.isset
        #if self.activated:
        #    self.background_color = [1,1,1,1]
        #else:
        #    self.background_color = [1,0,0,1]
            
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
        
        for i in range(6):
            btn = TouchPanelButton(index=i)
            self.button_layout.add_widget(btn)

        for i in range(6):
            sld = TouchPanelSlider(index=i)
            self.slider_layout.add_widget(sld)
            
    
class TouchPanelApp(App):
    def build(self):
        return TouchPanelMain(app=self)


if __name__ == '__main__':
    TouchPanelApp().run()