mac:
	gcc -I/Library/Frameworks/SDL.framework/Headers chip8.c SDLmain.m -framework SDL -framework Cocoa -o chip8

linux:
	gcc chip8.c -o chip8 -lSDL

ems:
	emcc -s WASM=1 chip8.c -o chip8.js --emrun -O3 --preload-file chip.bin
