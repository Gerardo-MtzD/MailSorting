import os
import pandas as pd
from pathlib import Path
import glob

from utils.send_to_trash import send_to_trash


def delete_unwanted(root: Path, archive: str, to_eliminate: list) -> None:
    for element in to_eliminate:
        if element in archive:
            print(f"Sending {str(Path(root / archive))} to trash")
            send_to_trash(Path(root / archive))


def check_names(names: list, archive: str) -> bool:
    for i in names:
        if i in archive:
            return True
    return False


def delete_unwanted_path(path: Path, names: list, to_eliminate: list) -> None:
    """Deletes unwanted files from main folder"""
    for r, d, f in os.walk(str(path)):
        for archive in f:
            if not check_names(names, archive):
                delete_unwanted(root=Path(r), archive=archive, to_eliminate=to_eliminate)


def check_folder(path: Path, element: str):
    if not Path(path / str(element)).is_dir():
        Path(path / str(element)).mkdir()


def move_doc_to_folder(path: Path, name: str) -> None:
    # print(f"move_doc_to_folder: {name}")
    file = path
    check_folder(path.parent, name)
    if not file.rename(path.parent / name / file.name).is_file():
        file.rename(path.parent / name / file.name)

    # print(f" move doc to folder path {file}")


def compare_xml_to_pdf(root: Path, names: list, to_trash_check: list) -> None:
    files = glob.glob(f"{root}/*pdf")
    for file in glob.glob(f"{root}/*pdf"):
        file = Path(file)
        for n in names:
            # print(f"{file.stem}.xml")
            try:
                if f"{root}/{n}/{file.stem}.xml" in list((glob.glob(f"{root}/{n}/*.xml"))):
                    file.rename(root / n / file.name)
                elif f"{root}/{file.stem}.xml" in to_trash_check:
                    file.unlink()
            except FileNotFoundError:
                pass


def validate_frame(frame: pd.DataFrame, name: str, subset: str) -> None:
    if len(frame) > 0:
        path = frame[subset].tolist()
        for p in path:
            # print(f"VALIDATE FRAME INFO:  \n {str(p).split('/')[-1]}  \n {path} \n {name}")
            try:
                move_doc_to_folder(path=Path(p), name=name)
            except FileNotFoundError:
                pass


def sort_file(path: Path, frame: pd.DataFrame, name: str) -> None:
    """Sorts files in corresponding assorted folders"""
    xml_subset = 'XML_PATH'
    # pdf_subset = 'PDF_PATH'
    validate_frame(frame, name, subset=xml_subset)
    # validate_frame(frame_pdf, name, subset=pdf_subset)
