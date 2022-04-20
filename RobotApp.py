from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from ComponentManager import ComponentManager

"""
This file implements the gui for working with the robot code.
The robot app is the root widget, and it creates 3 other widgets:
    At the top, 5 buttons for creating components in a box layout
    In the middle, a stack layout where the components are added
    At the bottom, an anchor layout with a remove and play button
Component preferences can be accessed by double tapping on a component.
"""

# TODO: Add creation of component instance inside stack at the top of the gui.
# TODO: Enable component config editing
class ComponentInstance(Widget):
    pass
        

class ComponentButton(Button):
    def createComponent(self):
        manager.createComponent(self.text)

class RunButton(Button):
    def run(self):
        manager.runTimeline()

class ClearButton(Button):
    def clear(self):
        manager.clearTimeline()



class RobotController(BoxLayout):
    pass



class RobotApp(App):
    pass
        


if __name__ == '__main__':
    manager = ComponentManager()
    RobotApp().run()