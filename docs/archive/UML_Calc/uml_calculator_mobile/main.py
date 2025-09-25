# Kivy-based mobile UI for UML Calculator
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'core')))
from core.ris import ris, ris_explain

class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.input_a = TextInput(hint_text='Enter first number (a)', multiline=False, input_filter='float')
        self.input_b = TextInput(hint_text='Enter second number (b)', multiline=False, input_filter='float')
        self.result_label = Label(text='Result will appear here')
        self.explain_label = Label(text='')
        self.calc_btn = Button(text='Calculate RIS')
        self.explain_btn = Button(text='Explain RIS')
        self.calc_btn.bind(on_press=self.calculate)
        self.explain_btn.bind(on_press=self.explain)
        self.add_widget(self.input_a)
        self.add_widget(self.input_b)
        self.add_widget(self.calc_btn)
        self.add_widget(self.explain_btn)
        self.add_widget(self.result_label)
        self.add_widget(self.explain_label)

    def calculate(self, instance):
        try:
            a = float(self.input_a.text)
            b = float(self.input_b.text)
            result = ris(a, b)
            self.result_label.text = f'RIS({a}, {b}) = {result}'
            self.explain_label.text = ''
        except Exception as e:
            self.result_label.text = 'Error: ' + str(e)
            self.explain_label.text = ''

    def explain(self, instance):
        try:
            a = float(self.input_a.text)
            b = float(self.input_b.text)
            result, explanation = ris_explain(a, b)
            self.result_label.text = f'RIS({a}, {b}) = {result}'
            self.explain_label.text = explanation
        except Exception as e:
            self.result_label.text = 'Error: ' + str(e)
            self.explain_label.text = ''

class UMLCalculatorApp(App):
    def build(self):
        return CalculatorLayout()

if __name__ == '__main__':
    UMLCalculatorApp().run()
