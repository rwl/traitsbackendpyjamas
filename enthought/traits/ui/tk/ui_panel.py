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
#            resizable, contents = fill_panel_for_group( panel, content[0], ui )
            pass

        return panel
    else:
#        nb = create_notebook_for_items(content, ui, parent, None)
        return Tkinter.Frame(parent)

#------------------------------------------------------------------------------
#  "FillPanel" class:
#------------------------------------------------------------------------------

class FillPanel:

    def add_items(self, content, panel, sizer):
        """ Adds a list of Item objects to the panel. """
        # Get local references to various objects we need:
        ui      = self.ui
        info    = ui.info
        handler = ui.handler

        group            = self.group
        show_left        = group.show_left
        padding          = group.padding

        show_labels      = False
        for item in content:
            show_labels |= item.show_label

        # Process each Item in the list:
        for item in content:

            # Get the name in order to determine its type:
            name = item.name

            # Check if is a label:
            if name == '':
                continue

            # Check if it is a separator:
            if name == '_':
                continue

            # Convert a blank to a 5 pixel spacer:
            if name == ' ':
                name = '5'

            # Check if it is a spacer:
            if all_digits.match( name ):
                continue

            # Otherwise, it must be a trait Item:
            object = eval( item.object_, globals(), ui.context )
            trait  = object.base_trait( name )
            desc   = trait.desc or ''
            label  = None

            # If we are displaying labels on the left, add the label to the
            # user interface:
            if show_left:
                if item.show_label:
                    label = self.create_label( item, ui, desc, panel,
                                               item_sizer )
                elif (cols > 1) and show_labels:
                    label = self.dummy_label( panel, item_sizer )

            # Get the editor factory associated with the Item:
            editor_factory = item.editor
            if editor_factory is None:
                editor_factory = trait.get_editor()

            # If we are displaying labels on the right, add the label to the
            # user interface:
            if not show_left:
                pass

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
                pass

    #---------------------------------------------------------------------------
    #  Creates an item label:
    #---------------------------------------------------------------------------

    def create_label ( self, item, ui, desc, parent, sizer, suffix = ':',
                       pad_side = "left" ):
        """ Creates an item label.
        """

        return ""

    #---------------------------------------------------------------------------
    #  Creates a dummy item label:
    #---------------------------------------------------------------------------

    def dummy_label ( self, parent, sizer ):
        """ Creates an item label.
        """

        return ""

# EOF -------------------------------------------------------------------------
