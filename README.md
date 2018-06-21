# Portable Cell Inititive - Captive Portal
A project by [Beamlink](https://www.beamlink.io)

Landing page for new users connecting to Beamlink cell towers during natural disasters or other emergencies

## Getting Started

The system works by integrating with the main [Portable Cell Initiative](https://github.com/Ironarcher/portable-cell-initiative/tree/master/software) code.

The master server, or VPN host, is a cloud server that is a gateway and control unit for the cell base stations. Install the code on that server, and use `twitter_cache.py` as the flask python file.

Each base station should be connected as a VPN client to the master server, and should install the code with `captiveportal.py` as the flask python file.

## Installing

First, install python and clone this repository in a new directory (the following example is for Ubuntu or Debian). On Windows, this can be done mostly manually, from the python website and using any git tools.
```
sudo apt-get install python
mkdir ~/code
cd ~/code
git clone https://github.com/Ironarcher/beamlink_captiveportal.git
```

Activate the virtual environment with:
`. venv/bin/activate` on Linux\OSX or `venv\Scripts\activate` on Windows

Choose server file (either captiveportal.py or twitter_cache.py): `export FLASK_APP=captiveportal.py` on Linux or `set FLASK_APP=captiveportal.py` on Windows

Run the development server: `flask run`

Now the server should be providing the webpage at http://127.0.0.1:5000 or the address listed after starting the development server 

Why use a virtual environment (venv)? It keeps the dependencies seperate from the rest of the system and keeps different python environments seperate from each other. On a system running multiple web servers and pieces of software, this is important.

## Using as a default page for mobile clients

The code of the Portable Cell Initiative configuration assigns new mobile connections IP addresses on the local network as 192.168.99.0/24 (range of IP addresses that are reserved).

## Built with
- [Flask](http://flask.pocoo.org/docs/1.0/installation/#installation) - Lightweight web server for Python
- [Tweepy](http://tweepy.readthedocs.io/en/v3.5.0/) - API library for accessing tweets on Python
- [Requests](http://docs.python-requests.org/en/master/user/quickstart/) - Make HTTP requests very easily in Python, for communicating between the master and client servers

## Going further

Enable the server everytime your computer reboots by adding it to the crontab with `crontab -e` on Linux. At the end of the file, add
`@reboot ~/code/

Use a production server like nginx and secure the firewall to only allow communication with the masterVPN and allowable mobile clients (192.168.99.0/24 for the Portable Cell Initiative configuration)
