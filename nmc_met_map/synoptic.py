# _*_ coding: utf-8 _*_

"""
Synoptic analysis or diagnostic maps for numeric weather model.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from nmc_met_io.retrieve_micaps_server import get_model_grid
import nmc_met_graphics.plot.synoptic as metp
from nmc_met_graphics.plot.util import add_logo, add_model_title
from nmc_met_map.utility import model_filename


def gh500_uv850_mslp(initial_time, fhour=0, model='ECMWF'):
    """
    Analysis 500hPa geopotential height, 850hPa wind barbs, and
    mean sea level pressure.

    :param initial_time: initial time, string or datetime ojbect.
                         like '18042008' or datetime(2018, 4, 20, 8).
    :param fhour: forecast hour.
    :param model: model name.
    :return: None.
    """

    # micaps data directory
    data_dirs = {'ECMWF': ['ECMWF_LR/HGT/500', 'ECMWF_LR/UGRD/850',
                           'ECMWF_LR/VGRD/850', 'ECMWF_LR/PRMSL'],
                 'GRAPES': ['GRAPES_GFS/HGT/500', 'GRAPES_GFS/UGRD/850',
                            'GRAPES_GFS/VGRD/850', 'GRAPES_GFS/PRMSL'],
                 'NCEP': ['NCEP_GFS/HGT/500', 'NCEP_GFS/UGRD/850',
                          'NCEP_GFS/VGRD/850', 'NCEP_GFS/PRMSL']}
    try:
        data_dir = data_dirs[model.strip().upper()]
    except KeyError:
        raise ValueError('Unknown model, choose ECMWF, GRAPES or NCEP.')

    # get filename
    filename = model_filename(initial_time, fhour)

    # retrieve data from micaps server
    gh500 = get_model_grid(data_dir[0], filename=filename)
    if gh500 is None:
        return
    init_time = gh500.coords['init_time'].values[0]
    u850 = get_model_grid(data_dir[1], filename=filename)
    if u850 is None:
        return
    v850 = get_model_grid(data_dir[2], filename=filename)
    if v850 is None:
        return
    mslp = get_model_grid(data_dir[3], filename=filename)
    if mslp is None:
        return

    # prepare data
    gh500 = {'lon': gh500.coords['lon'].values,
             'lat': gh500.coords['lat'].values,
             'data': gh500.values}
    uv850 = {'lon': u850.coords['lon'].values,
             'lat': u850.coords['lat'].values,
             'udata': u850.values, 'vdata': v850.values}
    mslp = {'lon': mslp.coords['lon'].values,
            'lat': mslp.coords['lat'].values, 'data': mslp.values}

    # draw figure
    fig = plt.figure(figsize=(10.5, 6))
    plotcrs = ccrs.AlbersEqualArea(
        central_latitude=45., central_longitude=100.,
        standard_parallels=[30., 60.])
    gs = mpl.gridspec.GridSpec(
        1, 2, width_ratios=[1, .02], bottom=.07,
        top=.99, hspace=0.01, wspace=0.01)

    # draw main figure
    ax = plt.subplot(gs[0], projection=plotcrs)
    add_model_title(
        '500-hPa Heights (m), 850-hPa Winds, MSLP (hPa)', init_time,
        model=model, fhour=fhour, fontsize=14)
    plots = metp.draw_gh500_uv850_mslp(
        ax, mslp=mslp, gh500=gh500, uv850=uv850,
        map_extent=[50, 150, 0, 65], regrid_shape=20)

    # add color bar
    cax = plt.subplot(gs[1])
    cb = plt.colorbar(plots['mslp'], cax=cax, orientation='vertical',
                      extendrect='True', ticks=plots['mslp'].levels)
    cb.set_label('Mean sea level pressure', size=12)

    # add logo
    add_logo(fig, alpha=0.7)

    # show figure
    gs.tight_layout(fig)
    plt.show()
