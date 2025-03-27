"""
Various functions to plot emission inventory data
"""

import numpy as np
from mayavi import mlab
from mayavi.sources.builtin_surface import BuiltinSurface


def world3d(lat, lon, lev, var_s, save=False):
    """Plot Earth and atmosphere (not to scale) to visualize
    aircraft emissions in 3D"""

    # define background & window size
    mlab.figure(1, bgcolor=(1.0, 1.0, 1.0), fgcolor=(0, 0, 0), size=(2700, 2700))

    # clear current figure
    mlab.clf()

    # Earth radius & redefining altitude levels
    var_r = 6371
    var_rdr = lev * 300 + var_r

    # display a semi-transparent sphere, for the surface of the Earth,
    # the tropopause and the stratopause
    surface_sphere = mlab.points3d(
        0,
        0,
        0,
        scale_mode="none",
        scale_factor=var_r * 2,
        color=(0.67, 0.77, 0.93),
        resolution=50,
        opacity=1,
        name="Earth",
    )

    # lighting spot settings
    surface_sphere.actor.property.specular = 0.2
    surface_sphere.actor.property.specular_power = 50
    surface_sphere.actor.property.backface_culling = True  # more beautiful

    mlab.points3d(
        0,
        0,
        0,
        scale_mode="none",
        scale_factor=(var_r + 4500) * 2,
        color=(0.3, 0.5, 1.0),
        resolution=50,
        opacity=0.1,
        name="Tropopause",
    )

    mlab.points3d(
        0,
        0,
        0,
        scale_mode="none",
        scale_factor=(var_r + 15000) * 2,
        color=(0.2, 0.77, 0.93),
        resolution=50,
        opacity=0.05,
        name="Stratopause",
    )

    # display continents outline
    continents = BuiltinSurface(source="earth", name="Continents")
    continents.data_source.on_ratio = 3  # level of detail
    continents.data_source.radius = var_r
    continents = mlab.pipeline.surface(continents, color=(0, 0, 0))

    # plot the equator and the tropics, orientation axes xyz and
    # normal line on south pole

    # xyz
    mlab.orientation_axes()

    # orthogonal line
    mlab.plot3d([0, 0], [0, 0], [0, -(var_r + 8000)], color=(0, 0, 0), tube_radius=None)

    # equator and the tropics
    theta = np.linspace(0, 2 * np.pi, 100)
    for angle in (-np.pi / 6, 0, np.pi / 6):
        var_x = np.cos(theta) * np.cos(angle) * var_r
        var_y = np.sin(theta) * np.cos(angle) * var_r
        var_z = np.ones_like(theta) * np.sin(angle) * var_r

        mlab.plot3d(var_x, var_y, var_z, color=(1, 1, 1), opacity=0.2, tube_radius=None)

    # display data points at lat lon positions

    # calculate from degrees to rad to xyz on a unit sphere

    lonr = lon * np.pi / 180  # degrees to rad
    latr = lat * np.pi / 180  # degrees to rad

    var_x = np.cos(latr) * np.cos(lonr) * var_rdr
    var_y = np.cos(latr) * np.sin(lonr) * var_rdr
    var_z = np.sin(latr) * var_rdr

    pts = mlab.points3d(
        var_x,
        var_y,
        var_z,
        var_s,
        scale_mode="none",
        mode="cube",
        colormap='Reds',
        scale_factor=0.04 * var_r,
        opacity=0.1,
        resolution=20,
        vmin=np.min(var_s)*2,
        vmax=np.max(var_s)/2
    )

    #mlab.pipeline.volume(mlab.pipeline.gaussian_splatter(pts))
    if save:
        mlab.savefig("./output_3d.png")

    mlab.show()
