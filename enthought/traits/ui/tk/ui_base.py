#------------------------------------------------------------------------------
#
#  Copyright (c) 2008, Richard W. Lincoln
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Author: Richard W. Lincoln
#  Date:   28/01/2008
#
#------------------------------------------------------------------------------

""" Defines a base class for the Tkinter modal and non-modal dialogs. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tkinter

from enthought.traits.api \
    import HasStrictTraits, HasPrivateTraits, Instance, List, Event

from enthought.traits.ui.api \
    import UI

from enthought.traits.ui.menu \
    import Action

from editor \
    import Editor

from tooltip import ToolTip

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# List of all predefined system button names:
SystemButtons = [ 'Undo', 'Redo', 'Apply', 'Revert', 'OK', 'Cancel', 'Help' ]

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

#------------------------------------------------------------------------------
#  'BaseDialog' class:
#------------------------------------------------------------------------------

class BaseDialog ( object ):
    """ Base class for Traits UI dialog boxes.
    """
    #--------------------------------------------------------------------------
    #  Sets the frame's icon:
    #--------------------------------------------------------------------------

    def set_icon ( self, icon = None ):
        """ Sets the frame's icon.
        """
        from enthought.pyface.image_resource import ImageResource

        if not isinstance( icon, ImageResource ):
            icon = ImageResource( 'frame.ico' )
        self.control.wm_iconbitmap( icon.absolute_path )

    #--------------------------------------------------------------------------
    #  Coerces a string to an Action if necessary:
    #--------------------------------------------------------------------------

    def coerce_button ( self, action ):
        """ Coerces a string to an Action if necessary.
        """
        if isinstance(action, basestring):
            return Action( name   = action,
                           action = '?'[ (not action in SystemButtons): ] )
        return action

    #---------------------------------------------------------------------------
    #  Check to see if a specified 'system' button is in the buttons list, and
    # add it if it is not:
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
    #  Creates a user specified button:
    #---------------------------------------------------------------------------

    def add_button ( self, action, sizer, method  = None,
                                          enabled = True,
                                          name    = None ):
        """ Creates a button.
        """
        ui = self.ui
        if ((action.defined_when != '') and
            (not ui.eval_when( action.defined_when ))):
            return None

        if name is None:
            name = action.name
        id     = action.id
#        button = Tkinter.Button( self.control, label = name )
        button = Tkinter.Button( sizer, label = name )

        if enabled:
            button.config( state = "NORMAL" )
        else:
            button.config( state = "DISABLED" )

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

        button.bind( "<Button-1>", method )
        button.pack()

        if action.tooltip != '':
            tip = ToolTip(button, text=action.tooltip)

        return button

# EOF -------------------------------------------------------------------------
