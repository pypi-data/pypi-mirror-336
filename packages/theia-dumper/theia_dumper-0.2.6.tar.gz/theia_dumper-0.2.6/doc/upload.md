# Upload the collection

## Command line interface (CLI)

In the `theia-dumper` CLI, the `--storage_bucket` argument concatenates the actual bucket and the path prefix.

For instance if Jacques wants to upload a collection in `sm1-gdc/some-path`, he will have to call:

```commandLine
theia-dumper collection.json --storage_bucket sm1-gdc/some-path
```

In case he has an item, or an item collection, he can use the same command:

```commandLine
theia-dumper item.json --storage_bucket sm1-gdc/some-path
```
```commandLine
theia-dumper item-collection.json --storage_bucket sm1-gdc/some-path
```

For more details, see [this page](cli-ref.md).


## Python

Another way is to use the python API:

```python
from theia_dumper.stac import TransactionsHandler

handler = TransactionsHandler(
    stac_endpoint="https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr",
    storage_endpoint="https://s3-data.meso.umontpellier.fr",
    storage_bucket="sm1-gdc/some-path",
    assets_overwrite=True
)
handler.load_and_publish("/tmp/collection.json")
```
