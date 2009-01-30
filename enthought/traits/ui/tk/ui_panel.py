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

""" Creates a panel-based user interface for a specified UI object. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tkinter

import re

from enthought.traits.ui.api \
    import Group

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# Pattern of all digits
all_digits = re.compile( r'\d+' )

#------------------------------------------------------------------------------
#  Creates a panel-based user interface for a specified UI object:
#------------------------------------------------------------------------------

def panel ( ui, parent ):
    """ Creates a panel-based user interface for a specified UI object. """
    # Bind the context values to the 'info' object:
    ui.info.bind_context()

    # Get the content that will be displayed in the user interface:
    content = ui._groups

    # If there is 0 or 1 Groups in the content, create a single panel for it:
    if len( content ) <= 1:
        panel = Tkinter.Frame(parent)
        if len( content ) == 1:
            # Fill the panel with the Group's content:
            resizable, contents = fill_panel_for_group( panel, content[0], ui )

        return panel
    else:
#        nb = create_notebook_for_items(content, ui, parent, None)
        return None#Tkinter.Frame(parent)

#-------------------------------------------------------------------------------
#  Builds the user interface for a specified Group within a specified Panel:
#-------------------------------------------------------------------------------

def fill_panel_for_group ( panel, group, ui, suppress_label = False,
                           is_dock_window = False, create_panel = False ):
    """ Builds the user interface for a specified Group within a specified
        Panel.
    """
    fp = GroupPanel( panel, group, ui, suppress_label )
    return ( fp.control or fp.sizer, fp.resizable )

#------------------------------------------------------------------------------
#  "FillPanel" class:
#------------------------------------------------------------------------------

class GroupPanel:
    """ A subpanel for a single group of items.
    """

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, panel, group, ui, suppress_label ):
        """ Initializes the object.
        """
        # Get the contents of the group:
        content = group.get_content()

        # Create a group editor object if one is needed:
        self.control       = self.sizer = editor = None
        self.ui            = ui
        self.group         = group
        self.is_horizontal = (group.orientation == 'horizontal')
        layout             = group.layout
        is_scrolled_panel  = group.scrollable
        is_splitter        = (layout == 'split')
        is_tabbed          = (layout == 'tabbed')
        id                 = group.id

        # Assume our contents are not resizable:
        self.resizable = False

        if self.is_horizontal:
            self.side = Tkinter.LEFT
        else:
            self.side = Tkinter.TOP

        if len( content ) > 0:
            if isinstance( content[0], Group ):
                # If so, add them to the panel and exit:
                self.add_groups( content, panel )
            else:
                self.add_items( content, panel )


    def add_items( self, content, panel ):
        """ Adds a list of Item objects to the panel. """
        # Get local references to various objects we need:
        ui      = self.ui
        info    = ui.info
        handler = ui.handler

        group            = self.group
        show_left        = group.show_left
        padding          = group.padding
        col              = -1
        col_incr         = 1

        show_labels      = False
        for item in content:
            show_labels |= item.show_label

        # Process each Item in the list:
        for item in content:

            # Get the name in order to determine its type:
            name = item.name

            # Check if is a label:
            if name == '':
                Label( panel, text=item.label ).pack( side = side )

            # Check if it is a separator:
            if name == '_':
                separator = Tkinter.Frame(panel, height=2, bd=1,
                    relief=Tkinter.SUNKEN)
                separator.pack(fill=X, padx=5, pady=5)

            # Convert a blank to a 5 pixel spacer:
            if name == ' ':
                name = '5'

            # Check if it is a spacer:
            if all_digits.match( name ):
                # If so, add the appropriate amount of space to the sizer:
                n = int( name )

                raise NotImplementedError, "Spacer aren't implemented."

            # Otherwise, it must be a trait Item:
            object = eval( item.object_, globals(), ui.context )
            trait  = object.base_trait( name )
            desc   = trait.desc or ''
            label  = None

            # If we are displaying labels on the left, add the label to the
            # user interface:
            if item.show_label:
                label = self.create_label( item, ui, desc, panel )
            elif (cols > 1) and show_labels:
                label = self.dummy_label( panel )

            # Get the editor factory associated with the Item:
            editor_factory = item.editor
            if editor_factory is None:
                editor_factory = trait.get_editor()

                print "EDITOR FACTORY:", editor_factory

            item_panel = panel

            # Create the requested type of editor from the editor factory:
            factory_method = getattr( editor_factory, item.style + '_editor' )
            editor         = factory_method( ui, object, name, item.tooltip,
                                        item_panel ).set(
                                 item        = item,
                                 object_name = item.object )

            # Tell editor to actually build the editing widget:
            editor.prepare( item_panel )

            # Set the initial 'enabled' state of the editor from the factory:
            editor.enabled = editor_factory.enabled

            # Set the correct size on the control, as specified by the user:
            scrollable  = editor.scrollable
            item_width  = item.width
            item_height = item.height
            growable    = 0
            if (item_width != -1.0) or (item_height != -1.0):
                if (0.0 < item_width <= 1.0) and self.is_horizontal:
                    growable   = int( 1000.0 * item_width )
                    item_width = -1

                item_width = int( item_width )
                if item_width < -1:
                    item_width = -item_width
                elif item_width != -1:
                    item_width = max( item_width, width )

                if (0.0 < item_height <= 1.0) and (not self.is_horizontal):
                    growable    = int( 1000.0 * item_height )
                    item_height = -1

                item_height = int( item_height )
                if item_height < -1:
                    item_height = -item_height
                elif item_height != -1:
                    item_height = max( item_height, height )

                control.config( width = item_width, height = item_height )

    #---------------------------------------------------------------------------
    #  Creates an item label:
    #---------------------------------------------------------------------------

    def create_label ( self, item, ui, desc, parent, suffix = ':' ):
        """ Creates an item label.
        """

        label = item.get_label( ui )
        if (label == '') or (label[-1:] in '?=:;,.<>/\\"\'-+#|'):
            suffix = ''

        control = Tkinter.Label( parent, text = label + suffix )
        control.pack(side=self.side)

        # TODO: Tooltip using desc.

        return control

    #---------------------------------------------------------------------------
    #  Creates a dummy item label:
    #---------------------------------------------------------------------------

    def dummy_label ( self, parent ):
        """ Creates an item label.
        """

        return Tkinter.Label( parent, text = "" ).pack( side = self.side )

#-------------------------------------------------------------------------------
#  Displays a help window for the specified UI's active Group:
#-------------------------------------------------------------------------------

def show_help ( ui, button ):
    """ Displays a help window for the specified UI's active Group.
    """

    pass

# EOF -------------------------------------------------------------------------
