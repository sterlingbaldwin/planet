import argparse
import sys
from pathlib import Path

from enum import Enum

class image_band(Enum):
    costal_blue = 1
    blue = 2
    green_1 = 3
    green = 4
    yellow = 5
    red = 6
    red_edge = 7
    nir = 8

# set the default threshold to a small non-zero value
DEFAULT_THRESHOLD = 0.1
DESCRIPTION = "find the ndvi values from a GEOTIFF image, optionally filtering for a given threshold value"
    

def find_ndvi(input_path: str, output_path: str, threshold=DEFAULT_THRESHOLD):
    # I like to put heavy inputs after the argument parsing is done,
    # that way if a user does "-h" they dont have to wait for 
    # modules to load
    import numpy as np
    from osgeo import gdal
    
    # load the dataset, and pull out the two bands we care about
    dataset = gdal.Open(input_path, gdal.GA_ReadOnly)

    # extract the values we care about from the dataset
    nir = dataset.GetRasterBand(image_band.nir.value).ReadAsArray()
    r   = dataset.GetRasterBand(image_band.red.value).ReadAsArray()

    # We need to find the ndvi values for the whole dataset, replacing
    # nans with 0s. This will result in some divide by 0s
    # so lets turn off that warning since it doesnt give
    # us any meaningful information
    np.seterr(invalid='ignore')
    ndvi = np.nan_to_num((nir - r)/(nir + r), nan=0)

    # apply our threshold and set the detected values
    ndvi[ndvi < threshold] = 0
    ndvi[ndvi >= threshold] = 255
    
    rows, cols = ndvi.shape
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(output_path, cols, rows, 1, gdal.GDT_UInt16)
    
    outdata.SetGeoTransform(dataset.GetGeoTransform())
    outdata.SetProjection(dataset.GetProjection())
    outdata.GetRasterBand(1).WriteArray(ndvi)
    outdata.FlushCache()
    return


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '--input_path', '-i',
        type=str,
        required=True,
        help="Path to input file")
    parser.add_argument(
        '--output_path', '-o',
        type=str,
        help='Path to where output images should be stored, default = ./ndvi.tif',
        default='ndvi.tif')
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=DEFAULT_THRESHOLD,
        help="filter the output image for values greater then the threshold")

    args = parser.parse_args()
    input_path = Path(args.input_path)
    if(not input_path.is_file()):
        print(f"Input file {input_path} does not exist!")
        return -1
    output_path = Path(args.output_path)
    if(output_path.is_file()):
        print(f"Output file {output_path} already exists, overwrite? y/[n]")
        if(input() not in ['y', 'Y']):
            return -1
        # remove the previous output file
        output_path.unlink()

    find_ndvi(str(input_path), str(output_path), args.threshold)
    return 0


if __name__ == "__main__":
    sys.exit(main())