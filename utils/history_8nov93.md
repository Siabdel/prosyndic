 2048  more  vi /etc/nginx/sites-available/prosyndic 
 2049  vi /etc/nginx/sites-available/prosyndic 
 2050  gunicorn --bind 0.0.0.0:8000  prosyndic.wsgi
 2051  sudo systemctl disable gunicorn.socket
 2052  sudo nano /etc/systemd/system/gunicorn.socket
 2053  sudo nano /etc/systemd/system/gunicorn.service
 2054  more  nano /etc/systemd/system/gunicorn.service
 2055  more   /etc/systemd/system/gunicorn.service
 2056  sudo nano /etc/systemd/system/gunicorn.service
 2057  sudo systemctl stop gunicorn.socket
 2058  gunicorn --bind 0.0.0.0:8000  prosyndic.wsgi
 2059  ll
 2060  sudo systemctl enable gunicorn.socket
 2061  sudo systemctl status gunicorn.socket
 2062  file /run/gunicorn.sock
 2063  sudo systemctl status gunicorn
 2064  sudo journalctl -u gunicorn.socket
 2065  sudo systemctl status gunicorn
 2066  sudo journalctl -u gunicorn
 2067  sudo systemctl daemon-reload
 2068  sudo systemctl restart gunicorn
 2069  sudo nano /etc/nginx/sites-available/prosyndic 
 2070  sudo mv  /etc/nginx/sites-available/prosyndic  /etc/nginx/sites-available/prosyndic.conf
 2071  sudo nano /etc/nginx/sites-available/prosyndic.conf 
 2072  sudo ln -s /etc/nginx/sites-available/prosyndic.conf /etc/nginx/sites-enabled
 2073  ll
 2074  ./manage.py check
 2075  pip install django-debug-toolbar
 2076  ./manage.py check
 2077  mkdir staticfiles static media
 2078  ./manage.py check
 2079  ./manage.py runserver
 2080  sudo nginx -t
 2081  sudo rm -r  /etc/nginx/sites-available/prosyndic
 2082  sudo rm -r  /etc/nginx/sites-enabled/prosyndic
 2083  sudo mv  /etc/nginx/sites-available/prosyndic.conf  /etc/nginx/sites-available/prosyndic
 2084  sudo ln -s /etc/nginx/sites-available/prosyndic /etc/nginx/sites-enabled
 2085  sudo nginx -t
 2086  sudo mv  /etc/nginx/sites-available/prosyndic.conf  /etc/nginx/sites-available/prosyndic
 2087  sudo mv  /etc/nginx/sites-available/prosyndic  /etc/nginx/sites-available/prosyndic.conf
 2088  sudo nginx -t
 2089  sudo nano /etc/nginx/sites-available/prosyndic.conf 
 2090  sudo nano /etc/systemd/system/gunicorn.service
 2091  sudo nginx -t
 2092  sudo systemctl daemon-reload
 2093  sudo systemctl restart gunicorn
 2094  sudo systemctl restart nginx
 2095  sudo journalctl -u gunicorn
 2096  sudo systemctl status nginx
 2097  cd ..
 2098  bin/gunicorn 
 2099  sudo systemctl daemon-reload
 2100  more   /etc/systemd/system/gunicorn.service
 2101  sudo journalctl -u gunicorn
 2102  sudo nano /etc/nginx/sites-available/prosyndic.conf 
 2103  curl --unix-socket /run/gunicorn.sock localhost
 2104  cd prosyndic/
 2105  gunicorn --bind 0.0.0.0:8000 myproject.wsgi
 2106  gunicorn --bind 0.0.0.0:8000 prosyndic.wsgi
 2107  history | tail
 2108  history | tail > history_8nov93.md
 2109  more history_8nov93.md 
 2110  history | tail -50
 2111  history | tail -100
 2112  history | tail -65 > history_8nov93.md 
sudo ufw allow 8000
sudo systemctl status nginx.service
sudo systemctl restart nginx
# testing Gunicorn

$ gunicorn --bind 0.0.0.0:8000 myproject.wsgi
sudo nano /etc/systemd/system/gunicorn.service

sudo journalctl -u gunicorn.socket
