import pytest

from ipsurv.util.sys_util import Output, System
from ipsurv.util.network_util import DnsUtil
import socket
import re


class TestSystem:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_get_python_ver(self):
        ver = System.get_python_ver()

        assert ver > 2.0

    def test_verify_is(self):
        is_match = System.verify_os()

        assert not is_match

    def test_line(self, capfd):
        Output.line('ABC')

        captured = capfd.readouterr()
        assert re.search("ABC", captured.out.strip())

    def test_warn(self, capfd):
        Output.warn('ABC')

        captured = capfd.readouterr()
        assert re.search("ABC", captured.out.strip())


class TestDnsUtil:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_getaddrinfo(self):
        ip = DnsUtil.getaddrinfo('wikipedia.org')

        assert len(ip[0]) > 10

    def test_timeout(self):
        with pytest.raises((socket.timeout, socket.gaierror)):
            DnsUtil.getaddrinfo('ipsurv-2345253567456736533434563534.test', timeout=0.005)

    def test_resolve(self):
        ip = DnsUtil.resolve('wikipedia.org')

        assert len(ip) > 10

    def test_reverse(self):
        host = DnsUtil.reverse('8.8.8.8')

        assert host == 'dns.google'
