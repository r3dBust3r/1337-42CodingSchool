#!/bin/bash

(
# Banner
echo "---------------------- SERVER STATS ----------------------"

# Architecture and kernel
echo "[*] Architecture: $(uname -a)"

# Physical CPUs
num_of_phys=$(lscpu | awk '/Socket\(s\):/ {print $2}')
echo "[*] No of physical CPUs: ${num_of_phys}"

# Virtual CPUs
echo "[*] No of virtual CPUs: $(nproc)"

# RAM usage
free_output=$(free -m)
total_ram=$(echo "$free_output" | awk '/Mem:/ {print $2}')
used_ram=$(echo "$free_output"  | awk '/Mem:/ {print $3}')
utilization=$((used_ram * 100 / total_ram))
echo "[*] Memory usage: ${used_ram}/${total_ram}MB (${utilization}%)"

# Disk usage
df_output=$(df -h /)
used_strg=$(echo "$df_output" | awk 'NR==2 {print $3}')
total_strg=$(echo "$df_output" | awk 'NR==2 {print $2}')
used_percent=$(echo "$df_output" | awk 'NR==2 {print $5}')
echo "[*] Disk usage: ${used_strg}/${total_strg} (${used_percent})"

# CPU load
mpstat 1 1 | awk '/Average/ {print "[*] CPU load: " 100 - $12 "%"}'

# Last reboot
echo "[*] Last boot: $(uptime -s)"

# LVM
if lsblk | grep -q lvm; then
    echo "[*] LVM use: Yes"
else
    echo "[*] LVM use: No"
fi

# TCP connections
if command -v ss >/dev/null 2>&1; then
    echo "[*] No of TCP Connections: $(ss -ta | grep -c ESTAB) ESTABLISHED"
else
    echo "[*] Connections TCP: $(netstat -t | grep -c ESTABLISHED) ESTABLISHED"
fi

# Logged users
echo "[*] Logged User: $(users | wc -w)"

# Network IP + MAC
echo -n "[*] Network: IP "
/usr/sbin/ifconfig \
    | grep -E "inet [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" \
    | grep -v 127.0.0.1 \
    | awk '{printf "%s ", $2}'

echo -n "("
 /usr/sbin/ifconfig \
    | grep ether \
    | awk '{printf " %s ", $2}'
echo ")"

# Sudo commands count
num_of_exec_sudo=$(journalctl -t sudo | grep -c 'COMMAND=')
echo "[*] Sudo: ${num_of_exec_sudo} cmd"

echo
) | wall
