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
