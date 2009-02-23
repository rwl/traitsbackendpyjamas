#------------------------------------------------------------------------------
#
#  Copyright (c) 2009, Richard W. Lincoln
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Author: Richard W. Lincoln
#  Date:   23/02/2009
#
#------------------------------------------------------------------------------

""" The Pyjamas specific implementations the action manager internal classes.
"""

# Standard libary imports.
from inspect import getargspec

# Major package imports.
from pyjamas.ui import MenuItem

# Enthought library imports.
from enthought.traits.api import Any, Bool, HasTraits, Int

# Local imports.
from enthought.pyface.action.action_event import ActionEvent

#_STYLE_TO_KIND_MAP = {
#    'push'   : wx.ITEM_NORMAL,
#    'radio'  : wx.ITEM_RADIO,
#    'toggle' : wx.ITEM_CHECK
#}

class MenuItem:
    id = 0
    label = ''
    longtip = ''
    kind = ''
    bitmap = None


class _MenuItem(HasTraits):
    """ A menu item representation of an action item. """

    #### '_MenuItem' interface ################################################

    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any

    # Is the item enabled?
    enabled = Bool(True)

    # Is the item visible?
    visible = Bool(True)

    # The radio group we are part of (None if the menu item is not part of such
    # a group).
    group = Any


    # Index of the menu item in the menu.
    idx = Int

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, parent, menu, item, controller):
        """ Creates a new menu item for an action item. """

        self.item = item

        # Create an appropriate menu item depending on the style of the action.
        action  = item.action
        label   = action.name
#        kind    = _STYLE_TO_KIND_MAP[action.style]
        kind = action.style
        longtip = action.description

#        if len(action.accelerator) > 0:
#            label = label + '\t' + action.accelerator

        # This just helps with debugging when people forget to specify a name
        # for their action.
        if len(label) == 0:
            label = item.action.__class__.__name__

#        self.control_id = wx.NewId()
#        self.control = wx.MenuItem(menu, self.control_id, label, longtip, kind)
        self.control = MenuItem(text=label, asHtml=True, subMenu=menu)

        # If the action has an image then display it.
        bitmap = None
        if action.image is not None:
            bitmap = action.image.create_bitmap()

        self.idx = idx = len(menu.keys())

        if kind == "push":
            menu.addItem(label=label)
        elif kind == "radio":
            menu.addItem(label=label)
        elif kind == "toggle":
            menu.addItem(label=label)
        else:
            raise ValueError, "Invalid 'kind' trait value [%s]." % kind

        menu.addItem(self.control)

        # Set the initial enabled/disabled state of the action.
        if action.enabled and action.visible:
            menu.setEnabled(True)
        else:
            menu.setEnabled(False)

        # Set the initial checked state.
        if action.style in ['radio', 'toggle']:
            if action.checked:
#                self.control.Check(action.checked)
                raise NotImplementedError

        # Wire it up...create an ugly flag since some platforms dont skip the
        # event when we thought they would
        self._skip_menu_event = False
        menu.setCommand( self._on_menu )

        # Listen for trait changes on the action (so that we can update its
        # enabled/disabled/checked state etc).
        action.on_trait_change(self._on_action_enabled_changed, 'enabled')
        action.on_trait_change(self._on_action_visible_changed, 'visible')
        action.on_trait_change(self._on_action_checked_changed, 'checked')
        action.on_trait_change(self._on_action_name_changed, 'name')

        if controller is not None:
            self.controller = controller
            controller.add_to_menu(self)

        return


    def dispose(self):
        action = self.item.action
        action.on_trait_change(self._on_action_enabled_changed, 'enabled',
            remove=True)
        action.on_trait_change(self._on_action_visible_changed, 'visible',
            remove=True)
        action.on_trait_change(self._on_action_checked_changed, 'checked',
            remove=True)
        action.on_trait_change(self._on_action_name_changed, 'name',
            remove=True)

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _enabled_changed(self):
        """ Called when our 'enabled' trait is changed.
        """
        if self.enabled and self.visible:
            self.control.setEnabled( True )
        else:
            self.control.setEnabled( False )
        return


    def _visible_changed(self):
        """ Called when our 'visible' trait is changed.
        """
        if self.enabled and self.visible:
            self.control.setVisible( True )
        else:
            self.control.setVisible( False )
        return

    def _checked_changed(self):
        """ Called when our 'checked' trait is changed. """

        if self.item.action.style == 'radio':
            # fixme: Not sure why this is even here, we had to guard it to
            # make it work? Must take a look at svn blame!
            # FIXME v3: Note that menu_checked() doesn't seem to exist, so we
            # comment it out and do the following instead.
            #if self.group is not None:
            #    self.group.menu_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if self.checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

#        self.control.Check(self.checked)

        return


    def _on_action_enabled_changed(self, action, trait_name, old, new):
        """ Called when the enabled trait is changed on an action.
        """
        if action.enabled and action.visible:
            self.control.setEnabled( True )
        else:
            self.control.setEnabled( False )
        return


    def _on_action_visible_changed(self, action, trait_name, old, new):
        """ Called when the visible trait is changed on an action.
        """
        if action.enabled and action.visible:
            self.control.setVisible( True )
        else:
            self.control.setVisible( False )
        return


    def _on_action_checked_changed(self, action, trait_name, old, new):
        """ Called when the checked trait is changed on an action. """

        if self.item.action.style == 'radio':
            # fixme: Not sure why this is even here, we had to guard it to
            # make it work? Must take a look at svn blame!
            # FIXME v3: Note that menu_checked() doesn't seem to exist, so we
            # comment it out and do the following instead.
            #if self.group is not None:
            #    self.group.menu_checked(self)

            # If we're turning this one on, then we need to turn all the others
            # off.  But if we're turning this one off, don't worry about the
            # others.
            if action.checked:
                for item in self.item.parent.items:
                    if item is not self.item:
                        item.action.checked = False

        # This will *not* emit a menu event because of this ugly flag
        self._skip_menu_event = True
#        self.control.Check(action.checked)
        self._skip_menu_event = False

        return


    def _on_action_name_changed(self, action, trait_name, old, new):
        """ Called when the name trait is changed on an action.
        """
        self.control.setText( action.name )
        return

    #### wx event handlers ####################################################

#    def _on_menu(self, event):
#        """ Called when the menu item is clicked. """
#
#        # if the ugly flag is set, do not perform the menu event
#        if self._skip_menu_event:
#            return
#
#        action = self.item.action
#        action_event = ActionEvent()
#
#        is_checkable = action.style in ['radio', 'toggle']
#
#        # Perform the action!
#        if self.controller is not None:
#            if is_checkable:
#                # fixme: There is a difference here between having a controller
#                # and not in that in this case we do not set the checked state
#                # of the action! This is confusing if you start off without a
#                # controller and then set one as the action now behaves
#                # differently!
#                self.checked = self.control.IsChecked() == 1
#
#            # Most of the time, action's do no care about the event (it
#            # contains information about the time the event occurred etc), so
#            # we only pass it if the perform method requires it. This is also
#            # useful as Traits UI controllers *never* require the event.
#            args, varargs, varkw, dflts = getargspec(self.controller.perform)
#
#            # If the only arguments are 'self' and 'action' then don't pass
#            # the event!
#            if len(args) == 2:
#                self.controller.perform(action)
#
#            else:
#                self.controller.perform(action, action_event)
#
#        else:
#            if is_checkable:
#                action.checked = self.control.IsChecked() == 1
#
#            # Most of the time, action's do no care about the event (it
#            # contains information about the time the event occurred etc), so
#            # we only pass it if the perform method requires it.
#            args, varargs, varkw, dflts = getargspec(action.perform)
#
#            # If the only argument is 'self' then don't pass the event!
#            if len(args) == 1:
#                action.perform()
#
#            else:
#                action.perform(action_event)
#
#        return

#### EOF ######################################################################
