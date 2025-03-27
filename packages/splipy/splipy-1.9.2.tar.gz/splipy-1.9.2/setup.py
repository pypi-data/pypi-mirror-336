# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splipy', 'splipy.io', 'splipy.utils']

package_data = \
{'': ['*'], 'splipy': ['templates/*']}

install_requires = \
['numpy>=1.25,<3.0', 'scipy>=1.10,<2.0']

setup_kwargs = {
    'name': 'splipy',
    'version': '1.9.2',
    'description': 'Spline modelling library for Python',
    'long_description': '\n# ![Splipy Logo](images/logo_small.svg) SpliPy\n\nThis repository contains the SpliPy packages. SpliPy is a pure python library\nfor the creation, evaluation and manipulation of B-spline and NURBS geometries.\nIt supports n-variate splines of any dimension, but emphasis is made on the\nuse of curves, surfaces and volumes. The library is designed primarily for\nanalysis use, and therefore allows fine-grained control over many aspects which\nis not possible to achieve with conventional CAD tools.\n\n## Features\n\nSpliPy allows for the generation of parametric curves, surfaces and volumes in the form of non-uniform rational B-splines (NURBS). It supports traditional curve- and surface-fitting methods such as (but not limited to)\n\n### Curve fitting\n* Bezier curves\n* Hermite Interpolation\n* Cubic Curve Interpolation\n* B-spline Interpolation\n* Least Square Fit\n\n### Surface operations\n* Sweep\n* Revolve\n* Loft\n* Edge_Curves (interior from four edges)\n* Extrude\n* Structured Point Cloud Interpolation\n* Least Square Fit\n\n**Revolve**\n![Revolve](images/revolve.png)\n\n**Sweep**\n![Sweep](images/sweep.png)\n\n**Loft**\n![Loft](images/loft.png)\n\n### Volume operations\n* Revolve\n* Extrude\n* Loft\n* Structured Point Cloud Interpolation\n* Least Square Fit\n\nIn addition to these basic building blocks, it also supports a number of primitive shapes such as (but not limited to)\n\n### Primitive shapes\n* Cube\n* Circle\n* Disc\n* Cylinder\n* Torus\n* Teapot\n\n## Examples\n\n### Derivatives of spline curves\n``` python\n  from splipy import *\n  import numpy as np\n\n  n = 250                                  # number of evaluation points\n  c = curve_factory.circle()               # create the NURBS circle (r=1)\n  t = np.linspace(c.start(0), c.end(0), n) # parametric evaluation points\n  x = c(t)                                 # physical (x,y)-coordinates, size (n,2)\n  v = c.derivative(t, 1)                   # velocity at all points\n  a = c.derivative(t, 2)                   # acceleration at all points\n```\n\n![Missing circle animation](http://i.imgur.com/8MaBiTW.gif "Circle animation")\n\n### Curve fitting\nLissajous curves are a family of parametric curves of the type\n\n```\nx = A sin(at+d)\ny = B sin(bt)\n```\n\nMore info: [https://en.wikipedia.org/wiki/Lissajous_curve](https://en.wikipedia.org/wiki/Lissajous_curve). Stripping the [animation parts of the code](https://github.com/sintefmath/Splipy/blob/master/examples/lissajous.py), one can generate these curves in the following way\n\n\n``` python\nfrom splipy import *\nimport numpy as np\nfrom fractions import gcd\n\ndef lissajous(a, b, d):\n  # request a,b integers, so we have closed, periodic curves\n  n = np.gcd(a,b)\n  N = (a/n) * (b/n) # number of periods before looping\n\n  # compute a set of interpolation points\n  numb_pts = max(3*N, 100) # using 3N interpolation points is decent enough\n  t = np.linspace(0,2*np.pi/n, numb_pts)\n  x = np.array([np.sin(a*t + d), np.sin(b*t)])\n\n# do a cubic curve interpolation with periodic boundary conditions\nmy_curve = curve_factory.cubic_curve(x.T, curve_factory.Boundary.PERIODIC)\n```\n\n![Missing Lissajous curve animation](http://i.imgur.com/HKr59BT.gif "lissajous(3,4,pi/2)")\n\nAnimation of the lissajous curve with a=3, b=4 and d=pi/2\n\n### Surface Sweep\n\nThis produces the trefoil knot shown above\n\n``` python\nfrom splipy import *\nfrom numpy import pi,cos,sin,transpose,array,sqrt\n\n# define a parametric representation of the trefoil knot (to be sampled)\ndef trefoil(u):\n  x = [41*cos(u) - 18*sin(  u) -  83*cos(2*u) - 83*sin(2*u) - 11*cos(3*u) + 27*sin(3*u),\n       36*cos(u) + 27*sin(  u) - 113*cos(2*u) + 30*sin(2*u) + 11*cos(3*u) - 27*sin(3*u),\n       45*sin(u) - 30*cos(2*u) + 113*sin(2*u) - 11*cos(3*u) + 27*sin(3*u)]\n  return transpose(array(x))\n\nknot_curve   = curve_factory.fit(trefoil, 0, 2*pi) # adaptive curve fit of trefoil knot\nsquare_curve = 15 * curve_factory.n_gon(4)         # square cross-section\nmy_surface   = surface_factory.sweep(crv, square)  # sweep out the surface\n```\n\n### Working with the controlpoints\n\n``` python\n>>> from splipy import *\n>>> my_curve = curve_factory.circle(r=3)\n>>> print(my_curve[0])\n[3. 0. 1.]\n>>> print(my_curve[1])\n[2.12132034 2.12132034 0.70710678]\n>>> for controlpoint in my_curve:\n...     print(controlpoint)\n[3. 0. 1.]\n[2.12132034 2.12132034 0.70710678]\n[0. 3. 1.]\n[-2.12132034  2.12132034  0.70710678]\n[-3.  0.  1.]\n[-2.12132034 -2.12132034  0.70710678]\n[ 0. -3.  1.]\n[ 2.12132034 -2.12132034  0.70710678]\n```\n\n### Creating STL files\n\nSTL files are used extensively for 3D representation and is one of the only supported formats for 3D printing.\n\n``` python\nfrom splipy.io import STL\nfrom splipy import surface_factory\n\n# create a NURBS torus\nmy_torus = surface_factory.torus(minor_r=1, major_r=4)\n\n# STL files are tessellated linear triangles. View with i.e. meshlab\nwith STL(\'torus.stl\') as my_file:\n    my_file.write(my_torus, n=(50, 150)) # specify resolution of 50x150 evaluation pts\n```\n\n**Torus tessellation as viewed in Meshlab**\n![Torus](images/torus.png)\n\n\n## Citations\n\nIf you use Splipy in your work, please consider citing\n[K. A. Johannessen and E. Fonn 2020 *J. Phys.: Conf. Ser.* **1669** 012032](https://iopscience.iop.org/article/10.1088/1742-6596/1669/1/012032/meta).\n',
    'author': 'Kjetil Andre Johannessen',
    'author_email': 'kjetijo@gmail.com',
    'maintainer': 'Kjetil Andre Johannessen',
    'maintainer_email': 'kjetijo@gmail.com',
    'url': 'https://github.com/SINTEF/Splipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}
from build_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
