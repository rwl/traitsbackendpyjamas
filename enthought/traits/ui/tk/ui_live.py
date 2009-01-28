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

""" Creates a non-modal user interface for a specified UI object, where the
UI is "live", meaning that it immediately updates its underlying object(s).

"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import Tkinter

#-------------------------------------------------------------------------------
#  Creates a 'live update' user interface for a specified UI object:
#-------------------------------------------------------------------------------

def ui_live(ui, parent):
    """ Creates a 'live update' user interface for a specified UI object. """

    if ui.owner is None:
        ui.owner = LiveWindow()

#    ui.owner.init(ui, parent, "live")
#    ui.control = ui.owner.control
#    ui.control._parent = parent
#
#    try:
#        ui.prepare_ui()
#    except:
#        ui.control.Destroy()
#        ui.control.ui = None
#        ui.control = None
#        ui.owner = None
#        ui.result = False
#        raise
#
#    ui.handler.position(ui.info)
#    restore_window(ui, is_popup=(style in Popups))

    Tkinter.start(ui.owner)


class LiveWindow:
    """ User interface window that immediately updates its underlying
    object(s).

    """

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def init(self, ui, parent, style):
        """ Initialises the object. """

        self.ui = ui
        self.control = ui.control
        view = ui.view
        history = ui.history

#    @cherrypy.expose
    def index(self):
        return "Hello world!!!"

# EOF -------------------------------------------------------------------------
