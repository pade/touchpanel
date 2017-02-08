# -*- coding: UTF-8 -*-

'''
Created on 27 janv. 2017

@author: dassierp
'''

import kivy
import socket
from distutils.command.config import config
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
    isset = BooleanProperty(False)
    background_color_normal = ListProperty([1, 1, 1, 1])
    background_color_down = ListProperty([1, 1, 1, 1])

    def __init__(self, color, **kwargs):
        super(TouchPanelButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color_normal = color + [0.4]
        self.background_color_down = color + [1]
        self.background_color = self.background_color_normal

    def on_press(self):
        if self.state == 'down':
            self.background_color = self.background_color_down
        else:
            self.background_color = self.background_color_normal


class ImageButton(ButtonBehavior, Image):
    pass

class TouchPanelSlider(Slider):
    index = NumericProperty(0)
    activate = BooleanProperty(True)
    
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
        prefix = self.config.get('network', 'prefix')
        
        color_list = [[1, 0, 0], [0, 0, 1], [0, 1, 0], [1, 1, 0], [1, 0, 1], [0, 1, 1]]
        i = 0
        btn_list = {}
        for color in color_list:
            btn = TouchPanelButton(color=color, index=i)
            btn.bind(state=self.on_button_state)
            self.app.osc.addhandler('/{}/button/{}'.format(prefix, i), self.on_button_change)
            i = i + 1
            self.button_layout.add_widget(btn)
            btn_list[i] = btn


        nb_slider = int(self.config.get('interface', 'sliders_nb'))

        slider_list = {}
        for i in range(nb_slider):
            sld = TouchPanelSlider(index=i, min=0, max=1)
            sld.bind(value=self.on_slider_value)
            self.slider_layout.add_widget(sld)
            slider_list[i] = sld

    def on_slider_value(self, instance, value):
        prefix = self.config.get('network', 'prefix')
        index = instance.index
        self.app.osc.send('/{}/slider/{}'.format(prefix, index), float(value))
    
    def on_button_change(self, addr, tags, data, client_address):
        index = addr.split('/')[-1]
        if data[0] == 1.0:
            self.btn_list[index].state = 'down'

    def on_button_state(self, instance, value):
        prefix = self.config.get('network', 'prefix')
        index = instance.index
        if instance.state == 'down':
            print("1.0")
            self.app.osc.send('/{}/button/{}'.format(prefix, index), 0.0)
            self.app.osc.send('/{}/button/{}'.format(prefix, index), 1.0)
        else:
            self.app.osc.send('/{}/button/{}'.format(prefix, index), 0.0)
            self.app.osc.send('/{}/button/{}'.format(prefix, index), 1.0)
            print("0.0")
        
        
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
        self.osc.close()
        host = self.config.get('network', 'host')
        rport = self.config.getint('network', 'receive_port')
        self.osc.startServer(host, rport)
        sport = self.config.getint('network', 'send_port')
        self.osc.startClient(host, sport)
        self.root.update_cfg()

            
    def build(self):
        # Start OSC server and client
        self.osc = oscbackend.TouchPanelOSCBackend()
        host = self.config.get('network', 'host')
        rport = self.config.getint('network', 'receive_port')
        self.osc.startServer(host, rport)
        sport = self.config.getint('network', 'send_port')
        self.osc.startClient(host, sport)
        
        return TouchPanelMain()

    def build_config(self, config):
        config.add_section('interface')
        config.set('interface', 'sliders_nb', '6')
        config.add_section('network')
        config.set('network', 'prefix', 'touchpanel')
        config.set('network', 'host', '127.0.0.1')
        config.set('network', 'receive_port', '9000')
        config.set('network', 'send_port', '7700')

    def build_settings(self, settings):
        data = '''[
            { "type": "title", "title": "User interface" },
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
              "section": "network", "key": "send_port" },
            { "type": "numeric", "title": "Receive port",
              "desc": "Receive port to use, from 1024 to 65535",
              "section": "network", "key": "receive_port" }
        ]'''
        settings.add_json_panel('TouchPanel', self.config, data=data)
        
    def on_stop(self):
        self.osc.close()

if __name__ == '__main__':
    TouchPanelApp().run()
    
