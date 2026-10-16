# Twell Evans (c) copyright 2026
# This file contains the main core for the absistfetch 
# functionality, this fetches all the necessary information.

from os import environ as SystemEnviron
from os import statvfs as StatFS
from os import uname as OSUname

# Special files that contains system information
OS_RELEASE_FILE      = "/etc/os-release"
KERNEL_VERSION_FILE  = "/proc/version"
CPU_INFORMATION_FILE = "/proc/cpuinfo"
MEM_INFORMATION_FILE = "/proc/meminfo"
UPTIME_FILE          = "/proc/uptime"
ROOT_DIRECTORY       = "/"

# Other constants
SECONDS_ON_A_DAY     = 86_400
SECONDS_ON_AN_HOUR   = 3600

def GetKernel() -> str:
    with open(KERNEL_VERSION_FILE, "r") as VersionFile:
        VersionFileContent: str = VersionFile.read()
    return VersionFileContent.split()[2]

def GetOSRelease() -> str:
    with open(OS_RELEASE_FILE, "r") as OSReleaseFile:
        OSReleaseFileContent: list[str] = OSReleaseFile.readlines()
    return OSReleaseFileContent[1].split("=")[1].strip()[1:-1]

def GetCPUInformation() -> str:
    with open(CPU_INFORMATION_FILE, "r") as CPUInfoFile:
        CPUInfoFileContent: list[str] = CPUInfoFile.readlines()
    return CPUInfoFileContent[4].split(":")[1].strip()

def GetCPUBits() -> int:
    with open(CPU_INFORMATION_FILE, "r") as CPUInfoFile:
        CPUInfoFileContent: list[str] = CPUInfoFile.readlines()
    LineToRead: str = ""
    for Line in CPUInfoFileContent:
        if Line.startswith("flags"):
            LineToRead = Line
            break
    for Flag in LineToRead.split(":")[1].split():
        if Flag == "lm":
            return 64
    return 32

def GetAllCPUInfo():
    return f"{GetCPUInformation()} ({GetCPUBits()} bits)"

def GetUptime():
    with open(UPTIME_FILE, "r") as UptimeFile:
        UptimeFileContent: str = UptimeFile.read()
    
    UptimeInSeconds: int = int(float(UptimeFileContent.split()[0]))

    Days: int = UptimeInSeconds // SECONDS_ON_A_DAY
    Hours: int = (
        UptimeInSeconds - (Days * SECONDS_ON_A_DAY)
    ) // SECONDS_ON_AN_HOUR
    Minutes: int = (
        UptimeInSeconds - (Days * SECONDS_ON_A_DAY) - (Hours * SECONDS_ON_AN_HOUR)
    ) // 60
    Seconds: int = UptimeInSeconds - (Days * SECONDS_ON_A_DAY) - (Hours * SECONDS_ON_AN_HOUR) - (Minutes * 60)

    return f"{Days}d {Hours}h {Minutes}m {Seconds}s"

def GetShell():
    return SystemEnviron.get("SHELL", "Unknown")

def GetTerminal():
    return SystemEnviron.get("TERM", "Unknown")

def GetRAMInfo():
    with open(MEM_INFORMATION_FILE, "r") as MemInfoFile:
        MIFContent: list[str] = MemInfoFile.readlines()
    TotalRAM: int = int(MIFContent[0].split(":")[1].split()[0])
    NotUsedRAM: int = int(MIFContent[2].split(":")[1].split()[0])
    UsedRAM: int = TotalRAM - NotUsedRAM
    
    TotalRAMInGB: float = round(TotalRAM / 1_000_000, 2)
    UsedRAMInGB: float = round(UsedRAM / 1_000_000, 2)
    return f"{UsedRAMInGB} GB / {TotalRAMInGB} GB"

def GetStorageInfo():
    FilesystemStats = StatFS(ROOT_DIRECTORY)
    TotalFSBytes: int = FilesystemStats.f_blocks * FilesystemStats.f_frsize
    TotalGBUsed: float = round(TotalFSBytes / (1000 ** 3), 2)

    AvailableFSBytes: int = FilesystemStats.f_bavail * FilesystemStats.f_frsize
    FreeFSBytes: int = TotalFSBytes - AvailableFSBytes
    FreeGB: float = round(FreeFSBytes / (1000 ** 3), 2)

    return f"{FreeGB} GB / {TotalGBUsed} GB"

def GetHostname():
    return OSUname().nodename