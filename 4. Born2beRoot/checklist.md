## Theory
- [ ] What is a virtual machine and how it works
- [ ] What is Hypervisor
- [ ] What is Debian
- [ ] What is Rocky
- [ ] What is the diff between Debian and Rocky
- [ ] What is SELinux and AppArmor and what's the diff between them
- [ ] What is LVM
- [ ] `lsblk`
- [ ] What is `aptitude` and `apt` and what's the diff between them
- [ ] What is VirtualBox and UTM, What's the diff between them
- [ ] What is UFW and firewalld
- [ ] What is SWAP
- [ ] What is SSH
- [ ] What is TTY

## Practice
#### Mendatory
- [ ] Download the latest stable Debian server 
- [ ] Install the server with at least 2 encrypted partitions using LVM

- [ ] Install SSH
- [ ] Config SSH on Port `4242`
- [ ] Disable root access over SSH
- [ ] SSH must run at every boot 

- [ ] Config UFW by disabling all ports except `4242`
- [ ] UFW must run at every boot 

- [ ] Config Hostname with the login ending with 42 `ottalhao42`
- [ ] Add a user as the login `ottalhao`
- [ ] This user must belong to group `user42` & `sudo` only

- [ ] Implement Strong password policy
- [ ] Your password has to expire every 30 days.
- [ ] The minimum number of days allowed before the modification of a password will be set to 2.
- [ ] The user has to receive a warning message 7 days before their password expires.
- [ ] Your password must be at least 10 characters long. it contains uppercase, lowercase, number, it must not contain more than 3 consecutive identical characters.
- [ ] The password must not include the name of the user.
- [ ] The following rule does not apply to the root password: The password must have at least 7 characters that are not part of the former password
- [ ] Of course, your root password has to comply with this policy.

- [ ] Auth with sudo has to be limited to 3 attempts in the event of an incorrect password.
- [ ] A custom message of your choice has to be displayed if an error due to a wrong password occurs when using sudo
- [ ] Each action using sudo has to be archived, both inputs and outputs. The log file has to be saved in the `/var/log/sudo/`
- [ ] The TTY mode has to be enabled for security reasons.
- [ ] For security reasons too, the paths that can be used by sudo must be restricted. Example `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin`

- [ ] Create a script `monitoring.sh` in bash
- [ ] At server startup (cronjob), the script will display some information on all terminals and *every 10 minutes* (take a look at wall). The banner is optional. No error must be visible
- [ ] The architecture of your operating system and its kernel version.
- [ ] The number of physical processors.
- [ ] The number of virtual processors.
- [ ] The current available RAM on your server and its utilization rate as a percentage.
- [ ] The current available storage on your server and its utilization rate as a percentage.
- [ ] The current utilization rate of your processors as a percentage.
- [ ] The date and time of the last reboot.
- [ ] Whether LVM is active or not.
- [ ] The number of active connections.
- [ ] The number of users using the server.
- [ ] The IPv4 address of your server and its MAC address.
- [ ] The number of commands executed with the sudo program.

#### Bonus
- [ ] Make a custom partitionning at the install level [See: page14](https://cdn.intra.42.fr/pdf/pdf/189107/en.subject.pdf)
- [ ] Setup a Wordpress website using *lighttpd*, *MariaDB*, and *PHP*.
- [ ] Setup a service of your choise, don't forget to modify the firewall

### EOW
- [ ] Check partitions
- [ ] Check username
- [ ] Check hostname
- [ ] Check groups
- [ ] Check sudo
- [ ] Check ssh
- [ ] Check password policies
- [ ] Check monitoring.sh
- [ ] Check firewall
- [ ] Check appArmor
- [ ] Check php, mariadb, lighthttpd
- [ ] Check wordpress
- [ ] Calculate the signature checksum value of *.vdi* file in *sha1* format
- [ ] Submit the finale `signature.txt`

### NOTE
- Note that your virtual machine’s *signature may be altered*
after your first evaluation. To solve this problem, you can
duplicate your virtual machine or *use save state*.

- The use of snapshots is *FORBIDDEN*.
