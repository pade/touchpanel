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
    
    def build_config(self, config):
        config.add_section('monome')
        config.set('monome', 'prefix', 'touchpanel')
        config.add_section('network')
        config.set('network', 'host', '127.0.0.1')
        config.set('network', 'receive_port', '9001')
        config.set('network', 'send_port', '9000')

    def build_settings(self, settings):
        data = '''[
            { "type": "title", "title": "Monome configuration" },
            { "type": "string", "title": "Prefix",
              "desc": "Monome prefix to use",
              "section": "monome", "key": "prefix" },


            { "type": "title", "title": "Network configuration" },
            { "type": "string", "title": "Host",
              "desc": "Host or ip address to use",
              "section": "network", "key": "host" },
            { "type": "numeric", "title": "Send port",
              "desc": "Send port to use, from 1024 to 65535",
              "section": "network", "key": "send_port" },
            { "type": "numeric", "title": "Receive port",
              "desc": "Receive port to use, from 1024 to 65535",
              "section": "network", "key": "receive_port" }
        ]'''
        settings.add_json_panel('TouchPanel', self.config, data=data)


if __name__ == '__main__':
    TouchPanelApp().run()