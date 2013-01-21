"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import pyatspi as atspi
import pyatspi.Accessibility as Accessibility
import debug

COORD_TYPE_ABS = 0
COORD_TYPE_WIN_RELA = 1


def getWindows():
    '''
    Returns all Windows on all Desktops
    @rtype: List of Accessible
    '''
    windows = []
    reg = atspi.Registry()
    for i in range(0, reg.getDesktopCount()):
        desktop = reg.getDesktop(i)
        for j in range (0, desktop.childCount):
            windows.append(desktop.getChildAtIndex(j))
    return windows


def isPointInRect(x, y, rectX, rectY, rectWidht, rectHeight):
    if x >= rectX and x < rectX + rectWidht:
        if y >= rectY and y < rectY + rectHeight:
            return True
    return False


def getAcessibleByCoordInWindow(x, y, parent):
    '''
    @type x: int
    @type y: int
    @type parent: Accessible
    '''
    for i in range(0, parent.getChildCount()):
        child = parent.getChildAtIndex(i)
        chX, chY = child.getPosition(COORD_TYPE_ABS)
        chWidth, chHeight = child.getSize()

        if isPointInRect(x, y, chX, chY, chWidth, chHeight):
            nestedAccessible = getAcessibleByCoordInWindow(x, y, child)
            if nestedAccessible:
                return nestedAccessible
            return child
    return None


def getAccessibleByCoords(x, y, window=None):
    '''
    @param window: Parent Window
    @type x: int
    @type y: int
    @type window: Accessible
    '''
    if window is None:
        windows = getWindows()
    else:
        windows = [window]

    for win in windows:
        accessible = getAcessibleByCoordInWindow(x, y, win)
        if accessible:
            return accessible
    return None


def getNameByEvent(event):
    accessible = event.source
    return getNameByAccessible(accessible)


def getNameByAccessible(accessible):
    name = accessible.name
    if name and name != '':
        return name
    return None


def getWindowName(accessible):
    window = _getWindow(accessible)
    name = getNameByAccessible(window)
    return name


def _getWindow(accessible):
    if accessible is None:
        return None
    role = accessible.getRole()
    roles = [
             Accessibility.ROLE_ALERT,
             Accessibility.ROLE_DIALOG,
             Accessibility.ROLE_FILE_CHOOSER,
             Accessibility.ROLE_FONT_CHOOSER,
             Accessibility.ROLE_FRAME,
             Accessibility.ROLE_WINDOW,
             ]
    if role in roles:
        return accessible
    parent = None
    handle = None
    try:
        parent = accessible.parent
        handle = _getWindow(parent)
    except:
        pass
    return handle
