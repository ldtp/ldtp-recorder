"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

class Context:

    _weAreTheBorg = {}

    def __init__(self):
        self.__dict__ = self._weAreTheBorg
        if 'initWasHere' in self.__dict__:
            return
        self.__dict__['initWasHere'] = True
        self._init()


    def _init(self):
        ''' set to True to wait for the second CheckBox Event '''
        self.isWaitingForThe2ndCheckBox = False

        ''' set to True to wait for the second Menu Event '''
        self.isWaitingForThe2ndMenu = False

        ''' set to True to wait for the second PageTab Event '''
        self.isWaitingForThe2ndPageTab = False

        ''' set to True to wait for the second PushButton Event '''
        self.isWaitingForThe2ndPushButton = False

        ''' set to True to wait for the second RadioButton Event '''
        self.isWaitingForThe2ndRadioButton = False

        ''' set to True to wait for the second SpinButton Event '''
        self.isWaitingForThe2ndSpinButton = False

        ''' store the name of the MenuItem '''
        self.menuItemValue = None
        self.menuItemWindowName = None
        self.resetMenuItem()


    def resetMenuItem(self):
        self.lastWasMenuItem = False
