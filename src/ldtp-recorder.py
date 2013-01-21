#! /usr/bin/env python2
"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import sys

import gui
import recorder


if __name__ == '__main__':
    if 'gui' in sys.argv:
        gui.Gui()
    else:
        rec = recorder.Recorder()
        try:
            rec.start()
        except KeyboardInterrupt:
            rec.stop()
