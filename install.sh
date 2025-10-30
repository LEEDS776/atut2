#!/bin/bash

echo "Installing ATUT Tool on Termux..."
echo "=================================="

pkg update && pkg upgrade -y
pkg install python python-pip git -y

echo "Installing Python dependencies..."
pip install scapy

echo "Cloning repository..."
git clone https://github.com/yourusername/atut-tool.git
cd atut-tool

echo "Making script executable..."
chmod +x atut.py

echo "Installation completed!"
echo "Usage: python atut.py -i TARGET_IP -p PORT -t THREADS"
echo "Example: python atut.py -i 192.168.1.1 -p 80 -t 100"
