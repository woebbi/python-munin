
Munin Plugins for Mobience
============

Plugins
----------
* mobience_delay   : time delay (minute)

Requirements
-----------
* python3+

Installation (ubuntu)
------------

**Install plugins**

    git clone https://github.com/madmanteam/python-munin.git /tmp/python-munin
    sudo cp /tmp/python-munin/mobience_delay /usr/share/munin/plugins
    sudo ln -sf /usr/share/munin/plugins/mobience_delay /etc/munin/plugins/mobience_delay
    sudo chmod +x /usr/share/munin/plugins/mobience_delay
    sudo service munin-node restart

Check if plugins are running:

    munin-node-configure | grep "mobience_delay"

Test plugin output:

    munin-run mobience_delay

FILE LOG
-----------

In file  plugins/mobience_delay:

    path = os.environ.get('LOG_URI', "/home/vagrant/log/mobience_log")

Edit "/home/vagrant/log/mobience_log" to path of your log.
Or set LOG_URI to environ

