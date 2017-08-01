from custom_t import NIC_TYPES

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

        self.tap = 'tap10'
        print "ifconfig tap create"
        print "ifconfig %s addm %s" % (self.bridge, self.tap)
        return '-s %s,%s,%s%s ' % (i, self.driver, self.tap, mac_str)

    def __repr__(self):
        return '<virtual %s nic attached to %s mac: %s>' % (self.driver, self.bridge, self.mac)

