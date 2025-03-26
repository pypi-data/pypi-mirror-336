import subprocess
from pathlib import Path

import git
import pytest

import lhcbdiracx.client.generated

pytestmark = pytest.mark.enabled_dependencies([])
# pytestmark = pytest.mark.enabled_dependencies(["ConfigSource", "AuthSettings"])


AUTOREST_VERSION = "6.13.7"


@pytest.fixture
def test_client(client_factory):
    with client_factory.unauthenticated() as client:
        yield client


def test_regenerate_client(test_client, tmp_path):
    """Regenerate the AutoREST client and run pre-commit checks on it.

    This test is skipped by default, and can be enabled by passing
    --regenerate-client to pytest. It is intended to be run manually
    when the API changes.

    The reason this is a test is that it is the only way to get access to the
    test_client fixture, which is required to get the OpenAPI spec.

    WARNING: This test will modify the source code of the client!
    """
    r = test_client.get("/api/openapi.json")
    r.raise_for_status()

    openapi_spec = tmp_path / "openapi.json"
    openapi_spec.write_text(r.text)
    output_folder = Path(lhcbdiracx.client.generated.__file__).parent
    assert (output_folder).is_dir()
    repo_root = output_folder.parents[4]
    assert (repo_root / "lhcbdiracx-client" / "src").is_dir()
    assert (repo_root / ".git").is_dir()
    repo = git.Repo(repo_root)
    if repo.is_dirty(
        path=repo_root / "lhcbdiracx-client" / "src" / "lhcbdiracx" / "client"
    ):
        raise AssertionError(
            "Client is currently in a modified state, skipping regeneration"
        )

    cmd = [
        "autorest",
        "--python",
        f"--input-file={openapi_spec}",
        "--models-mode=msrest",
        "--namespace=generated",
        f"--output-folder={output_folder.parent}",
    ]

    # This is required to be able to work offline
    # TODO: if offline, find the version already installed
    # and use it
    # cmd += [f"--use=@autorest/python@{AUTOREST_VERSION}"]

    subprocess.run(cmd, check=True)  # noqa

    cmd = ["pre-commit", "run", "--all-files"]
    print("Running pre-commit...")
    subprocess.run(cmd, check=False, cwd=repo_root)  # noqa
    print("Re-running pre-commit...")
    subprocess.run(cmd, check=True, cwd=repo_root)  # noqa
    if repo.is_dirty(path=repo_root / "src" / "lhcbdiracx" / "client"):
        raise AssertionError("Client was regenerated with changes")


if __name__ == "__main__":
    print(AUTOREST_VERSION)
