"""
Class for storing movements and options on the timeline.
Type dictates which group of functionality is targeted
Config is a dictionary of variables or commands, dependent on the function.
"""
# TODO: currently execute just prints what's in the component list. Need to hook up execute method to robot code.
class Component:
    config = ""
    type = ""

    def create(text):
        if text == "Motor":
            return MotorComponent("")
        elif text == "Head":
            return HeadComponent("")
        elif text == "Waist":
            return WaistComponent("")
        elif text == "Speech In":
            return speechInput("")
        elif text == "Speech Out":
            return speechOutput("")

    def getConfig(self):
        return self.config

    def editConfig(self, newConfig):
        self.config = newConfig

    def execute():
        pass


class MotorComponent(Component):

    def __init__(self, config):
        self.type = "Motor"
        self.config = config

    def execute(self):
        print(self.type)

class HeadComponent(Component):

    def __init__(self, config):
        self.type = "Head"
        self.config = config

    def execute(self):
        print(self.type)

class WaistComponent(Component):

    def __init__(self, config):
        self.type = "Waist"
        self.config = config

    def execute(self):
        print(self.type)

class speechInput(Component):

    def __init__(self, config):
        self.type = "speechInput"
        self.config = config

    def execute(self):
        print(self.type)

class speechOutput(Component):

    def __init__(self, config):
        self.type = "speechOutput"
        self.config = config

    def execute(self):
        print(self.type)
