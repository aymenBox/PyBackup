import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re
import json

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def System_information():
    system_info = {}

    uname = platform.uname()
    system_info['System'] = uname.system
    system_info['Node Name'] = uname.node
    system_info['Release'] = uname.release
    system_info['Version'] = uname.version
    system_info['Machine'] = uname.machine
    system_info['Processor'] = uname.processor
    system_info['Processor'] = cpuinfo.get_cpu_info()['brand_raw']
    system_info['Ip-Address'] = socket.gethostbyname(socket.gethostname())
    system_info['Mac-Address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    system_info['Boot Time'] = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

    cpufreq = psutil.cpu_freq()
    cpu_info = {
        'Physical cores': psutil.cpu_count(logical=False),
        'Total cores': psutil.cpu_count(logical=True),
        'Max Frequency': f"{cpufreq.max:.2f}Mhz",
        'Min Frequency': f"{cpufreq.min:.2f}Mhz",
        'Current Frequency': f"{cpufreq.current:.2f}Mhz",
        'CPU Usage Per Core': {}
    }

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_info['CPU Usage Per Core'][f'Core {i}'] = f"{percentage}%"

    cpu_info['Total CPU Usage'] = f"{psutil.cpu_percent()}%"

    system_info['CPU Info'] = cpu_info

    svmem = psutil.virtual_memory()
    memory_info = {
        'Total': get_size(svmem.total),
        'Available': get_size(svmem.available),
        'Used': get_size(svmem.used),
        'Percentage': f"{svmem.percent}%"
    }
    system_info['Memory Information'] = memory_info

    swap = psutil.swap_memory()
    swap_info = {
        'Total': get_size(swap.total),
        'Free': get_size(swap.free),
        'Used': get_size(swap.used),
        'Percentage': f"{swap.percent}%"
    }
    system_info['SWAP'] = swap_info

    disk_info = {'Partitions and Usage': []}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_info = {
            'Device': partition.device,
            'Mountpoint': partition.mountpoint,
            'File system type': partition.fstype
        }
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_info['Total Size'] = get_size(partition_usage.total)
            partition_info['Used'] = get_size(partition_usage.used)
            partition_info['Free'] = get_size(partition_usage.free)
            partition_info['Percentage'] = f"{partition_usage.percent}%"
        except PermissionError:
            continue

        disk_info['Partitions and Usage'].append(partition_info)

    disk_io = psutil.disk_io_counters()
    disk_io_info = {
        'Total read': get_size(disk_io.read_bytes),
        'Total write': get_size(disk_io.write_bytes)
    }
    disk_info['IO Statistics'] = disk_io_info

    system_info['Disk Information'] = disk_info

    network_info = {'Network Interfaces': []}
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        interface_info = {'Interface': interface_name}
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                interface_info['IP Address'] = address.address
                interface_info['Netmask'] = address.netmask
                interface_info['Broadcast IP'] = address.broadcast
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                interface_info['MAC Address'] = address.address
                interface_info['Netmask'] = address.netmask
                interface_info['Broadcast MAC'] = address.broadcast
        network_info['Network Interfaces'].append(interface_info)

    net_io = psutil.net_io_counters()
    network_io_info = {
        'Total Bytes Sent': get_size(net_io.bytes_sent),
        'Total Bytes Received': get_size(net_io.bytes_recv)
    }
    network_info['IO Statistics'] = network_io_info

    system_info['Network Information'] = network_info

    return json.dumps(system_info, indent=4)

if __name__ == "__main__":
    print(System_information())
