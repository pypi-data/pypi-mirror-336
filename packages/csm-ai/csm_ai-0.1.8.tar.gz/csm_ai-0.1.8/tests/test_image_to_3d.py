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


_ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# TODO: use env variable
client = CSMClient(
    #api_key='3431Aa1a2aeAD1350faC8Efdc387C686', Nitin (prod)
    api_key='3C8A79cB792F61B6744B9A9E08344aaf', # admin (prod)
)

# @pytest.mark.parametrize("a,b,expected", [(0, 0, 0), (2, 2, 4), (10, 5, 15)])
# def test_add_numbers_parametrized(a, b, expected):
#     assert add_numbers(a, b) == expected


def test_geo():
    image_path = os.path.join(_ASSETS_DIR, 'flip12.png')

    with tempfile.TemporaryDirectory() as output_dir:
        result = client.image_to_3d(
            image_path,
            mesh_format='glb',
            output=output_dir,
            verbose=True,
            # API arguments
            generate_texture=False,
        )
        assert os.path.isfile(result.mesh_path)


@pytest.mark.skip()
def test_baked_texture():
    image_path = os.path.join(_ASSETS_DIR, 'flip12.png')

    with tempfile.TemporaryDirectory() as output_dir:
        result = client.image_to_3d(
            image_path,
            mesh_format='glb',
            output=output_dir,
            verbose=True,
            # optional arguments
            generate_texture=True, 
            texture_model='baked',
        )
        assert os.path.isfile(result.mesh_path)


@pytest.mark.skip()
def test_pbr_texture():
    image_path = os.path.join(_ASSETS_DIR, 'flip12.png')

    with tempfile.TemporaryDirectory() as output_dir:
        result = client.image_to_3d(
            image_path,
            mesh_format='glb',
            output=output_dir,
            verbose=True,
            # optional arguments
            generate_texture=True, 
            texture_model='pbr',
        )
        assert os.path.isfile(result.mesh_path)