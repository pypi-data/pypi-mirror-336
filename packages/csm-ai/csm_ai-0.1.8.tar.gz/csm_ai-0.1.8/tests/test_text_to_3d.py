"""
Run from /path/to/csm-ai:
    pytest
Disable capture-output ('show output' option):
    pytest -s
"""
import os
import tempfile
import pytest
from csm import CSMClient

# TODO: use env variable
client = CSMClient(
    #api_key='3431Aa1a2aeAD1350faC8Efdc387C686', Nitin (prod)
    api_key='3C8A79cB792F61B6744B9A9E08344aaf', # admin (prod)
)

# @pytest.mark.parametrize("a,b,expected", [(0, 0, 0), (2, 2, 4), (10, 5, 15)])
# def test_add_numbers_parametrized(a, b, expected):
#     assert add_numbers(a, b) == expected


# @pytest.mark.skip()
def test_geo():
    prompt = "3d asset of a character head, cartoon style, low poly, front view"

    with tempfile.TemporaryDirectory() as output_dir:
        result = client.text_to_3d(
            prompt,
            style_id="",
            guidance=6,
            mesh_format='glb',
            output=output_dir,
            verbose=True,
            # API arguments
            generate_texture=False,
        )
        assert os.path.isfile(result.mesh_path)
