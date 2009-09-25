#------------------------------------------------------------------------------
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

""" Helper functions used to define Pyjamas based trait editors and trait
    editor factories.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import Enum, CTrait, BaseTraitHandler, TraitError

from enthought.traits.ui.ui_traits \
    import convert_image, SequenceTypes

#-------------------------------------------------------------------------------
#  Positions a window on the screen with a specified width and height so that
#  the window completely fits on the screen if possible:
#-------------------------------------------------------------------------------

def position_window ( window, width = None, height = None, parent = None ):
    """ Positions a window on the screen with a specified width and height so
        that the window completely fits on the screen if possible.
    """
    # Get the available geometry of the screen containing the window.
#    sgeom = QtGui.QApplication.desktop().availableGeometry(window)
    screen_dx = 0#sgeom.width()
    screen_dy = 0#sgeom.height()

    # Use the frame geometry even though it is very unlikely that the X11 frame
    # exists at this point.
    fgeom = window.frameGeometry()
    width = width or fgeom.width()
    height = height or fgeom.height()

    if parent is None:
        parent = window._parent

    if parent is None:
        # Center the popup on the screen.
        window.move((screen_dx - width) / 2, (screen_dy - height) / 2)
        return

    # Calculate the desired size of the popup control:
    if isinstance(parent, Widget):
#        gpos = parent.mapToGlobal(QtCore.QPoint())
        x = 0#gpos.x()
        y = 0#gpos.y()
        cdx = parent.width()
        cdy = parent.height()

        # Get the frame height of the parent and assume that the window will
        # have a similar frame.  Note that we would really like the height of
        # just the top of the frame.
        pw = parent.window()
        fheight = pw.frameGeometry().height() - pw.height()
    else:
        # Special case of parent being a screen position and size tuple (used
        # to pop-up a dialog for a table cell):
        x, y, cdx, cdy = parent

        fheight = 0

    x -= (width - cdx) / 2
    y += cdy + fheight

    # Position the window (making sure it will fit on the screen).
    window.move(max(0, min(x, screen_dx - width)),
                max(0, min(y, screen_dy - height)))

#-------------------------------------------------------------------------------
#  Recomputes the mappings for a new set of enumeration values:
#-------------------------------------------------------------------------------

def enum_values_changed ( values ):
    """ Recomputes the mappings for a new set of enumeration values.
    """

    if isinstance( values, dict ):
        data = [ ( str( v ), n ) for n, v in values.items() ]
        if len( data ) > 0:
            data.sort( lambda x, y: cmp( x[0], y[0] ) )
            col = data[0][0].find( ':' ) + 1
            if col > 0:
                data = [ ( n[ col: ], v ) for n, v in data ]
    elif not isinstance( values, SequenceTypes ):
        handler = values
        if isinstance( handler, CTrait ):
            handler = handler.handler
        if not isinstance( handler, BaseTraitHandler ):
            raise TraitError, "Invalid value for 'values' specified"
        if handler.is_mapped:
            data = [ ( str( n ), n ) for n in handler.map.keys() ]
            data.sort( lambda x, y: cmp( x[0], y[0] ) )
        else:
            data = [ ( str( v ), v ) for v in handler.values ]
    else:
        data = [ ( str( v ), v ) for v in values ]

    names           = [ x[0] for x in data ]
    mapping         = {}
    inverse_mapping = {}
    for name, value in data:
        mapping[ name ] = value
        inverse_mapping[ value ] = name

    return ( names, mapping, inverse_mapping )

# EOF -------------------------------------------------------------------------
