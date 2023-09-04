from pathlib import Path
from typing import Optional, Union


def send_to_trash(document: Optional[Union[str, Path, list]], root: Path = Path(Path.home() / ".Trash")) -> None:

    print(f"sending {document} to trash")
    # root = Path(Path.home() / f".Trash")
    if isinstance(document, str):
        document = Path(document)
        try:
            document.unlink()
        except FileNotFoundError:
            print(f"File: {document.name} already deleted")
    elif isinstance(document,Path):
        document.unlink()

    elif isinstance(document, list):
        for d in document:
            d = Path(d)
            try:
                d.unlink()
            except FileNotFoundError:
                print(f"File: {d.name} already deleted")
    else:
        raise Exception
