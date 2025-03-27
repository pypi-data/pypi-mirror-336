import time
from importlib.resources import files

import jpype


def get_jvm_path() -> str:
    """
    From the resources directory, return the path to the packages Java interpreter
    """
    return str(files("pythermogis") / "resources" / "java" / "coretto-17" / "bin" / "server" / "jvm.dll")

def get_thermogis_jar_path() -> str:
    """
    From the resources directory, return the path to the ThermoGIS Jar
    """
    return str(files("pythermogis") / "resources" / "thermogis_jar" / "thermogis-1.7.0-shaded_newprops.jar")

def start_jvm():
    """
    To use the JPype package a java .jar file has to be instantiated with a java virtual machine (jvm)
    This method ensures a clean startup of the jvm packaged with this repo
    :return:
    """
    if not jpype.isJVMStarted():
        jpype.startJVM(get_jvm_path(), classpath=[get_thermogis_jar_path()])


if __name__ == "__main__":
    start_jvm()