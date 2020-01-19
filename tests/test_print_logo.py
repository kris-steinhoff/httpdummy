import pytest

from httpdummy.server import print_logo


@pytest.mark.parametrize('in_reloader', (
    True,
    False,
))
def test_reloader_check(in_reloader, mocker, capsys):
    mock_is_running_from_reloader = mocker.patch(
        'httpdummy.server.is_running_from_reloader')
    mock_is_running_from_reloader.return_value = in_reloader

    print_logo()

    out, err = capsys.readouterr()

    assert in_reloader != (len(out) > 0)
