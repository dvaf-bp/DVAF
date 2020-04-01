#!/bin/bash

ssh-add /tmp/secrets/secrets/predserver_rsa
rsync -aqr -v "$TRAVIS_BUILD_DIR"/* dvaf_backend@predserver.tk.informatik.tu-darmstadt.de:/opt/dvaf_backend --exclude=/venv
ssh dvaf_backend@predserver.tk.informatik.tu-darmstadt.de sudo /bin/systemctl restart dvaf_backend.service
