TraitsBackendPyjamas
--------------------

The TraitsBackendPyjamas project contains an implementation of TraitsGUI using
Pyjamas-Desktop. It provides Webkit-based support for visualisation and editing
of Traits-based objects.

Usage
-----

Install Traits::

    $ easy_install Traits

Then either set an environment variable::

    $ export ETS_TOOLKIT="pyjd"

or set the GUI toolkit::

    from enthought.traits.trait_base import ETSConfig

    ETSConfig.toolkit = "pyjd"

Notes
-----

traits.ui.pyjd.toolkit.GUIToolkit().view_application(view)
traits.ui.view.View().ui()
traits.ui.ui.UI().ui() # kind = "live"
traits.ui.pyjd.toolkit.GUIToolkit.ui_live()
traits.ui.pyjd.ui_live.ui_live()
traits.ui.pyjd.ui_live.ui_panel(NONMODAL)
traits.ui.pyjd.ui_live.LiveWindow().init()
traits.ui.pyjd.ui_panel.panel()
traits.ui.pyjd.ui_panel.fill_panel_for_group()
traits.ui.pyjd.ui_panel.GroupPanel().create_label()
