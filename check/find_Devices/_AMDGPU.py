#   AMDGPU_LLVM_TARGET
#   Information from: [
#       https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html
#       https://www.techpowerup.com/gpu-specs/
#     ]
#   Note: New devices should be added to this list as they become available.

#   Add list: From Radeon -> Radeon Pro -> Radeon MI / CDNA.

from utils.status import NOTFOUND, NOTDEFINED
from utils import *

_amdgpu = {
    # RDNA 3
    "gfx1100": [
        "AMD Radeon RX 7900 XTX",
        "AMD Radeon RX 7900 XT",
        "AMD Radeon RX 7900 GRE",
        "AMD Radeon PRO W7900 Dual Slot",
        "AMD Radeon PRO W7900",
        "AMD Radeon PRO W7800 48GB",
        "AMD Radeon PRO W7800",
    ],
    "gfx1101": [
        "AMD Radeon RX 7800 XT",
        "AMD Radeon RX 7800",
        "AMD Radeon RX 7700 XT",
        "AMD Radeon RX 7700",
        "AMD Radeon PRO W7700",
        "AMD Radeon PRO V710",
    ],
    "gfx1102": [
        "AMD Radeon RX 7700S",
        "AMD Radeon RX 7650 GRE",
        "AMD Radeon RX 7600 XT",
        "AMD Radeon RX 7600",
        "AMD Radeon RX 7400",
    ],
    "gfx1103": [
        "AMD Radeon 780M",
    ],
    # RDNA 3.5
    "gfx1151": [
        "AMD Strix Halo",
    ],
    "gfx1150": [
        "AMD Strix Point",
    ],
    "gfx1152": [
        " AMD Krackan Point",
    ],
    "gfx1153": [
        "AMD Radeon 820M",
    ],
    # RDNA 4
    "gfx1201": [
        "AMD Radeon RX 9070 XT",
        "AMD Radeon RX 9070 GRE",
        "AMD Radeon RX 9070",
        "AMD Radeon AI PRO R9700",
    ],
    "gfx1200": [
        "AMD Radeon RX 9060 XT",
        "AMD Radeon RX 9060 XT 8GB",
        "AMD Radeon RX 9060",
    ],
    # RDNA 2
    "gfx1030": [
        "AMD Radeon RX 6950 XT",
        "AMD Radeon RX 6900 XT",
        "AMD Radeon RX 6800 XT",
        "AMD Radeon PRO W6800",
        "AMD Radeon PRO V620",
    ],
    "gfx1031": [
        "AMD Radeon RX 6750 XT",
        "AMD Radeon RX 6700 XT",
        "AMD Radeon RX 6700",
    ],
    "gfx1032": [
        "AMD Radeon RX 6650 XT",
        "AMD Radeon RX 6600 XT",
        "AMD Radeon RX 6600",
        "AMD Radeon PRO W6600",
    ],
    "gfx1034": [
        "AMD Radeon RX 6500 XT",
        "AMD Radeon RX 6500",
        "AMD Radeon RX 6500 4GB",
        "AMD Radeon PRO W6400",
    ],
    # RDNA 1
    "gfx1010": [
        "AMD Radeon RX 5700 XT 50th Anniversary",
        "AMD Radeon RX 5700 XT",
        "AMD Radeon RX 5700",
        "AMD Radeon RX 5600 XT",
        "AMD Radeon RX 5600",
    ],
    "gfx1011": [
        "AMD Radeon RX 5500 XT",
        "AMD Radeon RX 5500",
    ],
    "gfx1012": ["AMD Radeon RX 5300 XT", "AMD Radeon Pro W5500"],
    # Radeon VEGA
    "gfx906": [
        "AMD Radeon VII",
    ],
}


class AMDGPU_LLVM_TARGETS:
    def __init__(self, GPU: str):
        if GPU is None:
            raise ValueError("class AMDGPU_LLVM_TARGETS required a GPU name.")

        self.gpu = GPU
        self.gfx = self.__gfx__()

    def __gfx__(self):
        name_to_gfx = {}
        for gfx, names in _amdgpu.items():
            for name in names:
                name_to_gfx[name] = gfx

        gpu_llvm = (
            f"{self.gpu} ({name_to_gfx[self.gpu]})"
            if self.gpu in name_to_gfx
            else NOTFOUND
        )

        return gpu_llvm

    def __str__(self):
        return self.gfx

    def __repr__(self):
        return f"AMDGPU_LLVM_TARGET(GPU='{self.gpu}', LLVM_Target='{self.gfx}')"


def therock_avail_status(
    file_path: str = None,
) -> dict[str, dict[str, str]]:  # 注意這裡型別提示改成了 dict[str, dict]

    file_path = (
        gitrepo / "cmake/therock_amdgpu_targets.cmake"
        if file_path is None
        else file_path
    )

    import re

    final_dict = {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r"therock_add_amdgpu_target\s*\((.*?)\)"
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            block_content = match.group(1)
            tokens = block_content.split()
            if not tokens:
                continue

            target_name = tokens[0].strip('"').strip()

            # --- 解析 Excludes (黃框) 更新 ---
            exclude_dict = {}  # 改用字典儲存

            if "EXCLUDE_TARGET_PROJECTS" in block_content:
                parts = block_content.split("EXCLUDE_TARGET_PROJECTS", 1)
                if len(parts) > 1:
                    raw_excludes = parts[1]

                    for line in raw_excludes.split("\n"):
                        line = line.strip()
                        # 跳過空行或 CMake 的右括號
                        if not line or line.startswith(")"):
                            continue

                        if "#" in line:
                            # 分離專案名稱與註解
                            proj_part, comment_part = line.split("#", 1)
                            proj = proj_part.strip()
                            comment = comment_part.strip()

                            if proj:
                                # 嘗試從 GitHub 網址中萃取出 Issue ID
                                if "issues/" in comment:
                                    issue_id = comment.split("issues/")[-1].strip()
                                else:
                                    issue_id = comment  # 若非標準網址，保留原始註解

                                exclude_dict[proj] = issue_id
                        else:
                            # 如果沒有註解 (例如純寫 composable_kernel)
                            proj = line.strip()
                            if proj:
                                exclude_dict[proj] = "No Issue tracked"

            final_dict[target_name] = exclude_dict

        return final_dict

    except FileNotFoundError:
        print(f"找不到檔案: {file_path}")
        return {}


def amdgpu_gfx_name(GPU):
    name_to_gfx = {}
    for gfx, names in _amdgpu.items():
        for name in names:
            name_to_gfx[name] = gfx

    gpu_llvm = name_to_gfx[GPU] if GPU in name_to_gfx else NOTDEFINED

    return gpu_llvm
