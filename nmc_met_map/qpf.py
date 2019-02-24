# _*_ coding: utf-8 _*_

"""
  Quantitative precipitation forecast of numerical weather models.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from nmc_met_io.retrieve_micaps_server import get_model_grid
from nmc_met_graphics.plot.china_map import add_china_map_2cartopy
from nmc_met_graphics.plot.util import add_logo, add_model_title
from nmc_met_map.utility import model_filename


def qpf_24h(initial_time, fhour=0, model='ECMWF',
            map_center=(117, 39), map_width=12):
    """
    Draw 24h accumulated QPF.

    Arguments:
        initial_time {string or datetime object} -- model initital time,
            like '18042008' or datetime(2018, 4, 20, 8).

    Keyword Arguments:
        fhour {int} -- model initial time (default: {0})
        model {str} -- model name (default: {'ECMWF'})
    """

    # micaps data directory
    data_dirs = {'ECMWF': ['ECMWF_HR/RAIN24']}
    try:
        data_dir = data_dirs[model.strip().upper()]
    except KeyError:
        raise ValueError('Unknown model, choose ECMWF, GRAPES or NCEP.')

    # get file name
    filename = model_filename(initial_time, fhour)

    # retrieve data from micaps server
    rain24 = get_model_grid(data_dir[0], filename=filename)
    if rain24 is None:
        print('Can not retrieve {} from Micaps server.'.format(filename))
        return
    init_time = rain24.coords['init_time'].values[0]
    rain24 = {'lon': rain24.coords['lon'].values,
              'lat': rain24.coords['lat'].values,
              'data': np.squeeze(rain24.values)}

    # set up map projection
    datacrs = ccrs.PlateCarree()
    plotcrs = ccrs.AlbersEqualArea(
        central_latitude=map_center[1], central_longitude=map_center[0],
        standard_parallels=[30., 60.])

    # set up figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_axes([0, 0, 1, 1], projection=plotcrs)

    # add model title
    add_model_title(
        '24h accumulated QPF', init_time, model=model,
        fhour=fhour, fontsize=18, multilines=True, atime=24)

    # add map background
    map_extent = (
        map_center[0] - map_width/2.0, map_center[0] + map_width/2.0,
        map_center[1] - map_width/2.0, map_center[1] + map_width/2.0)
    ax.set_extent(map_extent, crs=datacrs)
    land_50m = cfeature.NaturalEarthFeature(
        'physical', 'land', '50m', edgecolor='face',
        facecolor=cfeature.COLORS['land'])
    ax.add_feature(land_50m)
    add_china_map_2cartopy(
        ax, name='province', edgecolor='darkcyan',
        lw=1, zorder=100)

    # draw QPF
    clevs = [0.1, 10, 25, 50, 100, 250]
    colors = ["#88F492", "#00A929", "#2AB8FF", "#1202FC", "#FF04F4", "#850C3E"]
    cmap, norm = mpl.colors.from_levels_and_colors(clevs, colors, extend='max')
    ax.pcolormesh(
        rain24['lon'], rain24['lat'], rain24['data'], norm=norm,
        cmap=cmap, transform=datacrs, zorder=2)

    # add custom legend
    legend_elements = [
        Patch(facecolor=colors[0], label='0.1~10mm'),
        Patch(facecolor=colors[1], label='10~25mm'),
        Patch(facecolor=colors[2], label='25~50mm'),
        Patch(facecolor=colors[3], label='50~100mm'),
        Patch(facecolor=colors[4], label='100~250mm'),
        Patch(facecolor=colors[5], label='>250mm')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=16)

    # add logo
    add_logo(fig, alpha=0.7)

    # show figure
    ax.set_adjustable('datalim')
    plt.show()
