# Theia Dumper

<p align="center">
<img src="logo.png" width="320px">
<br>
<a href="https://forgemia.inra.fr/cdos-pub/theia-dumper/-/releases">
<img src="https://forgemia.inra.fr/cdos-pub/theia-dumper/-/badges/release.svg">
</a>
<a href="https://forgemia.inra.fr/cdos-pub/theia-dumper/-/commits/main">
<img src="https://forgemia.inra.fr/cdos-pub/theia-dumper/badges/main/pipeline.svg">
</a>
<a href="LICENSE">
<img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">
</a>
</p>

**Theia-dumper** enables to share Spatio Temporal Assets Catalogs (STAC) on the THEIA-MTP geospatial data center. If spatioreferenced raster assets are not in COG format, Theia-dumper generates COG before publishing catalogs.

## Installation and requirements

```commandline
pip install theia_dumper
```

To be able to upload data, make sure:

- you are [allowed to push](access.md)
- you have [credentials](https://cdos-pub.pages.mia.inra.fr/dinamis-sdk/credentials/)

## Create a STAC catalog

To see how to generate a pystac catalog, you can take a look [here](sample.md). 
You can find interesting tutorials in the [pystac documentation](https://pystac.readthedocs.io/en/stable/tutorials.html).

## Upload the catalog

Say you want to publish your local `collection.json`:
```commandLine
theia-dumper publish collection.json --storage_bucket sm1-gdc-example
```
With `smi-gdc-example` a bucket where you are [authorized to write](https://forgemia.inra.fr/cdos-pub/admin/cdos-ops).

Take a look closer in the [corresponding section](upload.md).

## Contribute

You can open issues or merge requests at 
[INRAE's gitlab](https://forgemia.inra.fr/cdos-pub/theia-dumper).

## Contact

Rémi Cresson at INRAE dot fr
