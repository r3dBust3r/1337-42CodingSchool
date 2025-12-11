This project has been created as part of the 42 curriculum by **ottalhao**.

**Disclaimer:** I originally wrote the entire README.md myself, then used ChatGPT to rephrase and correct the English grammar.

## Born2beroot Project Description

This project involves setting up and securing a virtual server. I chose Debian as the operating system because it is stable, well-documented, and easy to maintain. It is a reliable choice for beginners and long-term server environments, offering strong community support and a consistent package system. Its main drawback is that it tends to use older software versions.
Rocky Linux is also stable and enterprise-oriented, but it can feel heavier and slightly more complex for a first server configuration.

---

## Instructions

I began by downloading the Debian ISO from the official website and creating a new VirtualBox VM with a 30.8 GB disk.
After booting the installer, I partitioned the drive according to the layout required in the Born2beroot subject (page 14), proceeded with the installation, and finished by installing GRUB.

Once the installation completed, I logged in using the credentials created during setup.

To verify connectivity, I tested the network with:

```bash
ping google.com -c3
```

Then I installed OpenSSH:

```bash
sudo apt install openssh-server
```

The subject requires SSH to listen on port **4242** and to block root login.
I configured this in `/etc/ssh/sshd_config`:

```ini
Port 4242
PermitRootLogin no
```

Next, I installed UFW:

```bash
sudo apt install ufw
```

Configured the default policies:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Allowed SSH:

```bash
sudo ufw allow 4242/tcp
```

Then I added a VirtualBox port-forwarding rule so I could connect from the host system:

```
SSH | TCP | 127.0.0.1 | 2222 | 10.0.2.15 | 4242
```

Enabled UFW:

```bash
sudo ufw enable
```

---

### User and Group Configuration

Created a new group:

```bash
sudo addgroup user42
```

Added my user to this group:

```bash
sudo usermod -aG user42 ottalhao
```

---

### Password Policy

Installed the necessary module:

```bash
sudo apt install libpam-pwquality
```

Configured password rules in `/etc/pam.d/common-password`:

```ini
password requisite pam_pwquality.so retry=3 minlen=10 ucredit=-1 lcredit=-1 dcredit=-1 maxrepeat=3 reject_username difok=7 enforce_for_root
```

Rule meanings:

* `retry=3` three attempts allowed
* `minlen=10` minimum length
* `ucredit=-1` at least one uppercase
* `lcredit=-1` at least one lowercase
* `dcredit=-1` at least one digit
* `maxrepeat=3` max repeating characters
* `reject_username` password cannot contain username
* `difok=7` at least 7 characters different from the old password
* `enforce_for_root` applies to root as well

---

### Sudo Configuration

Edited sudo policies with `visudo`, which writes to `/etc/sudoers`:

```ini
Defaults passwd_tries=3
Defaults badpass_message="a message for a bad auth"
```

Set up sudo logs:

```bash
sudo mkdir -p /var/log/sudo
sudo chmod 700 /var/log/sudo
```

Enabled logging inside `visudo`:

```ini
Defaults log_input
Defaults log_output
Defaults iolog_dir="/var/log/sudo"
```

Required a TTY:

```ini
Defaults requiretty
```

Restricted the secure execution path:

```ini
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

Viewed logs with:

```bash
sudo sudoreplay -l -d /var/log/sudo
sudo sudoreplay -d /var/log/sudo 000001
```

---

## Bonus Part

### Web Stack (Lighttpd, PHP, MariaDB)

Installed Lighttpd, PHP, and MariaDB:

```bash
sudo apt install lighttpd
sudo apt install php-cgi php-mysql
sudo apt install mariadb-server
```

Enabled the services:

```bash
sudo systemctl start lighttpd
sudo systemctl enable lighttpd
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

Enabled FastCGI:

```bash
sudo lighty-enable-mod fastcgi
sudo lighty-enable-mod fastcgi-php
sudo systemctl force-reload lighttpd
```

### WordPress Installation

Downloaded the latest WordPress zip from `wordpress.org`.

Went to `/var/www/html/` and installed `zip`:

```bash
sudo apt install zip
```

Extracted and moved WordPress files into `/var/www/html`.

Allowed HTTP traffic:

```bash
sudo ufw allow 80/tcp
```

Created a VirtualBox port forwarding entry:

```
HTTP | TCP | 127.0.0.1 | 8080 | 10.0.2.15 | 80
```

Created the WordPress database:

```bash
sudo mysql -u root
```

```sql
CREATE DATABASE ottalhao_wordpress;
CREATE USER webuser@localhost IDENTIFIED BY 'W3b@@Us3r%Sf11x';
GRANT ALL PRIVILEGES ON ottalhao_wordpress.* TO webuser@localhost;
FLUSH PRIVILEGES;
```

Completed the online WordPress setup via `http://localhost:8080`.

---

### FTP Service (vsftpd)

Installed vsftpd:

```bash
sudo apt install vsftpd
```

Edited `/etc/vsftpd.conf`:

```ini
listen_port=2150
chroot_local_user=YES
allow_writeable_chroot=YES
local_root=/var/vsftpd
pasv_min_port=40000
pasv_max_port=40005
dirmessage_enable=YES
```

UFW rules:

```bash
sudo ufw allow 2150/tcp
sudo ufw allow 40000:40005/tcp
```

Enabled and started the service:

```bash
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
```

---

## Monitoring Script

Created `/root/monitoring.sh` with all required statistics.
After testing it manually, I added cron jobs in `/etc/crontab`:

```
*/10 * * * * root /root/monitoring.sh
@reboot root /usr/bin/sleep 30 && /root/monitoring.sh
```

---

## Comparisons

### Debian vs Rocky Linux

**Debian**

* Very stable and reliable
* Large community support
* Beginner-friendly
* Older software versions

**Rocky Linux**

* Enterprise-focused
* Compatible with Red Hat environments
* Strong for production use
* Slightly more complex for beginners

---

### AppArmor vs SELinux

**AppArmor**

* Simple to configure
* Profile-based
* Good for small deployments
* Default on Debian

**SELinux**

* Very powerful
* Label-based access control
* More complex to manage
* Default on Rocky Linux

---

### UFW vs firewalld

**UFW**

* Very easy to use
* Ideal for small servers
* Works well on Debian

**firewalld**

* More advanced and flexible
* Supports zones
* Better for large or dynamic systems
* Common on Rocky Linux

---

### VirtualBox vs UTM

**VirtualBox**

* Widely supported
* User-friendly
* Great for testing and learning

**UTM**

* Designed for Apple Silicon
* Clean interface
* Multi-architecture support
* Less feature-rich than VirtualBox

---

## Resources Used

### Articles

* [https://www.vmware.com/topics/virtual-machine](https://www.vmware.com/topics/virtual-machine)
* [https://www.geeksforgeeks.org/linux-unix/linux-vs-unix/](https://www.geeksforgeeks.org/linux-unix/linux-vs-unix/)
* [https://en.wikipedia.org/wiki/AppArmor](https://en.wikipedia.org/wiki/AppArmor)
* [https://en.wikipedia.org/wiki/UTM_(software)](https://en.wikipedia.org/wiki/UTM_%28software%29)

### Videos

* [https://www.youtube.com/watch?v=yIVXjl4SwVo](https://www.youtube.com/watch?v=yIVXjl4SwVo)
* [https://www.youtube.com/watch?v=FZR0rG3HKIk](https://www.youtube.com/watch?v=FZR0rG3HKIk)
