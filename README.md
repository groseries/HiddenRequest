### HiddenRequest
A toll to combine Torrequests and 


## Dependencies 
Tor and ProtonVPN installed on your local machine.

## Setup
Tor via homebrew:
brew install tor
or use the tor debian repo: https://support.torproject.org/apt/tor-deb-repo/

edit /etc/tor/torrc and uncomment the line for ControlPorts to allow the application to control tor


Install ProtonVPN CLI following directions here: https://github.com/Rafficer/linux-cli-community/blob/master/USAGE.md

Open your sudo file to allow you to run protonVPN passwordless:
sudo visudo
below %sudo ALL=(ALL:ALL) ALL
add "username ALL=(ALL) NOPASSWD:/usr/local/bin/protonvpn" replacing username with your name

