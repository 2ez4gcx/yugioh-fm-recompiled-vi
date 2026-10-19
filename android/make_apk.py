"""APK riêng: APK chính thức YFM Re-Decomp v0.3.0 + các mod của người chơi + gói HD, làm mod đi kèm.

App Android giải nén những file liệt kê trong assets/build/files.txt (đặt ở assets/build/files/)
thành mod đi kèm ở lần chạy đầu (src/pc/platform/android.c, unpack_files); mod đi kèm có
"enabled": true thì bật sẵn. Script này:
  * chép mọi mục của APK gốc, trừ chữ ký cũ (META-INF) và mod ai-hard-mode gốc (thay bằng bản
    0.1.10 hợp với Monster Effects), cùng kiểu nén như cũ;
  * thêm các mod trong MODS (chỉ đối tượng .aarch64.o của mod code; viet-hoa-gfx lấy bản build
    theo SDK v0.3.0, API 12, vì bản API 16 bị game v0.3.0 từ chối);
  * 3d-monsters: "Monsters attack" mặc định "On the field" (2);
  * ghi files.txt mới. zipalign và apksigner làm ở bước sau (build-tools 35).

    python make_apk.py
"""
import hashlib, json, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_APK = os.path.join(HERE, "dl", "apk", "yfm-redecomp-v0.3.0-android-arm64.apk")
USER_MODS = os.path.join(os.path.expanduser("~"), "Documents", "My Games", "YFM Re-Decomp", "mods")
GFX_V030 = os.path.join(HERE, "gfx-v030", "viet-hoa-gfx")
OUT = os.path.join(HERE, "build", "unsigned.apk")
MODS = {   # thư mục trong APK -> nguồn
    "viet-hoa": os.path.join(USER_MODS, "viet-hoa"),
    "viet-hoa-gfx": os.path.join(USER_MODS, "viet-hoa-gfx"),
    "du-722-la": os.path.join(USER_MODS, "du-722-la"),
    "monster-effects": os.path.join(USER_MODS, "monster-effects"),
    "monster-effects-vi": os.path.join(USER_MODS, "monster-effects-vi"),
    "simon-at-table": os.path.join(USER_MODS, "simon-at-table"),
    "dual-play": os.path.join(USER_MODS, "dual-play"),
    "ai-hard-mode": os.path.join(USER_MODS, "ai-hard-mode"),
    "assets-hd": os.path.join(USER_MODS, "assets-hd"),
    "3d-duel-arena": os.path.join(USER_MODS, "3d-duel-arena"),     # jonasfelix92 0.6.2, API 12
    "translation-vi": os.path.join(USER_MODS, "translation-vi"),   # bản dịch khác, tắt sẵn; xung đột với viet-hoa
    "roi-nhieu-la": os.path.join(HERE, "roi-nhieu-la"),            # rơi 5 lá: build theo SDK v0.3.0
}
STORED = (".png", ".jpg", ".ogg", ".zip")   # đã nén sẵn


def wanted(name):
    """Bỏ đối tượng của nền khác: Android nạp <library>.aarch64.o."""
    if name.endswith(".o") and not name.endswith(".aarch64.o"):
        return False
    return not name.endswith((".pdb", ".undefined"))


def main():
    source = zipfile.ZipFile(SOURCE_APK)
    shipped = source.read("assets/build/files.txt").decode().splitlines()
    replaced = {"mods/" + m + "/" for m in MODS}
    keep_list = [line for line in shipped if line and not any(line.startswith(p) for p in replaced)]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    added = []
    # App chỉ giải nén lại mod đi kèm khi assets/build/buildid khác bản đã giải nén (android.c,
    # unpack_program): mỗi bộ mod một mã mới, để cài đè bản cũ cũng nhận mod mới. Mã là
    # buildid của bản gốc trộn với nội dung mod; bảng ký hiệu (symbols/<id>.txt, cho save state)
    # được chép thêm dưới tên mới.
    digest = hashlib.sha256(source.read("assets/build/buildid"))
    for folder, source_dir in sorted(MODS.items()):
        for root, _dirs, files in sorted(os.walk(source_dir)):
            for file in sorted(files):
                relative = os.path.relpath(os.path.join(root, file), source_dir).replace("\\", "/")
                if wanted(relative):
                    digest.update(f"{folder}/{relative}".encode())
                    with open(os.path.join(root, file), "rb") as handle:
                        digest.update(handle.read())
    old_id = source.read("assets/build/buildid").decode().strip()
    new_id = digest.hexdigest()[:8]
    with zipfile.ZipFile(OUT, "w") as out:
        for info in source.infolist():
            name = info.filename
            if name.startswith("META-INF/") or name in ("assets/build/files.txt", "assets/build/buildid"):
                continue
            if name == f"assets/build/symbols/{old_id}.txt":
                renamed = zipfile.ZipInfo(f"assets/build/symbols/{new_id}.txt", date_time=info.date_time)
                renamed.compress_type = info.compress_type
                out.writestr(renamed, source.read(info))
            if name.startswith("assets/build/files/") and \
                    any(name[len("assets/build/files/"):].startswith(p) for p in replaced):
                continue
            data = source.read(info)
            if name == "assets/build/files/mods/3d-monsters/mod.json":
                manifest = json.loads(data.decode("utf-8-sig"))
                for setting in manifest["settings"]:
                    if setting["key"] == "attack":
                        setting["default"] = 2   # On the field: đánh thẳng trên bàn
                data = (json.dumps(manifest, ensure_ascii=False, indent=4) + "\n").encode("utf-8")
            copy = zipfile.ZipInfo(name, date_time=info.date_time)
            copy.compress_type = info.compress_type
            copy.external_attr = info.external_attr
            out.writestr(copy, data)
        for folder, source_dir in MODS.items():
            for root, _dirs, files in os.walk(source_dir):
                for file in sorted(files):
                    path = os.path.join(root, file)
                    relative = os.path.relpath(path, source_dir).replace("\\", "/")
                    if not wanted(relative):
                        continue
                    if folder == "viet-hoa-gfx" and relative == "viet-hoa-gfx.aarch64.o":
                        path = os.path.join(GFX_V030, "viet-hoa-gfx.aarch64.o")
                    entry = f"mods/{folder}/{relative}"
                    if folder == "viet-hoa" and relative == "problems.txt":
                        continue
                    info = zipfile.ZipInfo("assets/build/files/" + entry, date_time=(2026, 10, 16, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_STORED if file.lower().endswith(STORED) else zipfile.ZIP_DEFLATED
                    with open(path, "rb") as handle:
                        out.writestr(info, handle.read())
                    added.append(entry)
        files = keep_list + added
        info = zipfile.ZipInfo("assets/build/files.txt", date_time=(2026, 10, 16, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(info, "\n".join(files) + "\n")
        info = zipfile.ZipInfo("assets/build/buildid", date_time=(2026, 10, 16, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(info, new_id + "\n")
    print(f"buildid {old_id} -> {new_id}")
    for folder in MODS:
        json.loads(open(os.path.join(MODS[folder], "mod.json"), encoding="utf-8-sig").read())
    print(f"{OUT}: {len(added)} files added in {len(MODS)} mods, files.txt {len(files)} lines, "
          f"{os.path.getsize(OUT) / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())
