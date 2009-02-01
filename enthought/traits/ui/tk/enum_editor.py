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

import Tix as tix

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.file_editor file.
from enthought.traits.ui.editors.file_editor \
    import ToolkitEditorFactory

from editor \
    import Editor

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

#class SimpleEditor ( BaseEditor ):
#    """ Simple style of enumeration editor, which displays a combo box.
#    """
#
#    #---------------------------------------------------------------------------
#    #  Finishes initialising the editor by creating the underlying toolkit
#    #  widget:
#    #---------------------------------------------------------------------------
#
#    def init ( self, parent ):
#        """ Finishes initialising the editor by creating the underlying toolkit
#            widget.
#        """
#        super( BaseEditor, self ).init( parent )
#
#        factory = self.factory
#        if factory.evaluate is None:
#            self.control = control = wx.Choice( parent, -1, wx.Point( 0, 0 ),
#                                                wx.Size( -1, -1 ), self.names )
#            wx.EVT_CHOICE( parent, self.control.GetId(), self.update_object )
#        else:
#            self.control = control = wx.ComboBox( parent, -1, '',
#                                wx.Point( 0, 0 ), wx.Size( -1, -1 ), self.names,
#                                style = wx.CB_DROPDOWN )
#            wx.EVT_COMBOBOX( parent, control.GetId(), self.update_object )
#            wx.EVT_TEXT_ENTER( parent, control.GetId(),
#                               self.update_text_object )
#            wx.EVT_KILL_FOCUS( control, self.on_kill_focus )
#            if (not factory.is_grid_cell) and factory.auto_set:
#                wx.EVT_TEXT( parent, control.GetId(), self.update_text_object )
#
#        self._no_enum_update = 0
#        self.set_tooltip()
#
#    def dispose ( self ):
#        """ Disposes of the contents of an editor.
#        """
#        disconnect( self.control,
#                    wx.EVT_COMBOBOX, wx.EVT_TEXT_ENTER, wx.EVT_TEXT )
#
#        disconnect_no_id( self.control, wx.EVT_KILL_FOCUS )
#
#        super( SimpleEditor, self ).dispose()
#
#    #---------------------------------------------------------------------------
#    #  Handles the user selecting a new value from the combo box:
#    #---------------------------------------------------------------------------
#
#    def update_object ( self, event ):
#        """ Handles the user selecting a new value from the combo box.
#        """
#        self._no_enum_update += 1
#        try:
#            self.value = self.mapping[ event.GetString() ]
#        except:
#            pass
#        self._no_enum_update -= 1
#
#    #---------------------------------------------------------------------------
#    #  Handles the user typing text into the combo box text entry field:
#    #---------------------------------------------------------------------------
#
#    def update_text_object ( self, event ):
#        """ Handles the user typing text into the combo box text entry field.
#        """
#        if self._no_enum_update == 0:
#            value = self.control.GetValue()
#            try:
#                value = self.mapping[ value ]
#            except:
#                try:
#                    value = self.factory.evaluate( value )
#                except Exception, excp:
#                    self.error( excp )
#                    return
#
#            self._no_enum_update += 1
#            try:
#                self.value = value
#                self.control.SetBackgroundColour( OKColor )
#                self.control.Refresh()
#            except:
#                pass
#            self._no_enum_update -= 1
#
#    #---------------------------------------------------------------------------
#    #  Handles the control losing the keyboard focus:
#    #---------------------------------------------------------------------------
#
#    def on_kill_focus ( self, event ):
#        """ Handles the control losing the keyboard focus.
#        """
#        self.update_text_object( event )
#        event.Skip()
#
#    #---------------------------------------------------------------------------
#    #  Updates the editor when the object trait changes external to the editor:
#    #---------------------------------------------------------------------------
#
#    def update_editor ( self ):
#        """ Updates the editor when the object trait changes externally to the
#            editor.
#        """
#        if self._no_enum_update == 0:
#            if self.factory.evaluate is None:
#                try:
#                    self.control.SetStringSelection(
#                                     self.inverse_mapping[ self.value ] )
#                except:
#                    pass
#            else:
#                try:
#                    self.control.SetValue( self.str_value )
#                except:
#                    pass
#
#    #---------------------------------------------------------------------------
#    #  Handles an error that occurs while setting the object's trait value:
#    #---------------------------------------------------------------------------
#
#    def error ( self, excp ):
#        """ Handles an error that occurs while setting the object's trait value.
#        """
#        self.control.SetBackgroundColour( ErrorColor )
#        self.control.Refresh()
#
#    #---------------------------------------------------------------------------
#    #  Rebuilds the contents of the editor whenever the original factory
#    #  object's 'values' trait changes:
#    #---------------------------------------------------------------------------
#
#    def rebuild_editor ( self ):
#        """ Rebuilds the contents of the editor whenever the original factory
#            object's **values** trait changes.
#        """
#        # Note: This code is unnecessarily complex due to a strange bug in
#        # wxWidgets implementation of the wx.Combobox control that has strange
#        # behavior when the current text field value is one of the selection
#        # values when 'Clear' is called. In this case, even saving and
#        # restoring the text field value does not work, so we go to great
#        # lengths to detect this case and avoid using 'Clear', but still get
#        # the equivalent visual results. Modify this code at your own risk...
#
#        control  = self.control
#        clear    = True
#        cur_name = None
#        if self.factory.evaluate is not None:
#            n         = control.GetCount()
#            cur_names = [ control.GetString( i ) for i in range( n ) ]
#            cur_name  = control.GetValue()
#            if cur_name in self.names:
#                clear   = False
#                include = True
#                for i in range( n - 1, -1, -1 ):
#                    if cur_name == cur_names[i]:
#                        include = False
#                    else:
#                        control.Delete( i )
#                for name in self.names:
#                    if include or (name != cur_name):
#                        control.Append( name )
#                cur_name = None
#            else:
#                point = control.GetInsertionPoint()
#
#        if clear:
#            control.Clear()
#            control.AppendItems( self.names )
#
#        if cur_name is not None:
#            self._no_enum_update += 1
#            control.SetValue( cur_name )
#            control.SetInsertionPoint( point )
#            self._no_enum_update -= 1
#
#        self.update_editor()

# EOF -------------------------------------------------------------------------
