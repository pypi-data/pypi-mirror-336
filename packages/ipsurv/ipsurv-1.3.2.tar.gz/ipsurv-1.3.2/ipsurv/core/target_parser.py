import logging
import re
import urllib.parse
from abc import ABC

from ipsurv.configs import Constant
from ipsurv.core.entity import Target
from ipsurv.core.entity import ValueData
from ipsurv.core.pipeline import Pipeline
from ipsurv.requester.dns_resolver import DnsResolveRequester
from ipsurv.util.sys_util import Output
import ipaddress


class TargetParser(ABC):
    """
    Description:
    https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/program_architecture_classes.html#targetparser
    """
    def __init__(self, args, pipeline, dns_resolver):
        """
        :param args:
        :type args: argparse.Namespace
        :param pipeline:
        :type pipeline: Pipeline
        :param dns_resolver:
        :type dns_resolver: DnsResolveRequester
        """
        self.pipeline = pipeline  # type: Pipeline
        self.autodetect = args.autodetect  # type: bool
        self.identify_int = args.identify_int  # type: bool
        self.ranges = args.fixed_ranges  # type: list
        self.dns_resolver = dns_resolver  # type: DnsResolveRequester

    def parse(self, data, original, args):
        # type: (ValueData, str, object) -> Target
        """
        :param data:
        :type data: ValueData
        :param original:
        :type original: str
        :param args:
        :type args: argparse.Namespace
        :rtype: Target
        """
        target = self._parse_target(data, original, args)

        identify = self.pipeline.pre_target_identify(data, target)

        if identify:
            self._identify_target(data, target, args)

        if target.status != Constant.STATUS_EXIST:
            target.identifier = target.status

        self._assign_data_target(data, target)

        if Output.is_logging():
            logging.log(logging.DEBUG, 'TARGET_RAW:' + target.raw)
            logging.log(logging.INFO, 'TARGET_IDENTIFIER:' + str(target.identifier))

            Output.output_data('TARGET_DATA', target.get_values())

        return target

    def _parse_target(self, data, original, args):
        # type: (ValueData, str, object) -> Target
        """
        :param data:
        :type data: ValueData
        :param original:
        :type original: str
        :param args:
        :type args: argparse.Namespace
        :rtype: Target
        """

        if self.autodetect:
            raw = self._detect_target_raw(original, args)
        else:
            raw = original

        return self._create_target(raw.strip())

    def _identify_target(self, data, target, args):
        # type: (ValueData, Target, object) -> None
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :param args:
        :type args: argparse.Namespace
        """

        if target.raw:
            target.identified = self._identify_target_ip(data, target, args)
        else:
            target.status = Constant.STATUS_EMPTY

        if target.identified:
            target.status = Constant.STATUS_EXIST

            self._prepare_target_data(data, target)

        logging.info('IP:' + str(target.ip))
        logging.info('FQDN:' + str(target.fqdn))
        logging.info('PORT:' + str(target.port))

    def _prepare_target_data(self, data, target):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        """
        ip_address = ipaddress.ip_address(target.identifier)
        target.identifier_int = int(ip_address)

        data.set('ip', target.ip)
        data.set('ip_int', target.identifier_int)
        data.set('ip_hex', '.'.join(f'{v:02x}' for v in ip_address.packed).upper())
        data.set('ip_reversed', '.'.join(reversed(ip_address.exploded.split('.'))))
        data.set('port', target.port)

        self._evaluate(data, target)

    def _identify_ip_int(self, raw):
        def convert_ip(match):
            ip_int = int(match.group(1))
            return str(ipaddress.ip_address(ip_int))

        return re.sub(r'(?<!\d)(\d{8,10})(?!\d)', convert_ip, raw)

    def _identify_target_ip(self, data, target, args):
        # type: (ValueData, Target, object) -> bool

        identified = False

        netloc = self._find_ip(target.raw, True)

        if not netloc:
            url = self._find_url(target.raw)

            if url:
                target.url = url

                parsed = urllib.parse.urlparse(url)
                netloc = parsed.netloc
            else:
                if not self.identify_int:
                    netloc = target.raw
                else:
                    netloc = self._identify_ip_int(target.raw)

        (fqdn_ip, port) = self._split_port(netloc)

        target.port = port

        if fqdn_ip:
            ip = self._find_ip(fqdn_ip, False)

            if not ip:
                fqdn = self._find_fqdn(fqdn_ip)

                target.fqdn = fqdn

                if fqdn:
                    if args.resolve:
                        try:
                            ip = self.dns_resolver.resolve_ip(fqdn)
                        except Exception:
                            target.status = Constant.STATUS_RESOLVE_FAIL
                else:
                    target.status = Constant.STATUS_ILLEGAL_FORMAT

            target.identifier = target.ip = ip

            if ip:
                identified = True

        return identified

    def _evaluate(self, data, target):
        # type: (ValueData, Target) -> None

        ip_address = ipaddress.ip_address(target.ip)

        self._evaluate_ip_type(data, ip_address)

        if len(self.ranges) > 0:
            self._evaluate_in_ranges(data, ip_address)

    def _evaluate_ip_type(self, data, ip_address):
        ip_type = Constant.IP_TYPE_PRIVATE if ip_address.is_private else Constant.IP_TYPE_PUBLIC

        data.set('ip_type', ip_type)

    def _evaluate_in_ranges(self, data, ip_address):
        # type: (ValueData, Target) -> None

        in_range = False

        for range in self.ranges:
            network = ipaddress.ip_network(range, strict=False)

            if ip_address in network:
                in_range = True
                break

        data.set('in_range', in_range)

    def _assign_data_target(self, data, target):
        # type: (ValueData, Target) -> None
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        """

        data.set('identifier', target.identifier)
        data.set('identifier_int', target.identifier_int)

        data.set('target', target)

    def _detect_target_raw(self, original, args):
        rows = re.split(args.fixed_delimiter, original)

        for row in rows:
            if self._find_url(row) or self._find_fqdn(row) or self._find_ip(row):
                return row

        return ''

    def _split_port(self, v):
        vals = v.split(':')
        port = None

        if len(vals) == 2:
            fqdn_ip = vals[0]

            try:
                port = int(vals[1])
            except Exception:
                pass
        else:
            fqdn_ip = vals[0]

        return fqdn_ip, port

    def _find_url(self, v):
        m = re.search(r'(https?:\/\/|\/\/)[a-z0-9][a-z0-9.\-/?=&_%!+:]+', v, flags=re.IGNORECASE)

        return m.group() if m is not None else None

    def _find_fqdn(self, v):
        m = re.search(r'([a-z0-9\-]{1,128}(?<!\-)\.)+[a-z0-9]{2,}', v, flags=re.IGNORECASE)

        return m.group() if m is not None else None

    def _find_ip(self, v, with_port=False):
        regex = r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}'

        if with_port:
            regex += r'(:\d{2,5})?'

        m = re.search(regex, v)

        return m.group() if m is not None else None

    def _create_target(self, raw):
        return Target(raw.strip())
