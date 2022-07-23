sudo apt install python3 cython3 build-essentials
cython3 --embed -o spotify.c spotify.py
gcc -Os -I /usr/include/python3.10/ spotify.c -lpython3.10 -o spotify
