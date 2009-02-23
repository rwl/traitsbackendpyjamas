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
#  Date:   21/02/2009
#
#------------------------------------------------------------------------------

""" Creates a non-modal user interface for a specified UI object, where the
    UI is "live", meaning that it immediately updates its underlying object(s).
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from pyjamas import Window
from pyjamas.ui import PopupPanel

from ui_base import \
    BaseDialog

from ui_panel \
    import panel

from enthought.traits.ui.undo \
    import UndoHistory

from enthought.traits.ui.menu \
    import UndoButton, RevertButton, OKButton, CancelButton, HelpButton

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# Window title to use if not specified in the view:
DefaultTitle = "Edit properties"

# Types of supported windows:
NONMODAL = 0
MODAL    = 1
POPUP    = 2
POPOVER  = 3
INFO     = 4

# Types of 'popup' dialogs:
Popups = set( ( POPUP, POPOVER, INFO ) )

#------------------------------------------------------------------------------
#  Creates a 'live update' user interface for a specified UI object:
#------------------------------------------------------------------------------

def ui_live(ui, parent):
    """ Creates a live, non-modal Pyjamas web interface for a specified UI
        object.
    """
    _ui_dialog( ui, parent, NONMODAL )


def _ui_dialog ( ui, parent, style ):
    """ Creates a live Pyjamas user interface for a specified UI object.
    """
    if ui.owner is None:
        ui.owner = LiveWindow()

    ui.owner.init( ui, parent, style )
    ui.control = ui.owner.control
#    ui.control._parent = parent
    ui.control.transient(parent) # Associate this window with a parent window.

    try:
        ui.prepare_ui()
    except:
        ui.control.destroy()
        ui.control.ui = None
        ui.control    = None
        ui.owner      = None
        ui.result     = False
        raise

    ui.handler.position( ui.info )
    # TODO: Restore the user preference items for a specified UI.
#    restore_window( ui, is_popup = (style in Popups) )

    if style == MODAL:
        ui.control.grab_set()
        ui.control.focus_set()
        parent.wait_window(ui.control)
    else:
        ui.control.mainloop()


class LiveWindow(BaseDialog):
    """ User interface window that immediately updates its underlying
        object(s).
    """

    #--------------------------------------------------------------------------
    #  Initializes the object:
    #--------------------------------------------------------------------------

    def init(self, ui, parent, style):
        """ Initialises the dialog. """

        self.is_modal = (style == MODAL)
        window_style = 0
        view = ui.view
#        if view.resizable:
#            window_style |= (True, True)

        title = view.title
        if title == '':
            title = DefaultTitle

        history = ui.history
        window = ui.control
        if window is not None:
            if history is not None:
                history.on_trait_change( self._on_undoable, 'undoable',
                                         remove = True )
                history.on_trait_change( self._on_redoable, 'redoable',
                                         remove = True )
                history.on_trait_change( self._on_revertable, 'undoable',
                                         remove = True )
#            window.SetSizer( None )
            ui.reset()
        else:
            self.ui = ui
            if style == MODAL:
                window = Window
                window.setTitle( title )
                if view.resizable:
                    pass
            elif style == NONMODAL:
                window = Window
                window.setTitle( title )
                if parent is not None:
                    pass
            else:
                window = PopupPanel
#                window.bind("<Leave>", self._on_close_popup )
                window.addWindowCloseListener( self._on_close_popup )
                window._kind  = ui.view.kind
#                self._monitor = MouseMonitor( ui )

            # TODO: Set the correct default window background color.

            self.control = window
#            window.protocol( "WM_DELETE_WINDOW", self._on_close_page )
#            window.bind( "<Key>", self._on_key )

#        self.set_icon( view.icon )

        # Buttons -------------------------------------------------------------

        buttons  = [self.coerce_button( button ) for button in view.buttons]
        nbuttons = len( buttons )

        no_buttons  = ((nbuttons == 1) and self.is_button( buttons[0], '' ))
        has_buttons = ((not no_buttons) and ((nbuttons > 0) or view.undo or
                                        view.revert or view.ok or view.cancel))

        if has_buttons or (view.menubar is not None):
            if history is None:
                history = UndoHistory()
        else:
            history = None
        ui.history = history

        #----------------------------------------------------------------------
        #  Create the actual trait frame filled with widgets:
        #----------------------------------------------------------------------

        if ui.scrollable:
            sw = panel( ui, window )
        else:
            sw = panel( ui, window )

        #----------------------------------------------------------------------
        #  Add special function buttons (OK, Cancel, etc) as necessary:
        #----------------------------------------------------------------------

        if (not no_buttons) and (has_buttons or view.help):

            b_frame = Panel()

            # Convert all button flags to actual button actions if no buttons
            # were specified in the 'buttons' trait:
            if nbuttons == 0:
                if view.undo:
                    self.check_button( buttons, UndoButton )
                if view.revert:
                    self.check_button( buttons, RevertButton )
                if view.ok:
                    self.check_button( buttons, OKButton )
                if view.cancel:
                    self.check_button( buttons, CancelButton )
                if view.help:
                    self.check_button( buttons, HelpButton )

            # Create a button for each button action.
            for button in buttons:
                button = self.coerce_button( button )
                # Undo button:
                if self.is_button( button, 'Undo' ):
                    self.undo = self.add_button( button, b_frame,
                                                 self._on_undo, False )

                    self.redo = self.add_button( button, b_frame,
                                                 self._on_redo, False, 'Redo' )

                    history.on_trait_change( self._on_undoable, 'undoable',
                                             dispatch = 'ui' )

                    history.on_trait_change( self._on_redoable, 'redoable',
                                             dispatch = 'ui' )

                    if history.can_undo:
                        self._on_undoable( True )

                    if history.can_redo:
                        self._on_redoable( True )

                # Revert button.
                elif self.is_button( button, 'Revert' ):
                    self.revert = self.add_button( button, b_frame,
                                                   self._on_revert, False )
                    history.on_trait_change( self._on_revertable, 'undoable',
                                             dispatch = 'ui' )
                    if history.can_undo:
                        self._on_revertable( True )

                # OK button.
                elif self.is_button( button, 'OK' ):
                    self.ok = self.add_button( button, b_frame, self._on_ok )
                    ui.on_trait_change( self._on_error, 'errors',
                                        dispatch = 'ui' )

                # Cancel button.
                elif self.is_button( button, 'Cancel' ):
                    self.add_button( button, b_frame, self._on_cancel )

                # Help button.
                elif self.is_button( button, 'Help' ):
                    self.add_button( button, b_frame, self._on_help )

                elif not self.is_button( button, '' ):
                    self.add_button( button, b_frame )

            RootPanel.add( b_frame )

        # Add the menu bar, tool bar and status bar (if any):
        self.add_menubar()
#        self.add_toolbar()
#        self.add_statusbar()

    #--------------------------------------------------------------------------
    #  Closes the dialog window:
    #--------------------------------------------------------------------------

    def close ( self, rc = None ):
        """ Closes the dialog window.
        """
        ui = self.ui
        ui.result = (rc == OK)
        # TODO: Save the user preference items for a specified UI.
#        save_window( ui )

        self.control.destroy()

        ui.finish()
        self.ui = self.undo = self.redo = self.revert = self.control = None

    #--------------------------------------------------------------------------
    #  Handles the user clicking the window/dialog 'close' button/icon:
    #--------------------------------------------------------------------------

    def _on_close_page ( self, event ):
        """ Handles the user clicking the window/dialog "close" button/icon.
        """
        if self.ui.view.close_result == False:
            self._on_cancel( event )
        else:
            self._on_ok( event )

    #--------------------------------------------------------------------------
    #  Handles the user giving focus to another window for a 'popup' view:
    #--------------------------------------------------------------------------

    def _on_close_popup ( self, event ):
        """ Handles the user giving focus to another window for a 'popup' view.
        """
#        if not event.GetActive():
        self.close_popup()


    def close_popup ( self ):
        # Close the window if it has not already been closed:
        if self.ui.info.ui is not None:
            if self._on_ok():
#                self._monitor.Stop()
                self.ui.control.destroy()

    #--------------------------------------------------------------------------
    #  Handles the user clicking the 'OK' button:
    #--------------------------------------------------------------------------

    def _on_ok ( self, event = None ):
        """ Handles the user clicking the **OK** button.
        """
        if self.ui.handler.close( self.ui.info, True ):
            self.control.bind( "<Button-1>", None )
            self.close( OK )
            return True

        return False

    #--------------------------------------------------------------------------
    #  Handles the user hitting the 'Esc'ape key:
    #--------------------------------------------------------------------------

    def _on_key ( self, event ):
        """ Handles the user pressing the Escape key.
        """
        if event.keycode() == 0x1B:
           self._on_close_page( event )

    #---------------------------------------------------------------------------
    #  Handles an 'Undo' change request:
    #---------------------------------------------------------------------------

    def _on_undo ( self, event ):
        """ Handles an "Undo" change request.
        """
        self.ui.history.undo()

    #---------------------------------------------------------------------------
    #  Handles a 'Redo' change request:
    #---------------------------------------------------------------------------

    def _on_redo ( self, event ):
        """ Handles a "Redo" change request.
        """
        self.ui.history.redo()

    #---------------------------------------------------------------------------
    #  Handles a 'Revert' all changes request:
    #---------------------------------------------------------------------------

    def _on_revert ( self, event ):
        """ Handles a request to revert all changes.
        """
        ui = self.ui
        if ui.history is not None:
            ui.history.revert()
        ui.handler.revert( ui.info )

    #---------------------------------------------------------------------------
    #  Handles a 'Cancel' all changes request:
    #---------------------------------------------------------------------------

    def _on_cancel ( self, event ):
        """ Handles a request to cancel all changes.
        """
        if self.ui.handler.close( self.ui.info, False ):
            self._on_revert( event )
            self.close( CANCEL )

    #---------------------------------------------------------------------------
    #  Handles editing errors:
    #---------------------------------------------------------------------------

    def _on_error ( self, errors ):
        """ Handles editing errors.
        """
#        if errors == 0:
#            self.ok.config( state = Tkinter.NORMAL )
#        else:
#            self.ok.config( state = Tkinter.DISABLED )

    #---------------------------------------------------------------------------
    #  Handles the 'Help' button being clicked:
    #---------------------------------------------------------------------------

    def _on_help ( self, event ):
        """ Handles the 'user clicking the Help button.
        """
        self.ui.handler.show_help( self.ui.info, event.widget )

    #---------------------------------------------------------------------------
    #  Handles the undo history 'undoable' state changing:
    #---------------------------------------------------------------------------

    def _on_undoable ( self, state ):
        """ Handles a change to the "undoable" state of the undo history
        """
#        if state:
#            self.undo.config( state = Tkinter.NORMAL )
#        else:
#            self.undo.config( state = Tkinter.DISABLED )

    #---------------------------------------------------------------------------
    #  Handles the undo history 'redoable' state changing:
    #---------------------------------------------------------------------------

    def _on_redoable ( self, state ):
        """ Handles a change to the "redoable state of the undo history.
        """
#        if state:
#            self.undo.config( state = Tkinter.NORMAL )
#        else:
#            self.undo.config( state = Tkinter.DISABLED )

    #---------------------------------------------------------------------------
    #  Handles the 'revert' state changing:
    #---------------------------------------------------------------------------

    def _on_revertable ( self, state ):
        """ Handles a change to the "revert" state.
        """
#        if state:
#            self.undo.config( state = Tkinter.NORMAL )
#        else:
#            self.undo.config( state = Tkinter.DISABLED )

# EOF -------------------------------------------------------------------------
