import pysftp


class CnOpts(pysftp.CnOpts):
    def __init__(self, port=None):
        super().__init__()
        self.port = port

    def get_hostkey(self, host):
        # fix handling of custom port when looking up key in known hosts
        if self.port is not None:
            host = f"[{host}]:{self.port}"
        return super().get_hostkey(host)
