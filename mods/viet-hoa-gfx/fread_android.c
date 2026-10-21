/* fread for the translated Android game (v0.3.1-preview.1 and later), whose
 * C library lends fgets, fseek, fwrite and fclose to mods but not fread.
 * fgets with room for one byte reads exactly one byte, whatever its value
 * (a newline or a zero included), or returns NULL at the end of the file.
 * Only built for that game (MEMORIES_TRANSLATED); every other game keeps the
 * C library's own fread. Added by the Vietnamese mod bundle to build this mod
 * for that game; the mod's own sources are unchanged. */
#if defined(MEMORIES_TRANSLATED)
#include <stdio.h>

size_t fread(void *buffer, size_t size, size_t count, FILE *file)
{
    unsigned char *out = buffer;
    char one[2];
    size_t total, got = 0;
    if (!size || !count || count > (size_t)-1 / size) return 0;
    total = size * count;
    while (got < total && fgets(one, sizeof(one), file))
        out[got++] = (unsigned char)one[0];
    return got / size;
}
#endif
