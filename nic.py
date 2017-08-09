from custom_t import NIC_TYPES
from utils import shell

class Nic():
    def __init__(self, bridge, driver, mac='auto'):
        if driver not in NIC_TYPES:
            raise TypeError('Invalid driver %s' % driver)
        self.mac    = mac
        self.bridge = bridge
        self.driver = driver
        self.tap = 'none' 
    def dump(self):
        rtrn = {}
        for v in vars(self):
            rtrn[v] = vars(self)[v]
        return rtrn

    def start(self, i):
        if 'auto' not in self.mac:
            mac_str = ',mac=%s' % self.mac
        else:
            mac_str = ""

        try:
            self.tap = shell("ifconfig tap create | tr -d '\n'")
            shell('ifconfig %s addm %s' % (self.bridge, self.tap))
            return '-s %s,%s,%s%s ' % (i, self.driver, self.tap, mac_str)
        except:
            raise

    def stop(self):
        try:
            shell('ifconfig %s deletem %s' % (self.bridge, self.tap))
            shell('ifconfig %s destroy' % self.tap)
        except:
            raise

    def __repr__(self):
        conndisc = 'Disconnected'
        if self.tap is not None:
            conndisc = 'Connected'
        return '<virtual %s nic attached to %s mac: %s, %s>' % (self.driver, self.bridge, self.mac, conndisc)

