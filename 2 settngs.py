# python3 "<scriptname>" in terminal to run the script
# DO NOT RUN AS SUDO!!!!!

import os

HOME_DIR = os.getenv("HOME")
DCONF_DUMP_SETTINGS = ""

print("\n###################################################")
print("COPYING USERDATA FOLDER")
print("###################################################")

userdataDir = ""
while 1==1:
    userInput = input("Downloaded \"userdata\" folder directory (ex. \"/home/john/post-install/userdata\"):\n").strip()
    if userInput.endswith("/"): userInput = userInput[:-1]
    if os.path.exists(userInput): userdataDir = userInput; break
    else: print("*** Invalid input. Try again.\n")
    
os.system(f"cp --recursive --force \"{userdataDir}\"* \"{HOME_DIR}\" > /dev/null 2>&1")

print("\n###################################################")
print("APPLYING GNOME SETTINGS")
print("###################################################")
# These are things that you can typically accomplish manually by altering settings and dconf-editor, gnome-tweaks and what not

###################################################################
# PRIVACY

# disable location services
os.system("gsettings set org.gnome.system.location enabled false")

# disable recent files
os.system("gsettings set org.gnome.desktop.privacy remember-recent-files false")
os.system(f"rm {HOME_DIR}/.local/share/recently-used.xbel > /dev/null 2>&1")

# disable searching for anything but your installed applications
os.system("gsettings set org.gnome.desktop.search-providers disable-external true")

###################################################################
# KEYBOARD

# replace "switch applications" with "switch windows" (the way Alt+Tab is supposed to work)
os.system("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"[]\"")
os.system("gsettings set org.gnome.desktop.wm.keybindings switch-windows \"['<Alt>Tab']\"")

# Super+Tab to show the overview (instead of Super+S)
os.system("gsettings set org.gnome.shell.keybindings toggle-overview \"['<Super>Tab']\"")

###################################################################
# WORKSPACES

# workspaces to apply to all monitors (else if you have an app on your second monitor it will remain when you switch)
os.system("gsettings set org.gnome.mutter workspaces-only-on-primary false")

# Static workspaces (like in Windows). Dynamic can be problematic (automatically closes ones on left when empty)
os.system("gsettings set org.gnome.mutter dynamic-workspaces false")

# Set workspaces to 3 instead of 4 (personally I don't ever need more than 3)
os.system("gsettings set org.gnome.desktop.wm.preferences num-workspaces 3")

###################################################################
# UI STUFF

# disable animations
os.system("gsettings set org.gnome.desktop.interface enable-animations false")

# disable hot corner
os.system("gsettings set org.gnome.desktop.interface enable-hot-corners false")

# minimize, maximize buttons in windows
os.system("gsettings set org.gnome.desktop.wm.preferences button-layout \"appmenu:minimize,maximize,close\"")

# Dark theme (new gnome thing in Settngs>Appearance + legacy gtk theme)
os.system("gsettings set org.gnome.desktop.interface color-scheme \"prefer-dark\"")
os.system("gsettings set org.gnome.desktop.interface gtk-theme \"Adwaita-dark\"")

# universal access always show icon (on screen keyboard, large text etc.)
os.system("gsettings set org.gnome.desktop.a11y always-show-universal-access-status true")

# Large text (lower than regular - 1.10)
os.system("gsettings set org.gnome.desktop.interface text-scaling-factor 1.10")

# Make night light manual (0:00-0:00), set temperature (lower = more orange), enable it
os.system("gsettings set org.gnome.settings-daemon.plugins.color night-light-schedule-from 0")
os.system("gsettings set org.gnome.settings-daemon.plugins.color night-light-schedule-to 0")
os.system("gsettings set org.gnome.settings-daemon.plugins.color night-light-schedule-automatic false")
os.system("gsettings set org.gnome.settings-daemon.plugins.color night-light-temperature 2700")
os.system("gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled true")

# Favorite applications
os.system("gsettings set org.gnome.shell favorite-apps \"['firefox.desktop', 'thunar.desktop']\"")

print("\n###################################################")
print("APPLYING EXTENSION SETTINGS")
print("###################################################")
# settings are saved to a file using "dconf dump /dconf/path/to/extension > out.txt".
# New line is replaced with \n and double quotes are escaped (\"). The result is then copied into the variables below

def apply_dconf_dump_settings(localFolderName, gsettingsDir):
    schemasDir = f"{HOME_DIR}/.local/share/gnome-shell/extensions/{localFolderName}/schemas/"
    for keyValuePair in DCONF_DUMP_SETTINGS.split("\n"):
        keyValuePair = keyValuePair.strip()
        if keyValuePair == "[/]" or keyValuePair == "": continue
        # replace first occurance of "=" with "space"
        # values that have space and no qutes need to be quoted (ones that start with {,[)
        keyValuePairSplit = keyValuePair.split("=")
        key = keyValuePairSplit[0].strip()
        value = "=".join(keyValuePairSplit[1:]).strip()
        if value.startswith("{") or value.startswith("["): value = f"\"{value}\""
        keyValuePair = f"{key} {value}"
        os.system(f"gsettings --schemadir {schemasDir} set {gsettingsDir} {keyValuePair} > /dev/null 2>&1")

print("APPLYING TRAY ICONS RELOADED SETTINGS")
DCONF_DUMP_SETTINGS="icon-size=24\nicons-limit=1";
apply_dconf_dump_settings("trayIconsReloaded@selfmade.pl", "org.gnome.shell.extensions.trayIconsReloaded")

print("APPLYING ARC MENU SETTINGS")
DCONF_DUMP_SETTINGS="apps-show-extra-details=false\narc-menu-icon=18\narc-menu-placement='DTP'\navailable-placement=[false, true, false]\nborder-color='rgb(255,120,0)'\nbutton-item-icon-size='Default'\nbutton-padding=-1\ncategory-icon-type='Full_Color'\ncustom-menu-button-icon=''\ncustom-menu-button-icon-size=28.0\ndistro-icon=16\nenable-custom-arc-menu=true\nforce-menu-location='Off'\nhighlight-color='rgb(64,27,27)'\nhighlight-foreground-color='rgba(255,255,255,1)'\nmenu-arrow-size=12\nmenu-border-size=3\nmenu-button-appearance='Icon'\nmenu-button-icon='Distro_Icon'\nmenu-button-position-offset=0\nmenu-color='rgb(0,0,0)'\nmenu-corner-radius=5\nmenu-font-size=9\nmenu-foreground-color='rgb(223,223,223)'\nmenu-height=814\nmenu-hotkey='Super_L'\nmenu-item-grid-icon-size='Default'\nmenu-item-icon-size='Default'\nmenu-layout='AZ'\nmenu-margin=24\nmenu-width=290\nmenu-width-adjustment=100\nmisc-item-icon-size='Default'\nmulti-monitor=true\npinned-app-list=['Settings', '', 'org.gnome.Settings.desktop', 'Terminal', '', 'org.gnome.Terminal.desktop', 'System Monitor', '', 'gnome-system-monitor.desktop', 'Extensions', '', 'org.gnome.Extensions.desktop', 'Disk Usage Analyzer', '', 'org.gnome.baobab.desktop', 'Cleaner', '', 'cleaner.desktop', 'Light/Dark Mode Switcher', '', 'gnome-light-dark-mode-switcher.desktop', 'Software', '', 'org.gnome.Software.desktop', 'Calculator', '', 'org.gnome.Calculator.desktop', 'Calendar', '', 'org.gnome.Calendar.desktop', 'Geary', '', 'org.gnome.Geary.desktop', 'Oracle VM VirtualBox', '', 'virtualbox.desktop', 'Sound Recorder', '', 'org.gnome.SoundRecorder.desktop', 'Cheese', '', 'org.gnome.Cheese.desktop', 'Blue Recorder', '', 'sa.sy.bluerecorder.desktop', 'GNU Image Manipulation Program', '', 'org.gimp.GIMP.desktop', 'Ciano', '', 'com.github.robertsanseries.ciano.desktop', 'Shotcut', '', 'org.shotcut.Shotcut.desktop', 'Xtreme Download Manager', '', 'xdman.desktop', 'JDownloader', '', 'org.jdownloader.JDownloader.desktop', 'qBittorrent', '', 'org.qbittorrent.qBittorrent.desktop', 'Steam', '', 'com.valvesoftware.Steam.desktop', 'ZapZap', '', 'com.rtosta.zapzap.desktop', 'Discord', '', 'com.discordapp.Discord.desktop', 'Skype', '', 'com.skype.Client.desktop', 'LibreOffice Writer', '', 'org.libreoffice.LibreOffice.writer.desktop', 'VSCodium', '', 'com.vscodium.codium.desktop', 'Text Editor', '', 'org.gnome.TextEditor.desktop', 'Thunar File Manager', '', 'thunar.desktop', 'Firefox', '', 'firefox.desktop']\nprefs-visible-page=0\nquicklinks-item-icon-size='Default'\nrecently-installed-apps=['org.gnome.gedit.desktop', 'gimp.desktop', 'io.elementary.switchboard.desktop', 'org.openrgb.OpenRGB.desktop', 'org.flameshot.Flameshot.desktop', 'org.cubocore.CoreShot.desktop', 'midnight-commander.desktop', 'mpv.desktop', 'info.smplayer.SMPlayer.desktop']\nright-panel-width=205\nseparator-color='rgb(255,120,0)'\nshortcut-icon-type='Symbolic'\nvert-separator=false"
apply_dconf_dump_settings("arcmenu@arcmenu.com", "org.gnome.shell.extensions.arcmenu")

print("APPLYING DASH TO PANEL SETTINGS")
DCONF_DUMP_SETTINGS="animate-app-switch=false\nanimate-appicon-hover=false\nanimate-appicon-hover-animation-extent={'RIPPLE': 4, 'PLANK': 4, 'SIMPLE': 1}\nanimate-appicon-hover-animation-type='RIPPLE'\nanimate-window-launch=false\nappicon-margin=4\nappicon-padding=4\navailable-monitors=[1, 0]\nclick-action='TOGGLE-SHOWPREVIEW'\ndot-color-dominant=true\ndot-color-override=false\ndot-position='BOTTOM'\ndot-style-focused='SEGMENTED'\ndot-style-unfocused='SEGMENTED'\nenter-peek-mode-timeout=50\nhide-overview-on-startup=true\nhotkeys-overlay-combo='TEMPORARILY'\nisolate-monitors=true\nisolate-workspaces=true\nleave-timeout=0\nleftbox-padding=-1\nmiddle-click-action='LAUNCH'\npanel-anchors='{\"0\":\"MIDDLE\",\"1\":\"MIDDLE\"}'\npanel-element-positions='{\"0\":[{\"element\":\"showAppsButton\",\"visible\":false,\"position\":\"stackedTL\"},{\"element\":\"leftBox\",\"visible\":true,\"position\":\"stackedTL\"},{\"element\":\"activitiesButton\",\"visible\":true,\"position\":\"stackedTL\"},{\"element\":\"taskbar\",\"visible\":true,\"position\":\"stackedTL\"},{\"element\":\"centerBox\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"rightBox\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"dateMenu\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"systemMenu\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"desktopButton\",\"visible\":true,\"position\":\"stackedBR\"}],\"1\":[{\"element\":\"showAppsButton\",\"visible\":false,\"position\":\"stackedTL\"},{\"element\":\"leftBox\",\"visible\":true,\"position\":\"stackedTL\"},{\"element\":\"activitiesButton\",\"visible\":true,\"position\":\"stackedTL\"},{\"element\":\"taskbar\",\"visible\":true,\"position\":\"stackedTL\"},{\"element\":\"centerBox\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"rightBox\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"dateMenu\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"systemMenu\",\"visible\":true,\"position\":\"stackedBR\"},{\"element\":\"desktopButton\",\"visible\":true,\"position\":\"stackedBR\"}]}'\npanel-lengths='{\"0\":100,\"1\":100}'\npanel-positions='{\"0\":\"RIGHT\",\"1\":\"RIGHT\"}'\npanel-sizes='{\"0\":40,\"1\":40}'\npeek-mode=false\npeek-mode-opacity=40\npreview-custom-opacity=80\npreview-middle-click-close=true\npreview-use-custom-opacity=true\nprimary-monitor=1\nshift-click-action='MINIMIZE'\nshift-middle-click-action='LAUNCH'\nshow-tooltip=false\nshow-window-previews=false\nshow-window-previews-timeout=0\nstatus-icon-padding=4\ntrans-bg-color='#310000'\ntrans-gradient-bottom-color='#1a5fb4'\ntrans-gradient-bottom-opacity=0.10000000000000014\ntrans-gradient-top-color='#ed333b'\ntrans-gradient-top-opacity=0.0\ntrans-panel-opacity=0.75\ntrans-use-custom-bg=false\ntrans-use-custom-gradient=false\ntrans-use-custom-opacity=false\ntrans-use-dynamic-opacity=false\ntray-padding=2\nwindow-preview-animation-time=0\nwindow-preview-aspect-ratio-x=16\nwindow-preview-aspect-ratio-y=9\nwindow-preview-custom-icon-size=16\nwindow-preview-fixed-x=false\nwindow-preview-fixed-y=true\nwindow-preview-hide-immediate-click=true\nwindow-preview-padding=8\nwindow-preview-show-title=true\nwindow-preview-size=400\nwindow-preview-title-font-color='#dddddd'\nwindow-preview-title-font-size=14\nwindow-preview-title-font-weight='inherit'\nwindow-preview-title-position='TOP'\nwindow-preview-use-custom-icon-size=false"
apply_dconf_dump_settings("dash-to-panel@jderose9.github.com", "org.gnome.shell.extensions.dash-to-panel")


print("\n###################################################")
print("ENABILING EXTENSIONS")
print("###################################################")

# gnome-extensions list
# gnome-extensions enable
# gnome-extensions disable

os.system("gnome-extensions enable sound-output-device-chooser@kgshank.net")
os.system("gnome-extensions enable trayIconsReloaded@selfmade.pl")
os.system("gnome-extensions enable arcmenu@arcmenu.com")
os.system("gnome-extensions enable true-color-invert@jackkenney")
os.system("gnome-extensions enable dash-to-panel@jderose9.github.com")
# os.system("gnome-extensions enable extension-list@tu.berry")
# os.system("gnome-extensions enable colortint@matt.serverus.co.uk")
os.system("gnome-extensions enable clipboard-indicator@tudmotu.com")
os.system("gnome-extensions enable bluetooth-quick-connect@bjarosze.gmail.com")
os.system("gnome-extensions enable tiling-assistant@leleat-on-github")
os.system("gnome-extensions enable arrangeWindows@sun.wxg@gmail.com")
