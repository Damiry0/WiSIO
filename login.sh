sshpass -p 'password-here'  ssh -tt pi@192.168.1.14 bash << EOF
    cd WiSIO
    python3 client.py
    exit
EOF
