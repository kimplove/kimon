# kimon
A Process Monitoring Script using ps and iostat

This script is written by python language and very simple. 

Prerequisites
1. Python 2
2. Linux (Debian, Redhat)
3. Working linux commands of ps and iostat
4. Enalbed running with nopasswd sudo

Feautures
1. Monitoring specific processes that you want.
2. Reported CPU, Memory, Read/Write speed etc.. (ps -ax, iostat, iostat -x)
3. In case of multiple processes you want, reported sum values of CPU and Memory (ps -ax)

Usage: kimon-0.1.py [-h] [--period PERIOD] [--user USER] [--disk DISK] [--file FILE] [--output OUTPUT]
