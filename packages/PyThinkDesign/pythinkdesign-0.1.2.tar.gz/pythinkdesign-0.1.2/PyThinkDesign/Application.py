import win32com.client
from win32com.client import gencache
import pythoncom

def GetApplication():
    appLib = gencache.EnsureDispatch('ThinkDesign.Application')

    # 初始化COM库
    pythoncom.CoInitialize()

    # 创建TD Application对象实例
    app = win32com.client.Dispatch('ThinkDesign.Application')

    return app
