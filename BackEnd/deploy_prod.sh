#!/bin/bash

ssh-add /tmp/secrets/secrets/mstar_rsa
rsync -aqr -v "$TRAVIS_BUILD_DIR"/* dvaf_backend@mstar.tk.informatik.tu-darmstadt.de:/opt/dvaf_backend --exclude=/venv
ssh dvaf_backend@mstar.tk.informatik.tu-darmstadt.de sudo /bin/systemctl restart dvaf_backend.service