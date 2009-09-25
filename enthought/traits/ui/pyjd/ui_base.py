#------------------------------------------------------------------------------
#  Copyright (c) 2005, Enthought, Inc.
#  Copyright (c) 2009, Richard Lincoln
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#------------------------------------------------------------------------------

""" Defines a base class for the Pyjamas modal and non-modal dialogs.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import pyjd

from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.DialogBox import DialogBox
from pyjamas.ui.Label import Label
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.VerticalPanel import VerticalPanel

#from Tooltip import TooltipListener

from enthought.traits.api \
    import HasStrictTraits, HasPrivateTraits, Instance, List, Event

from enthought.traits.ui.api \
    import UI

from enthought.traits.ui.menu \
    import Action

from editor \
    import Editor

from constants \
    import DefaultTitle

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# List of all predefined system button names:
SystemButtons = ['Undo', 'Redo', 'Apply', 'Revert', 'OK', 'Cancel', 'Help']

#-------------------------------------------------------------------------------
#  'ButtonEditor' class:
#-------------------------------------------------------------------------------

class ButtonEditor ( Editor ):
    """ Editor for buttons.
    """
    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # Action associated with the button
    action = Instance( Action )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        self.set( **traits )

    #---------------------------------------------------------------------------
    #  Handles the associated button being clicked:
    #---------------------------------------------------------------------------

    def perform ( self, event ):
        """ Handles the associated button being clicked.
        """
        self.ui.do_undoable( self._perform, event )


    def _perform ( self, event ):
        method_name = self.action.action
        if method_name == '':
            method_name = '_%s_clicked' % (self.action.name.lower())
        method = getattr( self.ui.handler, method_name, None )
        if method is not None:
            method( self.ui.info )
        else:
            self.action.perform( event )

#-------------------------------------------------------------------------------
#  'BasePanel' class:
#-------------------------------------------------------------------------------

class BasePanel(object):
    """ Base class for Traits UI panels.
    """

    #---------------------------------------------------------------------------
    #  Performs the action described by a specified Action object:
    #---------------------------------------------------------------------------

    def perform ( self, action ):
        """ Performs the action described by a specified Action object.
        """
        self.ui.do_undoable( self._perform, action )


    def _perform ( self, action ):
        method = getattr( self.ui.handler, action.action, None )
        if method is not None:
            method( self.ui.info )
        else:
            action.perform()

    #---------------------------------------------------------------------------
    #  Check to see if a specified 'system' button is in the buttons list, and
    #  add it if it is not:
    #---------------------------------------------------------------------------

    def check_button ( self, buttons, action ):
        """ Adds *action* to the system buttons list for this dialog, if it is
            not already in the list.
        """
        name = action.name
        for button in buttons:
            if self.is_button( button, name ):
                return
        buttons.append( action )

    #---------------------------------------------------------------------------
    #  Check to see if a specified Action button is a 'system' button:
    #---------------------------------------------------------------------------

    def is_button ( self, action, name ):
        """ Returns whether a specified action button is a system button.
        """
        if isinstance(action, basestring):
            return (action == name)
        return (action.name == name)

    #---------------------------------------------------------------------------
    #  Coerces a string to an Action if necessary:
    #---------------------------------------------------------------------------

    def coerce_button ( self, action ):
        """ Coerces a string to an Action if necessary.
        """
        if isinstance(action, basestring):
            return Action( name   = action,
                           action = '?'[ (not action in SystemButtons): ] )
        return action

    #---------------------------------------------------------------------------
    #  Creates a user specified button:
    #---------------------------------------------------------------------------

    def add_button ( self, action, bbox, method=None, enabled=True,
                     name=None ):
        """ Creates a button.
        """
        ui = self.ui
        if ((action.defined_when != '') and
            (not ui.eval_when( action.defined_when ))):
            return None

        if name is None:
            name = action.name
        id     = action.id
        button = Button(name)
        bbox.add(button)
#        button.setAutoDefault(False)
        button.setEnabled(enabled)
        if (method is None) or (action.enabled_when != '') or (id != ''):
            editor = ButtonEditor( ui      = ui,
                                   action  = action,
                                   control = button )
            if id != '':
                ui.info.bind( id, editor )
            if action.visible_when != '':
                ui.add_visible( action.visible_when, editor )
            if action.enabled_when != '':
                ui.add_enabled( action.enabled_when, editor )
            if method is None:
                method = editor.perform

        if method is not None:
            button.addClickListener(method)

        if action.tooltip != '':
#            button.setToolTip(action.tooltip)
            print "Tooltips for buttons are not implemeted,"

        return button


    def _on_help(self):
        """Handles the user clicking the Help button.
        """
        # FIXME: Needs porting to Pyjamas.
#        self.ui.handler.show_help(self.ui.info, event.GetEventObject())


    def _on_undo(self):
        """Handles a request to undo a change.
        """
        self.ui.history.undo()


    def _on_undoable(self, state):
        """Handles a change to the "undoable" state of the undo history
        """
        self.undo.setEnabled(state)


    def _on_redo(self):
        """Handles a request to redo a change.
        """
        self.ui.history.redo()


    def _on_redoable(self, state):
        """Handles a change to the "redoable" state of the undo history.
        """
        self.redo.setEnabled(state)


    def _on_revert(self):
        """Handles a request to revert all changes.
        """
        ui = self.ui
        if ui.history is not None:
            ui.history.revert()
        ui.handler.revert(ui.info)


    def _on_revertable(self, state):
        """ Handles a change to the "revert" state.
        """
        self.revert.setEnabled(state)

#------------------------------------------------------------------------------
#  'BaseDialog' class:
#------------------------------------------------------------------------------

class BaseDialog(BasePanel):
    """ Base class for Traits UI dialog boxes.
    """

    # The different dialog styles.
    NONMODAL, MODAL, POPUP = range(3)

    def init(self, ui, parent, style):
        """ Initialise the dialog by creating the controls.
        """
        raise NotImplementedError


    def create_dialog(self, parent, style):
        """ Create the dialog control.
        """
        self.control = control = DialogBox(modal=(style == BaseDialog.MODAL))

        master = self.master = VerticalPanel()

        control.setWidget(master)

        view = self.ui.view

#        control.setTitle(view.title or DefaultTitle)

#        QtCore.QObject.connect(control, QtCore.SIGNAL('finished(int)'),
#                self._on_finished)


    def add_contents(self, panel, buttons):
        """Add a panel (either a widget, layout or None) and optional buttons
        to the dialog."""

        if panel is not None:
#            self.control.setWidget(panel)
            self.master.add(panel)

        # Add the optional buttons.
        if buttons is not None:
            self.master.add(buttons)

        # Add the menu bar, tool bar and status bar (if any).
        self._add_menubar()
        self._add_toolbar()
        self._add_statusbar()


    def close(self, rc=True):
        """Close the dialog and set the given return code."""

        self.ui.dispose(rc)
        self.ui = self.control = None


    @staticmethod
    def display_ui(ui, parent, style):
        """Display the UI."""

        ui.owner.init(ui, parent, style)
        ui.control = ui.owner.control
        ui.control._parent = parent

        try:
            ui.prepare_ui()
        except:
            ui.control.setParent(None)
            ui.control.ui = None
            ui.control = None
            ui.owner = None
            ui.result = False
            raise

        ui.handler.position(ui.info)
#        restore_window(ui)

        RootPanel().add(ui.control)
        pyjd.run()

        if style == BaseDialog.NONMODAL:
            ui.control.show()
        else:
#            ui.control.setWindowModality(QtCore.Qt.WindowModal)
            ui.control.exec_()

        RootPanel().add(ui.control)
        pyjd.run()


    def set_icon(self, icon=None):
        """Sets the dialog's icon."""

        from enthought.pyface.image_resource import ImageResource

        if not isinstance(icon, ImageResource):
            icon = ImageResource('frame')

#        self.control.setWindowIcon(icon.create_icon())
        print "Seting dialog icon is not implemented."


    def _on_error(self, errors):
        """Handles editing errors."""

        self.ok.setEnabled(errors == 0)

    #---------------------------------------------------------------------------
    #  Adds a menu bar to the dialog:
    #---------------------------------------------------------------------------

    def _add_menubar(self):
        """Adds a menu bar to the dialog.
        """
        menubar = self.ui.view.menubar
        if menubar is not None:
            self._last_group = self._last_parent = None
#            self.control.layout().setMenuBar(
#                menubar.create_menu_bar( self.control, self ) )
            self.master.add( menubar.create_menu_bar( self.control, self ) )
            self._last_group = self._last_parent = None

    #---------------------------------------------------------------------------
    #  Adds a tool bar to the dialog:
    #---------------------------------------------------------------------------

    def _add_toolbar ( self ):
        """ Adds a toolbar to the dialog.
        """
        toolbar = self.ui.view.toolbar
        if toolbar is not None:
            self._last_group = self._last_parent = None
            toolbar_panel = toolbar.create_tool_bar( self.control, self )
#            qt_toolbar.setMovable( False )
            self.master.add( toolbar_panel )
            self._last_group = self._last_parent = None

    #---------------------------------------------------------------------------
    #  Adds a status bar to the dialog:
    #---------------------------------------------------------------------------

    def _add_statusbar ( self ):
        """ Adds a statusbar to the dialog.
        """
        if self.ui.view.statusbar is not None:
            control = HorizontalPanel()
#            control.setSizeGripEnabled(self.ui.view.resizable)
            listeners = []
            for item in self.ui.view.statusbar:
                # Create the status widget with initial text
                name = item.name
                item_control = Label()
                item_control.setText(self.ui.get_extended_value(name))

                # Add the widget to the control with correct size
#                width = abs(item.width)
#                stretch = 0
#                if width <= 1.0:
#                    stretch = int(100 * width)
#                else:
#                    item_control.setMinimumWidth(width)
                control.add(item_control)

                # Set up event listener for updating the status text
                col = name.find('.')
                obj = 'object'
                if col >= 0:
                    obj = name[:col]
                    name = name[col+1:]
                obj = self.ui.context[obj]
                set_text = self._set_status_text(item_control)
                obj.on_trait_change(set_text, name, dispatch='ui')
                listeners.append((obj, set_text, name))

            self.master.add(control)
            self.ui._statusbar = listeners


    def _set_status_text(self, control):
        """ Helper function for _add_statusbar.
        """
        def set_status_text(text):
            control.setText(text)

        return set_status_text

    #---------------------------------------------------------------------------
    #  Adds a menu item to the menu bar being constructed:
    #---------------------------------------------------------------------------

    def add_to_menu ( self, menu_item ):
        """ Adds a menu item to the menu bar being constructed.
        """
        item   = menu_item.item
        action = item.action

        if action.id != '':
            self.ui.info.bind( action.id, menu_item )

        if action.style == 'radio':
#            if ((self._last_group is None) or
#                (self._last_parent is not item.parent)):
#                self._last_group = RadioGroup()
#                self._last_parent = item.parent
#            self._last_group.items.append( menu_item )
#            menu_item.group = self._last_group
            print "Radio menu buttons not implemented."

#        if action.enabled_when != '':
#            self.ui.add_enabled( action.enabled_when, menu_item )

#        if action.checked_when != '':
#            self.ui.add_checked( action.checked_when, menu_item )

    #---------------------------------------------------------------------------
    #  Adds a tool bar item to the tool bar being constructed:
    #---------------------------------------------------------------------------

    def add_to_toolbar ( self, toolbar_item ):
        """ Adds a toolbar item to the toolbar being constructed.
        """
        self.add_to_menu( toolbar_item )


    def can_add_to_menu(self, action, action_event=None):
        """Returns whether the action should be defined in the user interface.
        """
        if action.defined_when == '':
            return True

        return self.ui.eval_when(action.defined_when)


    def can_add_to_toolbar(self, action):
        """Returns whether the toolbar action should be defined in the user
           interface.
        """
        return self.can_add_to_menu(action)


#class BaseDialog ( object ):
#    """ Base class for Traits UI dialog boxes.
#    """
#
#    #--------------------------------------------------------------------------
#    #  Adds a menu bar to the dialog:
#    #--------------------------------------------------------------------------
#
#    def add_menubar ( self ):
#        """ Adds a menu bar to the dialog.
#        """
#        menubar = self.ui.view.menubar
#        if menubar is not None:
#            self._last_group = self._last_parent = None
#            menu = menubar.create_menu_bar( self.control, self )
#
#            RootPanel().add( menu )
#
#            self._last_group = self._last_parent = None
#
#    #---------------------------------------------------------------------------
#    #  Adds a menu item to the menu bar being constructed:
#    #---------------------------------------------------------------------------
#
#    def add_to_menu ( self, menu_item ):
#        """ Adds a menu item to the menu bar being constructed.
#        """
#        item   = menu_item.item
#        action = item.action
#
#        if action.id != '':
#            self.ui.info.bind( action.id, menu_item )
#
##        if action.style == 'radio':
##            if ((self._last_group is None) or
##                (self._last_parent is not item.parent)):
##
##                self._last_group = RadioGroup()
##                self._last_parent = item.parent
##
##            self._last_group.items.append( menu_item )
##            menu_item.group = self._last_group
#
#        if action.enabled_when != '':
#            self.ui.add_enabled( action.enabled_when, menu_item )
#
#        if action.checked_when != '':
#            self.ui.add_checked( action.checked_when, menu_item )
#
#    #--------------------------------------------------------------------------
#    #  Returns whether the menu action should be defined in the user interface:
#    #--------------------------------------------------------------------------
#
#    def can_add_to_menu ( self, action, action_event = None ):
#        """ Returns whether the action should be defined in the user interface.
#        """
#        if action.defined_when == '':
#            return True
#
#        return self.ui.eval_when( action.defined_when )
#
#    #---------------------------------------------------------------------------
#    #  Performs the action described by a specified Action object:
#    #---------------------------------------------------------------------------
#
#    def perform ( self, action ):
#        """ Performs the action described by a specified Action object.
#        """
#        self.ui.do_undoable( self._perform, action )
#
#    def _perform ( self, action ):
#        method = getattr( self.ui.handler, action.action, None )
#        if method is not None:
#            method( self.ui.info )
#        else:
#            context = self.ui.context
#            for item in PerformHandlers:
#                handler = context.get( item, None )
#                if handler is not None:
#                    method = getattr( handler, action.action, None )
#                    if method is not None:
#                        method()
#                        break
#            else:
#                action.perform()
#
#    #--------------------------------------------------------------------------
#    #  Sets the frame's icon:
#    #--------------------------------------------------------------------------
#
#    def set_icon ( self, icon = None ):
#        """ Sets the frame's icon.
#        """
#        pass
#
#    #--------------------------------------------------------------------------
#    #  Coerces a string to an Action if necessary:
#    #--------------------------------------------------------------------------
#
#    def coerce_button ( self, action ):
#        """ Coerces a string to an Action if necessary.
#        """
#        if isinstance(action, basestring):
#            return Action( name   = action,
#                           action = '?'[ (not action in SystemButtons): ] )
#        return action
#
#    #---------------------------------------------------------------------------
#    #  Check to see if a specified 'system' button is in the buttons list, and
#    # add it if it is not:
#    #---------------------------------------------------------------------------
#
#    def check_button ( self, buttons, action ):
#        """ Adds *action* to the system buttons list for this dialog, if it is
#        not already in the list.
#        """
#        name = action.name
#        for button in buttons:
#            if self.is_button( button, name ):
#                return
#        buttons.append( action )
#
#    #---------------------------------------------------------------------------
#    #  Check to see if a specified Action button is a 'system' button:
#    #---------------------------------------------------------------------------
#
#    def is_button ( self, action, name ):
#        """ Returns whether a specified action button is a system button.
#        """
#        if isinstance(action, basestring):
#            return (action == name)
#        return (action.name == name)
#
#    #---------------------------------------------------------------------------
#    #  Creates a user specified button:
#    #---------------------------------------------------------------------------
#
#    def add_button ( self, action, sizer, method  = None,
#                                          enabled = True,
#                                          name    = None ):
#        """ Creates a button.
#        """
#        ui = self.ui
#        if ((action.defined_when != '') and
#            (not ui.eval_when( action.defined_when ))):
#            return None
#
#        if name is None:
#            name = action.name
#        id     = action.id
#        button = Button( name )#, editor.perform )
#
#        print "Adding button:", name, self.control
#
#        button.setEnabled(enabled)
#
#        if (method is None) or (action.enabled_when != '') or (id != ''):
#            editor = ButtonEditor( ui      = ui,
#                                   action  = action,
#                                   control = button )
#            if id != '':
#                ui.info.bind( id, editor )
#            if action.visible_when != '':
#                ui.add_visible( action.visible_when, editor )
#            if action.enabled_when != '':
#                ui.add_enabled( action.enabled_when, editor )
#            if method is None:
#                method = editor.perform
#
#        self.control.add(button)
#
##        if action.tooltip != '':
##            listener = TooltipListener(action.tooltip)
##            button.addMouseListener(listener)
#
#        return button

# EOF -------------------------------------------------------------------------
