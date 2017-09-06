
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from glob import glob

ncfiles = glob('*.nc')

first = True
for nc in ncfiles:
    if first:
        ds_all = xr.open_dataset(nc)
        first = False
    else:
        ds = xr.open_dataset(nc)
        ds_all = xr.concat([ds_all,ds], dim='time')

figsetup = dict(cmap='RdBu',vmin=0,vmax=50,extend='neither')

scale = 0.7
figsetup['figsize'] = (10*scale,10*scale)
figsetup['x'] = 'lons'
figsetup['y'] = 'lats'
figsetup['col'] = 'time'  # <- faceting
figsetup['col_wrap'] = 2
figsetup['transform'] = ccrs.PlateCarree()
figsetup['subplot_kws'] = {'projection': ccrs.PlateCarree()}

plot_handle = ds_all.pwat.plot(**figsetup);

# opciones para la grilla
gl_setup = dict(crs=ccrs.PlateCarree(), 
                  draw_labels=False,
                  linewidth=2, 
                  color='gray', 
                  alpha=0.5, 
                  linestyle='--')

for ax in plot_handle.axes.flat:
    ax.add_feature(cartopy.feature.BORDERS)
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.set_extent([-100, -65, -45, -15]) # utilizar extent en lugar de xlim/ylim
    ax.set_aspect('equal','box-forced')  # <- obligatorio
    
    # formato de grilla lat/lon
    gl = ax.gridlines(**gl_setup)
    gl.xlabels_bottom = True
    gl.ylabels_left = True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
plt.show()