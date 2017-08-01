from custom_t import DISK_TYPES

class Disk():
    def __init__(self, path, driver):
        if driver not in DISK_TYPES:
            raise TypeError('Invalid driver %s' % driver)
        self.path = path
        self.driver = driver

    def dump(self):
        rtrn = {}
        for v in vars(self):
            rtrn[v] = vars(self)[v]
        return rtrn

    def start(self, i):
        return '-s %s,%s,%s ' % (i, self.driver, self.path)

    def __repr__(self):
        return '<virtual %s disk attached to %s>' % (self.driver, self.path)

