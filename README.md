# The System Controller 4
The working code of the System Conroller 4 designed for grass roots industrial systems management.


# Install the code on a BeagleBone Black and get the application running

To ssh in, plug in BeagleBone via USB and then:

	ssh root@192.168.7.2

The default root password on these systems is known to default to empty.  So, for security, change root user password with this command to something only you know and don't forget it:

	:> passwd
	
These systems have an out of the box user named 'debian'. The debian user has a known default password of 'temppwd'.  So, change the debian user password with this command to something only you know and don't forget it:

	:> passwd debian

Add a personal user/password and add them to the admin group.  admin is needed to have sudo rights:

	:> adduser USERNAME
	:> usermod -a -G admin USERNAME

Also, you will want to add this user to the sudoers file with the following commands:

	:> sudo adduser USERNAME sudo
	
BeagleBoard.org can't ship support for everything on release day, so they push out new kernels as fixes, support for new capes, etc are posted on the BeagleBoard.org mainline list.  Run the following to upgrade the kernel:

	:> cd /opt/scripts/tools/
	:> git pull
	:> sudo ./update_kernel.sh
	:> sudo reboot
	
You will now be kicked back out to your host computer's terminal prompt.  Once the Beagle Bone has had a minute to rebbot, you will want to shell back into it with the instructions for root shell at the very first of this readme.  Remember to use the new password that you set and then continue.

Make the networking through the router work.  Change the networking over to primary eth0 availability by editing /etc/network/interfaces.  In this example below, which you can copy, we are choosing 192.168.0.50 as the IP address but it can be aligned in different ways.  Remember what you set it to because we will use this address in the end to view your system controller.  Edit the primary section to look like this:

	# The primary network interface
	allow-hotplug eth0
	iface eth0 inet static
	    address 192.168.0.50
	    netmask 255.255.255.0
	    gateway 192.168.0.1

Now take the Beaglebone off the USB connection and add power to from the AC adapter and give it a hard line connection to your network router.  

It needs it's own network address and internet access at this point to continue to install the code and the dependencies.  The USB connection has trouble providing the BeagleBone with outer web.

So, now we can shell into the BeagleBone with the USERNAME and password you created above.  You will need to also remember the address line that you added to the /etc/network/interfaces file.  Shell into the BeagleBone now like this:

	:> ssh USERNAME@IP_ADDRESS_YOU_SET

Once you are in, set the correct time:

	:> sudo ntpdate pool.ntp.org

Install the python pin IO library dependencies.  These packages allow your your python code to turn on and off pins and read analog input pins from python.

	:> sudo apt-get update
	:> sudo apt-get install build-essential python-setuptools python-pip python-smbus
	
Now that you have all the libraries you want installed from apt-get, you can do a full debian distribution upgrade to make sure everything installed is up to date.  This may take several minutes.

	:> sudo apt-get dist-upgrade

Install the IO lib through pip and other dependencies.  This took around 10 minutes on my BeagleBone.  So, don't think it crashed.

	:> sudo pip install Adafruit_BBIO gevent webapp2 webob python-memcached ws4py jinja2 peewee

Test your install with:

	:> sudo python -c "import Adafruit_BBIO.GPIO as GPIO; print GPIO"

Should result in:

	<module 'Adafruit_BBIO.GPIO' from '/usr/local/lib/python2.7/dist-packages/Adafruit_BBIO/GPIO.so'>

Disable Apache2 ( or get it off listening to port 8080):
	
	:> update-rc.d apache2 disable

Also, turn Apache2 off so that we can run our code through 8080 soon:

	:> sudo service apache2 stop

For later reference, you can add the apache auto-start back in with:

	:> sudo update-rc.d apache2 enable

Install the code.  Find the revision you want on GitHub.com and git clone the current code or preferred revision, like:

	:> git clone https://github.com/dsmurl/TheSystemController4.git

Run the code and check the site:

	:> cd TheSystemController4
	:> sudo python wsgi.py

Run with debug logging by adding --log_level=debug

	:> sudo python wsgi.py --log_level=debug
	
To see your system controller, with a browser, go to the static IP address you set in the network setting section above on the port 8080.  In our example it was 192.168.0.50.  So, go to the following address:

	192.168.0.50:8080

Enjoy and let me know what you think.  Please feel free to check out the code, project feature requests, and milestones to help me code some.  Thanks for checking out my project!

