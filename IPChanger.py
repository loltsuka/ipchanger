#pyqt_test2.py
#!/usr/bin/env python3

import os
import subprocess
import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        #super()
        self.setGeometry(50,50,200,300)
        self.setWindowTitle("IP changer")
        self.home()

    def home(self):
        self.ip_1 = "192.168.11.40"
        self.ip_2 = "192.168.1.10"
        self.ip_3 = "172.22.0.2"
        self.ip_4 = "10.0.0.1"
        self.ethernet_interface = find_ethernet_name()
        self.wlan_interface = find_wlan_name()

        btn = QtGui.QPushButton(self.ip_1, self)
        btn.clicked.connect(self.ip1)
        btn.resize(100,100)
        btn.move(0,0)

        btn2 = QtGui.QPushButton(self.ip_2, self)
        btn2.clicked.connect(self.ip2)
        btn2.resize(100,100)
        btn2.move(0,100)
        
        btn3 = QtGui.QPushButton(self.ip_3, self)
        btn3.clicked.connect(self.ip3)
        btn3.resize(100,100)
        btn3.move(100,0)
        
        btn4 = QtGui.QPushButton(self.ip_4, self)
        btn4.clicked.connect(self.ip4)
        btn4.resize(100,100)
        btn4.move(100,100)
        
        btn5 = QtGui.QPushButton('WLAN off' ,self)
        btn5.clicked.connect(self.wlan_off)
        btn5.resize(100,50)
        btn5.move(0,200)

        btn6 = QtGui.QPushButton('WLAN on' ,self)
        btn6.clicked.connect(self.wlan_on)
        btn6.resize(100,50)
        btn6.move(100,200)

        btn7 = QtGui.QPushButton('Toggle ethernet on/off' ,self)
        btn7.clicked.connect(self.toggle_ethernet)
        btn7.resize(200,50)
        btn7.move(0,250)

        self.show()

    def change_ip(self, ipaddr): 
        with open('/etc/network/interfaces', 'r') as f:
            lines = f.readlines()
            with open('/etc/network/interfaces_backup', 'w') as bu:
                i = 0
                while i<len(lines):
                     bu.write(lines[i])
                     i += 1

        with open('/etc/network/interfaces', 'w') as f:
            f.write("#The loopback network interface\n")
            f.write("auto lo "+ self.ethernet_interface +"\n")
            f.write("iface lo inet loopback\n")
            f.write("auto "+ self.ethernet_interface +"\n") 
            f.write("iface " + self.ethernet_interface + " inet static\n")
            f.write("address " + ipaddr + "\n")
            f.write("netmask 255.255.255.0\n")
            #f.write("gateway 192.168.11.1\n")
            f.write("dns-nameserver 8.8.8.8\n")

    def ip1(self):
        self.change_ip(self.ip_1)

    def ip2(self):
        self.change_ip(self.ip_2)

    def ip3(self):
        self.change_ip(self.ip_3)

    def ip4(self):
        self.change_ip(self.ip_4)

    def wlan_off(self):
        if self.wlan_interface == None:
            print('No WLAN interface found')
        else:
            subprocess.run(['sudo', 'ifdown', self.wlan_interface])

    def wlan_on(self):
        if self.wlan_interface == None:
            print('No WLAN interface found')
        else:
            subprocess.run(['sudo', 'ifup', self.wlan_interface])

    def toggle_ethernet(self):
        subprocess.run(['sudo', 'ifdown', self.ethernet_interface])
        subprocess.run(['sudo', 'ifup', self.ethernet_interface])

def run():
    find_ethernet_name()
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

def find_ethernet_name():
    all_interfaces = os.listdir('/sys/class/net/')
    if len(all_interfaces)<4:
        for interface in all_interfaces:
            if interface[0] == 'e':
                return(interface)
    else:
        print('Too many interfaces, paste name to ethernet_interface')

def find_wlan_name():
    all_interfaces = os.listdir('/sys/class/net/')
    if len(all_interfaces)<4:
        for interface in all_interfaces:
            if interface[0] == 'w':
                return(interface)
    else:
        print('Too many interfaces, paste name manually into wlan iface name!')

run()
