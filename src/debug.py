"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import os

import pyatspi.Accessibility as Accessibility


''' export LDTP_RECORDER_DEBUG=LVL '''

''' set LDTP_RECORDER_DEBUG to 5 to see all events' role '''
LVL_ALL_ROLES = 5
''' set LDTP_RECORDER_DEBUG to 9 to see all events (heavy spam) '''
LVL_ALL_EVENTS = 9


try:
    level = int(os.getenv('LDTP_RECORDER_DEBUG'))
except TypeError:
    level = None
except ValueError:
    level = None


def getStates(stateSet):
    states = [
              Accessibility.STATE_ACTIVE,
              Accessibility.STATE_ANIMATED,
              Accessibility.STATE_ARMED,
              Accessibility.STATE_BUSY,
              Accessibility.STATE_CHECKED,
              Accessibility.STATE_COLLAPSED,
              Accessibility.STATE_DEFUNCT,
              Accessibility.STATE_EDITABLE,
              Accessibility.STATE_ENABLED,
              Accessibility.STATE_EXPANDABLE,
              Accessibility.STATE_EXPANDED,
              Accessibility.STATE_FOCUSABLE,
              Accessibility.STATE_FOCUSED,
              Accessibility.STATE_HAS_TOOLTIP,
              Accessibility.STATE_HORIZONTAL,
              Accessibility.STATE_ICONIFIED,
              Accessibility.STATE_INDETERMINATE,
              Accessibility.STATE_INVALID,
              Accessibility.STATE_INVALID_ENTRY,
              Accessibility.STATE_IS_DEFAULT,
              Accessibility.STATE_LAST_DEFINED,
              Accessibility.STATE_MANAGES_DESCENDANTS,
              Accessibility.STATE_MODAL,
              Accessibility.STATE_MULTISELECTABLE,
              Accessibility.STATE_MULTI_LINE,
              Accessibility.STATE_OPAQUE,
              Accessibility.STATE_PRESSED,
              Accessibility.STATE_REQUIRED,
              Accessibility.STATE_RESIZABLE,
              Accessibility.STATE_SELECTABLE,
              Accessibility.STATE_SELECTABLE_TEXT,
              Accessibility.STATE_SELECTED,
              Accessibility.STATE_SENSITIVE,
              Accessibility.STATE_SHOWING,
              Accessibility.STATE_SINGLE_LINE,
              Accessibility.STATE_STALE,
              Accessibility.STATE_SUPPORTS_AUTOCOMPLETION,
              Accessibility.STATE_TRANSIENT,
              Accessibility.STATE_TRUNCATED,
              Accessibility.STATE_VERTICAL,
              Accessibility.STATE_VISIBLE,
              Accessibility.STATE_VISITED,
              ]
    for state in states:
        if stateSet.contains(state):
            yield state
