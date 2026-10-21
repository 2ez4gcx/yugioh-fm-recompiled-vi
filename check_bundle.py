import sys, zipfile

z = zipfile.ZipFile(sys.argv[1])
names = z.namelist()
total = sum(i.file_size for i in z.infolist())
print(len(names), "entries,", round(total / 1e6, 1), "MB unpacked; top:", sorted({n.split("/")[0] for n in names}))
print("mods:", sorted({n.split("/")[1] for n in names if n.startswith("mods/")}))
bad = [n for n in names if "\\" in n or n.startswith("/") or ".." in n.split("/") or ":" in n]
print("bad names:", bad)
print("translation-vi present:", any("translation-vi" in n for n in names))
print("importer limits ok:", len(names) < 20000 and total < 512e6)
# Mỗi mod code: đối tượng cho Windows (i386), Android v0.3.0 (.aarch64.o) và Android v0.3.1 (.aarch64-translated.o).
import json
for mod in sorted({n.split("/")[1] for n in names if n.startswith("mods/") and n.count("/") >= 2}):
    manifest = json.loads(z.read(f"mods/{mod}/mod.json").decode("utf-8-sig"))
    library = manifest.get("library")
    if library:
        missing = [s for s in (".o", ".aarch64.o", ".aarch64-translated.o") if f"mods/{mod}/{library}{s}" not in names]
        print(f"  {mod}: {'đủ 3 đối tượng' if not missing else 'THIẾU ' + ' '.join(missing)}")
