# -*- coding: UTF-8 -*-

'''
Created on 27 janv. 2017

@author: dassierp
'''

import kivy
kivy.require('1.9.1')

from kivy.uix.slider import Slider
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.button import Button


class TouchPanelButton(Button):
    index = NumericProperty(0)
    activated = BooleanProperty(False)
    
    def on_press(self):
        self.activated = not self.activated
        #if self.activated:
        #    self.background_color = [1,1,1,1]
        #else:
        #    self.background_color = [1,0,0,1]
            

class TouchPanelApp(App):
    def build(self):
        layout = GridLayout(cols=3)
        for i in range(9):
            btn = TouchPanelButton(text="{}".format(i), index=i)
            layout.add_widget(btn, index=i)
        return layout
        

if __name__ == '__main__':
    TouchPanelApp().run()