"""
ldtp-recorder

@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2012-2013 Friedrich Paetzke
@license: GPL

See 'LICENSE' in the source distribution for more information.
"""

import pyatspi as atspi

import actions
import context
import debug
import generator


class Recorder:

    _weAreTheBorg = {}

    def __init__(self):
        self.__dict__ = self._weAreTheBorg
        if 'initWasHere' in self.__dict__:
            return
        self.__dict__['initWasHere'] = True
        self._init()

    def _init(self):
        self._callback = None
        self._isRunning = False
        self._registry = atspi.Registry()
        self._context = context.Context()
        self._eventTypes = [
            'document:attributes-changed',
            'document:load-complete',
            'document:load-stopped',
            'document:reload',
            'focus:',
            #'mouse:abs',
            'mouse:button',
            'mouse:button:1p',
            'mouse:button:1r',
            'mouse:button:2p',
            'mouse:button:2r',
            'mouse:button:3p',
            'mouse:button:3r',
            #'mouse:rel',
            'object:active-descendant-changed',
            'object:attributes-changed',
            'object:bounds-changed',
            'object:children-changed',
            'object:children-changed:add',
            'object:children-changed:remove',
            'object:column-deleted',
            'object:column-inserted',
            'object:column-reordered',
            'object:link-selected',
            'object:model-changed',
            'object:property-change',
            'object:property-change:accessible-description',
            'object:property-change:accessible-name',
            'object:property-change:accessible-parent',
            'object:property-change:accessible-role',
            'object:property-change:accessible-table-caption',
            'object:property-change:accessible-table-column-description',
            'object:property-change:accessible-table-column-header',
            'object:property-change:accessible-table-row-description',
            'object:property-change:accessible-table-row-header',
            'object:property-change:accessible-table-summary',
            'object:property-change:accessible-value',
            'object:row-deleted',
            'object:row-inserted',
            'object:row-reordered',
            'object:selection-changed',
            'object:state-changed',
            'object:state-changed:',
            'object:text-attributes-changed',
            'object:text-bounds-changed',
            'object:text-caret-moved',
            'object:text-changed',
            'object:text-changed:delete',
            'object:text-changed:insert',
            'object:text-selection-changed',
            'object:visible-data-changed',
            'terminal:application-changed',
            'terminal:charwidth-changed',
            'terminal:columncount-changed',
            'terminal:line-changed',
            'terminal:linecount-changed',
            'window:activate',
            'window:close',
            'window:create',
            'window:deactivate',
            'window:desktop-create',
            'window:desktop-destroy',
            'window:lower',
            'window:maximize',
            'window:minimize',
            'window:move',
            'window:raise',
            'window:reparent',
            'window:resize',
            'window:restore',
            'window:restyle',
            'window:shade',
            'window:unshade',
            ]


    def setOnActionCallback(self, callback):
        self._callback = callback


    def start(self):
        if not self._isRunning:
            self._isRunning = True
            self._registry.registerEventListener(self._onEvent, *self._eventTypes)
            self._registry.start()


    def stop(self):
        if self._isRunning:
            self._isRunning = False
            self._registry.stop()
            self._registry.deregisterEventListener(self._onEvent, *self._eventTypes)


    def _onEvent(self, event):
        actionInfo = actions.getActionInfo(event)
        if actionInfo:
            if debug.level:
                print(actionInfo)

            cmd = generator.getLdtpCommand(actionInfo)
            if self._callback is None:
                print(cmd)
            else:
                self._callback(cmd)
        if debug.level:
            if debug.level == debug.LVL_ALL_ROLES:
                print(event.source.getRole())
            elif debug.level == debug.LVL_ALL_EVENTS:
                print(event)
