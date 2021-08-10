# PyBites YouTube Thumbnail creator

Simple script that uses [Pillow](https://pillow.readthedocs.io/en/stable/) to generate thumbnail images for [our YouTube channel](https://www.youtube.com/channel/UCBn-uKDGsRBfcB0lQeOB_gA).

## Usage

To start simple the script relies on short titles it splits by newline, for example:

```
python script.py "PyBites\nDev Tools\nTraining"
```

... creates this image in the `images/` output folder:

![example output image](images/example.png)
