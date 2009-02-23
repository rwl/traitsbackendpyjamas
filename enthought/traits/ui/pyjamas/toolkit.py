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

""" Defines the concrete implementations of the traits Toolkit interface for
    the Pyjamas user interface.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.ui.toolkit import Toolkit

from enthought.traits.ui.editor_factory import EditorFactory

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# Create a dummy singleton editor factory:
null_editor_factory = EditorFactory()

#------------------------------------------------------------------------------
#  "GUIToolkit" class:
#------------------------------------------------------------------------------

class GUIToolkit(Toolkit):
    """ Implementation class for Pyjamas toolkit.
    """

    def ui_live(self, ui, parent):
        """ Creates a non-modal "live update" user interface using information
            from the specified UI object.
        """
        import ui_live
        ui_live.ui_live(ui, parent)


#    def ui_nonmodal ( self, ui, parent ):
#        """ Creates a GUI-toolkit-specific non-modal dialog user interface
#            using information from the specified UI object.
#        """
#        import ui_modal
#        ui_modal.ui_nonmodal(ui, parent)


    def view_application(self, context, view, kind=None, handler=None,
            id="", scrollable=None, args=None):
        """ Creates a Pyjamas web application, using information from the
            specified View object.

        Parameters
        ----------
        context : object or dictionary
            A single object or a dictionary of string/object pairs, whose
            trait attributes are to be edited. If not specified, the current
            object is used.
        view : view or string
            A View object that defines a user interface for editing trait
            attribute values.
        kind : string
            The type of user interface window to create. See the
            **enthought.traits.ui.view.kind_trait** trait for values and
            their meanings. If *kind* is unspecified or None, the **kind**
            attribute of the View object is used.
        handler : Handler object
            A handler object used for event handling in the dialog box. If
            None, the default handler for Traits UI is used.
        id : string
            A unique ID for persisting preferences about this user interface,
            such as size and position. If not specified, no user preferences
            are saved.
        scrollable : Boolean
            Indicates whether the dialog box should be scrollable. When set to
            True, scroll bars appear on the dialog box if it is not large
            enough to display all of the items in the view at one time.
        """
        import view_application

        return view_application.view_application(
            context, view, kind, handler, id, scrollable, args)

    #--------------------------------------------------------------------------
    #  Positions the associated dialog window on the display:
    #--------------------------------------------------------------------------

    def position ( self, ui ):
        """ Positions the associated dialog window on the display.
        """
        view   = ui.view
        window = ui.control

        pass

    #---------------------------------------------------------------------------
    #  Shows a 'Help' window for a specified UI and control:
    #---------------------------------------------------------------------------

    def show_help ( self, ui, control ):
        """ Shows a help window for a specified UI and control.
        """
        import ui_panel
        ui_panel.show_help( ui, control )

    #--------------------------------------------------------------------------
    #  Hooks all specified events for all controls in a ui so that they can be
    #  routed to the correct event handler:
    #--------------------------------------------------------------------------

    def hook_events ( self, ui, control, events = None, handler = None,
                      drop_target = None ):
        """ Hooks all specified events for all controls in a UI so that they
            can be routed to the correct event handler.
        """
        if events is None:
            events = (
                "<Button-1>", "<Button-2>", "<Button-3>", "<ButtonRelease-1>",
                "<ButtonRelease-2>", "<ButtonRelease-3>", "<Double-Button-1>",
                "<Double-Button-2>", "<Double-Button-3>", "<B1-Motion>",
                "<B2-Motion>", "<B1-Motion>", "<Enter>", "<Leave>", "<Key>",
                "<Configure>"
            )
#            control.SetDropTarget( PythonDropTarget(
#                                   DragHandler( ui = ui, control = control ) ) )
        elif events == 'keys':
            events = ( "<Key>", )

        if handler is None:
            handler = ui.route_event

        for event in events:
            control.bind( event, handler )

        for id, child in control.children.iteritems():
            self.hook_events( ui, child, events, handler, drop_target )

    #--------------------------------------------------------------------------
    #  Destroys a specified GUI toolkit control:
    #--------------------------------------------------------------------------

    def destroy_control ( self, control ):
        """ Destroys a specified GUI toolkit control.
        """
        control.destroy()

    #--------------------------------------------------------------------------
    #  GUI toolkit dependent trait definitions:
    #--------------------------------------------------------------------------

    def color_trait ( self, *args, **traits ):
        import enthought.traits.ui.null.color_trait as ct
        return ct.NullColor( *args, **traits )


    def rgb_color_trait ( self, *args, **traits ):
        import enthought.traits.ui.null.rgb_color_trait as rgbct
        return rgbct.RGBColor( *args, **traits )


    def font_trait ( self, *args, **traits ):
        import enthought.traits.ui.null.font_trait as ft
        return ft.NullFont( *args, **traits )


    def kiva_font_trait ( self, *args, **traits ):
        import enthought.traits.ui.null.font_trait as ft
        return ft.NullFont( *args, **traits )


    def constants ( self, *args, **traits ):
        constants = {
            'WindowColor': ( 236 / 255.0, 233 / 255.0, 216 / 255.0, 1.0 )}
        return constants

    #---------------------------------------------------------------------------
    #  'Editor' class methods:
    #---------------------------------------------------------------------------

    # Generic UI-base editor:
    def ui_editor ( self ):
        import ui_editor
        return ui_editor.UIEditor

    #--------------------------------------------------------------------------
    #  'EditorFactory' factory methods:
    #--------------------------------------------------------------------------

    # Boolean:
    def boolean_editor ( self, *args, **traits ):
        import boolean_editor as be
        return be.ToolkitEditorFactory( *args, **traits )

    # Text:
    def text_editor ( self, *args, **traits ):
        import text_editor as te
        return te.ToolkitEditorFactory( *args, **traits )

# EOF -------------------------------------------------------------------------