from src.boundary.guiparam.paramtype import ParamType

class GuiParam:
    name : str = ""
    defvalue : any = []
    type : any = []
    mouesover : str = ""
    displayname : str = ""


class GuiParamCheckBox(GuiParam):
    def __init__(self):
        self.type = ParamType.CHECKBOX

class GuiParamDir(GuiParam):
    def __init__(self):
        self.type = ParamType.DIR

class GuiParamFile(GuiParam):
    def __init__(self):
        self.type = ParamType.FILE

class GuiParamSpinner(GuiParam):
    spinnerlist: dict = None
    def __init__(self):
        self.type = ParamType.SPINNER

class GuiParamNumber(GuiParam):
    minvalue : int = None
    maxvalue : int = None
    isinteger : bool = None
    step : float = None
    def __init__(self):
        self.type = ParamType.NUMBER

class GuiParamString(GuiParam):
    maxlenght : int = None
    def __init__(self):
        self.type = ParamType.STRING