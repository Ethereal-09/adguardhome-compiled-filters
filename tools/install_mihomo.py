"""Install the checksum-pinned official mihomo kernel used to export and test rules."""
import argparse
import gzip
import hashlib
from pathlib import Path
import platform
import tempfile
from urllib.request import Request, urlopen
import zipfile

VERSION = 'v1.19.32'
ASSETS = {
    'Windows': ('mihomo-windows-amd64-compatible-v1.19.32.zip',
                '974a4d7ad69aed27aa2e8f91d61113573c14dadb14562c63e58effabf59816f0'),
    'Linux': ('mihomo-linux-amd64-compatible-v1.19.32.gz',
              'ba3ce607747a07f948fc35780e108a4a7c7f552a38b9bd4d115f313ebcb89c20'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    system = platform.system()
    if system not in ASSETS or platform.machine().lower() not in ('amd64', 'x86_64'):
        raise SystemExit('This installer supports Windows/Linux amd64; provide an official v1.19.32 kernel on other systems.')
    filename, expected = ASSETS[system]
    output = args.output or Path('.cache/mihomo') / ('mihomo.exe' if system == 'Windows' else 'mihomo')
    url = f'https://github.com/MetaCubeX/mihomo/releases/download/{VERSION}/{filename}'
    with urlopen(Request(url, headers={'User-Agent': 'adguardhome-compiled-filters'}), timeout=90) as response:
        body = response.read()
    if hashlib.sha256(body).hexdigest() != expected:
        raise SystemExit('Official mihomo asset checksum differs from pinned release')
    if system == 'Windows':
        import io
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            names = [name for name in archive.namelist() if name.endswith('.exe')]
            if len(names) != 1:
                raise SystemExit('Unexpected release archive contents')
            binary = archive.read(names[0])
    else:
        binary = gzip.decompress(body)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(binary)
    temporary.chmod(0o755)
    temporary.replace(output)
    print(f'Installed official mihomo {VERSION}; SHA-256 verified: {output}')


if __name__ == '__main__':
    main()
