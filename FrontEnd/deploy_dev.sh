#!/bin/bash

ssh-add /tmp/secrets/secrets/predserver_rsa
rsync -aqr -v --delete --prune-empty-dirs --exclude=".*" ./build/ dvaf_frontend@predserver.tk.informatik.tu-darmstadt.de:/var/www/dvaf_frontend
