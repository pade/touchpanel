# -*- coding: UTF-8 -*-

'''
Created on 27 janv. 2017

@author: dassierp
'''

import kivy
import socket
import math
kivy.require('1.9.1')

from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty

import oscbackend

class TouchPanelButton(ToggleButton):
    index = NumericProperty(0)
    
class ImageButton(ButtonBehavior, Image):
    pass

class TouchPanelSlider(Slider):
    index = NumericProperty(0)
    
class IpAddress(Label):
    ip_address = ObjectProperty(None)
    text = StringProperty("@" + socket.gethostbyname(socket.gethostname()))
    

class TouchPanelControl(BoxLayout):
    '''
    Main windows
    '''
    menu_layout = ObjectProperty(None)
    button_layout = ObjectProperty(None)
    slider_layout = ObjectProperty(None)
    footer_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TouchPanelControl, self).__init__(**kwargs)

        self.app = App.get_running_app()
        self.config = self.app.config
        
        nb_button = int(self.config.get('interface', 'buttons_nb'))

        
        self.btn_list = {}
        for i in range(nb_button):
            btn = TouchPanelButton(index=i)
            btn.bind(state=self.on_button_state)
            self.button_layout.add_widget(btn)
            self.btn_list[i] = btn

        nb_slider = int(self.config.get('interface', 'sliders_nb'))

        self.slider_list = {}
        for i in range(nb_slider):
            sld = TouchPanelSlider(index=i, min=0, max=1)
            sld.bind(value=self.on_slider_value)
            self.slider_layout.add_widget(sld)
            self.slider_list[i] = sld

    def on_slider_change(self, addr, tags, data, client_address):
        index = int(addr.split('/')[-1])
        
        if math.fabs(data[0] - self.slider_list[index].value) > 0.01:
            self.slider_list[index].value = data[0]
    
    def on_slider_value(self, instance, value):
        prefix = self.config.get('network', 'prefix')
        index = instance.index
        self.app.osc.send('/{}/slider/{}'.format(prefix, index), float(value))
    
    def on_button_change(self, addr, tags, data, client_address):
        index = int(addr.split('/')[-1])
        if data[0] == 1.0:
            self.btn_list[index].state = 'down'
        else:
            self.btn_list[index].state = 'normal'
            
    def on_button_state(self, instance, value):
        prefix = self.config.get('network', 'prefix')
        index = instance.index
        if instance.state == 'down':
            self.app.osc.send('/{}/button/{}'.format(prefix, index), 1.0)
        else:
            self.app.osc.send('/{}/button/{}'.format(prefix, index), 0.0)
        
        
class TouchPanelMain(BoxLayout):
    '''
    Entry widget
    '''
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TouchPanelMain, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.control = TouchPanelControl()
        self.add_widget(self.control)
        
    def update_cfg(self):
        self.remove_widget(self.control)
        self.control = TouchPanelControl()
        self.add_widget(self.control)
        
class TouchPanelApp(App):
    
    use_kivy_settings = False
    
    def on_config_change(self, config, section, key, value):
        self.osc.closeClient()
        host = self.config.get('network', 'host')
        sport = self.config.getint('network', 'send_port')
        self.osc.startClient(host, sport)
        self.root.update_cfg()

            
    def build(self):
        self.osc = oscbackend.TouchPanelOSCBackend()
        host = self.config.get('network', 'host')
        sport = self.config.getint('network', 'send_port')
        self.osc.startClient(host, sport)
        
        return TouchPanelMain()

    def build_config(self, config):
        config.add_section('interface')
        config.set('interface', 'sliders_nb', '6')
        config.set('interface', 'buttons_nb', '6')
        config.add_section('network')
        config.set('network', 'prefix', 'tp')
        config.set('network', 'host', '127.0.0.1')
        config.set('network', 'send_port', '7700')

    def build_settings(self, settings):
        data = '''[
            { "type": "title", "title": "User interface" },
            { "type": "numeric", "title": "Buttons",
              "desc": "Number of buttons",
              "section": "interface", "key": "buttons_nb" },
            { "type": "numeric", "title": "Sliders",
              "desc": "Number of sliders",
              "section": "interface", "key": "sliders_nb" },
            { "type": "title", "title": "Network configuration" },
            { "type": "string", "title": "Prefix",
              "desc": "Monome prefix to use",
              "section": "network", "key": "prefix" },
            { "type": "string", "title": "Host",
              "desc": "Host or ip address to use",
              "section": "network", "key": "host" },
            { "type": "numeric", "title": "Send port",
              "desc": "Send port to use, from 1024 to 65535",
              "section": "network", "key": "send_port" }
        ]'''
        settings.add_json_panel('TouchPanel', self.config, data=data)
        
    def on_stop(self):
        #self.osc.close()
        self.osc.closeClient()

if __name__ == '__main__':
    TouchPanelApp().run()
    
