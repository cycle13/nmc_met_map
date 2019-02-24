# _*_ coding: utf-8 _*_
"""
  Weather maps for mesoscale weather models.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from metpy.plots import colortables
from nmc_met_io.retrieve_micaps_server import get_model_grid
from nmc_met_graphics.plot.china_map import add_china_map_2cartopy
from nmc_met_graphics.plot.util import add_model_title, get_model_time_stamp, add_titlebox
from nmc_met_map.utility import model_filename


def cref_uv850(initial_time, fhour=0, model='ShangHai',
               map_center=(117, 39), map_width=12, draw_wind=False):
    """
    Analysis composite reflectivity and 850hPa wind.
    
    Arguments:
        initial_time {string or datetime}} -- 
            initial time, string or datetime ojbect.
            like '18042008' or datetime(2018, 4, 20, 8).
    
    Keyword Arguments:
        fhour {int} -- forecast hour (default: {0})
        model {str} -- model name (default: {'ShangHai'})
        map_center {tuple} -- map center (default: {(117, 39)})
        map_width {int} -- map width (default: {12})
        draw_wind {bool} -- draw 850hPa wind or not (default: {False})
    
    Raises:
        ValueError -- [description]
    """

    # micaps data directory
    data_dirs = {
        'SHANGHAI': ['SHANGHAI_HR/COMPOSITE_REFLECTIVITY/ENTIRE_ATMOSPHERE',
                     'SHANGHAI_HR/UGRD/850', 'SHANGHAI_HR/VGRD/850'],
        'BEIJING': ['BEIJING_MR/COMPOSITE_REFLECTIVITY/ENTIRE_ATMOSPHERE',
                    'BEIJING_MR/UGRD/850', 'BEIJING_MR/VGRD/850'],
        'GRAPES_MESO': ['GRAPES_MESO_HR/RADAR_COMBINATION_REFLECTIVITY',
                        'GRAPES_MESO_HR/UGRD/850', 'GRAPES_MESO_HR/VGRD/850'],
        'GRAPES_3KM': ['GRAPES_3KM/RADAR_COMBINATION_REFLECTIVITY',
                       'GRAPES_3KM/UGRD/850', 'GRAPES_3KM/VGRD/850']}
    try:
        data_dir = data_dirs[model.strip().upper()]
    except KeyError:
        raise ValueError('Unknown model, choose ShangHai, BeiJing, Grapes_meso of Grapes_3km.')
        
    # get filename
    filename = model_filename(initial_time, fhour)
    
    # retrieve data from micaps server
    cref = get_model_grid(data_dir[0], filename=filename)
    if cref is None:
        return
    init_time = cref.coords['init_time'].values[0]
    if draw_wind:
        u850 = get_model_grid(data_dir[1], filename=filename)
        if u850 is None:
            return
        v850 = get_model_grid(data_dir[2], filename=filename)
        if v850 is None:
            return
    
    # prepare data
    data = np.ma.masked_array(cref.values)
    data[data == 9999] = np.ma.masked
    data[data < 10] = np.ma.masked
    cref_data = {'lon':cref.coords['lon'].values, 
                 'lat':cref.coords['lat'].values, 
                 'data':np.squeeze(data)}
    if draw_wind:
        uv850 = {'lon': u850.coords['lon'].values,
                 'lat': u850.coords['lat'].values,
                 'udata': np.squeeze(u850.values),
                 'vdata': np.squeeze(v850.values)}
    
    # set up map projection
    datacrs = ccrs.PlateCarree()
    plotcrs = ccrs.AlbersEqualArea(
        central_latitude=map_center[1], central_longitude=map_center[0],
        standard_parallels=[30., 60.])
    
    # set up figure
    fig = plt.figure(figsize=(12, 9))
    gs = mpl.gridspec.GridSpec(
        1, 2, width_ratios=[1, .03], 
        bottom=.01, top=.99, hspace=0.01, wspace=0.01)
    ax = plt.subplot(gs[0], projection=plotcrs)
    
    # add model title
    add_model_title(
        'CREF (dBz), 850-hPa Winds', init_time, model=model,
        fhour=fhour, fontsize=18, multilines=True)
    
    # add map background
    map_extent = (
        map_center[0] - map_width/2.0, map_center[0] + map_width/2.0,
        map_center[1] - map_width/3.0, map_center[1] + map_width/3.0)
    ax.set_extent(map_extent, crs=datacrs)
    add_china_map_2cartopy(
        ax, name='province', edgecolor='black',
        lw=2, zorder=100)
    
    # draw composite reflectivity
    x, y = np.meshgrid(cref_data['lon'], cref_data['lat'])
    norm, cmap = colortables.get_with_steps('NWSReflectivity', 12, 4)
    pm = ax.pcolormesh(x, y, cref_data['data'], norm=norm, cmap=cmap, transform=datacrs)
    cax = plt.subplot(gs[1])
    cb = plt.colorbar(pm, cax=cax, orientation='vertical', extendrect='True')
    cb.set_label('Composite reflectivity', size=12)

    # draw wind vector
    if draw_wind:
        x, y = np.meshgrid(uv850['lon'], uv850['lat'])
        ax.quiver(x, y, uv850['udata'], uv850['vdata'],
                  transform=datacrs, regrid_shape=25)
    
    # show figure
    gs.tight_layout(fig)
    plt.show()


def cref_uv850_compare(initial_time, fhour=0, map_center=(117, 39), map_width=12, draw_wind=False):
    """
    Compare mesoscale model's composite reflectivity.
    
    Arguments:
        initial_time {string or datetime}} -- 
            initial time, string or datetime ojbect.
            like '18042008' or datetime(2018, 4, 20, 8).
    
    Keyword Arguments:
        fhour {int} -- forecast hour (default: {0})
        map_center {tuple} -- map center (default: {(117, 39)})
        map_width {int} -- map width (default: {12})
        draw_wind {bool} -- draw 850hPa wind or not (default: {False})
    """

    # micaps data directory
    data_dirs = {'SHANGHAI': ['SHANGHAI_HR/COMPOSITE_REFLECTIVITY/ENTIRE_ATMOSPHERE',
                              'SHANGHAI_HR/UGRD/850', 'SHANGHAI_HR/VGRD/850'],
                 'BEIJING': ['BEIJING_MR/COMPOSITE_REFLECTIVITY/ENTIRE_ATMOSPHERE',
                             'BEIJING_MR/UGRD/850', 'BEIJING_MR/VGRD/850'],
                 'GRAPES_MESO': ['GRAPES_MESO_HR/RADAR_COMBINATION_REFLECTIVITY',
                                 'GRAPES_MESO_HR/UGRD/850', 'GRAPES_MESO_HR/VGRD/850'],
                 'GRAPES_3KM': ['GRAPES_3KM/RADAR_COMBINATION_REFLECTIVITY',
                                'GRAPES_3KM/UGRD/850', 'GRAPES_3KM/VGRD/850']}
    
    # get filename
    filename = model_filename(initial_time, fhour)
    
    # set up map projection
    datacrs = ccrs.PlateCarree()
    plotcrs = ccrs.AlbersEqualArea(
        central_latitude=map_center[1], central_longitude=map_center[0],
        standard_parallels=[30., 60.])
    
    # set up figure
    fig = plt.figure(figsize=(16, 12))
    axes_class = (GeoAxes, dict(map_projection=plotcrs))
    grid = AxesGrid(fig, 111, axes_class=axes_class, nrows_ncols=(2, 2),
                    axes_pad=0.05, cbar_location='right', cbar_mode='single',
                    cbar_pad=0.05, label_mode='')
    
    # loop every data directory
    for index, key in enumerate(data_dirs):
        # get axis and data directory
        ax = grid[index]
        data_dir = data_dirs[key]
        
        # retrieve data from micaps server
        cref = get_model_grid(data_dir[0], filename=filename)
        if cref is None:
            return
        init_time = cref.coords['init_time'].values[0]
        if draw_wind:
            u850 = get_model_grid(data_dir[1], filename=filename)
            if u850 is None:
                return
            v850 = get_model_grid(data_dir[2], filename=filename)
            if v850 is None:
                return
            
        # add title
        if index == 0:
            initial_str, fhour_str, valid_str = get_model_time_stamp(init_time, fhour)
            fig.suptitle('CREF (dBz), 850-hPa Winds    ' + initial_str + '; ' + fhour_str + '; ' + valid_str,
                         x=0.5, y=0.9, fontsize=16)
    
        # prepare data
        data = np.ma.masked_array(cref.values)
        data[data == 9999] = np.ma.masked
        data[data < 10] = np.ma.masked
        cref_data = {'lon':cref.coords['lon'].values, 
                     'lat':cref.coords['lat'].values, 
                     'data':np.squeeze(data)}
        if draw_wind:
            uv850 = {'lon': u850.coords['lon'].values,
                     'lat': u850.coords['lat'].values,
                     'udata': np.squeeze(u850.values),
                     'vdata': np.squeeze(v850.values)}
    
        # add map background
        map_extent = (
            map_center[0] - map_width/2.0, map_center[0] + map_width/2.0,
            map_center[1] - map_width/3.0, map_center[1] + map_width/3.0)
        ax.set_extent(map_extent, crs=datacrs)
        add_china_map_2cartopy(
            ax, name='province', edgecolor='black',
            lw=2, zorder=100)
    
        # draw composite reflectivity
        x, y = np.meshgrid(cref_data['lon'], cref_data['lat'])
        norm, cmap = colortables.get_with_steps('NWSReflectivity', 12, 4)
        pm = ax.pcolormesh(x, y, cref_data['data'], norm=norm, cmap=cmap, transform=datacrs)

        # draw wind vector
        if draw_wind:
            x, y = np.meshgrid(uv850['lon'], uv850['lat'])
            ax.quiver(x, y, uv850['udata'], uv850['vdata'],
                      transform=datacrs, regrid_shape=25)
            
        # add title
        add_titlebox(ax, key)
            
    # add color bar
    cbar = grid.cbar_axes[0].colorbar(pm)
    
    # show figure
    plt.show()
