import pytest
from click.testing import CliRunner
from cityjson2jsonfg import cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           args=["--help"])
    print(result.output)
    assert result.exit_code == 0


def test_read(input_model_5907_path, tmp_dir):
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           args=[str(input_model_5907_path),
                                 str(tmp_dir / "out.json")])
    if result.exit_code != 0:
        pytest.fail(result.stdout)
    else:
        assert True