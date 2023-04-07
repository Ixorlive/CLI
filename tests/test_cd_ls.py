import io
import os

import pytest

from command import commands
from columnify import columnify


@pytest.mark.parametrize(
    "args, expected_output, expected_errors, expected_return_code",
    [
        (
            ["tests/data/cd_ls_dirs"], 
            os.getcwd() + "/tests/data/cd_ls_dirs", 
            "", commands.CODE_OK
        ),
        (
            ["some_dir"], 
            os.getcwd() + "/tests/data/cd_ls_dirs/some_dir", 
            "", commands.CODE_OK
        ),
        (
            ["../"],
            os.getcwd() + "/tests/data/cd_ls_dirs",
            "", commands.CODE_OK
        ),
        (
            ["not_exist_dir"],
            os.getcwd() + "/tests/data/cd_ls_dirs",
            "cd: not_exist_dir: No such file or directory\n",
            commands.INTERNAL_COMMAND_ERROR
        ),
        (
            ["another_dir"],
            os.getcwd() + "/tests/data/cd_ls_dirs/another_dir", 
            "", commands.CODE_OK
        ),
        (
            ["../some_dir/inside_some_dir"], 
            os.getcwd() + "/tests/data/cd_ls_dirs/some_dir/inside_some_dir",
            "", commands.CODE_OK
        ),
        (
            ["../../"], 
            os.getcwd() + "/tests/data/cd_ls_dirs",
            "",
            commands.CODE_OK
        ),
        (
            ["some_file.txt"],
            os.getcwd() + "/tests/data/cd_ls_dirs",
            "cd: some_file.txt: Not a directory\n",
            commands.INTERNAL_COMMAND_ERROR
        ),
        (
            ["some_file.txt", "some_dir"],
            os.getcwd() + "/tests/data/cd_ls_dirs",
            "cd: too many arguments\n",
            commands.INTERNAL_COMMAND_ERROR
        ),
        (
            [],
            os.path.expanduser("~"),
            "",
            commands.CODE_OK
        ),
        ([os.getcwd()], os.getcwd(), "", commands.CODE_OK)
    ],
)
def test_cd(args, expected_output, expected_errors, expected_return_code):
    cd = commands.Cd()
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()

    assert (
        cd.execute(args, input_stream, output_stream, error_stream)
        == expected_return_code
    )

    output_stream.write(os.getcwd())
    output_stream.seek(0)
    assert output_stream.read() == expected_output
    error_stream.seek(0)
    assert error_stream.read() == expected_errors

@pytest.mark.parametrize(
    "cmd, args, expected_output, expected_errors, expected_return_code",
    [
        (
            "cd", ["tests/data/cd_ls_dirs"], 
            os.getcwd() + "/tests/data/cd_ls_dirs", 
            "", None
        ),
        (
            "ls", [], 
            columnify(["another_dir", "some_dir", "some_file.txt"], 80, 1)+'\n',
            "", commands.CODE_OK
        ),
        (
            "ls", ["some_dir"], 
            "some_dir:\n" + 
                columnify(
                    ["file_in_some_dir.sh", "inside_some_dir"], 80, 1
                ) + '\n',
            "", commands.CODE_OK
        ),
        (
            "ls", ["some_dir/inside_some_dir"], 
            "some_dir/inside_some_dir:\n\n", "", commands.CODE_OK
        ),
        (
            "ls", ["some_dir", "another_dir"], 
            "some_dir:\n" + 
                columnify(
                    ["file_in_some_dir.sh","inside_some_dir"], 80, 1
                ) + '\n' + "another_dir:\n" + 
                columnify(
                    ["1234567890.txt", "123abc.go", "2345678901.py", 
                    "3456789012.pdf", "4567890123.txt", "5678901234.py", 
                    "6789012345.pdf", "abcdefg.txt", "bcdefga.py",
                    "cdefgab.pdf"],
                    80, 1
                )+'\n',
            "", commands.CODE_OK
        ),
        (
            "ls", ["not_exist_dir"], 
            "",
            "ls: cannot access 'not_exist_dir': No such file or directory\n",
            commands.CODE_OK
        ),
        ("cd", [os.getcwd()], os.getcwd(), "", None)
    ],
)
def test_ls(cmd, args, expected_output, expected_errors, expected_return_code):
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()

    if cmd == "cd":
        os.chdir(args[0])
        output_stream.write(os.getcwd())
        
        output_stream.seek(0)
        assert output_stream.read() == expected_output
        error_stream.seek(0)
        assert error_stream.read() == expected_errors

        return

    ls = commands.Ls()

    assert (
        ls.execute(args, input_stream, output_stream, error_stream)
        == expected_return_code
    )

    output_stream.seek(0)
    assert output_stream.read() == expected_output
    error_stream.seek(0)
    assert error_stream.read() == expected_errors
