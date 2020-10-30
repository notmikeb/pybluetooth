import usb

# https://stackoverflow.com/questions/29345325/raspberry-pyusb-gets-resource-busy
dev = usb.core.find(idVendor=0x0a12, idProduct=0x0001)
# https://stackoverflow.com/questions/12542799/communication-with-the-usb-device-in-python/12543149#12543149][1]
reattach = True

if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

dev.set_configuration() 
cfg = dev.get_active_configuration() 

interface_number = cfg[(0,0)].bInterfaceNumber 
alternate_settting = usb.control.get_interface(dev, interface_number) 
intf = usb.util.find_descriptor(cfg, bInterfaceNumber = interface_number, 
                            bAlternateSetting = alternate_settting) 

ep = usb.util.find_descriptor(intf,custom_match = \
      lambda e: \
    usb.util.endpoint_direction(e.bEndpointAddress) == \
    usb.util.ENDPOINT_OUT) 
#ep.write("test\n\r")

# This is needed to release interface, otherwise attach_kernel_driver fails 
# due to "Resource busy"
usb.util.dispose_resources(dev)

# It may raise USBError if there's e.g. no kernel driver loaded at all
if reattach:
    dev.attach_kernel_driver(0) 
