#!/bin/bash
# bash "<scriptname>" in terminal to run the script
# DO NOT RUN AS SUDO!!!!!
# Make sure you have enabled third party repos, updated and installed nvidia before running
# Once run, restart computer.

echo "###################################################"
echo "ADDING NEEDED REPOSITORIES"
echo "###################################################"
# These repos give you access to a lot more things

flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
sudo dnf -yq install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf -yq install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

echo "###################################################"
echo "REMOVING SOME BUILT-IN APPS"
echo "###################################################"
# evince (pdf viewer), simple-scan (document scanner), totem (video player), rhythmbox (audio player), eog (photo viewer)

sudo dnf -yq erase gnome-tour evince simple-scan totem rhythmbox eog gnome-photos

echo "###################################################"
echo "REINSTALLING SYSTEM APPS USING FLATPAK"
echo "###################################################"
# gnome-boxes (virtual machine software), gnome-connections (remote desktop) baobab (disk usage analyzer)

sudo dnf -yq erase *libreoffice* gnome-boxes gnome-calculator gnome-characters gnome-calendar gnome-contacts gnome-clocks gnome-connections gnome-maps gnome-weather baobab

flatpak install flathub -y org.libreoffice.LibreOffice org.gnome.Boxes org.gnome.Calculator org.gnome.Characters org.gnome.Calendar org.gnome.Contacts org.gnome.clocks org.gnome.Connections org.gnome.Maps org.gnome.Weather org.gnome.baobab

# Some apps need obvious permissions (from my POV) added/removed
sudo flatpak override org.libreoffice.LibreOffice --unshare=network

echo "###################################################"
echo "INSTALLING CUSTOM DNF APPS"
echo "###################################################"
# dconf-editor (change all GNOME settings), gnome-tweaks (GUI for extra GNOME settings), ffmpeg (smooth video playback), xkill (click on program to terminate), gparted (disks manager), unar (extract module - works with all but rar - not perfeclty at least), unrar (for rar files), file-roller (browse archive files)

sudo dnf -yq install dconf-editor gnome-tweaks gnome-extensions-app ffmpeg mediainfo VirtualBox wireshark gparted unar unrar file-roller

sudo usermod -a -G wireshark $USER
sudo usermod -a -G vboxusers $USER

echo "###################################################"
echo "INSTALLING CUSTOM FLATPAK APPS"
echo "###################################################"
# bluerecorder (screen record), gwenview (photo viewer), zapzap (WhatsApp), Jdownloader (multi-purpose downloader), mkvtoolnix-gui (edit mkv files), ciano (media converter)

flatpak install flathub -y com.github.tchx84.Flatseal com.valvesoftware.Steam com.vscodium.codium org.videolan.VLC info.smplayer.SMPlayer org.shotcut.Shotcut sa.sy.bluerecorder org.gnome.SoundRecorder org.kde.gwenview org.gimp.GIMP com.skype.Client com.discordapp.Discord com.rtosta.zapzap org.qbittorrent.qBittorrent org.jdownloader.JDownloader org.bunkus.mkvtoolnix-gui org.gnome.Geary com.github.robertsanseries.ciano com.bitstower.Markets

sudo flatpak override com.vscodium.codium --nofilesystem=host --unshare=network
sudo flatpak override org.videolan.VLC --unshare=network
sudo flatpak override info.smplayer.SMPlayer --unshare=network
sudo flatpak override org.shotcut.Shotcut --unshare=network
sudo flatpak override org.gimp.GIMP --unshare=network
sudo flatpak override org.kde.gwenview --socket=session-bus
sudo flatpak override org.jdownloader.JDownloader --filesystem=host
sudo flatpak override com.github.robertsanseries.ciano --filesystem=host

echo "###################################################"
echo "REPLACING NAUTILUS FILE MANAGER WITH THUNAR"
echo "###################################################"

# Remove nautilus
sudo dnf -yq erase nautilus

# Install thunar (catfish - recursive search - seperate app - needs custom action - "catfish %f")
sudo dnf -yq install thunar catfish

# Make it default
xdg-mime default thunar.desktop inode/directory application/x-gnome-saved-search
sudo cp /usr/bin/thunar /usr/bin/nautilus # some GNOME apps may have the "nautilus" command hardcoded. With this, "nautilus" calls "thunar")

# Photo and video thumbs (tumbler - photo thumbs, the rest are for video thumbs)
sudo dnf -yq install tumbler gstreamer1-plugin-openh264 ffmpegthumbs ffmpegthumbnailer

# Icons in contect menus
# Lxappearance is an app that installs gtk2 dependencies needed for this. You can use this GUI instead of the gsettings command below. Go to the "Other" section and enable "Show image on buttons" and "Show images in menus".
# Note this doesnt work on Wayland NVIDIA as of wiritng it
sudo dnf -yq install lxappearance
gsettings set org.gnome.settings-daemon.plugins.xsettings overrides "{'Gtk/ButtonImages': <1>, 'Gtk/MenuImages': <1>}"

echo "###################################################"
echo "INSTALLING GNOME EXTENSIONS"
echo "###################################################"
# Logout or restart for them to show up and turn them on manually

if [ ! -d "$HOME/.local/share/gnome-shell/extensions" ]; then mkdir "$HOME/.local/share/gnome-shell/extensions"; fi

# ArcMenu
mkdir ~/arcmenu
cd ~/arcmenu
git clone https://gitlab.com/arcmenu/ArcMenu.git .
make install

# Dash to Panel
mkdir ~/dashtopanel
cd ~/dashtopanel
git clone https://github.com/home-sweet-gnome/dash-to-panel.git .
make install

# Tray Icons Reloaded
mkdir ~/trayicons
cd ~/trayicons
git clone https://github.com/MartinPL/Tray-Icons-Reloaded .
mkdir -p ~/.local/share/gnome-shell/extensions/trayIconsReloaded@selfmade.pl
cp -r * ~/.local/share/gnome-shell/extensions/trayIconsReloaded@selfmade.pl

# Sound input/output device chooser
mkdir ~/inputoutput
cd ~/inputoutput
git clone https://github.com/kgshank/gse-sound-output-device-chooser.git .
cp -r sound-output-device-chooser@kgshank.net ~/.local/share/gnome-shell/extensions/

# Color tint
mkdir ~/colortint
cd ~/colortint
wget "https://github.com/MattByName/color-tint/releases/download/v2.2.0/colortint@matt.serverus.co.uk.zip"
unzip "colortint@matt.serverus.co.uk.zip" -d "$HOME/.local/share/gnome-shell/extensions/colortint@matt.serverus.co.uk"

# Bluetooth quick connect
mkdir ~/btqc
cd ~/btqc
git clone https://github.com/bjarosze/gnome-bluetooth-quick-connect .
make install

# True color invert (Win/Super + I on any window to invert colors)
mkdir ~/colorinvert
cd ~/colorinvert
git clone https://github.com/jackkenney/gnome-true-color-invert .
mkdir -p ~/.local/share/gnome-shell/extensions/true-color-invert@jackkenney
cp -r * ~/.local/share/gnome-shell/extensions/true-color-invert@jackkenney

# Extensions List
mkdir ~/extlist
cd ~/extlist
git clone https://github.com/tuberry/extension-list.git .
make && make install

# Clipboard
mkdir ~/clipboard
cd ~/clipboard
git clone https://github.com/Tudmotu/gnome-shell-extension-clipboard-indicator.git .
mkdir -p ~/.local/share/gnome-shell/extensions/clipboard-indicator@tudmotu.com
cp -r * ~/.local/share/gnome-shell/extensions/clipboard-indicator@tudmotu.com

# Tiling assistant
mkdir ~/tilingassist
cd ~/tilingassist
git clone https://github.com/Leleat/Tiling-Assistant .
bash "scripts/build.sh" -i

# Arrange Windows
mkdir ~/arrangewindows
cd ~/arrangewindows
git clone https://github.com/sunwxg/gnome-shell-extension-arrangeWindows .
make install

# Remove downloadeded files
cd ~
sudo rm -r ~/arcmenu ~/dashtopanel ~/trayicons ~/inputoutput ~/colortint ~/btqc ~/colorinvert ~/extlist ~/clipboard ~/tilingassist ~/arrangewindows


echo "###################################################"
echo "OPERATION COMPLETED"
echo "###################################################"
