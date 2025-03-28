import win32com.client
import pythoncom
from win32com.client import gencache


def Point(x=0.0, y=0.0, z=0.0, tolerance=0.001):
    point = win32com.client.Dispatch("Geo3d.Point")
    point.Set(x, y, z, tolerance)
    return point


def Vector(x=0.0, y=0.0, z=0.0, tolerance=0.1):
    vector = win32com.client.Dispatch("Geo3d.Vector")
    vector.Set(x, y, z, tolerance)
    return vector

def Angle(angle_size=0.0):
    angle = win32com.client.Dispatch("Geo3d.Angle")
    angle.AngleSize = angle_size
    return angle

def Length(length_size = 0.0):
    length = win32com.client.Dispatch("Geo3d.Length")
    length.LengthSize = length_size
    return length