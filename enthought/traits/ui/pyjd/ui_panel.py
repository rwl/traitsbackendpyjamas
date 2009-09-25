#------------------------------------------------------------------------------
#  Copyright (c) 2007, Riverbank Computing Limited
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

""" Creates a panel-based user interface for a specified UI object.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------
#from Tooltip import TooltipListener

import re

from enthought.traits.api import Undefined
from enthought.traits.ui.api import Group
#from enthought.pyface.api import HeadingText

from pyjamas.ui.Widget import Widget
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.TabPanel import TabPanel
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui import HasHorizontalAlignment

from pyjamas.ui.vertsplitpanel import VerticalSplitPanel
from pyjamas.ui.horizsplitpanel import HorizontalSplitPanel

from editor import Editor

#------------------------------------------------------------------------------
#  Constants:
#------------------------------------------------------------------------------

# Pattern of all digits
all_digits = re.compile( r'\d+' )

#------------------------------------------------------------------------------
#  Creates a panel-based user interface for a specified UI object:
#------------------------------------------------------------------------------

def panel ( ui ):
    """ Creates a panel-based user interface for a specified UI object.
    """
    # Bind the context values to the 'info' object:
    ui.info.bind_context()

    # Get the content that will be displayed in the user interface:
    content = ui._groups
    nr_groups = len(content)

    if nr_groups == 0:
        panel = None
    if nr_groups == 1:
        panel = _GroupPanel(content[0], ui).control
    elif nr_groups > 1:
        panel = TabPanel()
        _fill_panel(panel, content, ui)
        panel.ui = ui

    # If the UI is scrollable then wrap the panel in a scroll area.
    if ui.scrollable and panel is not None:
        sp = ScrollPanel()
        sp.add(panel)
        panel = sp

    return panel

#-------------------------------------------------------------------------------
#  Fill a page based container panel with content:
#-------------------------------------------------------------------------------

def _fill_panel(panel, content, ui, item_handler=None):
    """ Fill a page based container panel with content.
    """
    active = 0

    for index, item in enumerate(content):
        page_name = item.get_label(ui)
        if page_name == "":
            page_name = "Page %d" % index

        if isinstance(item, Group):
            if item.selected:
                active = index

            gp = _GroupPanel(item, ui, suppress_label=True)
            page = gp.control
            sub_page = gp.sub_control

            # If the result is the same type with only one page, collapse it
            # down into just the page.
            if type(sub_page) is type(panel) and sub_page.count() == 1:
                new = sub_page.getWidget(0)
                if isinstance(panel, TabPanel):
                    sub_page.remove(sub_page.getWidget(0))
                else:
                    sub_page.remove(sub_page.getWidget(0))
            elif isinstance(page, Widget):
                new = page
            else:
                new = Widget()
                new.setLayoutData(page)

            layout = new.getLayoutData()
#            if layout is not None:
#                layout.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        else:
            new = Widget()
            layout = VerticalPanel()
            layout.setBorderWidth(0)
            item_handler(item, layout)

        # Add the content.
        if isinstance(panel, TabPanel):
            panel.add(new, page_name)
        else:
            panel.add(new)

    panel.setCurrentIndex(active)

#------------------------------------------------------------------------------
#  "GroupPanel" class:
#------------------------------------------------------------------------------

class _GroupPanel(object):
    """ A sub-panel for a single group of items. It may be either a layout or a
        widget.
    """

    def __init__(self, group, ui, suppress_label=False):
        """Initialise the object.
        """
        # Get the contents of the group:
        content = group.get_content()

        # Save these for other methods.
        self.group = group
        self.ui = ui

        self.is_horizontal = (group.orientation == 'horizontal')

        # outer is the top-level widget or layout that will eventually be
        # returned.  sub is the QTabWidget or QToolBox corresponding to any
        # 'tabbed' or 'fold' layout.  It is only used to collapse nested
        # widgets.  inner is the object (not necessarily a layout) that new
        # controls should be added to.
        outer = sub = inner = None

        # Get the group label.
        if suppress_label:
            label = ""
        else:
            label = group.label

        # Create a border if requested.
        if group.show_border:
#            outer = QtGui.QGroupBox(label)
#            inner = QtGui.QBoxLayout(self.direction, outer)
            print "Borders are not implemented."

        elif label != "":
            if self.is_horizontal:
                outer = inner = HorizontalPanel()
            else:
                outer = inner = VerticalPanel()
            inner.add(HeadingText(None, text=label).control)

        # Add the layout specific content.
        if len(content) == 0:
            pass

        elif group.layout == 'flow':
            outer = inner = FlowPanel()
            raise NotImplementedError, "'the 'flow' layout isn't implemented"

        elif group.layout == 'split':
            # Create the splitter.
            if self.is_horizontal:
                splitter = HorizontalSplitPanel()
            else:
                splitter = VerticalSplitPanel()

#            splitter.setOpaqueResize(False) # Mimic wx backend resize behavior

            # Default layout behaviour of HorizontalSplitPanels is to 100% fill
            # its parent vertically and horizontally [this is NOT normal!]
            splitter.setSplitPosition("50%")

#            policy = splitter.sizePolicy()
#            policy.setHorizontalStretch(50)
#            policy.setVerticalStretch(50)
#            if group.orientation == 'horizontal':
#                policy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
#            else:
#                policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
#            splitter.setSizePolicy(policy)

            if outer is None:
                outer = splitter
            else:
                inner.add(splitter)

            # Create an editor (saves and restores prefs).
#            editor = SplitterGroupEditor(control=outer,splitter=splitter,ui=ui)
#            self._setup_editor(group, editor)

            self._add_splitter_items(content, splitter)

        elif group.layout in ('tabbed', 'fold'):
            # Create the TabWidget or ToolBox.
            if group.layout == 'tabbed':
                sub = TabPanel()
            else:
                print "Fold layout not implemented."
                sub = VerticalPanel()

            # Give tab/tool widget stretch factor equivalent to default stretch
            # factory for a resizeable item. See end of '_add_items'.
#            policy = sub.sizePolicy()
#            policy.setHorizontalStretch(50)
#            policy.setVerticalStretch(50)
#            sub.setSizePolicy(policy)

            _fill_panel(sub, content, self.ui, self._add_page_item)

            if outer is None:
                outer = sub
            else:
                inner.addWidget(sub)

            # Create an editor.
#            editor = TabbedFoldGroupEditor(container=sub, control=outer, ui=ui)
#            self._setup_editor(group, editor)

        else:
            # See if we need to control the visual appearence of the group.
            if group.visible_when != '' or group.enabled_when != '':
                # Make sure that outer is a widget or a layout.
                if outer is None:
                    if self.is_horizontal:
                        outer = inner = HorizontalPanel()
                    else:
                        outer = inner = VerticalPanel()

                # Create an editor.
                self._setup_editor(group, GroupEditor(control=outer))

            if isinstance(content[0], Group):
                layout = self._add_groups(content, inner)
            else:
                layout = self._add_items(content, inner)
#            layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

            if outer is None:
                outer = layout
            elif layout is not inner:
                inner.add(layout)

        # Publish the top-level widget, layout or None.
        self.control = outer

        # Publish the optional sub-control.
        self.sub_control = sub


    def _setup_editor(self, group, editor):
        """Setup the editor for a group.
        """
        if group.id != '':
            self.ui.info.bind(group.id, editor)

        if group.visible_when != '':
            self.ui.add_visible(group.visible_when, editor)

        if group.enabled_when != '':
            self.ui.add_enabled(group.enabled_when, editor)


    def _add_groups(self, content, outer):
        """ Adds a list of Group objects to the panel, creating a layout if
            needed.  Return the outermost layout.
        """
        # Use the existing layout if there is one.
        if outer is None:
            if self.is_horizontal:
                outer = inner = HorizontalPanel()
            else:
                outer = inner = VerticalPanel()

        # Process each group.
        for subgroup in content:
            panel = _GroupPanel(subgroup, self.ui).control

            if isinstance(panel, Widget):
                outer.add(panel)
            else:
                # The sub-group is empty which seems to be used as a way of
                # providing some whitespace.
                outer.add(Label(' '))

        return outer

    def _add_items(self, content, outer=None):
        """Adds a list of Item objects, creating a layout if needed.  Return
           the outermost layout.
        """
        # Get local references to various objects we need:
        ui = self.ui
        info = ui.info
        handler = ui.handler

        group = self.group
        show_left = group.show_left
        padding = group.padding
        columns = group.columns

        # See if a label is needed.
        show_labels = False
        for item in content:
            show_labels |= item.show_label

        # See if a grid layout is needed.
        if show_labels or columns > 1:
            inner = FlexTable(Width="100%")
#            inner.getFlexCellFormatter().setColSpan(0, 0, 2)
#            inner.getFlexCellFormatter().setHorizontalAlignment(0, 0,
#                HasHorizontalAlignment.ALIGN_CENTER)

            if outer is None:
                outer = inner
            else:
                outer.add(inner)

            row = 0
            if show_left:
                label_alignment = HasHorizontalAlignment.ALIGN_RIGHT
            else:
                label_alignment = HasHorizontalAlignment.ALIGN_LEFT

        else:
            # Use the existing layout if there is one.
            if outer is None:
                if self.is_horizontal:
                    outer = inner = HorizontalPanel()
                else:
                    outer = inner = VerticalPanel()

            inner = outer

            row = -1
            label_alignment = HasHorizontalAlignment.ALIGN_RIGHT

        # Process each Item in the list:
        col = -1
        for item in content:

            print "COLUMNS:", row, col, columns

            # Keep a track of the current logical row and column unless the
            # layout is not a grid.
            col += 1
            if row >= 0 and col >= columns:
                col = 0
                row += 1

            # Get the name in order to determine its type:
            name = item.name

            # Check if is a label:
            if name == '':
                label = item.label
                if label != "":

                    # Create the label widget.
                    if item.style == 'simple':
                        label = Label(label)
                    else:
                        label = HeadingText(None, text=label).control

                    self._add_widget(inner, label, row, col, show_labels)

                    if item.emphasized:
                        self._add_emphasis(label)

                # Continue on to the next Item in the list:
                continue

            # Check if it is a separator:
            if name == '_':
                cols = columns

                # See if the layout is a grid.
#                if row >= 0:
#                    # Move to the start of the next row if necessary.
#                    if col > 0:
#                        col = 0
#                        row += 1
#
#                    # Skip the row we are about to do.
#                    row += 1
#
#                    # Allow for the columns.
#                    if show_labels:
#                        cols *= 2
#
#                for i in range(cols):
#                    line = QtGui.QFrame()
#
#                    if self.direction == QtGui.QBoxLayout.LeftToRight:
#                        # Add a vertical separator:
#                        line.setFrameShape(QtGui.QFrame.VLine)
#                        if row < 0:
#                            inner.addWidget(line)
#                        else:
#                            inner.addWidget(line, i, row)
#                    else:
#                        # Add a horizontal separator:
#                        line.setFrameShape(QtGui.QFrame.HLine)
#                        if row < 0:
#                            inner.addWidget(line)
#                        else:
#                            inner.addWidget(line, row, i)

#                    line.setFrameShadow(QtGui.QFrame.Sunken)

                # Continue on to the next Item in the list:
                continue

            # Convert a blank to a 5 pixel spacer:
            if name == ' ':
                name = '5'

            # Check if it is a spacer:
            if all_digits.match( name ):

                # If so, add the appropriate amount of space to the layout:
#                n = int( name )
#                if self.direction == QtGui.QBoxLayout.LeftToRight:
#                    # Add a horizontal spacer:
#                    spacer = QtGui.QSpacerItem(n, 1)
#                else:
#                    # Add a vertical spacer:
#                    spacer = QtGui.QSpacerItem(1, n)
#
#                self._add_widget(inner, spacer, row, col, show_labels)

                print "Spacers are not implemented."

                # Continue on to the next Item in the list:
                continue

            # Otherwise, it must be a trait Item:
            object      = eval( item.object_, globals(), ui.context )
            trait       = object.base_trait( name )
            desc        = trait.desc or ''
            fixed_width = False

            # Handle any label.
            if item.show_label:
                label = self._create_label(item, ui, desc)
                self._add_widget(inner, label, row, col, show_labels,
                                 label_alignment)

                col += 1

            else:
                label = None

            # Get the editor factory associated with the Item:
            editor_factory = item.editor
            if editor_factory is None:
                editor_factory = trait.get_editor()

                # If still no editor factory found, use a default text editor:
                if editor_factory is None:
                    from text_editor import ToolkitEditorFactory
                    editor_factory = ToolkitEditorFactory()

                # If the item has formatting traits set them in the editor
                # factory:
                if item.format_func is not None:
                    editor_factory.format_func = item.format_func

                if item.format_str != '':
                    editor_factory.format_str = item.format_str

                # If the item has an invalid state extended trait name, set it
                # in the editor factory:
                if item.invalid != '':
                    editor_factory.invalid = item.invalid

            # Create the requested type of editor from the editor factory:
            factory_method = getattr( editor_factory, item.style + '_editor' )
            editor         = factory_method( ui, object, name, item.tooltip,
                                        None).set(
                                 item        = item,
                                 object_name = item.object )

            # Tell the editor to actually build the editing widget.  Note that
            # "inner" is a layout.  This shouldn't matter as individual editors
            # shouldn't be using it as a parent anyway.  The important thing is
            # that it is not None (otherwise the main TraitsUI code can change
            # the "kind" of the created UI object).
            editor.prepare(inner)
            control = editor.control

            # Set the initial 'enabled' state of the editor from the factory:
            editor.enabled = editor_factory.enabled

            # Add emphasis to the editor control if requested:
            if item.emphasized:
                self._add_emphasis(control)

            # Give the editor focus if it requested it:
            if item.has_focus:
#                control.setFocus()
                print "Item 'has_focus' not implemented."

            # Set the correct size on the control, as specified by the user:
            stretch = 0
            scrollable = editor.scrollable
            item_width = item.width
            item_height = item.height
            if (item_width != -1) or (item_height != -1):
#                min_size = control.minimumSizeHint()
#                width = min_size.width()
#                height = min_size.height()
                height = width = 0

                if (0.0 < item_width <= 1.0) and self.is_horizontal:
                    stretch = int(100 * item_width)

                item_width = int(item_width)
                if item_width < -1:
                    item_width  = -item_width
                else:
                    item_width = max(item_width, width)

                if (0.0 < item_height <= 1.0) and (not self.is_horizontal):
                    stretch = int(100 * item_height)

                item_height = int(item_height)
                if item_height < -1:
                    item_height = -item_height
                else:
                    item_height = max(item_height, height)

#                control.setMinimumWidth(item_width)
#                control.setMinimumHeight(item_height)
                control.setWidth(item_width)
                control.setHeight(item_height)

            # Bind the editor into the UIInfo object name space so it can be
            # referred to by a Handler while the user interface is active:
            id = item.id or name
            info.bind( id, editor, item.id )

            # Also, add the editors to the list of editors used to construct
            # the user interface:
            ui._editors.append( editor )

            # If the handler wants to be notified when the editor is created,
            # add it to the list of methods to be called when the UI is
            # complete:
            defined = getattr( handler, id + '_defined', None )
            if defined is not None:
                ui.add_defined( defined )

            # If the editor is conditionally visible, add the visibility
            # 'expression' and the editor to the UI object's list of monitored
            # objects:
            if item.visible_when != '':
                ui.add_visible( item.visible_when, editor )

            # If the editor is conditionally enabled, add the enabling
            # 'expression' and the editor to the UI object's list of monitored
            # objects:
            if item.enabled_when != '':
                ui.add_enabled( item.enabled_when, editor )

            # Add the created editor control to the layout with the appropriate
            # size and stretch policies:
#            ui._scrollable |= scrollable
#            item_resizable  = ((item.resizable is True) or
#                               ((item.resizable is Undefined) and scrollable))
#            if item_resizable:
#                stretch = stretch or 50
#                self.resizable = True
#            elif item.springy:
#                stretch = stretch or 50
#            policy = control.sizePolicy()
#            if self.direction == QtGui.QBoxLayout.LeftToRight:
#                policy.setHorizontalStretch(stretch)
#                if item_resizable or item.springy:
#                    policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
#            else:
#                policy.setVerticalStretch(stretch)
#                if item_resizable or item.springy:
#                    policy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
#            control.setSizePolicy(policy)

            # FIXME: Need to decide what to do about border_size and padding
            self._add_widget(inner, control, row, col, show_labels)

            # Save the reference to the label control (if any) in the editor:
            editor.label_control = label

        return outer


    def _add_widget(self, layout, w, row, column, show_labels,
                    label_alignment=HasHorizontalAlignment.ALIGN_RIGHT):
        """ Adds a widget to a panel taking into account the orientation and
            the position of any labels.
        """
        # If the widget really is a widget then remove any margin so that it
        # fills the cell.
#        if isinstance(w, Widget):
#            wl = w.layout()
#            if wl is not None:
#                wl.setMargin(0)


        print "ADDING WIDGET", row, column, w, show_labels, label_alignment

        # See if the layout is not a grid.
        if row < 0:
            layout.add(w)
        else:
            if self.is_horizontal:
                # Flip the row and column.
                row, column = column, row

            if show_labels:
                # Convert the "logical" column to a "physical" one.
                column *= 2

                # Determine whether to place widget on left or right of
                # "logical" column.
                if (label_alignment != "right" and not self.group.show_left) \
                    or (label_alignment == "right" and self.group.show_left):
                    column += 1

            if isinstance(w, Widget):
                layout.setWidget(row, column, w)
                layout.getFlexCellFormatter().setHorizontalAlignment(row,
                    column, label_alignment)

            else:
                layout.addWidget(row, column, w)
                layout.getFlexCellFormatter().setHorizontalAlignment(row,
                    column, label_alignment)


    def _create_label(self, item, ui, desc, suffix = ':'):
        """ Creates an item label.
        """
        label = item.get_label(ui)
        if (label == '') or (label[-1:] in '?=:;,.<>/\\"\'-+#|'):
            suffix = ''

        print "LABEL:", label + suffix

        control = Label(label + suffix)

        if item.emphasized:
            self._add_emphasis(control)

        # FIXME: Decide what to do about the help.  (The non-standard wx way,
        # What's This style help, both?)
        #wx.EVT_LEFT_UP( control, show_help_popup )
        help = item.get_help(ui)

#        if desc != '':
#            control.setToolTip('Specifies ' + desc)

        return control


    def _add_emphasis(self, control):
        """Adds emphasis to a specified control's font.
        """
        print "Emphasis is not implemented."

#-------------------------------------------------------------------------------
#  A pseudo-editor that allows a group to be managed.:
#-------------------------------------------------------------------------------

class GroupEditor(Editor):
    """ A pseudo-editor that allows a group to be managed.
    """

    def __init__(self, **traits):
        """ Initialise the object.
        """
        self.set(**traits)

#-------------------------------------------------------------------------------
#  Displays a help window for the specified UI's active Group:
#-------------------------------------------------------------------------------

def show_help ( ui, button ):
    """ Displays a help window for the specified UI's active Group.
    """
    pass

# EOF -------------------------------------------------------------------------
