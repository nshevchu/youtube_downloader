
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu

from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.uix.screenmanager import Screen

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

import pytube_clear

import os
print(os.getcwd())


class MDCH(MDCheckbox):
    def __init__(self, name, **kwargs):
        #name=kwargs['name']
        super().__init__(**kwargs)
        self.name=name

        print(self.name)


class MainApp(MDApp):
    def menu_callback(self, x):
        self.menu.dismiss()
        self.resolution = x
        print(self.resolution)
        self.url_list = self.inp.text.split()
        for i in self.url_list:
            print(i)

    def start_download(self):
        print('start download')
        self.button_ch.disabled=True
        self.button_ch.text='Downloading.. wait'
        if self.ffmpeg_path.text:
            os.environ["PATH"] += ';{}'.format(self.ffmpeg_path.text)
        else:
            os.environ["PATH"] += self.ffpmeg_link
        self.url_list = self.inp.text.split()
        if len(self.url_list) == 0:
            print('Warning! nothing to download')
        for i in self.url_list:
            print(i)
            pytube_clear.downloader(url=i, mode=self.mode, resolution=self.resolution)

        self.button_ch.disabled = False
        self.button_ch.text = 'Start'



    def on_checkbox_active(self, checkbox, mode='v'):
        if checkbox.state == 'down':
            self.mode = checkbox.name
        print(self.mode)

    def build(self):
        #return MDLabel(text="Hello, World", halign="center")

        self.screen = Screen()
        self.resolution='1080p'
        self.mode='video'
        self.ffpmeg_link=';D:\\Scripts\\test\\ffmpeg\\ffmpeg-2021-08-25-git-e41bd075dd-full_build\\bin;{}\\ffmpeg'.format(os.getcwd())
        self.url_list = []

        self.path = '/'  # path to the directory that will be opened in the file manager
        self.file_manager = MDFileManager(
            #exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
            exit_manager=lambda x:print('1'),  # function called when the user reaches directory tree root
            #select_path=self.select_path,  # function called when selecting a file/directory
            select_path=lambda x:print('1'),  # function called when selecting a file/directory
        )
        #self.file_manager.show(self.path)

        self.scroll = ScrollView(size_hint=(0.7, 1), pos_hint={'center_x':0.5, 'center_y':0.0})

        resolution_list = ['best', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']

        self.menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in resolution_list

        ]

        #dropdown.items.append('хер1')
        #dropdown.items.append('хер2')
        self.inp = MDTextField(hint_text='url list here', multiline=True)

        self.button_resselect = MDRectangleFlatButton(text='Chose resolution',
                                          size_hint=(0.7, 0.2),
                                          pos_hint={'center_x': 0.5, 'center_y': 0.0},
                                          text_color=(1,1,1,1),
                                          line_color=(1,0,0,1), on_release=lambda x: self.menu.open()
                                          )

        self.button_ch = MDRectangleFlatButton(text='Start',
                                          size_hint=(0.7, 0.2),
                                          pos_hint={'center_x':0.5, 'center_y':0.0},
                                          text_color=(1,1,1,1),
                                          line_color=(1,0,0,1), on_release=lambda x: self.start_download()
                                          )
        self.menu = MDDropdownMenu(
            caller=self.button_ch,
            items=self.menu_items,
            width_mult=4,
        )

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.checkbox_layout = GridLayout(cols=2,rows=3, padding=10, spacing=10)

        self.scroll.add_widget(self.inp)
        self.layout.add_widget(self.scroll)
        #layout.add_widget(dropdown)

        self.layout.add_widget(self.button_resselect)

        self.channel_chb = MDCH(group='1', name='channel')
        self.playlist_chb = MDCH(group='1', name='playlist')
        self.video_chb = MDCH(group='1', active=True, name='video')

        self.channel_chb.bind(on_press=lambda x='channel': self.on_checkbox_active(self.channel_chb, x))
        self.playlist_chb.bind(on_press=lambda x='playlist': self.on_checkbox_active(self.playlist_chb, x))
        self.video_chb.bind(on_press=lambda x='video': self.on_checkbox_active(self.video_chb, x))

        self.checkbox_layout.add_widget(MDLabel(text='Video', halign='center'))
        self.checkbox_layout.add_widget(self.video_chb)
        self.checkbox_layout.add_widget(MDLabel(text='Playlist', halign='center'))
        self.checkbox_layout.add_widget(self.playlist_chb)
        self.checkbox_layout.add_widget(MDLabel(text='Channel', halign='center'))
        self.checkbox_layout.add_widget(self.channel_chb)

        self.ffmpeg_path = MDTextField(hint_text='ffmpeg path', size_hint=(0.7, 0.2), pos_hint={'center_x':0.5, 'center_y':0.0})

        self.layout.add_widget(self.checkbox_layout)
        self.layout.add_widget(self.ffmpeg_path)
        self.layout.add_widget(self.button_ch)
        self.screen.add_widget(self.layout)

        return self.screen


MainApp().run()