ssh-add /tmp/secrets/secrets/mstar_rsa
rsync -aqr -v --delete --prune-empty-dirs --exclude=".*" ./build/ dvaf_frontend@mstar.tk.informatik.tu-darmstadt.de:/var/www/dvaf_frontend
