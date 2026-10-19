/* Rơi nhiều lá: mỗi trận thắng cho N lá (Game > Card drops của port), đặt sẵn khi game khởi động.
 *
 * Bản v0.3.0 của port (APK Android chính thức) có thanh Game > Card drops nhưng chưa có khoá
 * "limits": {"card_drops": N} cho mod (API 13); trên điện thoại thanh trượt dễ bị bỏ sót, và
 * mỗi lần cài lại app thì về 1. Mod này đặt giá trị đó (Settings_Set, như menu) bằng tuỳ chọn
 * "drops" của nó lúc nạp, nên APK riêng mặc định rơi 5 lá. Đổi số lá: Mods > Rơi nhiều lá. */
#include "types.h"
#include "pc/mods/modapi.h"
#include "pc/platform/settings.h"

#define DROPS_DEFAULT 5
#define DROPS_MAX 99   /* Game > Card drops: 1 đến 99 */

int MemoriesModInit(const MemoriesModHost *host, MemoriesMod *mod)
{
    int drops = host->setting(host, "drops", DROPS_DEFAULT);
    if (drops < 1) drops = 1;
    if (drops > DROPS_MAX) drops = DROPS_MAX;
    if (Settings_Get(SET_CARD_DROPS) != drops) {
        Settings_Set(SET_CARD_DROPS, drops);
        host->log(host, "card drops set to %d", drops);
    }
    mod->api = MEMORIES_MOD_API;
    return 1;
}
