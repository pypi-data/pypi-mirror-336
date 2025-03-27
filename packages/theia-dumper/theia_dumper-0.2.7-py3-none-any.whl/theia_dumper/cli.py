"""Theia-dumper Command Line Interface."""

import os
import tempfile
import subprocess
import click

from . import diff
from .stac import (
    StacTransactionsHandler,
    StacUploadTransactionsHandler,
    DEFAULT_S3_EP,
    DEFAULT_STAC_EP,
    DEFAULT_S3_STORAGE,
)


@click.group()
def theia_dumper() -> None:
    """Theia dumper CLI tool."""


@theia_dumper.command(context_settings={"show_default": True})
@click.argument("stac_obj_path")
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
@click.option(
    "--storage_endpoint",
    type=str,
    help="Storage endpoint assets will be sent to",
    default=DEFAULT_S3_EP,
)
@click.option(
    "-b",
    "--storage_bucket",
    help="Storage bucket assets will be sent to",
    type=str,
    default=DEFAULT_S3_STORAGE,
)
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite assets if already existing",
)
@click.option(
    "--keep_cog_dir",
    help="Set a directory to keep converted COG files",
    type=str,
    nargs=1,
    default="",
)
def publish(
    stac_obj_path: str,
    stac_endpoint: str,
    storage_endpoint: str,
    storage_bucket: str,
    overwrite: bool,
    keep_cog_dir: str,
):
    """Publish a STAC object (collection or item collection)."""
    StacUploadTransactionsHandler(
        stac_endpoint=stac_endpoint,
        sign=False,
        storage_endpoint=storage_endpoint,
        storage_bucket=storage_bucket,
        assets_overwrite=overwrite,
        keep_cog_dir=keep_cog_dir,
    ).load_and_publish(stac_obj_path)


@theia_dumper.command(context_settings={"show_default": True})
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
@click.option("-c", "--col_id", type=str, help="STAC collection ID", required=True)
@click.option("-i", "--item_id", type=str, default=None, help="STAC item ID")
@click.option("-s", "--sign", is_flag=True, default=False, help="Sign assets HREFs")
@click.option("-p", "--pretty", is_flag=True, default=False, help="Pretty indent JSON")
@click.option("-o", "--out_json", type=str, help="Output .json file", required=True)
def grab(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    stac_endpoint: str,
    col_id: str,
    item_id: str,
    sign: bool,
    pretty: bool,
    out_json: str,
):
    """Grab a STAC object (collection, or item) and save it as .json."""
    StacTransactionsHandler(stac_endpoint=stac_endpoint, sign=sign).load_and_save(
        col_id=col_id, obj_pth=out_json, item_id=item_id, pretty=pretty
    )


@theia_dumper.command(context_settings={"show_default": True})
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
@click.option("-c", "--col_id", type=str, help="STAC collection ID", required=True)
@click.option("-i", "--item_id", type=str, default=None, help="STAC item ID")
def edit(stac_endpoint: str, col_id: str, item_id: str):
    """Edit a STAC object (collection, or item)."""
    with tempfile.NamedTemporaryFile(suffix=".json") as tf:
        StacTransactionsHandler(stac_endpoint=stac_endpoint, sign=False).load_and_save(
            col_id=col_id, obj_pth=tf.name, item_id=item_id, pretty=True
        )
        editor = os.environ.get("EDITOR") or "vi"
        subprocess.run([editor, tf.name], check=False)
        StacTransactionsHandler(
            stac_endpoint=stac_endpoint, sign=False
        ).load_and_publish(obj_pth=tf.name)


@theia_dumper.command(context_settings={"show_default": True})
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
@click.option("-c", "--col_id", type=str, help="STAC collection ID", required=True)
@click.option("-i", "--item_id", type=str, default=None, help="STAC item ID")
def delete(
    stac_endpoint: str,
    col_id: str,
    item_id: str,
):
    """Delete a STAC object (collection or item)."""
    StacTransactionsHandler(stac_endpoint=stac_endpoint, sign=False).delete_item_or_col(
        col_id=col_id, item_id=item_id
    )


@theia_dumper.command(context_settings={"show_default": True})
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
def list_cols(
    stac_endpoint: str,
):
    """List collections."""
    cols = list(
        StacTransactionsHandler(
            stac_endpoint=stac_endpoint, sign=False
        ).client.get_collections()
    )
    print(f"Found {len(cols)} collection(s):")
    for col in sorted(cols, key=lambda x: x.id):
        print(f"\t{col.id}")


@theia_dumper.command(context_settings={"show_default": True})
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
@click.option("-c", "--col_id", type=str, help="STAC collection ID", required=True)
@click.option(
    "-m", "--max_items", type=int, help="Max number of items to display", default=20
)
@click.option("-s", "--sign", is_flag=True, default=False, help="Sign assets HREFs")
def list_col_items(stac_endpoint: str, col_id: str, max_items: int, sign: bool):
    """List collection items."""
    items = StacTransactionsHandler(stac_endpoint=stac_endpoint, sign=sign).get_items(
        col_id=col_id, max_items=max_items
    )
    print(f"Found {len(items)} item(s):")
    for item in items:
        print(f"\t{item.id}")


@theia_dumper.command(context_settings={"show_default": True})
@click.option(
    "--stac_endpoint",
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default=DEFAULT_STAC_EP,
)
@click.option("-p", "--col_path", type=str, help="Local collection path", required=True)
@click.option(
    "-r",
    "--remote_id",
    type=str,
    help="Remote collection ID. If not specified, will use local collection ID",
    required=False,
)
def collection_diff(
    stac_endpoint: str,
    col_path: str,
    remote_id: str = "",
):
    """List collection items."""
    diff.compare_local_and_upstream(
        StacTransactionsHandler(stac_endpoint=stac_endpoint, sign=False),
        col_path,
        remote_id,
    )
