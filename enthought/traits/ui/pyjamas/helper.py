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
#  Date:   22/02/2009
#
#------------------------------------------------------------------------------

""" Helper functions used to define Pyjamas based trait editors and trait
    editor factories.
"""

#------------------------------------------------------------------------------
#  'PyjsDelegate' class:
#------------------------------------------------------------------------------

class PyjsDelegate ( object ):

   #---------------------------------------------------------------------------
   #  Initialize the object:
   #---------------------------------------------------------------------------

   def __init__ ( self, delegate = None, **kw ):
       self.delegate = delegate
       for name, value in kw.items():
           setattr( self, name, value )

   #---------------------------------------------------------------------------
   #  Return the handle method for the delegate:
   #---------------------------------------------------------------------------

   def __call__ ( self ):
       return self.on_event

   #---------------------------------------------------------------------------
   #  Handle an event:
   #---------------------------------------------------------------------------

   def on_event ( self, *args ):
       self.delegate( self, *args )

# EOF -------------------------------------------------------------------------
