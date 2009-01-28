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

#from enthought.traits.api \
#    import HasStrictTraits, HasPrivateTraits, Instance, List, Event
#
#from enthought.traits.ui.api \
#    import UI
#
#from enthought.traits.ui.menu \
#    import Action
#
#from editor \
#    import Editor

#-------------------------------------------------------------------------------
#  'BaseDialog' class:
#-------------------------------------------------------------------------------

class BaseDialog ( object ):
    """ Base class for Traits UI dialog boxes.
    """
    #---------------------------------------------------------------------------
    #  Sets the frame's icon:
    #---------------------------------------------------------------------------

    def set_icon ( self, icon = None ):
        """ Sets the frame's icon.
        """
        from enthought.pyface.image_resource import ImageResource

        if not isinstance( icon, ImageResource ):
            icon = ImageResource( 'frame.ico' )
#        self.control.SetIcon( icon.create_icon() )

# EOF -------------------------------------------------------------------------
