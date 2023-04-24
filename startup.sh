#!/bin/bash
cd 'DjangoBackend' || exit
chmod +x startup.sh
./startup.sh &
cd ..

cd 'ReactFrontend'  || exit
chmod +x startup.sh
./startup.sh &
cd ..