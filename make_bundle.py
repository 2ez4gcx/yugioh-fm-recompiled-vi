"""Gói mod duy nhất cho bản chính thức của Yu-Gi-Oh! Forbidden Memories Recompiled: v0.3.0 (Windows và Android)
và v0.3.1-preview.1 (Windows và Android).

Một file zip, thư mục mods/ ở gốc:
  * Android: Mods > Import mod... nhận mọi mod trong mods/ (trình nhập của v0.3.0 đọc thư mục bọc mods/);
  * PC: giải nén vào Documents/My Games/YFM Re-Decomp, được mods/<mod>.
Mod code có ba đối tượng:
  * <library>.o, i386 (Windows v0.3.0 và v0.3.1-preview.1), build theo API 12 (tools/pc/build_mod.py của port
    v0.3.0): bản API mới hơn bị game v0.3.0 từ chối;
  * <library>.aarch64.o, Android v0.3.0 (game bộ nhớ cố định), cùng API 12;
  * <library>.aarch64-translated.o, Android v0.3.1-preview.1 (game dịch), build bằng build_translated.py với
    SDK của bản v0.3.1-preview.1.

    python make_bundle.py --version 2.1 --out <thư mục> --others <thư mục mod của tác giả khác>
Mod của repo này lấy từ mods/; mod của tác giả khác mặc định từ thư mục mods/ của người chơi.
"""
import argparse, hashlib, json, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
USER_MODS = os.path.join(os.path.expanduser("~"), "Documents", "My Games", "YFM Re-Decomp", "mods")
OWN = ["viet-hoa", "viet-hoa-gfx", "du-722-la", "monster-effects-vi", "roi-nhieu-la", "may-choi-nhanh"]   # mods/ của repo này
# Mod của tác giả khác đi kèm. Bản Việt hoá là của repo này (viet-hoa), không gói bản dịch khác.
OTHERS = ["monster-effects", "simon-at-table", "3d-duel-arena", "dual-play", "ai-hard-mode"]
SKIP_SUFFIXES = (".pdb", ".undefined", ".partial")


def wanted(name):
    if name.endswith(SKIP_SUFFIXES) or name == "problems.txt":
        return False
    # Đối tượng của nền x86_64 chỉ cho bản build x64 từ mã nguồn; bản chính thức dùng i386 và aarch64.
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--others", default=USER_MODS, help="thư mục chứa mod của tác giả khác")
    arguments = parser.parse_args()
    name = f"yfm-viet-hoa-mods-v{arguments.version}.zip"
    out = os.path.join(arguments.out, name)
    os.makedirs(arguments.out, exist_ok=True)
    sources = [(m, os.path.join(HERE, "mods", m)) for m in OWN] + \
              [(m, os.path.join(arguments.others, m)) for m in OTHERS]
    files, objects = 0, {}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(HERE, "HUONG-DAN.txt"), "HUONG-DAN.txt")
        for mod, root in sources:
            manifest = json.load(open(os.path.join(root, "mod.json"), encoding="utf-8-sig"))
            if manifest.get("library"):
                have = sorted(f for f in os.listdir(root) if f.endswith(".o"))
                library = manifest["library"]
                for need in (f"{library}.o", f"{library}.aarch64.o", f"{library}.aarch64-translated.o"):
                    if need not in have:
                        sys.exit(f"{mod}: thiếu {need} (cần Windows i386, Android v0.3.0 và Android v0.3.1)")
                objects[mod] = have
            for folder, _dirs, names in os.walk(root):
                for f in sorted(names):
                    relative = os.path.relpath(os.path.join(folder, f), root).replace("\\", "/")
                    if wanted(relative):
                        z.write(os.path.join(folder, f), f"mods/{mod}/{relative}")
                        files += 1
    digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"{out}: {len(sources)} mod, {files} file, {os.path.getsize(out) / 1e6:.1f} MB\nSHA-256 {digest}")
    for mod, have in objects.items():
        print(f"  {mod}: {' '.join(have)}")


if __name__ == "__main__":
    sys.exit(main())
