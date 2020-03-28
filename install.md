# Communication with Vitoligno 300-P
## Hardware
* raspberry pi3
* optolink module

## Installation

### Installation de Raspbian
1. Installation de raspbian sur la carte SD
2. Lancer le Raspberry, effectuer configurations d'usage
3. Activer ssh :
Préférences -> Configuration du Raspberry Pi -> Interfaces


### Ajouter clé pour ssh
1. sur remote, générer la clé
`ssh-keygen`
2. copier la clé publique sur le raspberry
`ssh-copy-id -i ~/.ssh/id_rsa pi@192.168.1.23`


### Installation et configuration de domoticz via ssh
1. utiliser ssh
`ssh pi@192.168.1.23`
2. Installation de domoticz
`sudo curl -L install.domoticz.com | bash`

### Sur l'interface de domoticz 192.168.1.23:8080
1. Ajouter un hardware "Dummy"
2. Ajouter des capteurs virtuels
3. Mettre à jour le fichier settings.py pour mettre à jour les idx des capteurs

### Régler cron
1. open crontab
`crontab -e`
2. edit update every 20 min.
`*/20 * * * * /home/pi/pyvito/vito-domoticz.py`



### synchronize time of the raspberrypi
1. Renseigner les serveurs
`sudo nano -c /etc/systemd/timesyncd.conf`
>Servers= ntp.unice.fr ntp.midway.ovh
2. Activation
`sudo timedatectl set-ntp true`
3. Check
`timedatectl`


## Tricks
* copying file between remote and host
`scp -r pyvito  pi@192.168.1.23:~/`
* supprimer des points sur une courbe domoticz : shift+left click


## usefull links 
* [http://openv.wikispaces.com/]
* [https://github.com/steand/optolink]
* [https://gist.github.com/mqu/9519e39ccc474f111ffb]

