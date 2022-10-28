# Image Converter
Convert HEIC, Gif, BMP, PDF, EPS (Postscript), PSD (Photoshop), SVG, Tiff formats into JPG or PNG.

<br/>

## Convert a file
```
python3 src/convert.py -d='{JSON_DATA}'
```

<br />

## Options in JSON
```json
{
	"src": "/src/src_image.heic", // Path to the source image
	"dest": "src/result_image.png", // Path to the result image
	"maxSize": 1200, // Max width in pixels or False
	"type": "png", // png or jpg
	"removeSrc": true // True or False
}
```

<br />

## Result in JSON
```json
{
	"state": true, // True or False
	"size":[1200,1200], // [Width, height]
	"msg": "Success" // Outcome message if an error has occurred
}
```

<br />
<br />
<br />
<br />

## MIT License

Copyright (c) Surfy • [surfy.one](https://surfy.one)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.