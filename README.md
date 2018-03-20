# ipchanger
Changes the IP address of your pc with a GUI
You need to install pyqt4 for python3 
You need to add access to /etc/network/interfaces file for write access for all users, and also create an interfaces_backup file in /etc/network with write access so a backup of the interface file can be made.

You also need to allow for ifdown and ifup to be run as sudo without requiring password.

The script will create a shortcut in the current directory named shortcutter.desktop, you need to give this permission to run as executable either by terminal chmod +x or by rightclicking and selecting it from permissions if you want to run the script through the shortcut.
