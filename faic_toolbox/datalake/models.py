import requests
from typing import Optional
import os
import zipfile


def zipdir(path: str, ziph: zipfile.ZipFile):
    """Add file from directory to a zipfile

    Args:
        path (str): Directory path to zip
        ziph (zipfile.ZipFile): Zipfile
    """
    assert os.path.exists(path), "path must exist"
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
            )


def save_model(
    model_path: str,
    model_name: str,
    model_version: str,
    model_archive_path: Optional[str] = None,
    custom_headers: Optional[dict] = {},
) -> requests.models.Response:
    """Save a model dir to datalake

    Args:
        model_path (str): path to the model dir
        model_name (str): model name
        model_version (str): model version
        model_archive_path (Optional[str], optional): explicit path to save model zip. Defaults to None.
        custom_headers (Optional[dict], optional): custom headers. Defaults to {}.

    Returns:
        requests.models.Response: request response
    """
    from .config import datalake

    assert datalake is not None, "no datalake config found"
    assert os.path.exists(model_path), "model path must exist"

    if model_path.endswith(os.sep):
        model_path = model_path[:-1]

    if model_archive_path is None:
        model_archive_path = os.path.dirname(model_path)

    assert os.path.exists(model_archive_path), "model archive path must exist"

    zip_file_path = os.sep.join(
        [model_archive_path, f"{model_name}-{model_version}.zip"]
    )
    with zipfile.ZipFile(
        zip_file_path,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as zipf:
        zipdir(model_path, zipf)

    put_url_endpoint = f"{datalake.base_url}/model/{model_name}/{model_version}"
    url = requests.put(
        url=put_url_endpoint,
        headers={**datalake.get_headers, **custom_headers},
    ).json()["url"]

    with open(zip_file_path, "rb") as f:
        res = requests.put(
            url=url,
            data=f.read(),
            headers={"Content-Type": "application/zip"},
        )
    return res
