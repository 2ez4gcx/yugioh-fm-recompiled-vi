/* Máy chơi nhanh: lượt của máy (bên do AI điều khiển) chạy ở tốc độ của mod, như tự giữ Tab.
 *
 * Máy "nghĩ" rất nhanh (AiScript_Run xong trong chưa tới một khung khi chạy native); phần chậm là các hoạt cảnh của
 * game gốc: bài bay ra bàn, camera chuyển lên nhìn từ trên, con trỏ của máy dừng trên lá rồi trượt từng ô tới mục
 * tiêu. Mỗi khung, nếu đang là lượt của bên AI và không phải cảnh đánh nhau (trừ khi bật "battle"), mod đặt đồng hồ
 * game (Platform_SetClockRate, như menu Game speed và phím Turbo) lên "speed"; hết lượt thì trả lại tốc độ cũ.
 * Không đụng tới đồng hồ khi game đang dừng (P), không giới hạn, hay đã nhanh hơn (người chơi giữ Tab); người chơi
 * đổi tốc độ giữa chừng thì mod lấy tốc độ mới làm tốc độ để trả lại. Nhạc giữ nhịp như khi giữ Tab. */
#include "types.h"
#include "pc/mods/modapi.h"
#include "pc/platform/platform.h"
#define D_8009B360_AS_SIDE_ARRAY
#include "game/duel_side_state.h"
#include "game/duel_scene_state.h"

extern unsigned char D_8009B26C, D_8009B26E;   /* chế độ chính (3: trận đấu), cảnh (0x81: trận đang chạy) */

#define PHASE_BATTLE 9      /* gDuel_wSceneStateFlags & 0xF: DuelScene_UpdateBattle */
#define PHASE_LAST 11       /* 12 trở đi: kết quả, phần thưởng, Exodia */

static const MemoriesModHost *host;
static int ours;     /* tốc độ mod đã đặt, 0 khi không đặt */
static int before;   /* tốc độ mod sẽ trả lại */

static int setting(const char *key, int fallback, int low, int high)
{
    int n = host->setting(host, key, fallback);
    return n < low ? low : n > high ? high : n;
}

/* Lượt của bên AI, trong một trận đang chạy, ở pha mod tăng tốc. */
static int ai_turn(void)
{
    int phase = gDuel_wSceneStateFlags & DUEL_SCENE_PHASE_MASK;
    if ((D_8009B26C & 31) != 3 || D_8009B26E != 0x81) return 0;
    if (D_8009B1D5 > 1 || D_8009B360[D_8009B1D5] < 0) return 0;   /* bên người chơi (cả Dual Play) */
    if (phase < 1 || phase > PHASE_LAST) return 0;
    return phase != PHASE_BATTLE || setting("battle", 0, 0, 1);
}

static void give_back(void)
{
    if (ours && Platform_ClockRate() == ours) {
        Platform_SetClockRate(before);
        if (host->log_enabled(host)) host->log(host, "AI turn over: clock back to %d%%", before);
    }
    ours = 0;
}

static void frame(void)
{
    int rate = Platform_ClockRate();
    if (!ai_turn()) {
        give_back();
        return;
    }
    if (ours && rate != ours) ours = 0;   /* người chơi dừng, giữ Tab hay đổi tốc độ: tính lại từ đầu */
    if (!ours) {
        int speed = setting("speed", 300, 100, 400);
        if (rate <= 0 || rate >= speed) return;   /* đang dừng, không giới hạn, hoặc đã nhanh hơn */
        before = rate;
        ours = speed;
        Platform_SetClockRate(speed);
        if (host->log_enabled(host))
            host->log(host, "AI turn: clock %d%% -> %d%% (phase %d)", rate, speed, gDuel_wSceneStateFlags & 0xF);
    }
}

static void applied(int on)
{
    if (!on) give_back();
}

static void reset(void)
{
    give_back();
}

int MemoriesModInit(const MemoriesModHost *h, MemoriesMod *mod)
{
    host = h;
    mod->api = MEMORIES_MOD_API;
    mod->frame = frame;
    mod->applied = applied;
    mod->reset = reset;
    mod->shutdown = give_back;
    return 1;
}
