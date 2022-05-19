## Envirnment setup

The dependecies for this are very light, Im only using numpy and gdal, but for convenience if you're missing them, you can create a new env with them included by running the following.

    conda create -n ndvi -c conda-forge numpy gdal

## Usage

```
usage: ndvi.py [-h] --input_path INPUT_PATH [--output_path OUTPUT_PATH] [--threshold THRESHOLD]

find the ndvi values from a GEOTIFF image, optionally filtering for a given threshold value

optional arguments:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH, -i INPUT_PATH
                        Path to input file
  --output_path OUTPUT_PATH, -o OUTPUT_PATH
                        Path to where output images should be stored, default = ./ndvi.tif
  --threshold THRESHOLD, -t THRESHOLD
                        filter the output image for values greater then the threshold
```

