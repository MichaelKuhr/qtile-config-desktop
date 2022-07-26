#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

#Set your native resolution IF it does not exist in xrandr
#More info in the script
#run $HOME/.config/qtile/scripts/set-screen-resolution-in-virtualbox.sh

#Find out your monitor name with xrandr or arandr (save and you get this line)
#xrandr --output VGA-1 --primary --mode 1360x768 --pos 0x0 --rotate normal
#xrandr --output DP2 --primary --mode 1920x1080 --rate 60.00 --output LVDS1 --off &
#xrandr --output DP-2 --mode 3840x2160 --rate 60.00 --primary --output DP-4 --mode 3840x2160 --pos 2880x0 --rate 60.00 &
xrandr --output DP-2 --mode 2560x1440
xrandr --output DP-4 --mode 2560x1440
xrandr --output DP-2 --pos 0x0
xrandr --output DP-4 --pos -2560x0
#xrandr --output LVDS1 --mode 1366x768 --output DP3 --mode 1920x1080 --right-of LVDS1
#xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
#autorandr horizontal
xrandr -o inverted &
#sleep 1s &
#change your keyboard if you need it
#setxkbmap -layout be

keybLayout=$(setxkbmap -v | awk -F "+" '/symbols/ {print $2}')

if [ $keybLayout = "be" ]; then
  cp $HOME/.config/qtile/config-azerty.py $HOME/.config/qtile/config.py
fi

#autostart ArcoLinux Welcome App
#run dex $HOME/.config/autostart/arcolinux-welcome-app.desktop &

#Some ways to set your wallpaper besides variety or nitrogen
#feh --bg-fill /usr/share/backgrounds/arcolinux/arco-wallpaper.jpg &
#start the conky to learn the shortcuts
#(conky -c $HOME/.config/qtile/scripts/system-overview) &

#start sxhkd to replace Qtile native key-bindings
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &


#starting utility applications at boot time
run variety &
run nm-applet &
run pamac-tray &
run nitrogen --restore &
#run wireplumber &
#run xfce4-power-manager &
#run flatpak run com.github.debauchee.barrier &
run gammy start &
numlockx on &
#blueberry-tray &
picom --config $HOME/.config/qtile/scripts/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &

#starting user applications at boot time
run volumeicon &
#run flatpak run --command=barrierc com.github.debauchee.barrier --enable-drag-drop &
run firefox-developer-edition &
#run github &
run obsidian &
#run flatpak run org.ferdium.Ferdium &
run whatsapp-nativefier &
run telegram-desktop &
#run flatpak run org.onlyoffice.desktopeditors &
run devdocs-desktop &
#run firefox & 
run superproductivity &
run code &
run morgen &
run github-desktop &