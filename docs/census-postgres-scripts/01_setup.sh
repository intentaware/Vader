sudo su -
apt-get update
apt-get -y install mdadm xfsprogs
umount /mnt
yes | mdadm --create /dev/md0 --level=0 -c256 --raid-devices=2 /dev/xvdb /dev/xvdc
echo 'DEVICE /dev/xvdb /dev/xvdc' > /etc/mdadm/mdadm.conf
mdadm --detail --scan >> /etc/mdadm/mdadm.conf
blockdev --setra 65536 /dev/md0
mkfs.xfs -f /dev/md0
mkdir -p /mnt && mount -t xfs -o noatime /dev/md0 /mnt
exit
cd /mnt
sudo su -
apt-get -y install postgresql postgresql-contrib
exit
echo "us-census.c3udwfzrnadp.us-west-2.rds.amazonaws.com:5432:us_census:census:RnEnrChWdJUq9g6VTvhPbHEt8mRzW9We" > /home/ubuntu/.pgpass
chmod 0600 /home/ubuntu/.pgpass
sudo mkdir -p /mnt/tmp
sudo chown ubuntu /mnt/tmp
sudo apt-get install -y aria2 git
cd /home/ubuntu
git clone https://github.com/censusreporter/census-postgres-scripts.git
git clone https://github.com/censusreporter/census-postgres.git
cd census-postgres-scripts
