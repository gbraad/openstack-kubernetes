Generate diff

diff -Naur original.py patched.py > patch.diff

Apply patch

patch /path/to/script.py patch.diff