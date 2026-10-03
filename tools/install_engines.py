"""Install pinned official mihomo and build the AdGuard DNS audit wrapper."""
import argparse
import gzip
import hashlib
import io
import platform
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v1.19.32"
ASSETS = {
    "Windows": ("mihomo-windows-amd64-compatible-v1.19.32.zip", "974a4d7ad69aed27aa2e8f91d61113573c14dadb14562c63e58effabf59816f0"),
    "Linux": ("mihomo-linux-amd64-compatible-v1.19.32.gz", "ba3ce607747a07f948fc35780e108a4a7c7f552a38b9bd4d115f313ebcb89c20"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mihomo-only", action="store_true")
    args = parser.parse_args()
    system = platform.system()
    if system not in ASSETS or platform.machine().lower() not in {"amd64", "x86_64"}:
        raise SystemExit("Installer supports Windows/Linux x64 only")
    suffix = ".exe" if system == "Windows" else ""
    sys.path.insert(0, str(ROOT))
    from compiler.network import atomic
    if not args.mihomo_only:
        go = shutil.which("go")
        if not go:
            raise SystemExit("Install Go 1.27.1 before building the AdGuard audit wrapper")
        target = ROOT / ".cache" / ("dns-rule-validator" + suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([go, "test", "./..."], cwd=ROOT / "tools/engine", check=True)
        subprocess.run([go, "build", "-o", str(target), "."], cwd=ROOT / "tools/engine", check=True)
    name, checksum = ASSETS[system]
    url = f"https://github.com/MetaCubeX/mihomo/releases/download/{VERSION}/{name}"
    with urlopen(Request(url, headers={"User-Agent": "adguardhome-compiled-filters/2"}), timeout=90) as response:
        archive = response.read(100 * 1024 * 1024)
    if hashlib.sha256(archive).hexdigest() != checksum:
        raise SystemExit("Mihomo release checksum mismatch")
    if system == "Windows":
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            names = [n for n in bundle.namelist() if n.endswith(".exe")]
            if len(names) != 1:
                raise SystemExit("Unexpected release archive")
            executable = bundle.read(names[0])
    else:
        executable = gzip.decompress(archive)
    target = ROOT / ".cache/mihomo" / ("mihomo" + suffix)
    atomic(target, executable)
    target.chmod(0o755)
    print(f"Installed {VERSION}, SHA256 verified; engines ready")


if __name__ == "__main__":
    main()
