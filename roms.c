#include <dirent.h>
#include <string.h>
#ifdef __EMSCRIPTEN__
#include <emscripten.h>
#else
#define EMSCRIPTEN_KEEPALIVE ;
#endif

static DIR *roms;
static struct dirent *ent;
static char *romNames[0xFF];
static int romCnt = 0;
static int romsLoaded = 0;

void loadRoms() {
    if ( (roms = opendir("roms/")) != NULL ) {
        while ( (ent = readdir(roms)) != NULL ) {
            int is_dots = (strcmp(".", ent->d_name) == 0) | (strcmp("..", ent->d_name) == 0);
            if (!is_dots) {
                char *result = malloc(strlen("roms/") + strlen(ent->d_name) + 1);
                strcpy(result, "roms/");
                strcat(result, ent->d_name);
                romNames[romCnt] = result;
                romCnt++;
            }
        }
        closedir(roms);
    }
    romsLoaded = 1;
}

char **getRomNames() {
    if (!romsLoaded) loadRoms();
    return romNames;
}

EMSCRIPTEN_KEEPALIVE
char *getRomName(int index) {
    if (!romsLoaded) loadRoms();

    if (index < romCnt)
        return romNames[index];
    return "";
}

int getRomCnt() {
    if (!romsLoaded) loadRoms();
    return romCnt;
}