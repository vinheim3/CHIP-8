COMMON_FLAGS=-Wall
MAC_INCLUDES=-I/Library/Frameworks/SDL.framework/Headers -I/Library/Frameworks/SDL_mixer.framework
MAC_FRAMEWORKS=SDLmain.m -framework SDL -framework SDL_mixer -framework Cocoa
EMCC_FLAGS=--preload-file chip.bin --preload-file beep.wav --use-preload-plugins -s WASM=1

mac:
	gcc $(MAC_INCLUDES) chip8.c $(MAC_FRAMEWORKS) -o chip8 $(COMMON_FLAGS)

linux:
	gcc chip8.c -o chip8 -lSDL -lSDL_mixer $(COMMON_FLAGS)

ems:
	emcc chip8.c -o chip8.js -O3 $(EMCC_FLAGS) $(COMMON_FLAGS)
