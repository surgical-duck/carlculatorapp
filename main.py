import kivy
from kivy.app import App
from kivy.uix.widget import Widget


class CalcApp(App):
    pass


class MainWidget(Widget):

    def evaluate_expression(self, expression):

        result = str(eval(expression))

        split_str = result.split('.')
        if split_str[1] == '0':
            result = split_str[0]
        
        return result

if __name__ == '__main__':
    CalcApp().run()