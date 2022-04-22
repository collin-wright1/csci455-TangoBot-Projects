from Project_2_Robot_Movement_Code import TangoBot


"""
Class for storing movements and options on the timeline.
Type dictates which group of functionality is targeted
Config is a dictionary of variables or commands, dependent on the function.
"""
class Component:
    config = ""
    type = ""
    index = None

    # don't know if index or type is really necessary here but I'm scared to touch them

    # decides which component to create
    def create(text):
        if text == "Motor":
            return MotorComponent("")
        elif text == "Head":
            return HeadComponent("")
        elif text == "Waist":
            return WaistComponent("")
        elif text == "SpeechIn":
            return speechInput("")
        elif text == "SpeechOut":
            return speechOutput("")

    def getConfig(self):
        return self.config

    def getIndex(self):
        return self.index
    
    def setIndex(self, index):
        self.index = index

    def editConfig(self, newConfig):
        #print("in Component")
        #print(newConfig)
        self.config = newConfig

    def execute():
        pass


class MotorComponent(Component):

    # need speed and time, direction stored in speed

    def __init__(self, config):
        self.type = "Motor"
        self.config = config

    # TODO: Implement motor execute
    def execute(self):
        robot = TangoBot()
        print(self.type)
        print(self.config)

class HeadComponent(Component):

    def __init__(self, config):
        self.type = "Head"
        self.config = config

    # TODO: Implement Head Execute
    def execute(self):
        print(self.type)
        print(self.config)

class WaistComponent(Component):

    def __init__(self, config):
        self.type = "Waist"
        self.config = config

    # TODO: Implement waist execute
    def execute(self):
        print(self.type)
        print(self.config)

class speechInput(Component):

    def __init__(self, config):
        self.type = "speechInput"
        self.config = config

    # TODO: Implement speech in execute
    def execute(self):
        print(self.type)
        print(self.config)

class speechOutput(Component):

    def __init__(self, config):
        self.type = "speechOutput"
        self.config = config

    # TODO: Implement speech out execute
    def execute(self):
        print(self.type)
        print(self.config)
