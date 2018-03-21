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
        self.get_ip_from_file()
        #Interface names
        #Paste ethernet interface here if too many interfaces found
        self.ethernet_interface = self.find_ethernet_name()
        #Paste wlan interface name here if too many interfaces found.
        self.wlan_interface = self.find_wlan_name() 


        print(str(self.d) + 'Here are the IP:s')
        #The buttons themselves 
        btn1 = self.btn(self.d.get('ip0', 'No IP specified'), self.ip1, 100, 100, 0, 0)
        btn2 = self.btn(self.d.get('ip1', 'No IP specified'), self.ip2, 100, 100, 100, 0)
        btn3 = self.btn(self.d.get('ip2', 'No IP specified'), self.ip3, 100, 100, 0, 100)
        btn4 = self.btn(self.d.get('ip3', 'No IP specified'), self.ip4, 100, 100, 100, 100)
        btn5 = self.btn('WLAN off', self.wlan_off, 100, 50, 0, 200)
        btn6 = self.btn('WLAN on', self.wlan_on, 100, 50, 100, 200)
        btn7 = self.btn('ETH off', self.eth_off, 100, 50, 0, 250)
        btn8 = self.btn('ETH on', self.eth_on, 100, 50, 100, 250)
        
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
        if self.d.get('ip0', False):
            self.change_ip(self.d.get('ip0'))
        else:
            subprocess.run(['notify-send', 'No IP was specified in file'])

    def ip2(self):
        if self.d.get('ip1', False):
            self.change_ip(self.d.get('ip1'))
        else:
            subprocess.run(['notify-send', 'No IP was specified in file'])

    def ip3(self):
        if self.d.get('ip2', False):
            self.change_ip(self.d.get('ip2'))
        else:
            subprocess.run(['notify-send', 'No IP was specified in file'])

    def ip4(self):
        if self.d.get('ip3', False):
            self.change_ip(self.d.get('ip3'))
        else:
            subprocess.run(['notify-send', 'No IP was specified in file'])

    def wlan_off(self):
        if self.wlan_interface == None:
            subprocess.run(['notify-send', 'No WLAN interface found'])
        else:
            subprocess.run(['iconfig', self.wlan_interface, 'down'])

    def wlan_on(self):
        if self.wlan_interface == None:
            subprocess.run(['notify-send', 'No WLAN interface found'])
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
            msg = 'Too many interfaces, paste name to ethernet_interface'
            subprocess.run(['notify-send', msg])

    def find_wlan_name(self):
        all_interfaces = os.listdir('/sys/class/net/')
        if len(all_interfaces)<4:
            for interface in all_interfaces:
                if interface[0] == 'w':
                    return(interface)
        else:
            msg = 'Too many interfaces, paste name manually into wlan iface name!'
            subprocess.run(['notify-send', msg])

    def get_ip_from_file(self):
        with open(os.getcwd()+'/IP_list.txt', 'r') as f:
            Addresses = f.readlines()
            self.d = {}
            for i, address in enumerate(Addresses):
                self.d['ip{0}'.format(i)] = address
                print(self.d)
