"""Mọi dòng của assets/build/files.txt phải qua Paths_Contained của app (paths.c), không thì bị bỏ qua."""
import sys, zipfile

z = zipfile.ZipFile(sys.argv[1])
bad = []
for line in z.read("assets/build/files.txt").decode().splitlines():
    parts = line.split("/")
    if (not line or line.startswith("/") or "\\" in line or (len(line) > 1 and line[1] == ":")
            or any(p in ("", ".", "..") for p in parts)):
        bad.append(line)
print("lines:", len(z.read("assets/build/files.txt").decode().splitlines()), "rejected:", len(bad), bad[:5])
print("non-ASCII names:", [l for l in z.read("assets/build/files.txt").decode().splitlines() if not l.isascii()][:5])
sys.exit(1 if bad else 0)
