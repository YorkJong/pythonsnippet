"""
ref. http://wiki.erazor-zone.de/wiki:projects:python:pyusb:setup:examples:lsusb
"""
import usb


for bus in usb.busses():
    for dev in bus.devices:
        h = dev.open()
        print "device: %s" % dev.filename
        print "  bus: %s" % bus.dirname
        print "  id: %04X:%04X" % (dev.idVendor, dev.idProduct)
        print "  product: %s" % h.getString(dev.iProduct, 30)
        print "  manufacturer: %s" % h.getString(dev.iManufacturer, 30)
        print "  serial number: %s" % h.getString(dev.iSerialNumber, 30)
