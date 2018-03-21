# ipchanger
Changes the IP address of your pc with a GUI, and allows you to turn WLAN on and off. A tool made for someone who configures routers and needs to change pc IP daily.

You need to install pyqt4 for python3

You need to add access to /etc/network/interfaces file for write access for all users. A backup will be made on the first button click of the interface file into the scripts working directory.

You also need to allow for ifdown and ifup to be run as sudo without requiring password, or alternatively run the script as sudo (not recommended).

The script will create a shortcut in the current directory named shortcutter.desktop, you need to give this permission to run as executable either by terminal chmod +x or by rightclicking and selecting it from permissions if you want to run the script through the shortcut.


