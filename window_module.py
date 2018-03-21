#window_module.py

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
        #IP addresses for buttons
        self.ip_1 = "192.168.11.40"
        self.ip_2 = "192.168.1.10"
        self.ip_3 = "172.22.0.2"
        self.ip_4 = "10.0.0.1"

        #Interface names
        self.ethernet_interface = self.find_ethernet_name()
        self.wlan_interface = self.find_wlan_name()

        #The buttons themselves 
        btn1 = self.btn(self.ip_1, self.ip1, 100, 100, 0, 0)
        btn2 = self.btn(self.ip_2, self.ip2, 100, 100, 100, 0)
        btn3 = self.btn(self.ip_3, self.ip3, 100, 100, 0, 100)
        btn4 = self.btn(self.ip_4, self.ip4, 100, 100, 100, 100)
        btn5 = self.btn('WLAN off', self.wlan_off, 100, 50, 0, 200)
        btn6 = self.btn('WLAN on', self.wlan_on, 100, 50, 100, 200)
        btn7 = self.btn('ETH off', self.eth_off, 100, 50, 0, 250)
        btn8 = self.btn('ETH on', self.eth_on, 100, 50, 100, 250)
        btn9 = self.btn('Test', self.eth_on, 200, 100, 0, 300)
        
        #Show the GUI
        self.show()

    def change_ip(self, ipaddr): 
        with open('/etc/network/interfaces', 'r') as f:
            lines = f.readlines()
            with open(os.getcwd()+'/if_backup.txt', 'w') as bu:
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
            f.write("gateway 192.168.11.1\n")
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
            subprocess.run(['iconfig', self.wlan_interface, 'down'])

    def wlan_on(self):
        if self.wlan_interface == None:
            print('No WLAN interface found')
        else:
            subprocess.run(['iconfig', self.wlan_interface, 'up'])

    def eth_off(self):
        subprocess.run(['sudo', 'ifdown', self.ethernet_interface])
    
    def eth_on(self):
        subprocess.run(['sudo', 'ifup', self.ethernet_interface])

    def btn(self, name, func, xsize, ysize, xpos, ypos):
        btn = QtGui.QPushButton(name, self)
        btn.clicked.connect(func)
        btn.resize(xsize, ysize)
        btn.move(xpos, ypos)

    def find_ethernet_name(self):
        all_interfaces = os.listdir('/sys/class/net/')
        if len(all_interfaces)<4:
            for interface in all_interfaces:
                if interface[0] == 'e':
                    return(interface)
        else:
            print('Too many interfaces, paste name to ethernet_interface')

    def find_wlan_name(self):
        all_interfaces = os.listdir('/sys/class/net/')
        if len(all_interfaces)<4:
            for interface in all_interfaces:
                if interface[0] == 'w':
                    return(interface)
        else:
            print('Too many interfaces, paste name manually into wlan iface name!')
