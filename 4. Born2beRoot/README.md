This project has been created as part of the 42 curriculum by ottalhao

Disclaimer: I've written the entire README.md by myself, then gave it to chatgpt to rephrase and correct english grammer 

## Born2beroot Project Description
This project focuses on creating and configuring a secure virtual server. I chose to use Debian as the operating system. Debian is stable, well-documented, and easy to maintain, which makes it a good choice for beginners and for long-term server setups. Its main advantages are strong community support and a reliable package system. The downside is that it uses older software versions compared to some other distributions. Rocky Linux, on the other hand, is also stable and enterprise-focused, but it can feel heavier and more complex for a first server project.

## Instructions
First i started by downloading the debian iso image from the official server.
Created a new virtual machine on Virtualbox with 30.8GB.
Booted the installation
Splited the hard drive like the one on our subject (born2beroot page: 14)
Started the installation
then finished by installing GRUB

when the installation completed. I entered the system with the creds I choose during the installtion to login.

started by checking whatever i have internet connection or not by running
`ping google.com -c3`

then started installing the first package `ssh`
by running `sudo apt install openssh-server`

the subject says the server must listen on port 4242 and prevent root access over it
i search online where can i find openssh config.
i found it on `/etc/ssh/sshd_config`

```bash
Port 4242
PermitRootLogin no
```

then installed ufw by running `sudo apt install ufw`
i had to deny all incomming connections and allow outgoing
so i added these rules

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

then i allowed only ssh with this rule `sudo ufw allow 4242/tcp`

created a port forwarding on virtualbox so i can use SSH from my host
settings -> network -> advanced -> port forwarding

```
NAME | PROTOCOL | HOST IP   | HOST PORT | GUEST IP  | GUEST PORT
-----+----------+-----------+-----------+-----------+-----------
SSH  | TCP      | 127.0.0.1 | 2222      | 10.0.2.15 | 4242
```

i enabled ufw with this command
```bash
sudo ufw enable
```

after that, i had to create a new group called `user42`

`sudo addgroup user42`

then i added my user to this group
`sudo usermod -aG user42 ottalhao`


then i moved to apply those password policies

i searched online, then found out that i have to install extra package called *libpam-pwquality*
installed it with 
`sudo apt install libpam-pwquality`

then started doing those policies on `/etc/pam.d/common-password`
```
password requisite pam_pwquality.so retry=3 minlen=10 ucredit=-1 lcredit=-1 dcredit=-1 maxrepeat=3 reject_username difok=7 enforce_for_root
```

retry=3                    ->  3 retries
minlen=10                  ->  min length is 10 characters
ucredit=-1                 ->  at least 1 uppercase
lcredit=-1                 ->  at least 1 lowercase
dcredit=-1                 ->  at least 1 digit
maxrepeat=3                ->  max repeat of a character is 3 times
reject_username            ->  password doesn't include username
difok=7                    ->  less than 7 characters from the old password 
enforce_for_root           ->  apply the rules on root

then moved to the sudo policies by using `visudo`

visudo write to `/etc/sudoers`

so i had to add these lines

```bash
Defaults    passwd_tries=3
Defaults    badpass_message="Wa hassan hhh"
```

passwd_tries    -> how many try you will have
badpass_message -> what message you get when you enter an invalid password


then i had to config the sudo logs, created a directory /var/log/sudo where i wll store the logs
and prevet access to all users on the server except root

```bash
sudo mkdir -p /var/log/sudo
sudo chmod 700 /var/log/sudo
```

headed into the same file `visudo` so i can apply these logs

```bash
Defaults    log_input
Defaults    log_output
Defaults    iolog_dir="/var/log/sudo"
```

activated TTY with 
`Defaults    requiretty`

and secured the path where sudo will work on with
`Defaults    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"`


i found that the log captured on each sudo use,
i used these commands to load the log
`sudo sudoreplay -d /var/log/sudo -l` -> load all logs
`sudo sudoreplay -d /var/log/sudo 000001` -> load a specific one


then i headed to the bonus part.
now i have to install 3 packages
- lighttpd  -> webserver
- php		-> backend language
- mariadb 	-> database

installed all of them with


```bash
sudo apt install lighttpd
sudo apt install php-cgi php-mysql
sudo apt install mariadb-server
```

started & enabled the webserver and mariadb with

```bash
sudo systemctl start lighttpd
sudo systemctl enable lighttpd
sudo systemctl start mariadb
sudo systemctl enable mariadb
```



i loaded fastcgi module, so i can use php
```bash
sudo lighty-enable-mod fastcgi
sudo lighty-enable-mod fastcgi-php
```

restarted the web server
```bash
sudo systemctl force-reload lighttpd
```

now i had to install wordpress.
headed to the official website and downloaded the latest wordpress version
`https://wordpress.org/latest.zip`

did `cd` to `/var/www/html/`

installed a new package `zip` so i can extract the package
`sudo apt install zip`

moved all wordpress files from `/var/www/html/wordpress` to the root of the web server `/var/www/html`

added a new rule on ufw to allow port 80
```bash
sudo ufw allow 80/tcp
```

created a new port forwarding rule for the web service

```
NAME | PROTOCOL | HOST IP   | HOST PORT | GUEST IP  | GUEST PORT
-----+----------+-----------+-----------+-----------+-----------
HTTP | TCP      | 127.0.0.1 | 8080      | 10.0.2.15 | 80
```

created a database from mardiadb console
`sudo mysql -u root`
```sql
create database ottalhao_wordpress;
```

and create a new user for this database
```sql
CREATE USER webuser@localhost IDENTIFIED BY 'W3b@@Us3r%Sf11x';
GRANT ALL PRIVILEGES ON ottalhao_wordpress.* TO webuser@localhost;
FLUSH PRIVILEGES;
```

headed to my browser and visited to `http://localhost:8080`
installed wordpress, and configured it.


then moved to the second service, i choose ftp.
`sudo apt install vsftpd` 

headed to the config file `vim /etc/vsftpd.conf`
to customize my ftp server

```ini
# Change the listening port from the default 21 to 2150
listen_port=2150

# Trap users in their directory so they cannot browse the entire system (e.g., /etc, /usr)
chroot_local_user=YES

# Allow the chroot jail to work even if the directory is writable (prevents "500 OOPS" error)
allow_writeable_chroot=YES

# Force the user to land in this specific folder upon login
local_root=/var/vsftpd

# Set the minimum port for passive data transfers (allows traversing firewalls)
pasv_min_port=40000
# Set the maximum port for passive data transfers
pasv_max_port=40005

# Show a message to the user when they enter a directory (if a .message file exists)
dirmessage_enable=YES
```

added new rules for this ftp server to work properly
```bash 
ufw allow 2150/tcp
ufw allow 40000:40005/tcp
```

then enabled & restarted the server 
```bash
systemctl start vsftdp
systemctl enable vsftdp
```

now the last thing: monitoring.sh
created `/root/monitoring.sh` with all stats the subject said then:
testted the script manulay, when i made sure it's fine
added a new cron job for the script to work each 10 minutes and every reboot in `/etc/crontab`

like this:

```
*/10 * * * * root /root/monitoring.sh
@reboot root /usr/bin/sleep 30 && /root/monitoring.sh
```

### **Debian vs Rocky Linux**

**Debian**

* Very stable and reliable
* Large community and lots of documentation
* Easy to use for beginners
* Uses older software versions (less up to date)

**Rocky Linux**

* Enterprise-focused and very stable
* Compatible with Red Hat–based environments
* Good for production servers
* Can feel more complex for new users

### **AppArmor vs SELinux**

**AppArmor**

* Easier to configure
* Uses profile-based rules
* Good for simpler setups
* Supported by Debian

**SELinux**

* Very powerful and detailed
* Uses security contexts and labels
* Harder to configure and troubleshoot
* Used by Rocky Linux and other Red Hat systems

### **UFW vs firewalld**

**UFW (Uncomplicated Firewall)**

* Extremely easy to use
* Basic and fast rules
* Great for small servers
* Works well on Debian

**firewalld**

* More advanced and flexible
* Supports zones and complex rules
* Better for large or dynamic environments
* Common on Rocky Linux

### **VirtualBox vs UTM**

**VirtualBox**

* Very popular and widely supported
* Easy to use
* Works on many systems
* Great for learning and testing

**UTM**

* Designed for Apple Silicon devices
* Simple interface
* Supports many architectures
* Not as feature-rich as VirtualBox


## Resources I Used

### What is a VM

##### Articles
- https://www.vmware.com/topics/virtual-machine
- https://www.geeksforgeeks.org/linux-unix/linux-vs-unix/
- https://en.wikipedia.org/wiki/AppArmor
- https://en.wikipedia.org/wiki/UTM_(software)


##### Videos
- https://www.youtube.com/watch?v=yIVXjl4SwVo
- https://www.youtube.com/watch?v=FZR0rG3HKIk
