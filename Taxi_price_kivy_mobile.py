from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionPrevious
from kivy.uix.actionbar import ActionGroup
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image


class Container(BoxLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            Color(0, 1, 1, 0.1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.padding = [20, 0, 20, 15]
        self.with_previous = False
        self.menu()
        self.make_widget()
        self.popup_text = ''
        self.popup_title = 'Предупреждение'

    def make_widget(self):
        self.add_widget(Label(text='Пробеги', size_hint=(1, .3), font_size='25sp'))
        self.hbox1()
        self.add_widget(Label(text='Тарифы такси', size_hint=(1, .3), font_size='25sp'))
        self.hbox2()
        self.hbox3()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def menu(self):
        action_previous = ActionPrevious(title='Taxi price', app_icon='image/taxi_logo_16.png', on_press=self.back,
                                         with_previous=self.with_previous)
        ag = ActionGroup(text='Menu', mode='spinner')
        for i in [('Рассчитать', self.countresult), ('Инфо', self.info),
                  ('На главную', self.back), ('Выход', self.quit)]:
            bt = ActionButton(text=i[0])
            bt.bind(on_press=i[1])
            ag.add_widget(bt)
        aw = ActionView()
        aw.add_widget(ag)
        aw.add_widget(action_previous)
        menu = ActionBar()
        menu.add_widget(aw)
        self.add_widget(menu)

    def hbox1(self):
        self.entries = []
        hb = BoxLayout()
        hb_v1 = BoxLayout(orientation='vertical', spacing=1)
        hb_v2 = BoxLayout(orientation='vertical', spacing=1, size_hint=(0.2, 1))
        for i in ['Пробег город, км', 'Пробег трасса, км',
                  'Средняя поездка город, км', 'Средняя поездка трасса, км']:
            lb = Label(text=i, font_size='18sp')
            lb.bind(size=lb.setter('text_size'))
            hb_v1.add_widget(lb)
            ti = TextInput()
            self.entries.append(ti)
            hb_v2.add_widget(ti)
        hb.add_widget(hb_v1)
        hb.add_widget(hb_v2)
        self.add_widget(hb)

    def hbox2(self):
        self.tentries = []
        hb = BoxLayout()
        hb_v1 = BoxLayout(orientation='vertical', spacing=1)
        hb_v2 = BoxLayout(orientation='vertical', spacing=1, size_hint=(0.2, 1))
        for i in ['Тариф город, руб', 'Тариф загород, руб', 'Посадка город, руб',
                  'Посадка загород, руб', 'Включенные км']:
            lb = Label(text=i, font_size='18sp')
            lb.bind(size=lb.setter('text_size'))
            hb_v1.add_widget(lb)
            ti = TextInput()
            self.tentries.append(ti)
            hb_v2.add_widget(ti)
        hb.add_widget(hb_v1)
        hb.add_widget(hb_v2)
        self.add_widget(hb)

    def hbox3(self):
        hb = BoxLayout(spacing=5)
        actlist = [('Рассчитать', self.countresult), ('Инфо', self.info), ('Выход', self.quit)]
        for i in actlist:
            btn = (Button(text=i[0], size_hint=[0.5, 0.25]))
            btn.bind(on_press=i[1])
            hb.add_widget(btn)
        self.add_widget(hb)

    def clear(self):
        for child in list(self.children): # [:-1]:
            self.remove_widget(child)

    def onPopup(self):
        bl= BoxLayout(orientation='vertical')
        bl_lab = Label(text=self.popup_text, halign='center', valign='center')
        bl_lab.bind(size=bl_lab.setter('text_size'))
        bl_btn = Button(text='Закрыть', size_hint=[1, 0.1])
        bl.add_widget(bl_lab)
        bl.add_widget(bl_btn)
        content = bl
        popup = Popup(content=content, title=self.popup_title, auto_dismiss=False)
        bl_btn.bind(on_press=popup.dismiss)
        popup.open()

    def countresult(self, instance):
        res = []
        ent = self.entries + self.tentries
        for name in ent:
            s = name.text
            if s == '':
                self.popup_text = "Не введено значение"
                self.onPopup()
                return
            try:
                d = float(s)
            except:
                self.popup_text = "Введено недопустимое значение"
                self.onPopup()
                return
            else:
                res.append(d)
        self.result(res)

    def result(self, name):
        try:
            pcity = (name[0]/name[2])*name[6] + (name[0] - name[8]*(name[0]/name[2]))*name[4]
            proute = (name[1]/name[3])*name[7] +(name[1] - name[8]*(name[1]/name[3]))*name[5]
        except ZeroDivisionError:
            self.popup_text = "Значение поля\n 'средняя поездка'\n не должно быть нулевым"
            self.onPopup()
            return
        p = pcity + proute
        mes = '''[size=20sp]Затраты: %s руб.[/size]\n\n''' + '''[size=18sp][i]В том числе:[/i]\n\n''' +\
            '''Город: [b]%s[/b] руб.\n\n''' + '''За городом: [b]%s[/b] руб.[/size]'''
        self.with_previous = True
        self.clear()
        self.menu()
        self.add_widget(Label(text='Результаты:', size_hint=(1, 0.2), font_size='24sp'))
        lb = Label(text=mes % (p, pcity, proute), size_hint=(1, 0.7), markup=True,
                   halign='center', valign='top')
        lb.bind(size=lb.setter('text_size'))
        self.add_widget(lb)
        img = Image(source='image/taxi_PNG5_300px.png')
        self.add_widget(img)
        btc = Button(text='Close', on_press=self.quit, size_hint=(1, 0.1))
        self.add_widget(btc)

    def back(self, instance):
        self.with_previous = False
        self.clear()
        self.menu()
        self.make_widget()

    def info(self, instance):
        self.popup_title = 'О программе'
        self.popup_text = '''Данная программа позволяет\nопределить затраты на\nпользование такси и\n''' + \
                          '''сравнить их с затратами\n на личный автомобиль'''
        self.onPopup()

    def quit(self, instance):
        App.get_running_app().stop()
        Window.close()


class MyApp(App):
    def build(self):
        self.title = 'Taxi price'
        self.icon = 'image/taxi_logo_16.png'
        return Container()


if __name__ == '__main__':
    MyApp().run()


