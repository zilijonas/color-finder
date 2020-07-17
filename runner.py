#!/usr/bin/python3
import struct
import subprocess
import Quartz


def active_monitor() -> int:
    position = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    (err, ids, count) = Quartz.CGGetDisplaysWithPoint(position, 32, None, None)
    return ids[0]


def display_bounds(monitor_id: int) -> Quartz.CGRect:
    return Quartz.CGDisplayBounds(monitor_id)


def screenshot_as_bytes(bounds: Quartz.CGRect) -> Quartz.CFDataRef:
    (origin, size) = bounds
    CG = Quartz.CoreGraphics
    region = CG.CGRectMake(origin.x, origin.y, size.width, size.height)
    img = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)
    prov = CG.CGImageGetDataProvider(img)
    return CG.CGDataProviderCopyData(prov)


def mouse_position(bounds: Quartz.CGRect) -> tuple:
    position = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    x: int = position.x - bounds.origin.x
    y: int = position.y - bounds.origin.y
    return x, y


def pixel_color(x: int, y: int, bounds: Quartz.CGRect, bytes_per_row: int, data: Quartz.CFDataRef) -> tuple:
    data_format = "BBBB"
    pixels_per_point = bytes_per_row / bounds.size.width
    offset: int = pixels_per_point * ((bounds.size.width * int(y * pixels_per_point / 4)) + int(x))
    b, g, r, a = struct.unpack_from(data_format, data, offset=int(offset))
    return r, g, b


active_monitor_id = active_monitor()
screen_bounds = Quartz.CGDisplayBounds(active_monitor_id)
screen_bytes_per_row = Quartz.CGDisplayBytesPerRow(active_monitor_id)
raw_data = screenshot_as_bytes(screen_bounds)
pX, pY = mouse_position(screen_bounds)
rgb_color = pixel_color(pX, pY, screen_bounds, screen_bytes_per_row, raw_data)
subprocess.run("pbcopy", universal_newlines=True, input='#%02x%02x%02x' % rgb_color)
