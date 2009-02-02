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
#  Date:   30/01/2009
#
#------------------------------------------------------------------------------

""" Defines the file editors for the Tk user interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tix \
    as tix

from string \
    import capitalize

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.file_editor file.
from enthought.traits.ui.editors.file_editor \
    import ToolkitEditorFactory

from editor \
    import Editor

from constants \
    import OKColor

from helper \
    import TkDelegate

#------------------------------------------------------------------------------
#  'BaseEditor' class:
#------------------------------------------------------------------------------

class BaseEditor ( Editor ):
    """ Base class for enumeration editors.
    """

    #--------------------------------------------------------------------------
    #  Trait definitions:
    #--------------------------------------------------------------------------

    # Current set of enumeration names:
    names = Property

    # Current mapping from names to values:
    mapping = Property

    # Current inverse mapping from values to names:
    inverse_mapping = Property

    #---------------------------------------------------------------------------
    #  Finishes initialising the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        factory = self.factory
        if factory.name != '':
            self._object, self._name, self._value = \
                self.parse_extended_name( factory.name )
            self.values_changed()
            self._object.on_trait_change( self._values_changed,
                                          ' ' + self._name, dispatch = 'ui' )
        else:
            factory.on_trait_change( self.rebuild_editor, 'values_modified',
                                     dispatch = 'ui' )

    #---------------------------------------------------------------------------
    #  Gets the current set of enumeration names:
    #---------------------------------------------------------------------------

    def _get_names ( self ):
        """ Gets the current set of enumeration names.
        """
        if self._object is None:
            return self.factory._names

        return self._names

    #---------------------------------------------------------------------------
    #  Gets the current mapping:
    #---------------------------------------------------------------------------

    def _get_mapping ( self ):
        """ Gets the current mapping.
        """
        if self._object is None:
            return self.factory._mapping

        return self._mapping

    #---------------------------------------------------------------------------
    #  Gets the current inverse mapping:
    #---------------------------------------------------------------------------

    def _get_inverse_mapping ( self ):
        """ Gets the current inverse mapping.
        """
        if self._object is None:
            return self.factory._inverse_mapping

        return self._inverse_mapping

    #---------------------------------------------------------------------------
    #  Rebuilds the contents of the editor whenever the original factory
    #  object's 'values' trait changes:
    #---------------------------------------------------------------------------

    def rebuild_editor ( self ):
        """ Rebuilds the contents of the editor whenever the original factory
            object's **values** trait changes.
        """
        raise NotImplementedError

    #---------------------------------------------------------------------------
    #  Recomputes the cached data based on the underlying enumeration model:
    #---------------------------------------------------------------------------

    def values_changed ( self ):
        """ Recomputes the cached data based on the underlying enumeration model.
        """
        self._names, self._mapping, self._inverse_mapping = \
            enum_values_changed( self._value() )

    #---------------------------------------------------------------------------
    #  Handles the underlying object model's enumeration set being changed:
    #---------------------------------------------------------------------------

    def _values_changed ( self ):
        """ Handles the underlying object model's enumeration set being changed.
        """
        self.values_changed()
        self.rebuild_editor()

    #---------------------------------------------------------------------------
    #  Disposes of the contents of an editor:
    #---------------------------------------------------------------------------

    def dispose ( self ):
        """ Disposes of the contents of an editor.
        """
        if self._object is not None:
            self._object.on_trait_change( self._values_changed,
                                          ' ' + self._name, remove = True )
        else:
            self.factory.on_trait_change( self.rebuild_editor,
                                          'values_modified', remove = True )

        super( BaseEditor, self ).dispose()

#-------------------------------------------------------------------------------
#  'SimpleEditor' class:
#-------------------------------------------------------------------------------

class SimpleEditor ( BaseEditor ):
    """ Simple style of enumeration editor, which displays a combo box.
    """

    #---------------------------------------------------------------------------
    #  Finishes initialising the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initialising the editor by creating the underlying toolkit
            widget.
        """
        super( SimpleEditor, self ).init( parent )

        factory       = self.factory
        var           = tix.StringVar()
        update_object = TkDelegate( self.update_object, var = var )

        opts = "label.width %d label.anchor %s" % (10, Tix.E)
        control = tix.ComboBox( parent,
                                label    = "",
                                dropdown = 1,
                                command  = update_object,
                                variable = var,
                                options  = opts)

        for name in self.names:
            self.control.insert(tix.END, name)

        if factory.evaluate is None:
            control.config( editable = 0 )
        else:
            control.config( editable = 1 )
            control.bind( "<Return>", self.update_text_object )
            control.bind( "<FocusOut>", self.on_kill_focus )
            if (not factory.is_grid_cell) and factory.auto_set:
                control.bind( "<Key>", self.update_text_object )

        self.control         = control
        self._no_enum_update = 0
        self.set_tooltip()


    def dispose ( self ):
        """ Disposes of the contents of an editor.
        """
        control = self.control
        control.config( command = None )
        control.unbind( "<Return>" )
        control.unbind( "<FocusOut>" )
        control.unbind( "<Key>" )

        super( SimpleEditor, self ).dispose()

    #---------------------------------------------------------------------------
    #  Handles the user selecting a new value from the combo box:
    #---------------------------------------------------------------------------

    def update_object ( self, delegate ):
        """ Handles the user selecting a new value from the combo box.
        """
        self._no_enum_update += 1
        try:
            self.value = self.mapping[ delegate.var.get() ]
        except:
            pass
        self._no_enum_update -= 1

    #---------------------------------------------------------------------------
    #  Handles the user typing text into the combo box text entry field:
    #---------------------------------------------------------------------------

    def update_text_object ( self, delegate ):
        """ Handles the user typing text into the combo box text entry field.
        """
        if self._no_enum_update == 0:
            value = delegate.var.get()
            try:
                value = self.mapping[ value ]
            except:
                try:
                    value = self.factory.evaluate( value )
                except Exception, excp:
                    self.error( excp )
                    return

            self._no_enum_update += 1
            try:
                self.value = value
                self.control.config( bg = OKColor )
#                self.control.Refresh()
            except:
                pass
            self._no_enum_update -= 1

    #---------------------------------------------------------------------------
    #  Handles the control losing the keyboard focus:
    #---------------------------------------------------------------------------

    def on_kill_focus ( self, event ):
        """ Handles the control losing the keyboard focus.
        """
        self.update_text_object( event )
#        event.Skip()
        return "break"

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        var = self.control.cget( 'variable' )
        if self._no_enum_update == 0:
            var = self.control.cget( 'variable' )
            var.set( self.str_value )

    #---------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #---------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait value.
        """
        self.control.config( bg = ErrorColor )
#        self.control.Refresh()

    #---------------------------------------------------------------------------
    #  Rebuilds the contents of the editor whenever the original factory
    #  object's 'values' trait changes:
    #---------------------------------------------------------------------------

    def rebuild_editor ( self ):
        """ Rebuilds the contents of the editor whenever the original factory
            object's **values** trait changes.
        """
        lb = self.control.subwidget("listbox")
        lb.delete(0, tix.END) # delete all items
        for name in self.names:
            self.control.insert(tix.END, name)

        self.update_editor()

#-------------------------------------------------------------------------------
#  'RadioEditor' class:
#-------------------------------------------------------------------------------

class RadioEditor ( BaseEditor ):
    """ Enumeration editor, used for the "custom" style, that displays radio
        buttons.
    """
    #---------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        super( RadioEditor, self ).init( parent )

        # Create a panel to hold all of the radio buttons:
        control = tix.Frame(parent)
        control.pack()

        self.control = control
        self.rebuild_editor()

    #---------------------------------------------------------------------------
    #  Handles the user clicking one of the 'custom' radio buttons:
    #---------------------------------------------------------------------------

    def update_object( self, event ):
        """ Handles the user clicking one of the custom radio buttons.
        """
        try:
            var = event.cget( "variable" )
            self.value = var.get()
        except:
            pass

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        value = self.value
        if self.control.children:
            rb0 = self.control.children.values[0]
            var = rb0.cget( "variable" )
            var.set( value )

    #---------------------------------------------------------------------------
    #  Rebuilds the contents of the editor whenever the original factory
    #  object's 'values' trait changes:
    #---------------------------------------------------------------------------

    def rebuild_editor ( self ):
        """ Rebuilds the contents of the editor whenever the original factory
            object's **values** trait changes.
        """
        # Clear any existing content:
        for rb in self.control.values():
            rb.destroy()

        # Get the current trait value:
        cur_name = self.str_value

        var = tix.StringVar()
        update_object = TkDelegate( self.update_object, var = var )

        # Create a sizer to manage the radio buttons:
        names   = self.names
        mapping = self.mapping
        n       = len( names )
        cols    = self.factory.cols
        rows    = (n + cols - 1) / cols
        incr    = [ n / cols ] * cols
        rem     = n % cols
        for i in range( cols ):
            incr[i] += (rem > i)
        incr[-1] = -(reduce( lambda x, y: x + y, incr[:-1], 0 ) - 1)

        # Add the set of all possible choices:
        index = 0

        for i in range( rows ):
            for j in range( cols ):
                if n > 0:
                    name = label = names[ index ]
                    label = self.string_value( label, capitalize )
                    rb = tix.RadioButton( self.control,
                                          text     = label,
                                          variable = var,
                                          value    = mapping[name],
                                          command  = update_object)

                    if name == cur_name:
                        rb.select()

                    self.set_tooltip(rb)
                    rb.grid( row = i, column = j )

                    index += incr[j]
                    n -= 1

# EOF -------------------------------------------------------------------------
