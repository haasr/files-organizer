****************
files-organizer
****************

Python script to automagically sort your files according to their extensions.


.. contents:: Contents


Changes (6/13/2024)
###################

- Added logging options and incorporated basic INFO logging.
- Logging exception that may occur if user manually moves file at precisely the same time the program tries to.
- Added a few more audio extensions and the HEIC image extension to the default extensions map.
- Increased sleep time before file is moved from 1s to 2s.


Requirements
############

- Computer with Python 3.6+ installed

Setup
#####


Note that if ``python`` is used in a code block, you may have to substitute it for ``python3``
or ``py`` depending on your configuration. ``pip`` may also have to be substituted for ``pip3``.


1) Specify Your Path Prefix and username
----------------------------------------

In ``config.py``, uncomment the path prefix that matches your operating system. Comment out the other
path prefixes. Then replace 'User' with your computer's account username.


2) Customize which files get moved where
----------------------------------------

My default configuration in ``config.py`` is for my personal preferences. I listen for changes in both
my Downloads folder and my Desktop folder. If, for example, you do not wish to automatically sort files
in your Desktop folder, remove the second key-value pair in ``DIRECTORIES_MAP``.

``EXTENSIONS_MAP`` categorizes lists of extensions to check for. The lists are by no means
comprehensive. I just included the extensions that I expect to see often. You may, of course, alter
the categories (the keys) and the lists of extensions. Just ensure that all the categories used in
``DIRECTORIES_MAP`` are included as keys in ``EXTENSIONS_MAP`` to avert ``app.py`` from throwing a
``KeyError``. 

You can write as many key-value pairs as you like provided that you follow my format where each key in
``DIRECTORIES_MAP`` is a directory to monitor and the key's value is itself a dictionary listing the category
of files (which must be included as a key in ``EXTENSIONS_MAP``) and the directory to move such files.


3) Install the required packages
--------------------------------

From the root directory for this project, install the dependencies as such:

.. code:: powershell

    pip install -r requirements.txt


If you wish, you may create and install the required packages to a virtual environment instead:

(Powershell)

.. code:: powershell

    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt

(Linux)

.. code:: bash

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt


4) Configure ``files-organizer`` to Start Automagically
-------------------------------------------------------

Mac:
====

If you're using a Mac, you are going to have to figure this part out for yourself. I don't give a shit about
your Mac or your reasoning for why you use it. Apparently since some time in 2005 macOS uses an OS management
daemon called ``launchd``. You could try to write a ``launchd`` file in the form of a disturbingly verbose
plist XML script `like this <https://davidhamann.de/2018/03/13/setting-up-a-launchagent-macos-cron/>`_.

Windows:
========

In the ``system_scripts/Windows`` folder, I have created a one-line VB script to execute this project. simply
change the path to wherever the ``app.py`` file is located in your filesystem. Then copy the file into
``C:\Users\<User>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup``. To execute this program right
away, launch the ``Run dialog`` (Win + R), type "shell:startup" to open the startup folder, and double click on
the ``filesorganizer`` VB script.

Linux (with systemd):
=====================

If you're on Github *and* you use Linux, you probably don't need any help :D. Anyhow, I've created a ``start.bash``
script to work for the ``systemd`` service file in ``system_scripts/Linux`` to call on. I did that to simplify the
configuration if you wish to use a Python virtual environment for this project. If you are using a virtual environment
for this project, see where I have commented about inserting a command for activating your virtual environment in
``start.bash``.

Of course, if you are not using a virtual environment and for whatever reason it peaves you that ``systemd`` will be
indirectly invoking Python through the ``start.bash`` script, you can change the ExecStart line in
``system_scripts/Linux/filesorganizer.service`` to something like ``ExecStart=/usr/bin/python3 /home/<username>/files-organizer/app.py``
and just delete the start.bash script.

Ensure that you have edited the paths in ``start.bash`` and ``filesorganizer.service`` and that the bash script is
executable. Then copy the service file to ``/etc/systemd/system/``. Start and enable the service. Ex.:

.. code:: bash

    sudo cp /home/pi/files-organizer/system_scripts/Linux/filesorganizer.service /etc/systemd/system/
    sudo systemctl start filesorganizer
    sudo systemctl enable filesorganizer


| To check the status of the service and debug, use:
|  ``systemctl status filesorganizer``, and
|  ``sudo journalctl -u filesorganizer|tail -f``


Use Recursion
#############

The last line of code in ``config.py``, ``OBSERVER_RECURSIVE = False``
means that the Observer will not traverse any subdirectories for changes.
Toggle that to true if you wish to listen for changes in subdirectories
as well.

Logged output
#############

Logging settings are also configurable in ``config.py``. Unless you specify a path prefix in ``LOG_FILE_PATH``, the log file
will be stored in the program's working directory. E.g., if the program were invoked from a VB script in your startup folder,
you would find the log file in that folder.

If you notice that files are no longer being automagically moved as expected, check the log. If you identify bugs, please start
an issue in this repo, sharing the relevant log information, and your platform. Or if you've patched a bug, please reach out to
me or send a pull request!
