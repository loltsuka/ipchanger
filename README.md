# ipchanger
Changes the IP address of your pc with a GUI
You need to install pyqt4 for python3 
You need to add access to /etc/network/interfaces file for write access for all users, and also create a interfaces_backup file with write access so a backup of the interface file can be made.

You also need to allow for ifdown and ifup to be run as sudo without requiring password.
