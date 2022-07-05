# HiddenRequest
A tool to combine [TorRequest](https://github.com/erdiaker/torrequest), an extension of Python Software Foundation's [Requests](https://github.com/psf/requests), [RandomHeaders](https://github.com/theriley106/RandomHeaders), and [ProtonVPN](https://github.com/Rafficer/linux-cli-community/blob/master/USAGE.md) with some useful processes to hide traffic.

## Install
    
    pip install hiddenrequest


## Dependencies 
Tor and ProtonVPN installed on your local machine.

## Setup
Tor via homebrew:
	
	brew install tor

For linux use the debian repo [Tor](https://support.torproject.org/apt/tor-deb-repo/). Once installed, edit `/etc/tor/torrc` and uncomment the line `ControlPort 9051` to allow your application to control tor.


ProtonVPN CLI via directions here: [ProtonVPN](https://github.com/Rafficer/linux-cli-community/blob/master/USAGE.md)Once installed, follow the setup steps for `protonvpn init`.

Next, open your sudo file to allow you to run ProtonVPN passwordless:

	sudo visudo

Below `%sudo ALL=(ALL:ALL) ALL` add `"username ALL=(ALL) NOPASSWD:/usr/local/bin/protonvpn"`, replacing `username` with your own username.

## Usage

	import HiddenRequest
	with HiddenRequest() as hr:
		r = hr.get('https://www.google.com')
		
Hidden Request automatically configures your VPN and will verify that your traffic is hidden. You can verify no IP or DNS leakage yourself using:
	
	bool = HiddenRequest().verify_hidden()
	
Includes randomized headers using [RandomHeaders](https://github.com/theriley106/RandomHeaders).

	with HiddenRequest() as hr:
		my_header_data = {"Content-Type":"image.jpeg"}
		my_header_data.append(hr.random_header)
   		r = hr.get('https://www.google.com', headers = my_header_data)
   		
HiddenRequest also inherits TorRequest methods like `reset_identity`.
		
		with HiddenRequest() as hr:
				# Your own machines IP that you want to hide
				original_data = hr.original_ip_data
				# Your new IP from a Tor relay
				first_data = hr.public_ip_data
				hr.reset_identity()
				# Another Tor relay IP
				new_data = hr.public_ip_data

## Testing

	pytest --pyargs HiddenRequest	
		
