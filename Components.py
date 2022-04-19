"""
Class for storing movements and options on the timeline.
Type dictates which group of functionality is targeted
Config is a dictionary of variables or commands, dependent on the function.
"""

class Component:

    def __init__(self):
        self.type = ""
        self.config = ""

    def execute():
        pass


class MotorComponent(Component):

    def __init__(self, config):
        self.type = "Motor"
        self.config = config

    def execute():
        pass

class HeadComponent(Component):

    def __init__(self, config):
        self.type = "Head"
        self.config = config

    def execute():
        pass

class WaistComponent(Component):

    def __init__(self, config):
        self.type = "Waist"
        self.config = config

    def execute():
        pass

class speechInput(Component):

    def __init__(self, config):
        self.type = "speechInput"
        self.config = config

    def execute():
        pass

class speechOutput(Component):

    def __init__(self, config):
        self.type = "speechOutput"
        self.config = config
