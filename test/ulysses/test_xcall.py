
from ulysses import xcall
import time
import pytest
from ulysses.xcall import XCallbackError
import urlparse


class TestXCallApp:

    def test_xcall_to_ulysses(self):
        d = xcall.xcall('ulysses://x-callback-url/get-version')
        assert d == {'buildNumber': '33542', 'apiVersion': '2'}
        # TODO: should not be dependent on build number

    def test_xcall_to_ulysses_error(self):
        with pytest.raises(XCallbackError) as excinfo:
            xcall.xcall('ulysses://x-callback-url/not-a-valid-action')
        assert 'Invalid Action Code = 100' in str(excinfo.value)

    # @pytest.mark.skip(reason="speed test takes quite long")
    def test_speed_or_urlcall(self):
        t_start = time.time()
        # Run once to ensure ulysses is open
        xcall.xcall('ulysses://x-callback-url/get-version')
        n = 10
        for i in range(n):  # @UnusedVariable
            xcall.xcall('ulysses://x-callback-url/get-version')
        dt = time.time() - t_start
        time_per_run = dt / n
        assert time_per_run < 0.15


def test_encode_request():

    action_parameter_dict = {'param1': 'val1', 'param2': 'val2'}
    result = xcall.build_url('some-action', action_parameter_dict)

    split_result = urlparse.urlsplit(result)
    args = urlparse.parse_qs(split_result.query)
    for k, v in args.iteritems():
        args[k] = v[0]  # pull values out of the list parse_qs results in

    assert split_result.scheme == 'ulysses'
    assert split_result.netloc == 'x-callback-url'
    assert split_result.path == '/some-action'
    assert args == action_parameter_dict