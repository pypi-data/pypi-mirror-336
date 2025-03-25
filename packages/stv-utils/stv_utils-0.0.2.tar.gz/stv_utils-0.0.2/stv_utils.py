__version__ = "0.0.2"

def is_ch():
    """ 如果是Windows系统，且是中文环境，返回True"""
    import locale
    return 'Chinese' in str(locale.getlocale())


def system_check():
    """使用platform检测是否为Windows系统"""
    import platform
    return platform.system() == "Windows"


def is_idle():
    """通过检查 sys.modules 来判断是否在IDLE中运行"""
    import sys
    return 'idlelib' in sys.modules


def system_clear():
    import os
    """根据系统选择清屏命令"""
    """如果是IDLE则不执行清屏"""
    if not is_idle():
        os.system("cls" if system_check() else "clear")
