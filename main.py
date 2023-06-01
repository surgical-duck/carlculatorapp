from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from math import sin, cos, tan, acos, sin, atan, pi, sqrt, e, radians


class CalcApp(App):
     
    def build(self):        
        # Set screen manager settings
        if settings.default_calculator == 'advanced':
            sm_string = 'ScreenManager:\n    Advanced:\n        id: screen_adv\n    Simple:\n        id: screen_sim\n    Menu:\n        id: screen_menu'
        else:
            sm_string = 'ScreenManager:\n    Simple:\n        id: screen_sim\n    Advanced:\n        id: screen_adv\n    Menu:\n        id: screen_menu'

        # Read kv file
        with open('calc.kv', 'r') as f:
            kv_list = f.readlines()
        
        # Convert from list to string
        kv_string = ''
        for line in kv_list:
            kv_string += line
        
        # Build app
        build_string = sm_string + kv_string
        app_build = Builder.load_string(build_string)

        return app_build


class Calculator():
    display = ObjectProperty(None)
    decimals = 6
    operators = ['+', '-', '*', '/', '×', '÷', '^']
    replacement_dict_rad = {'^': '**', 
                            '×': '*', 
                            '÷': '/',
                            'π': 'pi',
                            }
    replacement_dict_deg = {'^': '**', 
                            '×': '*', 
                            '÷': '/',
                            'π': 'pi',
                            'cos': 'cos(radians',
                            'sin': 'sin(radians',
                            'tan': 'tan(radians',
                            'acos': 'acos(radians',
                            'asin': 'asin(radians',
                            'atan': 'atan(radians',
                            }
    
    def evaluate_expression(self, expression, rad_deg_mode):
        
        # Handle empty evaluations
        if expression == "":
            return ""      

        # Replace visual for functional operators
        expression = self.replace_operators(expression, rad_deg_mode)

        # Handle easter eggs
        easter_reply = self.handle_easter_eggs(expression)
        if easter_reply is not "":
            return easter_reply

        # Close open parentheses
        expression = self.close_parentheses(expression)

        # Exception handling
        try:
            result = str(eval(expression))
        except ZeroDivisionError as e:
            print(f'ZeroDivisionError: {e}.')
            return 'Zero division is illegal'
        except SyntaxError as e:
            print(f'SyntaxError: {e}.')
            return 'Syntax Error'
        except:
            print('Unknown error in exception handling of `evaluate_expression()`.')
            return 'Error'
        
        # Round to max number of decimals
        try:
            result = str(round(float(result), self.decimals))
        except ValueError as e:
            print(f'ValueError: {e}.')
            return 'Value Error'

        # Convert float to int whERRORen x.0
        split_str = result.split('.')
        if split_str[-1] == '0':
            result = split_str[0]
        
        return result
    
    @staticmethod
    def close_parentheses(expression):
        
        # Count parentheses
        start_count = expression.count('(')
        end_count = expression.count(')')
        diff = start_count - end_count

        if diff >= 0:
            for _ in range(diff):
                expression += ')'
        
        return expression
        
    @staticmethod
    def handle_easter_eggs(expression):

        if expression == "1337":
            return "ELITE"
        
        elif expression == "420":
            return "Blaze it"
        
        elif expression == "69":
            return "Noice"
        
        elif expression == "666":
            return "Number of the beast"
        
        elif expression == "42":
            return "Looks like the meaning of life"
        
        elif expression in ["80085", "58008", "5318008"]:
            return "very mature..."
        
        elif expression in ["35008"]:
            return "Is it already 15:40?"
        
        elif expression in ["01134", "14"]:
            return "Hey, how are you?"
        
        elif expression == "1+1":
            return "You should know that"
        
        elif expression == "You should know that":
            return "3 :P"
        
        elif expression == "Syntax Error":
            return "Error mannen"
        
        elif expression == "Error mannen":
            return "CHILLA"
        
        return ""

    def handle_operators(self, operator):
        
        # Get current expression in display
        expression = self.display.text

        # Comparison cannot be made when label empty
        if expression == '':
            pass
        # Special rules for the minus sign
        elif operator == '-' and (expression[-1] in ['*', '/', '×', '÷', '^']):
            pass
        # Replace operators
        elif expression[-1] in self.operators:
            expression = expression[:-1]
        
        # Standard case just adds the operator
        expression += operator

        return expression
        
    def replace_operators(self, expression, rad_deg_mode):

        # Loop through all visual operator and replace with functional
        if rad_deg_mode == 'RAD':
            for operator in self.replacement_dict_rad:
                expression = expression.replace(operator, self.replacement_dict_rad[operator])
        else:
            for operator in self.replacement_dict_deg:
                expression = expression.replace(operator, self.replacement_dict_deg[operator])

        return expression
    
    def backspace(self, expression):
        
        # Handle special case empty expression
        if expression == '':
            return ''
        
        # Handle special case cos, sin, tan
        if expression[-4:] in ['cos(', 'sin(', 'tan(']:
            return expression[:-4]
        
        # Handle special case sqrt and acos...
        elif expression[-5:] in ['sqrt(', 'acos(', 'asin(', 'atan(']:
            return expression[:-5]
        
        # Ordinary remove latest character
        return expression[:-1]

    def rad_deg_swap(self, current_mode):

        if current_mode == 'DEG':
            current_mode = 'RAD'
        else:
            current_mode ='DEG'
        
        return current_mode


class Simple(Screen, Calculator):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.settings = settings
        self.calculator_background = settings.calculator_background


class Advanced(Screen, Calculator):
    decimals = 10

    def __init__(self, **kw):
        super().__init__(**kw)
        self.settings = settings
        self.rad_deg_default = settings.default_angle_unit


class Menu(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        # Get default calculator
        self.default_calculator = settings.default_calculator
        
        # Get color theme
        self.color_theme = settings.color_theme
        
        # Get default angle unit
        self.default_angle_unit = settings.default_angle_unit

    def set_default_calc(self, text):

        # Set variable locally
        self.default_calculator = text

        # Set variable in settings object
        settings.default_calculator = text

        # Update settings file
        settings.save_settings()
    
    def set_color_theme(self, text):
        
        # Set variable locally
        self.color_theme = text

        # Set variable in settings object
        settings.color_theme = text

        # Update settings file
        settings.save_settings()

    def set_default_angle_unit(self, text):

        # Set variable locally
        self.default_angle_unit = text

        # Set variable in settings object
        settings.default_angle_unit = text

        # Update settings file
        settings.save_settings()

    def popup_color_theme(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        popup_label = Label(text="Restart app to change colors.", font_size=dp(20), text_size=(self.width, 0), halign='center')
        popup_button = Button(text='Ok', font_size=dp(20), pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(None, None), size=(dp(150), dp(55)))

        content.add_widget(popup_label)
        content.add_widget(popup_button)
        popup = Popup(title="Changing colors", content=content, size_hint=(None, None), 
                      size=(dp(300), dp(200)))
        popup_button.bind(on_press=popup.dismiss)#, on_release=popup.dismiss)
        popup.open()

    def popup_easter(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        popup_label = Label(text="There are 10 easter eggs. Can you evaluate the right expressions?", 
                            font_size=dp(19), text_size=(dp(260), self.height), halign='center', valign='center',
                            size_hint_y=0.7)
        popup_button = Button(text='Ok', font_size=dp(20), pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(None, None), size=(dp(150), dp(55)))

        content.add_widget(popup_label)
        content.add_widget(popup_button)
        popup = Popup(title="Easter eggs", content=content, size_hint=(None, None), 
                      size=(dp(300), dp(260)))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

    def popup_about(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        popup_label = Label(text="Info will come.", font_size=dp(20), text_size=(self.width, self.height), halign='center', valign='center')
        popup_button = Button(text='Ok', font_size=dp(20), pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(None, None), size=(dp(150), dp(55)))

        content.add_widget(popup_label)
        content.add_widget(popup_button)
        popup = Popup(title="About", content=content, size_hint=(None, None), 
                      size=(dp(300), dp(200)))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()


class DisplayLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.font_size = "45dp"
        self.font_color = settings.display_font
        self.halign = 'right'
        self.valign = 'middle'
        self.text_size = self.width*0.9, self.height
        self.id = 'display'
        self.size_hint_y = 0.3

        self.background_color = settings.display_background
        self.display_button_on_press = settings.display_button_on_press


class SettingsHandler():

    def __init__(self, file_name) -> None:

        # Store attribute file_name
        self.file_name = file_name

        # Read settings
        with open(file_name, 'r') as f:
            settings_list = f.readlines()
        
        # Store settings in attributes
        self.default_calculator = settings_list[0].strip()
        self.color_theme = settings_list[1].strip()
        self.default_angle_unit = settings_list[2].strip()

        # Get color theme
        self.get_color_theme(self.color_theme)
    
    def save_settings(self):
        with open(self.file_name, 'w') as f:
            f.write(self.default_calculator + '\n')
            f.write(self.color_theme + '\n')
            f.write(self.default_angle_unit)

    def get_color_theme(self, color_theme_string):
        if color_theme_string == 'light':
            self.set_theme_light()
        elif color_theme_string == 'pink':
            self.set_theme_pink_moto()
        else:
            self.set_theme_dark()

    def set_theme_dark(self):
        self.display_background = (0.16, 0.16, 0.16, 1)
        self.display_button_on_press = (0.26, 0.26, 0.26, 1)
        self.display_font = (1, 1, 1, 1)

        self.calculator_background = (0.22, 0.22, 0.22, 1)

        self.larger_button = (0.3, 0.3, 0.3, 1)
        self.larger_button_on_press = (0.4, 0.4, 0.4, 1)
        self.larger_button_font = (1, 1, 1, 1)

        self.smaller_button = (0.3, 0.3, 0.3, 1)
        self.smaller_button_on_press = (0.4, 0.4, 0.4, 1)
        self.smaller_button_font = (1, 1, 1, 1)

        self.equal_button = (0.3, 0.3, 0.9, 1)
        self.equal_button_on_press = (0.4, 0.4, 1, 1)
        self.equal_button_font = (1, 1, 1, 1)

        self.ac_button = (0.9, 0.3, 0.3, 1)
        self.ac_button_on_press = (1, 0.4, 0.4, 1)
        self.ac_button_font = (1, 1, 1, 1)

        self.menu_icon = 'images/menu_dark.png'
        self.swap_icon = 'images/swap_dark.png'
        self.backspace_icon = 'images/backspace_dark.png'
        self.sqrt_icon = 'images/sqrt_dark.png'

    def set_theme_light(self):
        self.display_background = (225/255, 245/255, 255/255, 1)
        self.display_button_on_press = (224/255, 1, 1, 1)
        self.display_font = (0, 0, 0, 1)

        self.calculator_background = (1, 1, 1, 1)

        self.larger_button = (0.95, 0.95, 0.95, 1)
        self.larger_button_on_press = (0.85, 0.85, 0.85, 1)
        self.larger_button_font = (0, 0, 0, 1)

        self.smaller_button = (0.95, 0.95, 0.95, 1)
        self.smaller_button_on_press = (0.85, 0.85, 0.85, 1)
        self.smaller_button_font = (0, 0, 0, 1)

        self.equal_button = (0.5, 0.5, 0.9, 1)
        self.equal_button_on_press = (0.6, 0.6, 1, 1)
        self.equal_button_font = (0, 0, 0, 1)

        self.ac_button = (0.9, 0.5, 0.5, 1)
        self.ac_button_on_press = (1, 0.6, 0.6, 1)
        self.ac_button_font = (0, 0, 0, 1)

        self.menu_icon = 'images/menu_light.png'
        self.swap_icon = 'images/swap_light.png'
        self.backspace_icon = 'images/backspace_light.png'
        self.sqrt_icon = 'images/sqrt_light.png'

    def set_theme_pink_laptop(self):
        self.display_background = (255/255, 213/255, 213/255, 1)
        self.display_button_on_press = (1, 233/255, 233/255, 1)
        self.display_font = (81/255, 52/255, 43/255, 1)

        self.calculator_background = (255/255, 185/255, 185/255, 1)

        self.larger_button = (255/255, 213/255, 213/255, 1)
        self.larger_button_on_press = (255/255, 233/255, 233/255, 1)
        self.larger_button_font = (81/255, 52/255, 43/255, 1)

        self.smaller_button = (255/255, 213/255, 213/255, 1)
        self.smaller_button_on_press = (255/255, 233/255, 233/255, 1)
        self.smaller_button_font = (81/255, 52/255, 43/255, 1)

        self.equal_button = (255/255, 230/255, 230/255, 1)
        self.equal_button_on_press = (1, 245/255, 245/255, 1)
        self.equal_button_font = (81/255, 52/255, 43/255, 1)

        self.ac_button = (255/255, 230/255, 230/255, 1)
        self.ac_button_on_press = (1, 245/255, 245/255, 1)
        self.ac_button_font = (81/255, 52/255, 43/255, 1)

        self.menu_icon = 'images/menu_pink.png'
        self.swap_icon = 'images/swap_pink.png'
        self.backspace_icon = 'images/backspace_pink.png'
        self.sqrt_icon = 'images/sqrt_pink.png'

    def set_theme_pink_moto(self):
        self.display_background = (255/255, 230/255, 210/255, 1)
        self.display_button_on_press = (255/255, 240/255, 220/255, 1)
        self.display_font = (81/255, 52/255, 43/255, 1)

        self.calculator_background = (255/255, 190/255, 170/255, 1)

        self.larger_button = (255/255, 230/255, 210/255, 1)
        self.larger_button_on_press = (255/255, 240/255, 220/255, 1)
        self.larger_button_font = (81/255, 52/255, 43/255, 1)

        self.smaller_button = (255/255, 230/255, 210/255, 1)
        self.smaller_button_on_press = (255/255, 240/255, 220/255, 1)
        self.smaller_button_font = (81/255, 52/255, 43/255, 1)

        self.equal_button = (255/255, 243/255, 235/255, 1)
        self.equal_button_on_press = (1, 255/255, 245/255, 1)
        self.equal_button_font = (81/255, 52/255, 43/255, 1)

        self.ac_button = (255/255, 243/255, 235/255, 1)
        self.ac_button_on_press = (1, 255/255, 245/255, 1)
        self.ac_button_font = (81/255, 52/255, 43/255, 1)

        self.menu_icon = 'images/menu_pink.png'
        self.swap_icon = 'images/swap_pink.png'
        self.backspace_icon = 'images/backspace_pink.png'
        self.sqrt_icon = 'images/sqrt_pink.png'

if __name__ == '__main__':
    # Moto g100, 9:21
    # Window.size = (386, 900)
    # Standard, 9:16
    # Window.size = (506, 900)

    settings = SettingsHandler(file_name='settings.txt')

    CalcApp().run()
