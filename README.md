# The System Controller 4
The working code of the System Conroller 4 designed for grass roots industrial systems management.


# Install the code on a BeagleBone Black and get the application running

To ssh in, plug in BeagleBone via USB and then:

	ssh root@192.168.7.2

Change root to password, ssh in as root then:

	:> passwd

Add a personal user/password and add them to the admin group.  admin is needed to have sudo rights:

	:> adduser USERNAME
	:> usermod -a -G admin USERNAME

Also, you will want to add this user to the sudoers file with the following commands:

	:> sudo adduser dsmurl sudo

Make the networking through the router work.  Change the networking over to primary eth0 availability by editing /etc/network/interfaces.  Edit the primary section to look like this:

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

Install the python pin IO library dependencies.  Turns on and off pins, reads analog input
pins from python:

	:> sudo apt-get update
	:> sudo apt-get install build-essential python-setuptools python-pip python-smbus

Install the IO lib through pip and other dependencies.  This took around 10 minutes on my BeagleBone so don't think it crashed.

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

	:> update-rc.d apache2 enable

Install the code.  Find the revision you want on GitHub.com and git clone the current code or preferred revision, like:

	:> git clone https://github.com/dsmurl/DiySystemController4.git

Run the code and check the site:

	:> cd DiySystemController4
	:> sudo python wsgi.py

Run with debug logging by adding --log_level=debug

	:> sudo python wsgi.py --log_level=debug
