from abc import ABC

from ipscap.configs import Constant
from ipscap.util.raw_socket_entity import IPHeader
from ipsurv.util.sys_util import Output
import base64
import copy


class ProtocolService(ABC):
    _instances = {}

    @classmethod
    def register_services(cls, icmp_service, tcp_service, udp_service):
        cls._instances[IPHeader.PROTOCOL_ICMP] = icmp_service
        cls._instances[IPHeader.PROTOCOL_TCP] = tcp_service
        cls._instances[IPHeader.PROTOCOL_UDP] = udp_service

    @classmethod
    def get_service(cls, protocol):
        return cls._instances.get(protocol)

    def show_transfer(self, ip_header, protocol_header, passage_num, now, args):
        if args.fixed_output != Constant.OUTPUT_NONE:
            if args.fixed_output != Constant.OUTPUT_LINE:
                self.show_overview(ip_header, protocol_header, now, passage_num, args.output_raw)
                self.show_payload(ip_header, protocol_header, args.fixed_output)
            else:
                self.show_line(ip_header, protocol_header, now, passage_num)

    def show_overview(self, ip_header, protocol_header, now, passage_num, output_raw):
        pass

    def create_decorated_ip_header(self, ip_header):
        ip_header = copy.deepcopy(ip_header)

        self.add_raw(ip_header, 'total_length')
        self.add_raw(ip_header, 'identification')
        self.add_raw(ip_header, 'ttl')
        self.add_raw(ip_header, 'src_ip')
        self.add_raw(ip_header, 'dest_ip')
        self.add_raw(ip_header, 'checksum')

        return ip_header

    def create_decorated_protocol_header(self, protocol_header):
        pass

    def create_decorated_headers(self, ip_header, protocol_header):
        ip_header = self.create_decorated_ip_header(ip_header)
        protocol_header = self.create_decorated_protocol_header(protocol_header)

        return ip_header, protocol_header

    def show_head(self, ip_header, now, passage_num):
        Output.line(self.label('Time:') + self.get_datatime(now) + ' / ' + self.get_timestamp(now) + ', Passage number: ' + str(passage_num))
        Output.line(self.label('IP header:') + 'Version: ' + str(ip_header.version) + ', IP header length: ' + str(ip_header.iph_length) + ', Identification: ' + str(ip_header.identification) + ', Total length: ' + str(ip_header.total_length) + ', Checksum: ' + str(ip_header.checksum) + ', TTL: ' + str(ip_header.ttl) + ', IP protocol: ' + ip_header.protocol_code + "[{}]".format(str(ip_header.protocol)))

    def show_middle(self, ip_header, protocol_header, show_data_len):
        Output.line(self.label('Source:') + self.label('IP: ' + str(ip_header.src_ip), 35) + 'Port: ' + str(protocol_header.src_port))
        Output.line(self.label('Destination:') + self.label('IP: ' + str(ip_header.dest_ip), 35) + 'Port: ' + str(protocol_header.dest_port))

        if ip_header.direction == 1:
            direction_msg = 'SEND [ >>> ]'
        elif ip_header.direction == 2:
            direction_msg = 'RECEIVE [ <<< ]'
        else:
            direction_msg = 'UNKNOWN'

        Output.line(self.label('Direction:') + direction_msg)

        if show_data_len:
            Output.line(self.label('Data length:') + str(protocol_header.payload_length) + ' byte')

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        pass

    def show_payload(self, ip_header, protocol_header, output):
        if output == Constant.OUTPUT_TEXT:
            data = protocol_header.payload_data.decode('utf-8', errors='ignore')

            if len(protocol_header.get_sanitized_data()) > 0:
                Output.line(data + "\n")
        elif output == Constant.OUTPUT_BINARY:
            Output.line(protocol_header.payload_data)
            Output.line('')
        elif output == Constant.OUTPUT_BINARY_ALL:
            Output.line(self.get_all_data(ip_header, protocol_header))
            Output.line('')
        elif output == Constant.OUTPUT_HEX:
            hex_data = self.get_hex_data(protocol_header.payload_data)
            Output.line(hex_data + "\n")
        elif output == Constant.OUTPUT_HEX_ALL:
            hex_data = self.get_hex_data(self.get_all_data(ip_header, protocol_header))
            Output.line(hex_data + "\n")
        elif output == Constant.OUTPUT_BASE64:
            data = self.get_base64_data(protocol_header.payload_data)
            Output.line(data + "\n")
        elif output == Constant.OUTPUT_BASE64_ALL:
            data = self.get_base64_data(self.get_all_data(ip_header, protocol_header))
            Output.line(data + "\n")

    def get_all_data(self, ip_header, protocol_header):
        return ip_header.header_data + protocol_header.header_data + protocol_header.payload_data

    def get_datatime(self, now):
        return now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-2]

    def get_timestamp(self, now):
        return str(now.timestamp())[:-2]

    def get_hex_data(self, data):
        hex_data = ''.join(f'{byte:02x} ' for byte in data)

        return hex_data

    def get_base64_data(self, data):
        base64_data = base64.b64encode(data)

        return base64_data.decode('utf-8')

    def label(self, v, n=16):
        return v.ljust(n)

    def add_raw(self, header, name, raw_name=None):
        v = str(getattr(header, name))

        raw_name = raw_name if raw_name is not None else name

        setattr(header, name, v + '[' + header.raws[raw_name] + ']')


class ICMPProtocolService(ProtocolService):
    def show_overview(self, ip_header, protocol_header, now, passage_num, output_raw):
        if output_raw:
            ip_header, protocol_header = self.create_decorated_headers(ip_header, protocol_header)

        self.show_head(ip_header, now, passage_num)

        Output.line(self.label('ICMP header:') + 'ICMP header length: ' + str(protocol_header.icmph_length) + ', Type: ' + str(protocol_header.icmp_type) + ', Code: ' + str(protocol_header.code))

        self.show_middle(ip_header, protocol_header, False)

        Output.line(self.label('IP-H data:') + self.get_hex_data(ip_header.header_data))
        Output.line(self.label('ICMP-H data:') + self.get_hex_data(protocol_header.header_data))
        Output.line('')

    def create_decorated_protocol_header(self, protocol_header):
        protocol_header = copy.deepcopy(protocol_header)

        self.add_raw(protocol_header, 'icmp_type')
        self.add_raw(protocol_header, 'code')
        self.add_raw(protocol_header, 'checksum')

        return protocol_header

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        line = ''

        line += self.get_datatime(now) + split
        line += str(passage_num) + split
        line = line.ljust(30)

        line += str(ip_header.version) + split + str(ip_header.iph_length) + split + str(ip_header.ttl) + split + str(ip_header.total_length) + split
        line = line.ljust(50)

        line += str(ip_header.protocol_code) + split
        line += str(protocol_header.icmph_length) + split
        line = line.ljust(60)

        line += str(protocol_header.icmp_type) + split + str(protocol_header.code) + split
        line = line.ljust(70)

        line += str(ip_header.src_ip) + split
        line = line.ljust(95)

        line += str(ip_header.dest_ip) + split
        line = line.ljust(120)

        line += ip_header.direction_code + split

        Output.line(line)

    def show_payload(self, ip_header, protocol_header, output):
        pass


class TCPProtocolService(ProtocolService):
    def show_overview(self, ip_header, protocol_header, now, passage_num, output_raw):
        if output_raw:
            ip_header, protocol_header = self.create_decorated_headers(ip_header, protocol_header)

        self.show_head(ip_header, now, passage_num)

        Output.line(self.label('TCP header:') + 'TCP header length: ' + str(protocol_header.tcph_length) + ', Checksum: ' + str(protocol_header.checksum) + ', Sequence: ' + str(protocol_header.seq_no) + ', Acknowledgement: ' + str(protocol_header.ack_no) + ', Window: ' + str(protocol_header.window) + ', Flags: ' + str(protocol_header.flag_codes))
        Output.line(self.label('TCP options:') + self._get_tcp_options(protocol_header.tcp_options))

        self.show_middle(ip_header, protocol_header, True)

        Output.line(self.label('IP-H data:') + self.get_hex_data(ip_header.header_data))
        Output.line(self.label('TCP-H data:') + self.get_hex_data(protocol_header.header_data))
        Output.line('')

    def create_decorated_protocol_header(self, protocol_header):
        protocol_header = copy.deepcopy(protocol_header)

        self.add_raw(protocol_header, 'src_port')
        self.add_raw(protocol_header, 'dest_port')
        self.add_raw(protocol_header, 'seq_no')
        self.add_raw(protocol_header, 'ack_no')
        self.add_raw(protocol_header, 'flags')
        self.add_raw(protocol_header, 'window')
        self.add_raw(protocol_header, 'checksum')

        return protocol_header

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        line = ''

        line += self.get_datatime(now) + split
        line += str(passage_num) + split
        line = line.ljust(30)

        line += str(ip_header.version) + split + str(ip_header.iph_length) + split + str(ip_header.ttl) + split + str(ip_header.total_length) + split
        line = line.ljust(50)

        line += str(ip_header.protocol_code) + split
        line += str(protocol_header.tcph_length) + split + str(protocol_header.seq_no) + split + str(protocol_header.ack_no) + split + str(protocol_header.window) + split
        line = line.ljust(90)

        line += str(protocol_header.flag_codes) + split
        line = line.ljust(112)

        line += str(protocol_header.payload_length) + split
        line = line.ljust(120)

        line += str(ip_header.src_ip) + ':' + str(protocol_header.src_port) + split
        line = line.ljust(145)

        line += str(ip_header.dest_ip) + ':' + str(protocol_header.dest_port) + split
        line = line.ljust(170)

        line += ip_header.direction_code + split
        line = line.ljust(185)

        line += self._get_tcp_options(protocol_header.tcp_options, ';')

        Output.line(line)

    def _get_tcp_options(self, tcp_options, split=', '):
        value = ''

        if len(tcp_options) > 0:
            for k, v in tcp_options.items():
                if isinstance(v, bool):
                    value += k
                else:
                    value += k + ':' + str(v)

                value += split

            value = value.strip(split)
        else:
            value = '-'

        return value


class UDPProtocolService(ProtocolService):
    def show_overview(self, ip_header, protocol_header, now, passage_num, output_raw):
        if output_raw:
            ip_header, protocol_header = self.create_decorated_headers(ip_header, protocol_header)

        self.show_head(ip_header, now, passage_num)

        Output.line(self.label('UDP header:') + 'UDP header length: ' + str(protocol_header.udph_length) + ', Checksum: ' + str(protocol_header.checksum))

        self.show_middle(ip_header, protocol_header, True)

        Output.line(self.label('IP-H data:') + self.get_hex_data(ip_header.header_data))
        Output.line(self.label('UDP-H data:') + self.get_hex_data(protocol_header.header_data))
        Output.line('')

    def create_decorated_protocol_header(self, protocol_header):
        protocol_header = copy.deepcopy(protocol_header)

        self.add_raw(protocol_header, 'src_port')
        self.add_raw(protocol_header, 'dest_port')
        self.add_raw(protocol_header, 'udph_length')

        return protocol_header

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        line = ''

        line += self.get_datatime(now) + split
        line += str(passage_num) + split
        line = line.ljust(30)

        line += str(ip_header.version) + split + str(ip_header.iph_length) + split + str(ip_header.ttl) + split + str(ip_header.total_length) + split
        line = line.ljust(50)

        line += str(ip_header.protocol_code) + split
        line += str(protocol_header.udph_length) + split
        line = line.ljust(55)

        line += str(protocol_header.payload_length) + split
        line = line.ljust(70)

        line += str(ip_header.src_ip) + ':' + str(protocol_header.src_port) + split
        line = line.ljust(95)

        line += str(ip_header.dest_ip) + ':' + str(protocol_header.dest_port) + split
        line = line.ljust(120)

        line += ip_header.direction_code + split

        Output.line(line)
