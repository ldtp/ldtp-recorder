"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

from gi.repository import Gtk
from recorder import Recorder


class Gui:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('gui.glade')
        Recorder().setOnActionCallback(self.actionCallback)

        window = builder.get_object('window1')
        window.connect('delete-event', Gtk.main_quit)
        window.show_all()

        btnStart = builder.get_object('btnStart')
        btnStart.connect('clicked', self.onStartClick)

        btnStop = builder.get_object('btnStop')
        btnStop.connect('clicked', self.onStopClick)

        self.textView = builder.get_object('textview')

        Gtk.main()


    def actionCallback(self, string):
        if 'ldtpRecorder' not in string:
            self.textView.get_buffer().insert_at_cursor(string + "\n")


    def onStartClick(self, toolButton):
        self.textView.get_buffer().insert_at_cursor("starting\n")
        Recorder().start()


    def onStopClick(self, toolButton):
        self.textView.get_buffer().insert_at_cursor("stopping\n")
        Recorder().stop()


if __name__ == '__main__':
    Gui()
