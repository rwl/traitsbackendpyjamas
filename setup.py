#!/usr/bin/env python
#
# Copyright (c) 2008-2009 by Richard Lincoln
# All rights reserved.

from setuptools import setup, find_packages

setup(author="Richard Lincoln",
      author_email="r.w.lincoln@gmail.com",
      description="Pyjamas-Desktop backend for Traits and TraitsGUI (PyFace).",
      url="http://github.com/rwl/traitsbackendpyjamas",
      version="0.1.1",
      install_requires=["Traits", "Pyjamas"],
      license="BSD",
      name="TraitsBackendPyjamas",
      namespace_packages = ['enthought',
                            'enthought.pyface',
                            'enthought.pyface.ui',
                            'enthought.traits',
                            'enthought.traits.ui'],
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False)
