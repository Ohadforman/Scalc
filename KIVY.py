#region IMPORTS
import subprocess
import sys
import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from  kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, \
    implicit_multiplication_application
#endregion

#region operitors with __init__

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.rows = 4
        self.submit = Button(text="Divergance", font_size=15,size_hint=(0.5,0.25),pos=(20,20))
        self.submit.bind(on_press=self.div)                   #activate function
        self.add_widget(self.submit)
        self.submit = Button(text="Gradient", font_size=15,size_hint=(0.5,0.25),pos=(40,40))
        self.submit.bind(on_press=self.grad)                   #activate function
        self.add_widget(self.submit)
        self.submit = Button(text="Curl", font_size=15,size_hint=(0.5,0.25),pos=(60,60))
        self.submit.bind(on_press=self.curl)                   #activate function
        self.add_widget(self.submit)
        self.submit = Button(text="Derivitives by parts", font_size=15,size_hint=(0.5,0.25),pos=(80,80))
        self.submit.bind(on_press=self.par)                   #activate function
        self.add_widget(self.submit)
        self.add_widget(self.inside)
        self.inside.add_widget(Label(text="equation:",size_hint=(0.5,0.25),pos=(20,20)))
        self.equation = TextInput(multiline=False)
        self.inside.add_widget(self.equation)
        self.inside.add_widget(Label(text="X for curl:",size_hint=(0.25,0.25),pos=(20,20)))
        self.X_comp = TextInput(multiline=False)
        self.inside.add_widget(self.X_comp)
        self.inside.add_widget(Label(text="Y for curl:",size_hint=(0.5,0.25),pos=(20,20)))
        self.Y_comp = TextInput(multiline=False)
        self.inside.add_widget(self.Y_comp)
        self.inside.add_widget(Label(text="Z for curl:",size_hint=(0.5,0.25),pos=(20,20)))
        self.Z_comp = TextInput(multiline=False)
        self.inside.add_widget(self.Z_comp)



    def par(self, instance):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        x, y, z = symbols('x y z ', real=True)
        self.eq = str(self.equation.text)
        self.eqget = self.eq
        self.eqget = self.eqget.lower()
        self.eq1 = parse_expr(self.eqget, locals(), transformations=transformations)
        r=101
        g=x**x*x**x
        info = (f'Partial by X:{diff(self.eq1, x)}\nPartial by Y:{diff(self.eq1, y)}'
                f'\nPartial by Z:{diff(self.eq1, z)}')
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Results'

    def grad(self, instance):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        x, y, z = symbols('x y z ', real=True)
        self.eq = str(self.equation.text)
        self.eqget = self.eq
        self.eqget = self.eqget.lower()
        self.eq1 = parse_expr(self.eqget, locals(), transformations=transformations)
        self.eq = str(self.equation.text)
        r = 101
        g = x ** x * x ** x
        info = (f'Gradient of {self.eqget} is:( {diff(self.eq1, x)}  ,  {diff(self.eq1, y)}  ,  {diff(self.eq1, z)}) ')
        chat_app.info_page.update_info(str(info))
        chat_app.screen_manager.current = 'Results'

    def div(self, instance):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        x, y, z = symbols('x y z ', real=True)
        self.eq = str(self.equation.text)
        self.eqget = self.eq
        self.eqget = self.eqget.lower()
        self.eq1 = parse_expr(self.eqget, locals(), transformations=transformations)
        self.eq = str(self.equation.text)
        r = 101
        g = x ** x * x ** x
        info = (f'Divergence of {self.eqget} is: 'f'{diff(self.eq1, x)} + {diff(self.eq1, y)} + {diff(self.eq1, z)}')
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Results'

    def curl(self, instance):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        x, y, z = symbols('x y z ', real=True)
        self.x_comp = str(self.X_comp.text)
        self.y_comp = str(self.Y_comp.text)
        self.z_comp = str(self.Z_comp.text)
        self.x_comp = parse_expr(self.x_comp, locals(), transformations=transformations)
        self.y_comp = parse_expr(self.y_comp, locals(), transformations=transformations)
        self.z_comp = parse_expr(self.z_comp, locals(), transformations=transformations)
        r = 101
        g = x ** x * x ** x
        info = (f'( {diff(self.z_comp, y) - diff(self.y_comp, z)} , {diff(self.x_comp, z) - diff(self.z_comp, x)} , {diff(self.y_comp, x) - diff(self.x_comp, y)} )')
        chat_app.info_page.update_info(str(info))
        chat_app.screen_manager.current = 'Results'

#endregion

#region second screen
class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label()
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9,None)
#endregion

#region main screen App
class MyApp(App):
    def build(self):

        self.screen_manager = ScreenManager()
        self.connect_page = MyGrid()
        screen = Screen(name="User Input")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.info_page = InfoPage()
        screen = Screen(name="Results")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)
        self.submit = screen.add_widget(Button(on_press=chat_app.stop,text="Exit", font_size=15,size_hint=(0.1,0.1),pos=(0,0)))
        #self.submit.bind(on_press=self.stop)                   #activate function

        return self.screen_manager


#endregion

#region main name
if __name__=="__main__":
    chat_app = MyApp()
    chat_app.run()
#endregion












