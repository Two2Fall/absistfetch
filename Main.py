# Twell Evans (c) copyright 2026
# This file is the main file for absistfetch.
# Just run this file and absistfetch will execute.

import Fetch as f
from cnf.Configuration import *
from os import getlogin as GetUsername
from os.path import join as JoinPath
from os.path import abspath as AbsolutePath
from os.path import dirname as Dirname

Username: str = GetUsername().strip()
Hostname: str = f.GetHostname().strip()
COLOR = f"\033[38;2;{KEY_COLOR[0]};{KEY_COLOR[1]};{KEY_COLOR[2]}m"
CLEAR = "\033[0m"

BASE_DIR = Dirname(AbsolutePath(__file__))
with open(JoinPath(BASE_DIR, "cnf", LOGO_PATH), "r") as File:
    LogoFileLines: list[str] = File.readlines()

def CreateParagraph(Key: str, Value: str):
    return COLOR + f"{Key}: " + CLEAR + f"{Value}"

InfoOutput: list[str] = [
    f"{COLOR + Username + CLEAR}@{COLOR + Hostname + CLEAR}",
    "-" * 32,
    CreateParagraph("OS", f.GetOSRelease()),
    CreateParagraph("Kernel", f.GetKernel()),
    CreateParagraph("Uptime", f.GetUptime()),
    CreateParagraph("Shell", f.GetShell()),
    CreateParagraph("Terminal", f.GetTerminal()),
    CreateParagraph("Processor", f.GetAllCPUInfo()),
    CreateParagraph("RAM", f.GetRAMInfo()),
    CreateParagraph("Storage", f.GetStorageInfo()),
]
PrintOutput: list[str] = []

if len(InfoOutput) > len(LogoFileLines):
    for Index in range(len(InfoOutput) - len(LogoFileLines)):
        LogoFileLines.append("")

MaximumLength: int = max(len(Line) for Line in LogoFileLines)

for LFLIndex, LogoFileLine in enumerate(LogoFileLines):
    CleanLogoLine: str = LogoFileLine.rstrip('\r\n')
    if LFLIndex >= len(InfoOutput):
        PrintOutput.append(CleanLogoLine)
    else:
        PrintOutput.append(" " + CleanLogoLine.ljust(MaximumLength + 2) + InfoOutput[LFLIndex])

for PrintLine in PrintOutput:
    print(PrintLine)