#!/usr/bin/python
import sys
import usb.core
import usb.util
import os
from random import choice 

from time import sleep

# decimal vendor and product values
dev = usb.core.find(idVendor=0x1532, idProduct=0x0208)
# or, uncomment the next line to search instead by the hexidecimal equivalent
#dev = usb.core.find(idVendor=0x45e, idProduct=0x77d)
# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
  # tell the kernel to detach
  dev.detach_kernel_driver(interface)
  # claim the device
  usb.util.claim_interface(dev, interface)


def sendrecv(msg):
  # send led msg
  print "Sending %s" % msg.encode('hex')
  ret = dev.ctrl_transfer(0x21, 9, 0x0300, 0, msg)
  print "Led msg ret: %s" % ret

  ret = dev.ctrl_transfer(0xA1, 1, 0x0300, 0, len(msg))
  sret = ''.join([chr(x) for x in ret])
  print "Led msg ret second package: %s" % sret.encode('hex')


# sequence 8 - all three lights out
led_control_sequence_8 = [
 "0000000000030300000e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00",
 "0000000000030300000c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00",
 "0000000000030300000d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00"
 ]

# sequence 1 - only top yellow light
led_control_sequence_1 = [
 "0000000000030300000e0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00",
 "0000000000030300000c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00",
 "0000000000030300000d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00"
 ]

# sequence 2 - only middle green light
led_control_sequence_2 = [
 "0000000000030300000e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00",
 "0000000000030300000c0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00",
 "0000000000030300000d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00"
 ]

# sequence 3 - only bottom blue light
led_control_sequence_3 = [
 "0000000000030300000e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00",
 "0000000000030300000c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00",
 "0000000000030300000d0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00"
 ]

# sequence 4 - top two lights
led_control_sequence_4 = [
 "0000000000030300000e0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00",
 "0000000000030300000c0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00",
 "0000000000030300000d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00"
 ]

# sequence 5 - top and bottom lights
led_control_sequence_5 = [
 "0000000000030300000e0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00",
 "0000000000030300000c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00",
 "0000000000030300000d0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00"
 ]

# sequence 6 - bottom two lights
led_control_sequence_6 = [
 "0000000000030300000e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00",
 "0000000000030300000c0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00",
 "0000000000030300000d0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00"
 ]

# sequence 7 - bottom two lights
led_control_sequence_7 = [
 "0000000000030300000e0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f00",
 "0000000000030300000c0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d00",
 "0000000000030300000d0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00"
 ]

led_seqs = [led_control_sequence_8,
led_control_sequence_1,
led_control_sequence_2,
led_control_sequence_3,
led_control_sequence_4,
led_control_sequence_5,
led_control_sequence_6,
led_control_sequence_7,
led_control_sequence_8]

# three fun sequences for backlights

static_backlight_seq_1 = [
 "000000000003030001050100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500",
 "00000000000303030105ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f800",
 "000000000004030a0600ff98000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006c00"
 ]

static_backlight_seq_2 = [
 "000000000003030001050100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500",
 "00000000000303030105ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f800",
 "000000000004030a06ff6fd9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004200"
]

static_backlight_seq_3 = [
 "000000000003030001050100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500",
 "00000000000303030105ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f800",
 "000000000004030a062f00ff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000db00"
]

static_backlight_seq_off = [
  "000000000003030001050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400",
  "000000000003030301050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000700",
  "000000000001030a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800"
]

lightshow = [
static_light_seq_off,
static_light_seq_1,
static_light_seq_2,
static_light_seq_3,
static_light_seq_1,
static_light_seq_off
]

for seq in lightshow:
  led_seq = choice(led_seqs)
  for led_packet in led_seq:
    sendrecv(led_packet.decode('hex'))
    sleep(0.3)

  for packet in seq:
    sendrecv(packet.decode('hex'))
    sleep(0.4)

  led_seq = choice(led_seqs)
  for led_packet in led_seq:
    sendrecv(led_packet.decode('hex'))
    sleep(0.3)


# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)