# smooth-image

> by Andrew D'Amario © January 2023

Image de-noising script to remove artifacts and smoothen images while preserving definition and quality.

## Usage

```shell
python smooth-image.py IMAGE RADIUS THRESHOLD
```

- IMAGE: image filename (path), supports png, jpg, and bmp but **png** is recommended
- RADIUS: radius of pixels to smoothen
- THRESHOLD: threshold of colour difference to smoothen

**Output:** Image with the same filename-smooth and image type.

## Examples

**Original image:**

![](media/triangles-preview.png)

**Command:**
```shell
python smooth-image.py media/triangles.png 2 80
```
**Smoothened image:**

![](media/triangles-smooth-preview.png)

---

**Original image:**

![](media/triangles-full.png)

**Command:**
```shell
python smooth-image.py media/triangles-full.png 10 80
```
**Smoothened image:**

![](media/triangles-full-smooth.png)

---

**Original image:**

![](media/Catullus.png)

**Command:**
```shell
python smooth-image.py media/Catullus.png 10 80
```
**Smoothened image:**

![](media/Catullus-smooth.png)


### Credits
- https://en.wikipedia.org/wiki/Catullus
- https://wallpapersden.com/3d-triangle-cube-wallpaper/1920x1080/

