from click.testing import CliRunner
from cityjson2jsonfg import cli


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           args=["--help"])
    print(result.output)
    assert result.exit_code == 0