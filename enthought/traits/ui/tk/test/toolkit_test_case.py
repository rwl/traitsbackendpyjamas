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
#  Date:   21/01/2008
#
#------------------------------------------------------------------------------

""" Defines a test for the Tkinter 'toolkit'. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import unittest

from enthought.traits.trait_base import ETSConfig

ETSConfig.toolkit = "tk" # Set the GUI toolkit:

from enthought.traits.api import HasTraits, Str, Int, Float, Bool
from enthought.traits.ui.api import View, Group, Item
from enthought.traits.ui.menu import MenuBar, ToolBar, Menu, Action
from enthought.pyface.image_resource import ImageResource

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

ICON_LOCATION = "" #enthought.traits.ui.tk.__init__.__file__

#------------------------------------------------------------------------------
#  File actions:
#------------------------------------------------------------------------------

new_action = Action(
    name="&New", accelerator="Ctrl+N", action="new_model",
    image=ImageResource("new.png", search_path=[ICON_LOCATION]),
    tooltip="New (Ctrl+N)"
)

open_action = Action(
    name="&Open", accelerator="Ctrl+O", action="open_file",
    image=ImageResource("open.png", search_path=[ICON_LOCATION]),
    tooltip="Open (Ctrl+O)"
)

save_action = Action(
    name="&Save", accelerator="Ctrl+S", action="save",
    image=ImageResource("save.png", search_path=[ICON_LOCATION]),
    tooltip="Save (Ctrl+S)"
)

close_action = Action(
    name="E&xit", accelerator="Alt+X", action="_on_close",
    image=ImageResource("exit.png", search_path=[ICON_LOCATION]),
    tooltip="Exit (Alt+X)"
)

#------------------------------------------------------------------------------
#  Menus:
#------------------------------------------------------------------------------

file_menu = Menu("|", new_action, "_", open_action, save_action, close_action,
    name="&File")

menu_bar = MenuBar(file_menu)

#------------------------------------------------------------------------------
#  "Person" class:
#------------------------------------------------------------------------------

class Person(HasTraits):
    name = Str
    age = Int
    height = Float
    alive = Bool(True)

    traits_view = View(Group(
        Item("name"),
        Item("age"),
        Item("height"),
        Item("alive")),
        buttons=["Undo", "Redo", "Revert", "OK", "Cancel", "Help"],
        kind="live", menubar=menu_bar
    )

#------------------------------------------------------------------------------
#  "ToolkitTestCase" class:
#------------------------------------------------------------------------------

class ToolkitTestCase(unittest.TestCase):
    """ Tests for the Tkinter toolkit. """

    person = None

    #--------------------------------------------------------------------------
    #  "TestCase" interface:
    #--------------------------------------------------------------------------

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.person = Person(name="Hannah", age=21, height=1.74)

    #--------------------------------------------------------------------------
    #  Tests:
    #--------------------------------------------------------------------------

    def test_something(self):
        """ Test something about the toolkit. """

        person = self.person
        person.configure_traits()


if __name__ == "__main__":
    unittest.main()

# EOF -------------------------------------------------------------------------
