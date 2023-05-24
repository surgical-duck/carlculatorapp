from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

import math

# Moto g100, 9:21
Window.size = (386, 900)

# Standard, 9:16
#Window.size = (506, 900)

class CalcApp(App):
    pass


class Calculator():
    display = ObjectProperty(None)
    decimals = 6
    operators = ['+', '-', '*', '/', '×', '÷', '^']
    replacement_dict = {'^': '**', 
                        '×': '*', 
                        '÷': '/',
                        'cos': 'math.cos',
                        'sin': 'math.sin',
                        'tan': 'math.tan',
                        'pi': 'math.pi',
                        'π': 'math.pi',
                        'sqrt': 'math.sqrt'}
    
    def evaluate_expression(self, expression):
        
        # Handle empty evaluations
        if expression == "":
            return ""      
        
        # Close open parentheses
        expression = self.close_parentheses(expression)

        # Replace visual for functional operators
        expression = self.replace_operators(expression)

        # Handle easter eggs
        easter_reply = self.handle_easter_eggs(expression)
        if easter_reply is not "":
            return easter_reply

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
            return "Is you stupid?"
        
        return ""

    def handle_operators(self, operator):
        # Comparison cannot be made when label empty
        if self.display.text == '':
            self.display.text = operator
            return

        # Check for multiple operators
        expression = self.display.text
        if expression[-1] in self.operators:
            expression = expression[:-1]
        
        # Add chosen operator
        self.display.text = expression + operator
        
    def replace_operators(self, expression):

        # Loop through all visual operator and replace with functional
        for operator in self.replacement_dict:
            expression = expression.replace(operator, self.replacement_dict[operator])
        
        return expression
    
    def backspace(self, expression):
        
        # Handle special case empty expression
        if expression == '':
            return ''
        
        # Handle special case cos, sin, tan
        if expression[-4:] in ['cos(', 'sin(', 'tan(']:
            return expression[:-4]
        
        # Handle special case sqrt
        elif expression[-5:] == 'sqrt(':
            return expression[:-5]
        
        # Ordinary remove latest character
        return expression[:-1]


class Simple(Screen, Calculator):
    pass


class Advanced(Screen, Calculator):
    decimals = 10


if __name__ == '__main__':
    CalcApp().run()
