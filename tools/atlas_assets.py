import hashlib
from pathlib import Path


def atlas_asset_version(root: Path) -> str:
    inputs = [
        root / "diagrams" / "contextweaver-nextgen-atlas-source.drawio",
        root / "tools" / "build_angled_nextgen_architecture.py",
        *sorted((root / "assets" / "media").glob("atlas-glass-*.png")),
    ]
    digest = hashlib.sha256()
    for path in inputs:
        content = path.read_bytes()
        if path.suffix == ".drawio":
            content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()[:12]
