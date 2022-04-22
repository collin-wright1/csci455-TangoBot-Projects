"""
Used for rendering the GUI and taking user input 
"""
from Components import Component, MotorComponent, HeadComponent, WaistComponent, speechInput, speechOutput

class ComponentManager:

    totalComponents = 0

    def __init__(self):
        self.timeline = []

    def createComponent(self, text):
        comp = Component.create(text)
        self.addToTimeline(comp)
        self.totalComponents += 1
        if not self.timeline:
            comp.setIndex(0)
        else:
            comp.setIndex(len(self.timeline) - 1)

    def getTotalComponents(self):
        return self.totalComponents


    def addToTimeline(self, component):
        self.timeline.append(component)

    def removeFromTimeline(self, component):
        self.timeline.remove(component)
    
    def clearTimeline(self):
        self.timeline = []
        self.totalComponents = 0
    
    def editConfig(self, index, config):
        #print("In Component Manager")
        #print(config)
        #print(self.timeline[index].getConfig())
        self.timeline[index].editConfig(config)
        
    def getTimeline(self):
        return self.timeline

    def runTimeline(self):
        for component in self.timeline:
            component.execute()
