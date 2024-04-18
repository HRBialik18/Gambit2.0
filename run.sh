#!/bin/bash

# Function to check Wi-Fi connection
check_wifi_connection() {
    if iwgetid | grep -q "ESSID"; then
        echo "Connected to Wi-Fi."
        return 0  # Return success status
    else
        echo "Not connected to Wi-Fi. Waiting..."
        return 1  # Return failure status
    fi
}

# Loop until Wi-Fi connection is established
while ! check_wifi_connection; do
    sleep 5  # Check Wi-Fi connection every 5 seconds
done

# Wi-Fi connection is established, proceed to run the Python program
echo "Wi-Fi connection established. Running Python program."

cd /home/pi/Documents/Gambit2.0/

source ./venv/bin/activate

# Run the Python program
python3 main.py
