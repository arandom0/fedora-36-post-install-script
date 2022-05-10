# fedora-36-post-install-script

A collection of scripts and configs to make Fedora the way I want after install.
Note that this is something I wrote specifically for myself. You can remove certain parts / apps etc. If you remove Skype or Geary from the install script, you should probably also remove their config / autostart files from userdata/.config/autostart and userdata/.var/app.

INSTALLATION

Extract the userdata.zip file to a folder called "userdata".

Open a terminal in the main folder where this repository was downloaded (where the scripts are) and run:

bash "1 installations.sh"

Reboot youc computer after this one. Open terminal in the download folder again and run:

python3 "2 settngs.py"

The manual document, you can take look and do the things is talks about if you want.
