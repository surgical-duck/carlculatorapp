import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class CalcApp(App):
    pass


class MainWidget(Widget):
    display = ObjectProperty(None)
    operators = ['+', '-', '*', '/']

    def evaluate_expression(self, expression):
        
        # Handle empty evaluations
        if expression == "":
            return ""      
        
        # Exception handling
        try:
            result = str(eval(expression))
        except ZeroDivisionError:
            return 'Never divide by zero...'
        except SyntaxError:
            return 'Syntax Error'
        except:
            return 'ERROR'

        # Convert float to int when x.0
        split_str = result.split('.')
        if split_str[-1] == '0':
            result = split_str[0]
        
        return result
    
    @staticmethod
    def easter_eggs(expression):

        if expression == "1337":
            return "ELITE"
        
        elif expression == "80085":
            return "Rly?"
        
        elif expression in ["01134", "14"]:
            return "Hey! How are you?"
        
        elif expression == "1+1":
            return "You should know this one"
        
        elif expression == "You should know this one":
            return "3 :P"

    def handle_operators(self, operator):

        if self.display.text == '':
            self.display.text = operator
            return

        # Check for bad expression
        expression = self.display.text
        if expression[-1] in self.operators:
            expression = expression[:-1]
        
        self.display.text = expression + operator
        

if __name__ == '__main__':
    CalcApp().run()