"""
 Copyright (c) 2022 Intel Corporation
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import pytest
from tests.common.helpers import create_venv_with_nncf
try:
    import tensorflow as tf
except ImportError:
    tf = None


@pytest.fixture(scope="function", autouse=True)
def clear_session():
    yield
    if tf:
        tf.keras.backend.clear_session()


def pytest_addoption(parser):
    parser.addoption(
        "--data", type=str, default=None,
        help="Path to test datasets"
    )
    parser.addoption(
        "--sota-checkpoints-dir", type=str, default=None, help="Path to checkpoints directory for sota accuracy test"
    )
    parser.addoption(
        "--sota-data-dir", type=str, default=None, help="Path to datasets directory for sota accuracy test"
    )
    parser.addoption(
        "--metrics-dump-path", type=str, default=None, help="Path to directory to store metrics. "
                                                            "Directory must be empty or should not exist."
                                                            "Metric keeps in "
                                                            "PROJECT_ROOT/test_results/metrics_dump_timestamp "
                                                            "if param not specified"
    )
    parser.addoption(
        "--ov-data-dir", type=str, default=None, help="Path to datasets directory for OpenVino accuracy test"
    )
    parser.addoption(
        "--run-openvino-eval", action="store_true", default=False, help="To run eval models via OpenVino"
    )
    parser.addoption(
        "--run-weekly-tests", action="store_true", default=False, help="To run weekly tests"
    )
    parser.addoption(
        "--models-dir", type=str, default=None, help="Path to checkpoints directory for weekly tests"
    )
    parser.addoption(
        "--run-install-tests", action="store_true", default=False, help="To run installation tests"
    )


@pytest.fixture(scope="module")
def sota_checkpoints_dir(request):
    return request.config.getoption("--sota-checkpoints-dir")


@pytest.fixture(scope="module")
def sota_data_dir(request):
    return request.config.getoption("--sota-data-dir")


@pytest.fixture(scope="module")
def metrics_dump_dir(request):
    pytest.metrics_dump_path = request.config.getoption("--metrics-dump-path")


@pytest.fixture(scope="module")
def dataset_dir(request):
    return request.config.getoption("--data")


@pytest.fixture(scope="module")
def ov_data_dir(request):
    return request.config.getoption("--ov-data-dir")


@pytest.fixture(scope="session")
def openvino(request):
    return request.config.getoption("--run-openvino-eval")


@pytest.fixture(scope="module")
def weekly_tests(request):
    return request.config.getoption("--run-weekly-tests")


@pytest.fixture(scope="module")
def models_dir(request):
    return request.config.getoption("--models-dir")


@pytest.fixture(scope="module")
def install_tests(request):
    return request.config.getoption("--run-install-tests")


@pytest.fixture(scope="function")
def tmp_venv_with_nncf(tmp_path, package_type, venv_type, install_tests):  # pylint:disable=redefined-outer-name
    if not install_tests:
        pytest.skip('To test the installation, use --run-install-tests option.')
    venv_path = create_venv_with_nncf(tmp_path, package_type, venv_type, extra_reqs='tf')
    return venv_path
