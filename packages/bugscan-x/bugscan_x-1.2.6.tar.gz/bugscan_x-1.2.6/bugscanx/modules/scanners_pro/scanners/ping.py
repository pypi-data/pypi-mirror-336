import socket
from .base import BaseScanner

class PingScanner(BaseScanner):
    host_list = []
    port_list = []

    def log_info(self, **kwargs):
        kwargs.setdefault('color', '')
        kwargs.setdefault('status', '')
        kwargs.setdefault('host', '')
        kwargs.setdefault('ip', '')

        messages = [
            self.colorize('{status:<8}', 'GREEN'),
            self.colorize('{port:<6}', 'CYAN'),
            self.colorize('{ip:<15}', 'YELLOW'),
            self.colorize('{host}', 'LGRAY'),
        ]

        super().log('  '.join(messages).format(**kwargs))

    def get_task_list(self):
        for host in self.filter_list(self.host_list):
            for port in self.filter_list(self.port_list):
                yield {
                    'host': host,
                    'port': port,
                }

    def init(self):
        super().init()
        self.log_info(status='Status', port='Port', ip='IP', host='Host')
        self.log_info(status='------', port='----', ip='--', host='----')

    def resolve_ip(self, host):
        try:
            return socket.gethostbyname(host)
        except Exception:
            return "Unknown"

    def task(self, payload):
        host = payload['host']
        port = payload['port']

        if not host:
            return
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((host, int(port)))

            if result == 0:
                ip = self.resolve_ip(host)
                data = {
                    'host': host,
                    'port': port,
                    'status': 'True',
                    'ip': ip
                }
                self.task_success(data)
                self.log_info(**data)

        except Exception:
            pass

        self.log_replace(f"{host}:{port}")

    def complete(self):
        self.log_replace(self.colorize("Scan completed", "GREEN"))
        super().complete()
