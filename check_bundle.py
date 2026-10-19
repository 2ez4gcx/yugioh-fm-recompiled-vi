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
