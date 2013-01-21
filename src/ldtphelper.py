"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import ldtp


def getTextFieldValue(windowName, txtName):
    if windowName is None or windowName == '':
        return None
    if txtName is None or txtName == '':
        return None
    return ldtp.gettextvalue(windowName, txtName)
