"""A collection of useful functions.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import json
import os

import nbformat
import requests
from nbformat import NotebookNode


def _read_notebook(fp: str) -> NotebookNode:
    return nbformat.read(fp, as_version=nbformat.NO_CONVERT)  # type: ignore


def notebook_to_cms(
    notebook_filename: str,
    endpoint: str,
    notebook_folder: str = "",
    display_name: str = "",
) -> str:
    r"""Sends all the markdown content of a notebook to a CMS endpoint.

    The CMS endpoint must satisfy two constraints:

    -   It must accept a post request with fields *id*, *displayName* and *markdown*.
    -   The response body must have a key *_id* whose value should be
        a unique string identifier of the content.

    Creating and updating content is handled in the following way:

    -   On the first request, an empty string is sent as *id*.
    -   If the request succeeds, the value of *_id* (in the response) is stored in a JSON file
        (created in the same directory as the notebook file).
    -   On subsequent requests, the stored value is sent as *id*.

    Args:
        notebook_filename (str): The name of the notebook file, e.g. `"my_notebook.ipynb"`.
        endpoint (str): The URL of the CMS endpoint.
        notebook_folder (str): Sets a custom notebook folder (as absolute path) containing the notebook file.
            If not set, the current folder is used.
        display_name (str): Send a custom *displayName* value to the CMS endpoint.
            If not set, the notebook filename is used (with the file extension removed,
            underscores replaced with spaces, and words capitalized).

    Returns:
        str: The response from the CMS endpoint, string-formatted.
    """
    if notebook_folder:
        os.chdir(notebook_folder)
    else:
        os.chdir(os.getcwd())

    basename = os.path.splitext(notebook_filename)[0]
    json_filename = basename + ".json"

    _id = ""
    if os.path.exists(json_filename):
        with open(json_filename) as file:
            _id = json.load(file)["_id"]

    if not display_name:
        display_name = basename.replace("_", " ").title()

    markdown = ""
    if os.path.exists(notebook_filename):
        notebook = _read_notebook(notebook_filename)
        markdown = "\n\n".join(
            cell.source for cell in notebook.cells if cell.cell_type == "markdown"
        )

    request_data = {"id": _id, "displayName": display_name, "markdown": markdown}
    response = requests.post(endpoint, data=request_data)

    return json.dumps(response, indent=4)
