mac:
	gcc -I/Library/Frameworks/SDL.framework/Headers -I/Library/Frameworks/SDL_mixer.framework chip8.c SDLmain.m -framework SDL -framework SDL_mixer -framework Cocoa -o chip8

linux:
	gcc chip8.c -o chip8 -lSDL -lSDL_mixer

ems:
	emcc -s WASM=1 chip8.c -o chip8.js --emrun -O3 --preload-file chip.bin --preload-file beep.wav --use-preload-plugins
