import pytest
from click.testing import CliRunner
from cityjson2jsonfg import cli
import subprocess


def fail_with_msg(result, runner):
    msg = (f"\n- output: {result.output}\n"
           f"- exec_info: {result.exc_info}\n"
           f"- stdout: {result.stdout}\n")
    if not runner.mix_stderr:
        msg += f"- stderr: {result.stderr}"
    pytest.fail(msg)


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli.main_cmd,
                           args=["--help"])
    assert result.exit_code == 0


def test_main(input_model_5907_path, tmp_dir):
    """Test the main converter function"""
    infile = input_model_5907_path.open("r")
    outfile = (tmp_dir / "out.test_main.json").open("w")
    cli.main(infile, outfile, ignore_duplicate_keys=True)


def test_main_stdin(input_model_5907_path, tmp_dir):
    """Test that reading from a pipe works"""
    with input_model_5907_path.open("r") as fo:
        ij = fo.read()
    runner = CliRunner()
    result = runner.invoke(cli.main_cmd,
                           input=ij,
                           args=["-", str(tmp_dir / "out.test_main_stdin.json"),])
    if result.exit_code != 0:
        fail_with_msg(result, runner)
    else:
        assert result.stdout.strip() == "887"


def test_test_stdin(input_model_5907_path, tmp_dir):
    """Test that reading from a pipe works"""
    with input_model_5907_path.open("r") as fo:
        ij = fo.read()
    runner = CliRunner()
    result = runner.invoke(cli.test_cmd,
                           input=ij,
                           args=["-", str(tmp_dir / "out.test_main_stdin.json"),])
    if result.exit_code != 0:
        fail_with_msg(result, runner)
    else:
        assert result.stdout.strip() == "887"