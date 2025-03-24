from pathlib import Path

import pooch
import pytest

HERE = Path(__file__).parent.absolute()
TEST_DATA_FOLDER = HERE / "test_resources"


HB0707_RAW = pooch.create(
    path=pooch.os_cache("water-column-sonar-processing"),
    base_url="https://noaa-wcsd-pds.s3.amazonaws.com/data/raw/Henry_B._Bigelow/HB0707/EK60/",
    retry_if_failed=1,
    registry={
        # https://noaa-wcsd-zarr-pds.s3.amazonaws.com/level_1/Henry_B._Bigelow/HB0707/EK60/D20070711-T182032.zarr/
        # https://noaa-wcsd-pds.s3.amazonaws.com/data/raw/Henry_B._Bigelow/HB0707/EK60/D20070711-T182032.raw
        # TODO: add bottom files
        "D20070712-T124906.raw": "sha256:44f9b2402a8d6d51c69235d1e33c3e4ab570fc541e9f269009924378bf4d97a2",  # 250 m, 158 MB
        "D20070712-T124906.bot": "sha256:9eebd8b85a514f3df6b7c4ba127967302dfea7c5e9fb47c22e3182ad1a93c78f",
        "D20070712-T152416.raw": "sha256:94a937eefd6ae5763c27c9ba1e4769b2b76fcc2d840e7db6c2e0edd925d6f70f",  # 1000 m, 200 MB
        "D20070712-T152416.bot": "sha256:65b16cff596502889f841e58061217660e066b07fb732ccf211f1c6e46ee8210",
    },
)

HB1906_RAW = pooch.create(
    path=pooch.os_cache("water-column-sonar-processing"),
    base_url="https://noaa-wcsd-pds.s3.amazonaws.com/data/raw/Henry_B._Bigelow/HB1906/EK60/",
    retry_if_failed=1,
    registry={
        # https://noaa-wcsd-pds.s3.amazonaws.com/data/raw/Henry_B._Bigelow/HB1906/EK60/D20191106-T034434.raw
        # "D20190903-T171901.raw": "", # 6 meter depth
        #
        "D20191106-T034434.raw": "sha256:8df1da62bfaca5d8e3bfd7be0b0f385c585bfb1ed0743e6aa8a9f108f765b968",  # has non-zero water_level
        "D20191106-T034434.bot": "sha256:027edd2eeca18bf16030c8f3c7867ffc70ec9080f4af7eab2b7210134da6d950",
        # Could also test: D20191106-T034434.raw & D20191106-T042540.raw
        "D20191106-T042540.raw": "sha256:e3457b098f1818169fcd13a925792e21a80ce7641312ba149f84a3d7fda45bd0",
        "D20191106-T042540.bot": "sha256:2aa7727a708cf2c25bca4bda650f599107be4a14c74850900be62fe6d83c6944",
    },
)


def fetch_raw_files():
    HB1906_RAW.fetch(fname="D20191106-T034434.raw", progressbar=True)
    HB1906_RAW.fetch(fname="D20191106-T034434.bot", progressbar=True)

    HB1906_RAW.fetch(fname="D20191106-T042540.raw", progressbar=True)
    HB1906_RAW.fetch(fname="D20191106-T042540.bot", progressbar=True)

    HB0707_RAW.fetch(fname="D20070712-T124906.raw", progressbar=True)
    HB0707_RAW.fetch(fname="D20070712-T124906.bot", progressbar=True)
    HB0707_RAW.fetch(fname="D20070712-T152416.raw", progressbar=True)
    file_name = HB0707_RAW.fetch(fname="D20070712-T152416.bot", progressbar=True)

    return Path(file_name).parent  # joinpath(Path(file_path).stem)


@pytest.fixture(scope="session")
def test_path():
    return {
        "RAW_TO_ZARR_TEST_PATH": TEST_DATA_FOLDER / "raw_to_zarr",
        "INDEX_TEST_PATH": TEST_DATA_FOLDER / "index",
        "ZARR_MANAGER_TEST_PATH": TEST_DATA_FOLDER / "zarr_manager",
        "PMTILE_GENERATION_TEST_PATH": TEST_DATA_FOLDER / "pmtile",
        "CREATE_EMPTY_ZARR_TEST_PATH": TEST_DATA_FOLDER / "create_empty_zarr",
        # 'RESAMPLE_REGRID_TEST_PATH': TEST_DATA_FOLDER / "resample_regrid",
        "RESAMPLE_REGRID_TEST_PATH": fetch_raw_files(),
        "S3FS_MANAGER_TEST_PATH": TEST_DATA_FOLDER / "s3fs_manager",
        "S3_MANAGER_TEST_PATH": TEST_DATA_FOLDER / "s3_manager",
    }


# """
# Windows
# C:\Users\<user>\AppData\Local\echopype\Cache\2024.12.23.10.10
# MacOS
# /Users//Library/Caches/echopype/2024.12.23.10.10
# """
