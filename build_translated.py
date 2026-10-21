"""Build đối tượng Android mới (<library>.aarch64-translated.o) cho mọi mod code trong các thư mục cho trước.

Từ v0.3.1-preview.1, game Android là bản "dịch" (translated): không cần vùng địa chỉ cố định nên chạy được trên
những máy mà v0.3.0 báo "the addresses from 0x80000000 to 0x801FFFFF could not be had". Mod code cho bản đó
phải build lại qua guest pass của game (<library>.aarch64-translated.o); <library>.aarch64.o của v0.3.0 bị tắt.

Thư viện C mà game dịch cho mod mượn có fgets, fseek, fwrite, fclose nhưng chưa có fread. Mod nào gọi fread thì
script chép thêm fread_android.c (fread viết bằng fgets, chỉ build cho game dịch) vào thư mục mod; mã nguồn
của mod giữ nguyên.

    python build_translated.py --sdk <yfm-redecomp-v0.3.1-preview.1>/sdk --cc <llvm-mingw 20260922>/bin/clang.exe \\
        mods/viet-hoa-gfx mods/roi-nhieu-la <thư mục mod khác> ...

Cần clang của llvm-mingw 20260922 (LLVM 23, cùng LLVM với memories-guest-ir.exe trong SDK).
Đối tượng i386 (<library>.o, Windows) và .aarch64.o (Android v0.3.0) giữ như cũ: build theo API 12 của v0.3.0.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SHIM = os.path.join(HERE, "fread_android.c")


def sources(mod):
    return [f for f in os.listdir(mod) if f.endswith((".c", ".h"))]


def calls_fread(mod):
    return any(re.search(r"\bfread\s*\(", open(os.path.join(mod, f), encoding="utf-8", errors="replace").read())
               for f in sources(mod) if f != "fread_android.c")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sdk", required=True, help="thư mục sdk của bản Windows v0.3.1-preview.1")
    parser.add_argument("--cc", required=True, help="clang.exe của llvm-mingw 20260922")
    parser.add_argument("mods", nargs="+")
    arguments = parser.parse_args()
    build_mod = os.path.join(arguments.sdk, "tools", "build_mod.py")
    environment = dict(os.environ, MEMORIES_MOD_CC=arguments.cc, PYTHONIOENCODING="utf-8")
    failed = 0
    for mod in arguments.mods:
        manifest = json.load(open(os.path.join(mod, "mod.json"), encoding="utf-8-sig"))
        library = manifest.get("library")
        if not library:
            print(f"{mod}: mod dữ liệu, bỏ qua")
            continue
        if calls_fread(mod):
            shutil.copyfile(SHIM, os.path.join(mod, "fread_android.c"))
        with tempfile.TemporaryDirectory() as out:
            result = subprocess.run([sys.executable, build_mod, mod, "--target", "aarch64-translated", "--out", out],
                                    env=environment, capture_output=True, text=True, encoding="utf-8")
            built = os.path.join(out, f"{library}.aarch64-translated.o")
            if result.returncode or not os.path.isfile(built):
                print(f"{mod}: LỖI\n{result.stdout}{result.stderr}")
                failed += 1
                continue
            shutil.copyfile(built, os.path.join(mod, f"{library}.aarch64-translated.o"))
            print(f"{mod}: {library}.aarch64-translated.o, {os.path.getsize(built)} byte"
                  f"{' (kèm fread_android.c)' if calls_fread(mod) else ''}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
