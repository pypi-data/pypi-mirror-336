.. _install-windows-exe:

####################
Windows Installation
####################

.. warning:: It is recommended that you enable long paths on Windows
            to prevent any files from not being copied during installation.
            Follow https://www.microfocus.com/documentation/filr/filr-4/filr-desktop/t47bx2ogpfz7.html,
            then reboot to enable long paths

.. _win_prereqs:

************************
Prerequisites
************************

==============
Installing WSL
==============

The only prerequisite for ChipWhisperer on Windows is enabling and installing a distribution
for Windows Subsystem for Linux (WSL). If you don't already have this enabled:

1. Follow `Microsoft's instructions for enabling WSL <https://learn.microsoft.com/en-us/windows/wsl/install>`_.
2. Restart your computer.
3. Open a command prompt or powershell windows and run :code:`wsl --install -d ubuntu`
4. Restart your computer again

Our Windows installer will install some compilers for building target firmware. This step requires an
internet connection, so if you want to complete this step ahead of time, or if this step fails during
installation, please see :ref:`Installing_Compilers_In_WSL`.

============================
Installing Compilers In WSL:
============================

Our Windows installer will attempt to install compilers for building target firmware in WSL. This is both
the only part of the install that requires an internet connection and the only part that requires
WSL during the install (the updater requires both as well, but doesn't run during the install). 
It is also completely independent of the rest of the install. As such, you may want to manually
complete this step before or after running the installer.

Installing the compilers can be easily done, if you have :ref:`WSL installed <win_prereqs>`, by
running the following commands:

1. Run WSL
2. Run :code:`sudo apt update`.
3. Run :code:`sudo apt install -y build-essential gcc-arm-none-eabi gcc-avr avr-libc`

.. image:: _images/win-installer-3.png
    :width: 800

.. _win_run_install:

************************
Running the Installer
************************

If you want to run a native Windows installation of ChipWhisperer, your best 
bet is to run the Windows installer, which takes care of getting the 
prerequisites for you. The steps for using the installer are as follows:

1. Navigate to the `ChipWhisperer release page <https://github.com/newaetech/chipwhisperer/releases>`_ on Github.

.. image:: _images/win-installer-1.png
  :width: 800

2. Find the latest ChipWhisperer Windows install executable (currently :code:`Chipwhisperer.v6.0.0.exe`)


3. Run the installer. A summary of the installation is given on the second page.

.. image:: _images/win-installer-2.png
  :width: 800

4. Run the executable and choose the path you want to install ChipWhisperer at. You must have read/write permissions for the location you install to, so avoid installing in a location like :code:`C:\\Program Files` or the like. The default install location (the user's home directory) will work for most users.

5. Choose whether or not you want to create a desktop shortcut for running ChipWhisperer.

6. Wait for the installation to finish. Additional windows will pop up during the installation to setup Python and install WSL compilers.

7. Some additional checks are run after the installation has completed. If any issues arise, you will be notified via a message box.

.. _Installing_Compilers_In_WSL:


**********************
Installed Applications
**********************

=====================
ChipWhisperer
=====================

Once you've completed the above, you should have a fully functioning, self-contained installation
with everything you need. 

The easiest way to launch ChipWhisperer and get started with the tutorials is by running the ChipWhisperer
application, available via the Start Menu, the folder where you installed ChipWhisperer, or, if you selected
this, via a desktop shortcut. After running, you should see a terminal pop up, followed by a new window open 
in your browser:

.. image:: _images/Jupyter\ ChipWhisperer.png

Once you see this open, we recommend clicking on :code:`jupyter`, then running through :code:`0 - Introduction to Jupyter Notebooks.ipynb`
to verify that everything installed correctly. If you run into any issues, please ask on our `forums`_ for help.

======================
Chipwhisperer Updater
======================

Installers for ChipWhisperer are only built every time we do a stable release. As the time between releases can be
quite lengthy, you may want to update ChipWhisperer before the next release. The easiest way to do this is to use the
:code:`ChipWhisperer-Updater` application, which automates the process.

.. warning:: During this process, we try to save changes made to the ChipWhisperer and ChipWhisperer-Jupyter repoisitores. If this
  process fails, the user will be notified and asked if they wish to continue. If they do, changes may be lost.

=======================
CW Compiler Environment
=======================

In addition to the main ChipWhisperer application and updater, an additional application is installed, :code:`CW Compiler Environment`.
This application launches a WSL instance with ChipWhisperer's compilers setup and available so that you can build
target firmware outside of Jupyter.

Note that Python and ChipWhisperer aren't available from this environment, or WSL in general. While it is simple to install
Python in WSL, USB devices aren't available in WSL. As such, the installer doesn't install Python or ChipWhisperer in WSL.

.. image:: _images/cw-compiler-env.png

*************
Common Issues
*************

=======================================================
Updater Fails Due to Dubious Ownership/Unsafe Directory
=======================================================

The most common cause of this error is not rebooting after installing your WSL distro,
as all files will be owned by root until this is done. The easiest way to fix this
is to simply reboot your computer, but you can also run the following command in
the chipwhisperer and jupyter folders via the CW Compiler Environment:

.. code:: bash

  git config --global --add safe.directory $(pwd)
  cd jupyter
  git config --global --add safe.directory $(pwd)

.. _releases: https://github.com/newaetech/chipwhisperer/releases

.. _forums: https://forum.newae.com/

.. _arm-none-eabi-gcc: https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads
.. _avr-gcc: https://blog.zakkemble.net/avr-gcc-builds/
.. _git-bash: https://git-scm.com/downloads
.. _WinPython: https://sourceforge.net/projects/winpython/files/
.. _nbstripout: https://github.com/kynan/nbstripout