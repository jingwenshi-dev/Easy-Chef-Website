#!/bin/bash
cd 'DjangoBackend' || exit
chmod +x run.sh
./run.sh &
cd ..

cd 'ReactFrontend'  || exit
chmod +x run.sh
./run.sh &
cd ..
