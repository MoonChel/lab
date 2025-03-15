## setup

sudo chown $(whoami) /etc/rancher/k3s/k3s.yaml

## install deb package

wget package_url
sudo apt install ./package.deb
rm package

## cleanup

keep configs
sudo apt-get remove nginx nginx-common

remove config also
sudo apt-get purge nginx nginx-common

remove deps
sudo apt-get autoremove
