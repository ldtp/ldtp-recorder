"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import pyatspi.Accessibility as Accessibility
import actions


def _strip(s):
    if s is None:
        return ''
    return s.replace(' ', '')


def getLdtpCommand(actionInfo):
    '''
    @type actionInfo: ActionInfo
    @rtype: string
    '''

    if actionInfo is None:
        return None

    role = actionInfo.role

    if False:
        pass

    elif role == Accessibility.ROLE_CHECK_BOX:
        if actionInfo.value == 1:
            cmd = 'check'
        elif actionInfo.value == 0:
            cmd = 'uncheck'

        return "ldtp.%s('%s', '%s')" % (
            cmd,
            _strip(actionInfo.windowName),
            _strip(actionInfo.name))

    elif role == Accessibility.ROLE_COMBO_BOX:
        return "ldtp.comboselect('%s', '%s', '%s')" % (
            _strip(actionInfo.windowName),
            _strip(actionInfo.name),
            _strip(actionInfo.value))

    elif role == Accessibility.ROLE_DIALOG:
        if actionInfo.actionType == actions._ACTION_TYPE_WINDOW_CLOSE:
            cmd = 'waittillnoguiexist'
        elif actionInfo.actionType == actions._ACTION_TYPE_WINDOW_OPEN:
            cmd = 'waittillguiexist'
        return "ldtp.%s('%s')" % (
            cmd,
            _strip(actionInfo.windowName))

    elif role == Accessibility.ROLE_PAGE_TAB:
        return "ldtp.selecttab('%s', '%s', '%s')" % (
            _strip(actionInfo.windowName),
            _strip(actionInfo.name),
            _strip(actionInfo.value))

    elif role == Accessibility.ROLE_MENU:
        return "ldtp.selectmenuitem('%s', '%s')" % (
            _strip(actionInfo.windowName),
            _strip(actionInfo.name))

    elif role == Accessibility.ROLE_PUSH_BUTTON:
        return "ldtp.click('%s', '%s')" % (
            _strip(actionInfo.windowName),
            _strip(actionInfo.name))

    elif role == Accessibility.ROLE_SPIN_BUTTON:
        return "ldtp.setvalue('%s', '%s', %s)" % (
            _strip(actionInfo.windowName),
            _strip(actionInfo.name),
            actionInfo.value)

    else:
        return str(actionInfo)
