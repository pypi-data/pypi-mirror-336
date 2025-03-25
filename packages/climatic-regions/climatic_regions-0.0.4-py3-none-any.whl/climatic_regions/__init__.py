__all__ = ["__version__"]

from math import ceil

import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT
from rio_tiler.reader import point
from skimage.transform import resize
from shapely.geometry import Point
import geopandas as gpd
import importlib.resources as pkg_resources

METEO_PATHS = {}

# NOTE: we need to use deprecated pkg_resources functionality
# because we need to support Python 3.8 on OpenEO
for year in range(2018, 2024):
    with pkg_resources.path(
        "climatic_regions.annual_agera_embeddings_v1",
        f"meteo_biomes_{year}.tif",
    ) as resource_path:
        METEO_PATHS[year] = resource_path


def buffer_bounds(bounds, buffer):
    bounds = np.array(bounds)
    bounds += np.array([-buffer, -buffer, buffer, buffer])
    return bounds.tolist()


def _read_warped_tif(
    fn, bounds, epsg, out_shape=None, resampling=Resampling.cubic_spline
):
    with rasterio.open(fn) as src:
        with WarpedVRT(
            src,
            crs=CRS.from_epsg(epsg),
            bounds=bounds,
            resampling=resampling,
            dtype="float32",
        ) as vrt:
            meteo = vrt.read(
                window=vrt.window(*bounds),
                out_shape=out_shape,
            )

        meteo[meteo == src.nodata] = np.nan
        meteo *= src.scales[0]

    return meteo


def shape_from_bounds(bounds, res):
    height = int(ceil((bounds[3] - bounds[1]) / res))
    width = int(ceil((bounds[2] - bounds[0]) / res))
    return height, width


def read_warped_lowres_tif(
    fn,
    bounds,
    epsg,
    resolution=10,
    bounds_buffer=None,
    resampling=Resampling.cubic_spline,
    order=3,
):
    buf_bounds = buffer_bounds(bounds, bounds_buffer)
    out_shape_low_res = None

    data = _read_warped_tif(
        fn,
        buf_bounds,
        epsg,
        out_shape=out_shape_low_res,
        resampling=resampling,
    )

    out_shape = shape_from_bounds(buf_bounds, resolution)
    high_res_data = np.zeros((data.shape[0], *out_shape))
    for i in range(data.shape[0]):
        high_res_data[i] = resize(
            data[i],
            out_shape,
            order=order,
            anti_aliasing=True,
            preserve_range=True,
        )

    buffered_pixels = bounds_buffer // resolution

    high_res_data = high_res_data[
        :, buffered_pixels:-buffered_pixels, buffered_pixels:-buffered_pixels
    ]

    return high_res_data


def load_meteo_embeddings(
    bounds, epsg, year, resolution=10, bounds_buffer=3000, order=3
):
    return read_warped_lowres_tif(
        METEO_PATHS[year],
        bounds,
        epsg,
        resolution=resolution,
        bounds_buffer=bounds_buffer,
        order=order,
    )


def load_meteo_point(lon, lat, year):
    with rasterio.open(METEO_PATHS[year]) as src:
        value = point(src, (lon, lat))
    return value.data


def lat_lon_to_unit_sphere(lat, lon):
    """
    Convert latitude and longitude arrays (in degrees) to 3D unit sphere coordinates (x, y, z).

    Parameters:
    lat (array-like): Array of latitudes in degrees.
    lon (array-like): Array of longitudes in degrees.

    Returns:
    tuple: Three NumPy arrays (x, y, z) with the same shape as the input lat and lon arrays.
    """
    # Convert latitude and longitude from degrees to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Calculate x, y, z on the unit sphere
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)

    return x, y, z


def load_latlon(bounds, epsg, resolution=10, steps=5):
    """
    Returns a lat, lon feature from the given bounds/epsg.

    This provide a coarse (but relatively fast) approximation to generate
    lat lon layers for each pixel.

    'steps' specifies how many points per axis should be use to perform
    the mesh approximation of the canvas
    """

    xmin, ymin, xmax, ymax = bounds
    out_shape = (
        int(np.floor((ymax - ymin) / resolution)),
        int(np.floor((xmax - xmin) / resolution)),
    )

    xx = np.linspace(xmin + resolution / 2, xmax - resolution / 2, steps)
    yy = np.linspace(ymax - resolution / 2, ymin + resolution / 2, steps)

    xx = np.broadcast_to(xx, [steps, steps]).reshape(-1)
    yy = np.broadcast_to(yy, [steps, steps]).T.reshape(-1)

    points = [Point(x0, y0) for x0, y0 in zip(xx, yy)]

    gs = gpd.GeoSeries(points, crs=CRS.from_epsg(epsg))
    gs = gs.to_crs(epsg=4326)

    lon_mesh = gs.apply(lambda p: p.x).values.reshape((steps, steps))
    lat_mesh = gs.apply(lambda p: p.y).values.reshape((steps, steps))

    lon = resize(lon_mesh, out_shape, order=1, mode="edge")
    lat = resize(lat_mesh, out_shape, order=1, mode="edge")

    return np.stack([lat, lon], axis=0).astype(np.float32)


def load_xyz(bounds, epsg, resolution=10, steps=5):
    """
    Returns a x, y, z feature from the given bounds/epsg.

    This provide a coarse (but relatively fast) approximation to generate
    x, y, z (lat lon on a unit sphere) layers for each pixel.

    'steps' specifies how many points per axis should be use to perform
    the mesh approximation of the canvas
    """

    latlon = load_latlon(bounds, epsg, resolution, steps)
    x, y, z = lat_lon_to_unit_sphere(latlon[0], latlon[1])

    return np.stack([x, y, z], axis=0).astype(np.float32)
