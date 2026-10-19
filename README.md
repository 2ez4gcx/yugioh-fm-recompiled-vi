# Yu-Gi-Oh! Forbidden Memories Recompiled — Việt hoá (PC + Android)

Bộ mod tiếng Việt cho [Yu-Gi-Oh! Forbidden Memories Recompiled](https://github.com/Unchiga/Yu-Gi-Oh-Forbidden-Memories-Recompiled)
(bản PC/Android dựng từ mã nguồn giải mã của game PS1, port v0.3.0), và một APK Android gói sẵn mọi mod.
Bản dịch lấy từ bản Việt hoá đĩa [yugioh-fm-vi-patch](https://github.com/2ez4gcx/yugioh-fm-vi-patch).

**Không kèm dữ liệu game.** File game gốc do người chơi tự cung cấp (xem [File game gốc](#file-game-gốc-người-chơi-tự-cung-cấp)).

![Thoại tiếng Việt, 4x + chữ HD](docs/anh/recompiled_thoai_hd.png)

## File game gốc (người chơi tự cung cấp)

Repo và các file ở Releases **không chứa** file game: không có đĩa, không có EXE `SLUS_014.11`, không có hình, nhạc
hay thoại gốc của game. Game chạy từ chính file đĩa của bạn, đọc trực tiếp lúc chơi. Các mod ở đây chỉ chứa phần
dịch, phần vẽ lại và các bảng chỉnh sửa.

Bạn cần:

| | |
|---|---|
| Game | Yu-Gi-Oh! Forbidden Memories, bản **Mỹ (USA)**, mã **SLUS-01411** |
| Định dạng | file **`.bin`** dạng thô (một track, MODE2/2352), tên file đặt tùy ý. Không dùng `.iso`, `.chd`, `.cue` thay cho `.bin` (file `.cue` không cần) |
| Kích thước | 517.872.768 byte |
| SHA-256 đĩa chuẩn | `6e22494a45bf50fa2d239cd3819a57163a5f9b91e0365babc3e101509b5c3a7c` |

- Dùng **đĩa gốc chưa vá**: không dùng file đã áp bản vá Việt hoá đĩa (`yugioh-fm-vi.ppf`) hay bản vá khác, vì port
  đọc dữ liệu thẳng từ đĩa và bản dịch của port là mod riêng. Bản châu Âu (PAL) hay Nhật không chạy được.
- Lấy file từ **đĩa game của chính bạn** bằng phần mềm chép đĩa ra BIN/CUE (sector thô 2352 byte). Đừng hỏi hay
  chia sẻ link tải file game trong repo này.
- Kiểm tra file trên Windows: `certutil -hashfile "tên-file.bin" SHA256` (PowerShell: `Get-FileHash "tên-file.bin"`).
  Mã khác mã ở trên thường là file đã vá, bản khác vùng, hoặc file chép lỗi.

Đặt file ở đâu:

- **Android:** chép file `.bin` vào điện thoại (ví dụ thư mục Download). Lần đầu mở app, chọn **Choose disc image...**
  rồi chọn file. App tự chép vào bộ nhớ của nó (`Android/data/org.yfmredecomp.game/files/game/`), lần sau không
  cần chọn lại; có thể xoá bản ở Download sau khi app đã chép xong.
- **PC (bản chính thức):** lần đầu chạy `memories-pc.exe`, chọn file `.bin` trong hộp thoại.
- **PC (build từ mã nguồn):** đặt file `.bin` vào thư mục `game\` của mã nguồn rồi chạy `play.bat`.

## Tải về

Ở mục [Releases](../../releases):

| File | Dùng cho |
|---|---|
| `YFM-ReDecomp-v0.3.0-VietHoa-arm64.apk` | Android (arm64, Android 7.0 trở lên): APK gói sẵn mọi mod và gói HD, cài là chơi |
| `yfm-mods-viet-hoa-android.zip` | APK **chính thức** v0.3.0: nhập bằng Mods > Import mod... |
| `yfm-mods-viet-hoa-pc.zip` | Windows: bản chính thức v0.3.0 hoặc bản build từ mã nguồn |

Mã SHA-256 của từng file nằm trong `SHA256SUMS.txt` của release.

## Có gì

- **Tiếng Việt (chữ)**: toàn bộ cốt truyện, menu, thẻ nhớ, 722 mô tả lá bài, loại bài, thủ hộ tinh, tên người,
  địa danh. Tên lá bài giữ tiếng Anh.
- **Tiếng Việt (đồ hoạ)**: BẤM NÚT START và dòng ghi công, menu tiêu đề và menu trong game, banner ĐẤU TỰ DO,
  CHÚ Ý!, ô ĐỊA HÌNH và tên địa hình, màn kết quả, tiêu đề CÀI ĐẶT, nhãn MỚI!.
- **Đủ 722 lá**: 82 lá vốn không rơi được thêm vào bảng rơi S/A của đối thủ dùng lá đó, 122 lá giá 999999 sao
  được hạ giá theo cấp, 24 lá không có mật mã được thêm mật mã thật.
- **Rơi nhiều lá**: mỗi trận thắng 5 lá (đổi ở Mods > Rơi nhiều lá).
- **Monster Effects – tiếng Việt**: mô tả hiệu ứng tiếng Việt cho 63 lá của mod Monster Effects.

APK riêng gói thêm (của tác giả khác, xem Ghi công): Monster Effects, Adversários à Mesa (đối thủ ngồi sau bàn),
3D Duel Arena (sân vận động giải đấu), gói Forbidden Memories HD, và 3D Monsters đặt sẵn **đánh thẳng trên bàn**
(không vào cảnh hai lá bài lớn). Dual Play, AI Hard Mode và một bản Việt hoá khác (translation-vi) có sẵn nhưng tắt.

| | |
|---|---|
| ![Mô tả lá bài](docs/anh/recompiled_mo_ta_la_bai_hd.png) | ![Kết quả, rơi 5 lá](docs/anh/roi-5-la.png) |
| ![Đánh trên bàn](docs/anh/danh-tren-ban.png) | ![Sân vận động](docs/anh/san-van-dong.png) |

## Cài trên Android: APK riêng

1. Nếu máy đang có YFM Re-Decomp **bản chính thức**, gỡ nó trước (khác khoá ký). Gỡ app sẽ xoá save trong app:
   muốn giữ thì chép `Android/data/org.yfmredecomp.game/files/saves` ra chỗ khác trước, cài xong chép lại.
   Nếu đang có một bản APK riêng trước đó thì cài đè luôn, save được giữ.
2. Chép APK và file `.bin` (file game gốc của bạn, xem [File game gốc](#file-game-gốc-người-chơi-tự-cung-cấp)) sang điện thoại, cài APK.
3. Mở app (lần đầu hơi lâu vì giải nén gói HD), chọn **Choose disc image...** và chọn file `.bin`.
4. Tuỳ chọn: Video > Internal 4x và HD text cho hình đẹp; máy yếu thì 2x.

## Cài trên Android: APK chính thức

1. Cài `yfm-redecomp-v0.3.0-android-arm64.apk` từ [release chính thức](https://github.com/Unchiga/Yu-Gi-Oh-Forbidden-Memories-Recompiled/releases/tag/v0.3.0), chọn file `.bin`.
2. Mods > **HD pack...** (tải gói HD), rồi **Import mod...** chọn `yfm-mods-viet-hoa-android.zip`.
3. Bật: Tiếng Việt, Tiếng Việt: đồ hoạ, Đủ 722 lá, Rơi nhiều lá, Monster Effects, Monster Effects – tiếng Việt,
   Adversários à Mesa, 3D Duel Arena. Trong 3D Monsters: Monsters attack = On the field. Apply rồi mở lại app.

## Cài trên PC (Windows)

1. Tải và giải nén `yfm-redecomp-v0.3.0-windows.zip` từ [release chính thức](https://github.com/Unchiga/Yu-Gi-Oh-Forbidden-Memories-Recompiled/releases/tag/v0.3.0)
   (hoặc build từ mã nguồn), chạy `memories-pc.exe` và chọn file `.bin`.
2. Gói HD: giải nén `yfm-redecomp-hd-mod-v0.3.0.zip` của release chính thức vào thư mục game.
3. Giải nén `yfm-mods-viet-hoa-pc.zip` vào `Documents\My Games\YFM Re-Decomp` (để có `mods\viet-hoa`, ...).
4. Mở game, F10 > Game > Mods: bật các mod như bước 3 của Android, 3D Monsters > Monsters attack = On the field,
   Apply. Video > Resolution > Internal 4x và Video > HD text.

## Save cũ

Save thẻ nhớ từ giả lập (`.mcr`, `.mcd`, `.srm`, `.gme`, `.mcs`, `.psv`...) hay từ bản Việt hoá đĩa: chép vào thư mục
`saves` (PC: `Documents\My Games\YFM Re-Decomp\saves`; Android: `Android/data/org.yfmredecomp.game/files/saves`)
rồi chọn LOAD ở màn tiêu đề. Tên nhân vật có dấu tiếng Việt từ bản đĩa sẽ hiện sai chữ (bảng mã khác).
Save state (F5/F7, hay của giả lập) không chuyển được giữa máy và phiên bản: lưu trong game trước khi chuyển.

## Lưu ý

- APK chưa được thử trên điện thoại thật bởi người làm; bộ mod đã chạy đúng trên bản Windows build từ cùng mã
  v0.3.0 (chữ, đồ hoạ, đánh trên bàn, rơi 5 lá, sân vận động).
- Hai bản Việt hoá (Tiếng Việt và translation-vi) không bật cùng lúc được: port từ chối bộ mod xung đột.
- Font port rộng cố định 8 px (bản đĩa dùng VWF): vài chỗ được ngắt dòng lại hoặc rút gọn cho vừa ô, như
  "Thung Lũng Vua" (ô bản đồ 16 chữ) và menu chọn thủ hộ tinh.

## Làm lại APK

`android/make_apk.py` thêm các mod vào APK chính thức v0.3.0 (mod đi kèm ở `assets/build/files`, mã build mới
mỗi bộ mod để cài đè nhận mod mới), rồi `zipalign -P 16 -f 4` và `apksigner` (build-tools 35, JDK 17). Mod code
phải build bằng `tools/pc/build_mod.py` của port **v0.3.0** (API 12): bản API mới hơn bị game v0.3.0 từ chối.
Khoá ký, APK chính thức và công cụ không nằm trong repo.

## Ghi công và giấy phép

- Port Yu-Gi-Oh! Forbidden Memories Recompiled: Unchiga và cộng sự (phần port: MIT). Giải mã gốc:
  [memories-decomp](https://github.com/krystalgamer/memories-decomp). Yu-Gi-Oh! và Forbidden Memories thuộc Konami.
- Gói Forbidden Memories HD: Unchiga, X@nder.
- Monster Effects, Adversários à Mesa, 3D Duel Arena, Dual Play và bản AI Hard Mode 0.1.10: jonasfelix92
  (AI Hard Mode gốc: DecompRecomp).
- translation-vi 0.9: tác giả ghi trong mod.
- Bản Việt hoá (chữ, đồ hoạ, mô tả hiệu ứng), Đủ 722 lá, Rơi nhiều lá: Bản Việt hóa phi lợi nhuận bởi KhươngKid.

APK và các file zip chứa mod và gói HD của các tác giả trên. Trước khi chia sẻ công khai, hãy hỏi ý họ.
