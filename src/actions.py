"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import inspect
import sys

import pyatspi.Accessibility as Accessibility

import context
import debug
import helper
import ldtphelper


_ACTION_TYPE_WINDOW_CLOSE = '_ACTION_TYPE_WINDOW_CLOSE'
_ACTION_TYPE_WINDOW_OPEN = '_ACTION_TYPE_WINDOW_OPEN'

_RETURN_VALUE_FALSE = 0
_RETURN_VALUE_TRUE = 1
_RETURN_VALUE_LATER = 2

class ActionInfo:

    def __init__(self, name=None, value=None, role=None, windowName=None, actionType=None):
        '''
        @param actionType: only used when role is not enough,
                           eg. window open/close action
        @type name: string
        @type value: string, int, boolean
        @type role: Accessibility.Role
        '''
        self.name = name
        self.value = value
        self.role = role
        self.windowName = windowName
        self.actionType = actionType

    def __str__(self):
        result = ''
        for key in ['name', 'value', 'windowName', 'role', 'actionType']:
            value = getattr(self, key)
            if value:
                result += '%s <%s> ' % (key, value)
        return result


def getActionInfo(event):
    '''
    @type event: Event
    @rtype: ActionInfo
    '''
    if event is None or event.source.getRole() in [
                                                   Accessibility.ROLE_INVALID,
                                                   Accessibility.ROLE_TERMINAL,
                                                   Accessibility.ROLE_TOOL_TIP,
                                                   Accessibility.ROLE_SCROLL_BAR,
                                                   ]:
        return None
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name not in ['AbstractAction', 'ActionInfo']:
            result = obj.matches(event)
            if result == _RETURN_VALUE_TRUE:
                widget = obj.getActionInfo(event)
                return widget
            elif result == _RETURN_VALUE_LATER:
                return None
    return None


def _matches(event, role, eventTypes, detail1=None):
    '''
    @type role: Accessibility.Role
    @rtype: True, False
    '''
    if event.source.getRole() == role:
        for eventType in eventTypes:
            if str(event.type).startswith(eventType):
                if detail1 is None or event.detail1 == detail1:
                    return True
    return False


def _isContextReady(valueName):
    '''
    @type valueName: string
    '''
    ctx = context.Context()
    if getattr(ctx, valueName):
        setattr(ctx, valueName, False)
        return _RETURN_VALUE_TRUE
    setattr(ctx, valueName, True)
    return _RETURN_VALUE_FALSE


class AbstractAction:
    ''' I am an Interface '''

    @staticmethod
    def matches(event):
        '''
        @type event: Event
        @rtype: _RETURN_VALUE_FALSE or _RETURN_VALUE_TRUE or _RETURN_VALUE_LATER
        '''
        raise NotImplementedError('Should have implemented this')

    @staticmethod
    def getActionInfo(event):
        '''
        @type event: Event
        @rtype: ActionInfo
        '''
        raise NotImplementedError('Should have implemented this')


class CheckBoxAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event,
                          Accessibility.ROLE_CHECK_BOX,
                          ['object:state-changed:armed'])
        if result:
            context.Context().resetMenuItem()
            stateSet = event.source.getState()
            if not stateSet.contains(Accessibility.STATE_FOCUSED):
                return _RETURN_VALUE_FALSE
            return _isContextReady('isWaitingForThe2ndCheckBox')
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        value = event.detail1
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, value=value, role=role, windowName=windowName)
        return actionInfo


class ComboBoxAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_COMBO_BOX,
                          ['object:selection-changed'])
        if result:
            context.Context().resetMenuItem()
            return _RETURN_VALUE_TRUE
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        value = context.Context().menuItemValue
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, role=role, value=value, windowName=windowName)
        return actionInfo


class MenuItemAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_MENU_ITEM,
                          ['object:state-changed:selected'])
        if result:
            ctx = context.Context()
            ctx.resetMenuItem()
            ctx.menuItemValue = helper.getNameByEvent(event)
            ctx.menuItemWindowName = helper.getWindowName(event.source)
            return _RETURN_VALUE_LATER
        else:
            if event.source.getRole() == Accessibility.ROLE_MENU_ITEM:
                ctx = context.Context()
                ctx.lastWasMenuItem = True
                ctx.menuItemValue = helper.getNameByEvent(event)
                ctx.menuItemWindowName = helper.getWindowName(event.source)
            return _RETURN_VALUE_FALSE


class MenuAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_MENU,
                          ['object:state-changed:selected'], detail1=1)
        if result:
            context.Context().resetMenuItem()
            return _isContextReady('isWaitingForThe2ndMenu')
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, role=role, windowName=windowName)
        return actionInfo


class MouseAction(AbstractAction):

    @staticmethod
    def matches(event):
        if str(event.type).startswith('mouse:button:1p'):
            ctx = context.Context()
            if ctx.lastWasMenuItem:
                x = event.detail1
                y = event.detail2

                accessible = helper.getAccessibleByCoords(x, y)
                if accessible:
                    print(accessible)
                '''
                @todo: check coords for proper type
                '''
                return _RETURN_VALUE_TRUE
        return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        ctx = context.Context()
        if ctx.lastWasMenuItem:
            name = ctx.menuItemValue
            role = Accessibility.ROLE_MENU_ITEM
            windowName = ctx.menuItemWindowName
            ctx.resetMenuItem()
        actionInfo = ActionInfo(name=name, role=role, windowName=windowName)
        return actionInfo


class PushButtonAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_PUSH_BUTTON,
                          ['object:state-changed:armed'], detail1=1)
        if result:
            context.Context().resetMenuItem()
            return _isContextReady('isWaitingForThe2ndPushButton')
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, role=role, windowName=windowName)
        return actionInfo


class RadioButtonAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_RADIO_BUTTON,
                          ['object:state-changed:checked'])
        if result:
            context.Context().resetMenuItem()
            return _isContextReady('isWaitingForThe2ndRadioButton')
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        role = event.source.getRole()
        value = event.detail1
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, role=role, value=value, windowName=windowName)
        return actionInfo


class SpinButtonAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_SPIN_BUTTON,
                          ['object:text-changed:insert'])
        if result:
            context.Context().resetMenuItem()
            return _isContextReady('isWaitingForThe2ndSpinButton')
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        value = event.source.get_current_value()
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, value=value, role=role, windowName=windowName)
        return actionInfo


class TabAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_PAGE_TAB,
                          ['object:state-changed:selected'], detail1=1)
        if result:
            context.Context().resetMenuItem()
            return _isContextReady('isWaitingForThe2ndPageTab')
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByAccessible(event.source.get_parent())
        value = helper.getNameByEvent(event)
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(name=name, role=role, value=value, windowName=windowName)
        return actionInfo


class TextFieldAction(AbstractAction):

    @staticmethod
    def matches(event):
        result = _matches(event, Accessibility.ROLE_TEXT,
                          ['object:text-changed:insert', 'object:text-changed:delete'])
        if result:
            context.Context().resetMenuItem()
            return _RETURN_VALUE_TRUE
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        name = helper.getNameByEvent(event)
        windowName = helper.getWindowName(event.source)
        role = event.source.getRole()
        value = ldtp-helper.getTextFieldValue(windowName, name)
        actionInfo = ActionInfo(name=name, windowName=windowName, role=role, value=value)
        return actionInfo


class WindowCloseAction(AbstractAction):

    @staticmethod
    def matches(event):
        ''' @todo: extend roles '''
        result = _matches(event, Accessibility.ROLE_DIALOG, ['window:deactivate'])

        if result:
            context.Context().resetMenuItem()
            if event.source.getState().contains(Accessibility.STATE_SHOWING):
                return _RETURN_VALUE_TRUE
            return _RETURN_VALUE_FALSE
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(windowName=windowName, role=role,
                                actionType=_ACTION_TYPE_WINDOW_CLOSE)
        return actionInfo


class WindowOpenAction(AbstractAction):

    @staticmethod
    def matches(event):
        ''' @todo: extend roles '''
        result = _matches(event, Accessibility.ROLE_DIALOG, ['window:create'])
        if result:
            context.Context().resetMenuItem()
            return _RETURN_VALUE_TRUE
        else:
            return _RETURN_VALUE_FALSE

    @staticmethod
    def getActionInfo(event):
        role = event.source.getRole()
        windowName = helper.getWindowName(event.source)
        actionInfo = ActionInfo(windowName=windowName, role=role,
                                actionType=_ACTION_TYPE_WINDOW_OPEN)
        return actionInfo
