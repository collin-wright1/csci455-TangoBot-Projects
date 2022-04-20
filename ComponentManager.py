"""
Used for rendering the GUI and taking user input 
"""
from Components import Component, MotorComponent, HeadComponent, WaistComponent, speechInput, speechOutput

class ComponentManager:

    def __init__(self):
        self.timeline = []

    def createComponent(self, text):
        self.addToTimeline(Component.create(text))

    def addToTimeline(self, component):
        self.timeline.append(component)

    def removeFromTimeline(self, component):
        self.timeline.remove(component)
    
    def clearTimeline(self):
        self.timeline = []

    def getTimeline(self):
        return self.timeline

    def runTimeline(self):
        for component in self.timeline:
            component.execute()
