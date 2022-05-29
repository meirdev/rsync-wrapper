from rsync_wrapper import process, types


def test_popen():
    out = list(process.popen("echo 'hello world'"))

    assert isinstance(out[0], types.StdOut)
    assert out[0] == "hello world\n"

    out = list(process.popen("echo 'hello world' >> /dev/stderr"))

    assert isinstance(out[0], types.StdErr)
    assert out[0] == "hello world\n"

    out = list(process.popen("true"))

    assert isinstance(out[0], types.ExitCode)
    assert out[0] == 0

    out = list(process.popen("false"))

    assert isinstance(out[0], types.ExitCode)
    assert out[0] == 1
