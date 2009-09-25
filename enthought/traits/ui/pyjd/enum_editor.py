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

""" Defines the file editors for the Pyjamas web interface toolkit.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from string \
    import capitalize

from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.Panel import Panel
from pyjamas.ui.RadioButton import RadioButton
from pyjamas.ui.FlexTable import FlexTable

from enthought.traits.api \
    import Bool, Property

# FIXME: ToolkitEditorFactory is a proxy class defined here just for backward
# compatibility. The class has been moved to the
# enthought.traits.ui.editors.file_editor file.
from enthought.traits.ui.editors.file_editor \
    import ToolkitEditorFactory

from editor \
    import Editor

from constants \
    import OKColor, ErrorColor

from helper \
    import enum_values_changed

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
        """ Finishes initialising the editor by creating the underlying toolkit
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
        """ Recomputes the cached data based on the underlying enumeration
            model.
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
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        super( SimpleEditor, self ).init( parent )

        self.control = control = self.create_combo_box()
        for name in self.names:
            control.addItem(name)

        self.control.addClickListener( getattr(self, "update_object") )

        if self.factory.evaluate is not None:
            print "Editable combo box not implemented."

            control.setEditable(True)
            self.control.addChangeLister( getattr(self, "update_text_object") )

        self._no_enum_update = 0
        self.set_tooltip()

    #---------------------------------------------------------------------------
    #  Returns the QComboBox used for the editor control:
    #---------------------------------------------------------------------------

    def create_combo_box(self):
        """ Returns the QComboBox used for the editor control.
        """
        control = ListBox()
        control.setVisibleItemCount(0)

#        control.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
#        control.setSizePolicy(QtGui.QSizePolicy.Maximum,
#                              QtGui.QSizePolicy.Fixed)
        return control

    #---------------------------------------------------------------------------
    #  Handles the user selecting a new value from the combo box:
    #---------------------------------------------------------------------------

    def update_object (self):
        """ Handles the user selecting a new value from the combo box.
        """
        if self._no_enum_update == 0:
            self._no_enum_update += 1
            text = self.control.getSelectedItemText()
            try:
                self.value = self.mapping[unicode(text)]
            except:
                pass
            self._no_enum_update -= 1

    #---------------------------------------------------------------------------
    #  Handles the user typing text into the combo box text entry field:
    #---------------------------------------------------------------------------

#    def update_text_object(self, text):
#        """ Handles the user typing text into the combo box text entry field.
#        """
#        if self._no_enum_update == 0:
#            value = unicode(text)
#            try:
#                value = self.mapping[value]
#            except:
#                try:
#                    value = self.factory.evaluate(value)
#                except Exception, excp:
#                    self.error( excp )
#                    return
#
#            self._no_enum_update += 1
#            self.value = value
#            self._set_background(OKColor)
#            self._no_enum_update -= 1

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        if self._no_enum_update == 0:
            self._no_enum_update += 1
            if self.factory.evaluate is None:
                try:
                    index = self.names.index(self.inverse_mapping[self.value])
                    self.control.setSelectedIndex(index)
                except:
                    self.control.setSelectedIndex(-1)
            else:
                print "Editable combo box not implemented."
                try:
                    self.control.setEditText(self.str_value)
                except:
                    self.control.setEditText('')
            self._no_enum_update -= 1

    #---------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #---------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait value.
        """
        pass

    #---------------------------------------------------------------------------
    #  Rebuilds the contents of the editor whenever the original factory
    #  object's 'values' trait changes:
    #---------------------------------------------------------------------------

    def rebuild_editor ( self ):
        """ Rebuilds the contents of the editor whenever the original factory
            object's **values** trait changes.
        """
        self.control.blockSignals(True)
        self.control.clear()
        for name in self.names:
            self.control.addItem(name)
        self.control.blockSignals(False)

        self.update_editor()

#-------------------------------------------------------------------------------
#  'RadioEditor' class:
#-------------------------------------------------------------------------------

class RadioEditor ( BaseEditor ):
    """ Enumeration editor, used for the "custom" style, that displays radio
        buttons.
    """

    # Is the button layout row-major or column-major?
    row_major = Bool( False )

    #---------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        super( RadioEditor, self ).init( parent )

        self.panel = FlexTable( BorderWidth=1, Width="100%" )
        self.panel.addTableListener( self.update_object )

        self.rebuild_editor()

    #---------------------------------------------------------------------------
    #  Handles the user clicking one of the 'custom' radio buttons:
    #---------------------------------------------------------------------------

    def update_object ( self, index ):
        """ Handles the user clicking one of the custom radio buttons.
        """
        try:
            self.value = self.mapping[ self.names[ index ] ]
        except:
            pass

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        table = self.panel
        value = self.value

        for row in range( table.getRowCount() ):
            for cell in range( table.getCellCount() ):
                rb = table.getWidget(row, cell)
                rb.setChecked(rb.getText == value)

    #---------------------------------------------------------------------------
    #  Rebuilds the contents of the editor whenever the original factory
    #  object's 'values' trait changes:
    #---------------------------------------------------------------------------

    def rebuild_editor ( self ):
        """ Rebuilds the contents of the editor whenever the original factory
            object's **values** trait changes.
        """
        # Clear any existing content:
        self.clear_layout()

        # Get the current trait value:
        cur_name = self.str_value

        # Create a sizer to manage the radio buttons:
        names   = self.names
        mapping = self.mapping
        n       = len( names )
        cols    = self.factory.cols
        rows    = (n + cols - 1) / cols
        if self.row_major:
            incr = [ 1 ] * cols
        else:
            incr = [ n / cols ] * cols
            rem  = n % cols
            for i in range( cols ):
                incr[i] += (rem > i)
            incr[-1] = -(reduce( lambda x, y: x + y, incr[:-1], 0 ) - 1)

        # Add the set of all possible choices:
        table = self.control
        index = 0
        for i in range( rows ):
            for j in range( cols ):
                if n > 0:
                    name = names[index]
                    rb = self.create_button(name)
                    rb.setText = mapping[name]

                    rb.setChecked(name == cur_name)

                    rb.addClickListener( getattr(self, "update_object") )

                    self.set_tooltip(rb)
                    table.setWidget(i, j, rb)

                    index += incr[j]
                    n -= 1

    #---------------------------------------------------------------------------
    #  Returns the Pyjamas Button used for the radio button:
    #---------------------------------------------------------------------------

    def create_button(self, name):
        """ Returns the Pyjamas Button used for the radio button.
        """
        label = self.string_value(name, capitalize)
        return RadioButton( group=id( self ), label=label )


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
#        super( SimpleEditor, self ).init( parent )
#
#        factory       = self.factory
##        var           = tix.StringVar()
##        update_object = PyjsDelegate( self.update_object, var = var )
#
#        if factory.evaluate is None:
#            control = ListBox()
#            control.setName( "" )
#            control.addChangeListener( self.update_object )
#            control.setMultipleSelect( True )
#
#            for key, value in self.mapping.iteritems():
#                control.addItem( item = key, value = value )
#
#            parent.add(control)
#        else:
##            raise NotImplementedError, "Editable list box not implemented."
#
#            control = ListBox()
#            control.setName( "" )
#            control.addChangeListener( self.update_object )
#            control.setMultipleSelect( False )
#            control.setVisibleItemCount( 0 )
#
#            for name in self.names:
#                self.control.addItem( name )
#
##            control.addKeyboardListener( self.update_text_object )
#            control.addFocusListener( self.on_kill_focus )
#
##            if (not factory.is_grid_cell) and factory.auto_set:
##                control.setKeyboardListener( self.update_text_object )
#
#            control.pack()
#
#        self.control = control
#        self._no_enum_update = 0
#        self.set_tooltip()


#    def dispose ( self ):
#        """ Disposes of the contents of an editor.
#        """
#        control = self.control
#        control.config( command = None )
#        control.removeKeyboardListener( self.update_text_object )
#        control.removeFocusListener( self.on_kill_focus )
##        control.removeKeyboardListener( self.update_text_object )
#
#        super( SimpleEditor, self ).dispose()
#
#    #---------------------------------------------------------------------------
#    #  Handles the user selecting a new value from the combo box:
#    #---------------------------------------------------------------------------
#
#    def update_object ( self, delegate ):
#        """ Handles the user selecting a new value from the combo box.
#        """
#        self._no_enum_update += 1
#        try:
#            index = delegate.getSelectedIndex()
#            self.value = self.mapping[ delegate.getValue( index ) ]
#        except:
#            pass
#        self._no_enum_update -= 1
#
#    #---------------------------------------------------------------------------
#    #  Handles the user typing text into the combo box text entry field:
#    #---------------------------------------------------------------------------
#
#    def update_text_object ( self, delegate ):
#        """ Handles the user typing text into the combo box text entry field.
#        """
#        if self._no_enum_update == 0:
#            index = delegate.getSelectedIndex()
#            value = delegate.getValue( index )
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
#                self.control.setStyleName( "color", OKColor )
##                self.control.Refresh()
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
##        event.Skip()
#        return "break"
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
#            self.control.setSelectedIndex( self.inverse_mapping[ self.value ] )
#
#    #---------------------------------------------------------------------------
#    #  Handles an error that occurs while setting the object's trait value:
#    #---------------------------------------------------------------------------
#
#    def error ( self, excp ):
#        """ Handles an error that occurs while setting the object's trait value.
#        """
#        self.control.setStyleName( "color", ErrorColor )
##        self.control.Refresh()
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
#        control = self.control
#
#        if factory.evaluate is None:
#            control.clear()
#
#            for key, value in self.mapping.iteritems():
#                control.addItem( item = key, value = value )
#        else:
#            control.clear()
#
#            for name in self.names:
#                control.addItem( item = name)
#
#        self.update_editor()
#
##-------------------------------------------------------------------------------
##  'RadioEditor' class:
##-------------------------------------------------------------------------------
#
#class RadioEditor ( BaseEditor ):
#    """ Enumeration editor, used for the "custom" style, that displays radio
#        buttons.
#    """
#    #---------------------------------------------------------------------------
#    #  Finishes initialising the editor by creating the underlying toolkit
#    #  widget:
#    #---------------------------------------------------------------------------
#
#    def init ( self, parent ):
#        """ Finishes initialising the editor by creating the underlying toolkit
#            widget.
#        """
#        super( RadioEditor, self ).init( parent )
#
#        # Create a panel to hold all of the radio buttons:
#        control = Panel()
#        parent.add( control )
#
#        self.control = control
#        self.rebuild_editor()
#
#    #---------------------------------------------------------------------------
#    #  Handles the user clicking one of the 'custom' radio buttons:
#    #---------------------------------------------------------------------------
#
#    def update_object( self, event ):
#        """ Handles the user clicking one of the custom radio buttons.
#        """
##        try:
##            index = event.getSelectedIndex()
##            self.value = event.getValue( index )
##        except:
##            pass
#
#        index = event.getSelectedIndex()
#        self.value = event.getValue( index )
#
#    #---------------------------------------------------------------------------
#    #  Updates the editor when the object trait changes external to the editor:
#    #---------------------------------------------------------------------------
#
#    def update_editor ( self ):
#        """ Updates the editor when the object trait changes externally to the
#            editor.
#        """
#        value = self.value
#        if self.control.children:
#            rb0 = self.control.children.values[0]
#            var = rb0.cget( "variable" )
#            var.set( value )
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
#        # Clear any existing content:
#        for rb in self.control.values():
#            rb.destroy()
#
#        # Get the current trait value:
#        cur_name = self.str_value
#
#        # Create a sizer to manage the radio buttons:
#        names   = self.names
#        mapping = self.mapping
#        n       = len( names )
#        cols    = self.factory.cols
#        rows    = (n + cols - 1) / cols
#        incr    = [ n / cols ] * cols
#        rem     = n % cols
#        for i in range( cols ):
#            incr[i] += (rem > i)
#        incr[-1] = -(reduce( lambda x, y: x + y, incr[:-1], 0 ) - 1)
#
#        grid = Grid( rows = rows, columns = cols )
#
#        # Add the set of all possible choices:
#        index = 0
#
#        for i in range( rows ):
#            for j in range( cols ):
#                if n > 0:
#                    name = label = names[ index ]
#                    label = self.string_value( label, capitalize )
#                    rb = RadioButton( group = id( self.control ),
#                                      label = label )
#
#                    if name == cur_name:
#                        self.control.setChecked( True )
#                    else:
#                        self.control.setChecked( False )
#
#                    self.set_tooltip( rb )
#                    grid.setWidget( row = i, column = j, widget = rb )
#
#                    index += incr[j]
#                    n -= 1

# EOF -------------------------------------------------------------------------
