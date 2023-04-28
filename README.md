
# Mixamo Bot that Automatically Downloads Mixamo Data

The scripts of this project automatically download the 3d bodies of some characters and the 3d animations as FBX files
from [Mixamo's website](https://www.mixamo.com).

There are two main scripts:
- [download_characters.py](download_characters.py);
- [download_animations.py](download_animations.py).

Both are Python scripts that use the Mixamo bot (calapy.mixamo.MixamoBot) of [CalaPy](https://pypi.org/project/calapy),
a Python library. Calapy is a collection of Python functions that I personally coded and that I tend to reuse in
different projects. The Mixamo bot is dependent on [Selenium](https://selenium-python.readthedocs.io), a Python library
to automatically control the web browser.

[download_characters.py](download_characters.py) downloads the 3d bodies of the characters, while
[download_animations.py](download_animations.py) downloads the 3d animations of the characters as 3d skeletons. In
another project, I scripted [Blender 3D](https://www.blender.org/), a 3d software, to animate the 3d characters with
their 3d animated skeletons and render multiple videos of the same actions from different viewpoints.

Warming: the scripts may crash in the future if they change the Mixamo website. So, if you get any errors, please,
report them to me and I will update the code.
