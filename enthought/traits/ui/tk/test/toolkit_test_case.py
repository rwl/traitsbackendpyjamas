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
        buttons=["OK", "Cancel"],
        kind="live"
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
