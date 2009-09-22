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

""" Defines a test for the Pyjamas web 'toolkit'. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import unittest

from enthought.traits.trait_base import ETSConfig

ETSConfig.toolkit = "pyjd" # Set the GUI toolkit:

from enthought.traits.api import HasTraits, Str, Int, Float, Bool
from enthought.traits.ui.api import View, Group, Item, Handler
from enthought.traits.ui.menu import MenuBar, ToolBar, Menu, Action
from enthought.pyface.image_resource import ImageResource

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

ICON_LOCATION = "" #enthought.traits.ui.pyjamas.__init__.__file__

#------------------------------------------------------------------------------
#  File actions:
#------------------------------------------------------------------------------

revert_action = Action(
    name="Revert", action="_on_revert",
    defined_when="ui.history is not None",
    enabled_when="ui.history.can_undo"
)

close_action = Action(
    name="Exit", accelerator="Alt+X", action="_on_close",
    image=ImageResource("exit", search_path=[ICON_LOCATION]),
    tooltip="Exit (Alt+X)"
)

undo_action = Action(
    name="Undo", action="_on_undo", accelerator="Ctrl+Z",
    defined_when="ui.history is not None",
    enabled_when="ui.history.can_undo",
    image=ImageResource("undo", search_path=[ICON_LOCATION]),
    tooltip="Undo (Ctrl+Z)"
)

redo_action = Action(
    name="Redo", action="_on_redo", accelerator="Ctrl+Y",
    defined_when="ui.history is not None",
    enabled_when="ui.history.can_redo",
    image=ImageResource("redo", search_path=[ICON_LOCATION]),
    tooltip="Redo (Ctrl+Y)"
)

help_action = Action(
    name="Help", action="show_help",
    image=ImageResource("help", search_path=[ICON_LOCATION]),
    tooltip="Help"
)

#------------------------------------------------------------------------------
#  Menus:
#------------------------------------------------------------------------------

menu_bar = MenuBar(
    Menu(revert_action, close_action, name="File"),
    Menu(undo_action, redo_action, name="Edit"),
    Menu(help_action, name="Help")
)

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
#        Item("age"),
#        Item("height"),
#        Item("alive")
        ),
        buttons=["Undo", "Redo", "Revert", "OK", "Cancel", "Help"],
        kind="live", menubar=menu_bar, handler=Handler()
    )

#------------------------------------------------------------------------------
#  "ToolkitTestCase" class:
#------------------------------------------------------------------------------

class ToolkitTestCase(unittest.TestCase):
    """ Tests for the Pyjamas web toolkit. """

    person = None

    #--------------------------------------------------------------------------
    #  "TestCase" interface:
    #--------------------------------------------------------------------------

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.person = Person(name="Tim", age=21, height=1.74)

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
