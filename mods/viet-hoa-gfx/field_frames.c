/* viet-hoa-gfx: khung ô ĐỊA HÌNH trong trận đấu (extra_gfx.field_names) cho bản PC Recompiled.
 *
 * Bản đĩa xếp lại tên 6 địa hình vào dải texture u 64..127, v 80..127 của trang WA_MRG 0xB50000
 * và sửa các mảnh sprite (x, y, uv, kích thước) của khung trong SLUS (RAM 0x801AD8A0..0x801AD9A7).
 * Port nạp SLUS thẳng từ đĩa (game_files.c, GameFiles_ReadExecutable), nên mục "data" của mod.json
 * không tới được; mod này ghi đúng các byte đó vào RAM của game (tail_data_start = 0x801AC000)
 * khi mod bật và trả lại byte gốc khi tắt. Texture thì do mục "data" (WA_MRG) và gói texture lo.
 *
 * Byte gốc và byte mới do tools/recompiled_gfx.py sinh từ đĩa của người chơi vào
 * field_frames.bin: "VHF1", u16 số đoạn, rồi mỗi đoạn u32 địa chỉ RAM, u16 độ dài, byte gốc,
 * byte mới. Chỉ ghi khi RAM đang đúng byte gốc (hoặc đúng byte mới khi trả lại), nên một bản
 * game khác hay một mod khác đã sửa chỗ đó thì không bị ghi đè. */
#include "pc/mods/modapi.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

extern char tail_data_start[];   /* RAM 0x801AC000: phần dữ liệu cuối của SLUS */

#define TAIL_START 0x801AC000u
#define TAIL_END 0x801D0800u
#define TABLE_MAX 1024

static const MemoriesModHost *host;
static unsigned char table[TABLE_MAX];
static int runs;

static unsigned read16(const unsigned char *p) { return p[0] | p[1] << 8; }
static uint32_t read32(const unsigned char *p) { return read16(p) | (uint32_t)read16(p + 2) << 16; }

/* Đọc và kiểm field_frames.bin; 0 nếu thiếu hoặc sai. */
static int load(void)
{
    FILE *file = host->open_asset(host, "field_frames.bin");
    size_t size, at = 6;
    int i;
    if (!file) return 0;
    size = fread(table, 1, sizeof(table), file);
    fclose(file);
    if (size < 6 || memcmp(table, "VHF1", 4) != 0) return 0;
    runs = (int)read16(table + 4);
    for (i = 0; i < runs; i++) {
        uint32_t address;
        unsigned length;
        if (at + 6 > size) return 0;
        address = read32(table + at);
        length = read16(table + at + 4);
        if (address < TAIL_START || address + length > TAIL_END || at + 6 + 2 * length > size) return 0;
        at += 6 + 2 * length;
    }
    return 1;
}

/* on = 1: byte gốc -> byte mới; on = 0: ngược lại. */
static void put(int on)
{
    size_t at = 6;
    int i;
    for (i = 0; i < runs; i++) {
        uint32_t address = read32(table + at);
        unsigned length = read16(table + at + 4);
        const unsigned char *old = table + at + 6, *now = old + length;
        unsigned char *ram = (unsigned char *)tail_data_start + (address - TAIL_START);
        const unsigned char *from = on ? old : now, *to = on ? now : old;
        if (memcmp(ram, from, length) == 0) memcpy(ram, to, length);
        at += 6 + 2 * length;
    }
}

/* Mỗi khung hình: rẻ (28 byte), và đúng lại ngay sau khi nạp save state. */
static void frame(void) { put(1); }
static void applied(int on) { put(on); }
static void reset(void) { put(1); }

int MemoriesModInit(const MemoriesModHost *from, MemoriesMod *mod)
{
    host = from;
    mod->api = MEMORIES_MOD_API;
    if (!load()) {
        host->log(host, "viet-hoa-gfx: field_frames.bin is missing or damaged; the FIELD box stays as it is");
        return 0;
    }
    mod->frame = frame;
    mod->applied = applied;
    mod->reset = reset;
    put(1);
    return 1;
}
