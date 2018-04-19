#!/usr/bin/env python3
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
        self.btnlist = []
        self.home()

    def home(self):
        self.get_ip_from_file()
        #Interface names
        #Paste ethernet interface here if too many interfaces found
        self.ethernet_interface = self.find_ethernet_name()
        #Paste wlan interface name here if too many interfaces found.
        self.wlan_interface = self.find_wlan_name() 

        #The buttons themselves 
        for ip in self.IPList:
           self.ip_btn(ip)
        
        self.w_off   = QtGui.QPushButton('WLAN OFF', self)
        self.w_off.clicked.connect(lambda : self.wlan_off())

        self.w_on    = QtGui.QPushButton('WLAN ON', self)
        self.w_off.clicked.connect(lambda : self.wlan_on())

        self.e_off   = QtGui.QPushButton('ETHERNET OFF', self)
        self.e_off.clicked.connect(lambda : self.eth_off())

        self.e_on    = QtGui.QPushButton('ETHERNET ON', self)
        self.e_on.clicked.connect(lambda : self.eth_on())
        
        #Create layouts and add buttons to them
        vbox = QtGui.QVBoxLayout()
        for butn in self.btnlist:
            vbox.addWidget(butn)

        vbox.addWidget(self.w_off)
        vbox.addWidget(self.w_on)
        vbox.addWidget(self.e_off)
        vbox.addWidget(self.e_on)

        wid = QtGui.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vbox)

        #Show the GUI
        self.show()

    def change_ip(self, ipaddr): 
        subprocess.run(['notify-send', 'Changing IP to: '+ipaddr, '-t', '1000'])
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

    def wlan_off(self):
        if self.wlan_interface == None:
            subprocess.run(['notify-send', 'No WLAN interface found'])
        else:
            subprocess.run(['iconfig', self.wlan_interface, 'down'])
            subprocess.run(['notify-send', 'Turned WLAN off'])
            
    def wlan_on(self):
        if self.wlan_interface == None:
            subprocess.run(['notify-send', 'No WLAN interface found'])
        else:
            subprocess.run(['iconfig', self.wlan_interface, 'up'])
            subprocess.run(['notify-send', 'Turned WLAN on'])

    def eth_off(self):
        subprocess.run(['sudo', 'ifdown', self.ethernet_interface])
        subprocess.run(['notify-send', 'Turned ethernet off'])
    
    def eth_on(self):
        subprocess.run(['sudo', 'ifup', self.ethernet_interface])
        subprocess.run(['notify-send', 'Turned ethernet on'])

    def btn(self, name, func):
        btn = QtGui.QPushButton(name, self)
        btn.clicked.connect(func)

    def ip_btn(self, ipaddr):
        btn = QtGui.QPushButton(ipaddr, self)
        btn.clicked.connect(lambda x : self.change_ip(ipaddr))
        self.btnlist.append(btn)

    def find_ethernet_name(self):
        all_interfaces = os.listdir('/sys/class/net/')
        interface_list = []
        for interface in all_interfaces:
            if interface[0] == 'e':
                interface_list.append(interface)
        
        if len(interface_list) == 1:
            return(interface_list[0])

        else:
            subprocess.run(['notify-send', 'No eth interface found or too many'])
            return(None)


    def find_wlan_name(self):
        all_interfaces = os.listdir('/sys/class/net/')
        interface_list = []
        for interface in all_interfaces:
            if interface[0] == 'w':
                interface_list.append(interface)

        if len(interface_list) == 1:
            return(interface_list[0])

        else:
            subprocess.run(['notify-send', 'No WLAN interface found or too many'])
            return(None)

    def get_ip_from_file(self):
        try:
            with open(__file__[:-16]+'/IP_list.txt', 'r') as f:
                Addresses = f.readlines()
                self.IPList = []
                for address in Addresses:
                    self.IPList.append(address)
        except:
            print('fuck')

