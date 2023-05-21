from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import math


class CalcApp(App):
    pass


class Calculator():
    display = ObjectProperty(None)
    decimals = 6
    operators = ['+', '-', '*', '/', '×', '÷']
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
            return "and vegana"
        
        elif expression in ["01134", "14"]:
            return "Hey, how are you?"
        
        elif expression == "1+1":
            return "You do the math"
        
        elif expression == "You do the math":
            return "3 :P"
        
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
        
        # Handle special case pi
        if expression[-2:] in ['pi']:
            return expression[:-2]
        
        # Ordinary remove latest character
        return expression[:-1]


class Simple(Screen, Calculator):
    pass


class Advanced(Screen, Calculator):
    decimals = 10


if __name__ == '__main__':
    CalcApp().run()