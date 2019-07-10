# welkomscherm

# requirements
# install 

sudo apt-get install python-bs4
sudo python3 -m pip install PyMySQL



# making it autostart


sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
#@xscreensaver -no-splash
@point-rpi
@/usr/bin/python3 /home/pi/welkomscherm/welkomscherm.py



sudo nano /etc/lightdm/lightdm.conf
Add the following lines to the [SeatDefaults] section:

# don't sleep the screen 
xserver-command=X -s 0 dpms
