import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from ComponentManager import ComponentManager
from kivy.uix.popup import Popup

"""
This file implements the gui for working with the robot code.
The robot app is the root widget, and it creates 3 other widgets:
    At the top, 5 buttons for creating components in a box layout
    In the middle, a stack layout where the components are added
    At the bottom, an anchor layout with a remove and play button
Component preferences can be accessed by double tapping on a component.
"""
kivy.require('2.1.0')

class MotorPopup(Popup):

    # inherits id from parent (the instance that spawned it)
    def __init__(self, parent, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.parentId = parent

    def getParentId(self):
        return self.parentId
    
    def changeMotorConfigValue(self, config):
        #print("In Robot App")
        #print(config)
        manager.editConfig(self.parentId, config)


# TODO: add popup to change config to each class
class MotorComponentInstance(BoxLayout):

    def createMotorPopup(self, id):
        pop = MotorPopup(id)
        pop.open()

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id


class HeadComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

    def editConfig(self, id, newConfig):
        manager.getTimeline()[id].editConfig(newConfig)

class WaistComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

    def editConfig(self, id, newConfig):
        manager.getTimeline()[id].editConfig(newConfig)

class SpeechInComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

    def editConfig(self, id, newConfig):
        manager.getTimeline()[id].editConfig(newConfig)

class SpeechOutComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

    def editConfig(self, id, newConfig):
        manager.getTimeline()[id].editConfig(newConfig)

class RobotController(BoxLayout):

    def createMotorComponent(self):
        if manager.getTotalComponents() == 8:
            pass
        else:
            manager.createComponent("Motor")
            mc = MotorComponentInstance()
            mc.setIndex(manager.getTotalComponents()-1)
            self.ids.stack.add_widget(mc)

    def createHeadComponent(self):
        if manager.getTotalComponents() == 8:
            pass
        else:
            manager.createComponent("Head")
            head = HeadComponentInstance()
            head.setIndex(manager.getTotalComponents()-1)
            self.ids.stack.add_widget(head)

    def createWaistComponent(self):
        if manager.getTotalComponents() == 8:
            pass
        else:
            manager.createComponent("Waist")
            waist = WaistComponentInstance()
            waist.setIndex(manager.getTotalComponents()-1)
            self.ids.stack.add_widget(waist)

    def createSpeechInComponent(self):
        if manager.getTotalComponents() == 8:
            pass
        else:
            manager.createComponent("SpeechIn")
            speech = SpeechInComponentInstance()
            speech.setIndex(manager.getTotalComponents()-1)
            self.ids.stack.add_widget(speech)

    def createSpeechOutComponent(self):
        if manager.getTotalComponents() == 8:
            pass
        else:
            manager.createComponent("SpeechOut")
            outspeech = SpeechOutComponentInstance()
            outspeech.setIndex(manager.getTotalComponents()-1)
            self.ids.stack.add_widget(outspeech)

    def run(self):
        manager.runTimeline()
    
    def clear(self):
        manager.clearTimeline()
        self.ids.stack.clear_widgets() 


class RobotApp(App):
    pass
        


if __name__ == '__main__':
    manager = ComponentManager()
    RobotApp().run()