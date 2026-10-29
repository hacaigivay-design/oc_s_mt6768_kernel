#!/usr/bin/env python3
import sys, re

P = "include/linux/mmu_notifier.h"
s = open(P).read()

# Nếu enum đã có định nghĩa đầy đủ → không patch
if re.search(r'enum\s+mmu_notifier_event\s*\{', s):
    print("[fix_mmu] enum mmu_notifier_event da duoc dinh nghia - khong patch")
    sys.exit(0)

lines = s.split("\n")

# Tìm dòng đầu tiên DÙNG enum (không phải định nghĩa)
idx_use = None
for i, ln in enumerate(lines):
    if "enum mmu_notifier_event" in ln and "{" not in ln:
        idx_use = i
        break

if idx_use is None:
    print("[fix_mmu] Khong tim thay cho dung enum - bo qua")
    sys.exit(0)

enum_def = (
    "enum mmu_notifier_event {\n"
    "\tMMU_NOTIFY_UNMAP = 0,\n"
    "\tMMU_NOTIFY_CLEAR,\n"
    "\tMMU_NOTIFY_PROTECTION_VMA,\n"
    "\tMMU_NOTIFY_PROTECTION_PAGE,\n"
    "\tMMU_NOTIFY_SOFT_DIRTY,\n"
    "\tMMU_NOTIFY_RELEASE,\n"
    "\tMMU_NOTIFY_MIGRATE,\n"
    "};\n"
)

# Chèn ngay TRƯỚC khối struct/function chứa dòng dùng
insert_at = idx_use
for j in range(idx_use, -1, -1):
    st = lines[j].lstrip()
    if st.startswith("struct ") or st.startswith("static inline") or st.startswith("void "):
        insert_at = j
        break

lines.insert(insert_at, enum_def)
open(P, "w").write("\n".join(lines))
print("[fix_mmu] Da chen enum tai dong %d (truoc cho dung dong %d)" % (insert_at + 1, idx_use + 1))