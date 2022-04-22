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
The robot controller is the root widget, and it creates 3 other widgets:
    At the top, a grid layout of at max 8 components where component instances are added
    In the middle, 5 buttons for creating components in a box layout
    At the bottom, an anchor layout with a remove and play button
Component preferences can be accessed by taping edit on a component instance.

The layout and connection to functions is done in the robot.kv file, the logic is implemented in RobotApp,
Components, and ComponentManager .py files.
"""
kivy.require('2.1.0')

# TODO: Create Waist, Head, SpeakIn, SpeakOut popup instance classes
# TODO: Create waist, head, speakin, speakout popout layouts in .kv file (use motor as reference)
class MotorPopup(Popup):

    # inherits id from parent (the instance that spawned it)
    def __init__(self, parent, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.parentId = parent

    def getParentId(self):
        return self.parentId
    
    # TODO: Add actual value being returned by buttons in the kv file
    def changeMotorConfigValue(self, config):
        #print("In Robot App")
        #print(config)
        manager.editConfig(self.parentId, config)

#Waist PopUp Class
class WaistPopup(Popup):

    # inherits id from parent (the instance that spawned it)
    def __init__(self, parent, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.parentId = parent

    def getParentId(self):
        return self.parentId
    
    # TODO: Add actual value being returned by buttons in the kv file
    def changeWaistConfigValue(self, config):
        #print("In Robot App")
        #print(config)
        manager.editConfig(self.parentId, config)
        
#Head PopUp Class
class HeadPopup(Popup):

    # inherits id from parent (the instance that spawned it)
    def __init__(self, parent, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.parentId = parent

    def getParentId(self):
        return self.parentId
    
    # TODO: Add actual value being returned by buttons in the kv file
    def changeHeadConfigValue(self, config):
        #print("In Robot App")
        #print(config)
        manager.editConfig(self.parentId, config)

#Speak In PopUp Class
class SpeakInPopup(Popup):

    # inherits id from parent (the instance that spawned it)
    def __init__(self, parent, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.parentId = parent

    def getParentId(self):
        return self.parentId
    
    # TODO: Add actual value being returned by buttons in the kv file
    def changeSpeakInConfigValue(self, config):
        #print("In Robot App")
        #print(config)
        manager.editConfig(self.parentId, config)

#Speak Out PopUp Class
class SpeakOutPopup(Popup):

    # inherits id from parent (the instance that spawned it)
    def __init__(self, parent, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.parentId = parent

    def getParentId(self):
        return self.parentId
    
    # TODO: Add actual value being returned by buttons in the kv file
    def changeSpeakOutConfigValue(self, config):
        #print("In Robot App")
        #print(config)
        manager.editConfig(self.parentId, config)
        
# TODO: add create{}Popup method
class MotorComponentInstance(BoxLayout):

    def createMotorPopup(self, id):
        pop = MotorPopup(id)
        pop.open()

    
    # keeps track of where in the component list the object is, so it can be edited later
    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

# TODO: add create{}Popup method
class HeadComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

# TODO: add create{}Popup method
class WaistComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id


# TODO: add create{}Popup method
class SpeechInComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id


# TODO: add create{}Popup method
class SpeechOutComponentInstance(BoxLayout):

    def setIndex(self, index):
        self.id = index

    def getId(self):
        return self.id

class RobotController(BoxLayout):

    def createMotorComponent(self):
        if manager.getTotalComponents() == 8: # don't make any more than 8 components (or the layout breaks lol)
            pass
        else:
            manager.createComponent("Motor") # The text gets passed to the component constructor which dictates the type of component
            mc = MotorComponentInstance()
            mc.setIndex(manager.getTotalComponents()-1) # super janky way of assigning ids based on how many are in the stack but it works
            self.ids.stack.add_widget(mc) # dynamically putting the instance onto the top grid

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
        manager.runTimeline() # loops through the components and runs their .execute() methods
    
    # removes all widgets from the stack. Easier than removing them one by one
    def clear(self):
        manager.clearTimeline()
        self.ids.stack.clear_widgets() 

# Don't touch, this has to be here
class RobotApp(App):
    pass
        


if __name__ == '__main__':
    manager = ComponentManager() # functions as the back end, managing the components and applying edits to their configs
    RobotApp().run()
