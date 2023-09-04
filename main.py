import time
import pandas as pd
from pathlib import Path
from typing import Any, Optional, Union
import shutil as sh
import glob
import socket
import logging
import argparse as ap

from utils import check_unwanted as cw
from utils.sort_month import sort_month
from utils.get_mail import get_mail
from utils.save import save_file
from utils.send_to_trash import send_to_trash


start_time = time.perf_counter()
USER = '' # DEFINED BY USER
SERVICE = 'mail'


def get_from_frame(root_frame: pd.DataFrame, target: str, name: str, subset: str) -> pd.DataFrame:
    frame = root_frame.loc[root_frame[target] == name]
    return frame


def check_folder(path: Path, element: str) -> None:
    """Checks if folder has been created"""
    if not Path(path / str(element)).is_dir():
        Path(path / str(element)).mkdir()


def update_path(root: Path, element: Any) -> Path:
    check_folder(root, element=element)
    return Path(root / str(element))

def zip_directory(base_name: str, root_dir: Path, format: str = 'zip') -> Optional[Union[Path,None]]:
    for file in glob.glob(str(root_dir)):
        if f"{base_name}.zip" == file:
            return
    try:
        if root_dir.is_dir():
            sh.make_archive(f"{root_dir}/{base_name}", format, root_dir)
        else:
            root_dir = Path(base_name)
            sh.make_archive(f"{root_dir}/{base_name}", format, root_dir)
        return Path(f"{root_dir}/{base_name}.zip")
    except RuntimeError:
        return

def ip_check() -> tuple[str,str]:
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print(f"Your Computer IP Address is: {IPAddr}")
    return hostname, IPAddr

def keep_log(host: str, client_ip: str, ):
    logging.basicConfig(filename="/Users/gerardomartinez/Documents/2023/python_log.log", level=logging.INFO)
    logging.info(f"{time.strftime('%d-%m-%Y %H:%M:%S')} {client_ip} - {host} Program run \n")

def pretty_frame(frame:pd.DataFrame) -> pd.DataFrame:
    if "XML_PATH" in frame.columns:
        frame = frame.drop('XML_PATH', axis=1)
    frame = frame.reset_index(drop=True)
    return frame

def main() -> None:
    host, ip_address = ip_check()
    keep_log(host, ip_address)
    ROOT_DIRECTION = Path(Path.home() / 'Documents')
    month_of_search, year = get_arguments()
    ROOT_DIRECTION = update_path(root=ROOT_DIRECTION,element=year)
    control_name = sort_month(month_of_search)
    ROOT_DIRECTION = update_path(root=ROOT_DIRECTION,element=control_name)
    mail = get_mail(path=ROOT_DIRECTION, month_search=control_name, year_search=year, email_user=USER, service=SERVICE)
    mail.double_check()
    file = mail.file
    FRAME = pd.DataFrame.from_dict(file.csv, orient='index',
                                   columns=['NAME', 'FOLIO', 'CONCEPT', 'SUBTOTAL', 'TAX', 'TOTAL', 'XML_PATH'])

    FRAME_to_trash = FRAME.loc[FRAME['SUBTOTAL']*FRAME['TOTAL'] == 0]
    mail.list_to_trash.append(str(FRAME_to_trash['XML_PATH']))
    FRAME = FRAME.drop_duplicates(subset=['FOLIO'], keep='first')
    FRAME_T = get_from_frame(root_frame=FRAME, target='NAME', name='TSE090522B18', subset='XML_PATH')
    FRAME_G = get_from_frame(root_frame=FRAME, target='NAME', name='MAMG650207659', subset='XML_PATH')
    FRAME_R = get_from_frame(root_frame=FRAME, target='NAME', name='DEMR650805NP2', subset='XML_PATH')

    sf = save_file(path=ROOT_DIRECTION, control=control_name, year=year)
    sf.get_frame(frame=FRAME_T, name='TCS')
    sf.get_frame(frame=FRAME_G, name='GM')
    sf.get_frame(frame=FRAME_R, name='RD')
    sf.close()  # Close excel writer

    cw.sort_file(path=ROOT_DIRECTION, frame=FRAME_T, name='TCS')
    cw.sort_file(path=ROOT_DIRECTION, frame=FRAME_G, name='GM')
    cw.sort_file(path=ROOT_DIRECTION, frame=FRAME_R, name='RD')

    cw.compare_xml_to_pdf(root=ROOT_DIRECTION, names=['TCS', 'GM', 'RD'], to_trash_check=mail.list_to_trash)

    # ENDING STAGES OF PROGRAM
    cw.delete_unwanted_path(path=ROOT_DIRECTION,
                            names=['GM', 'TCS', 'RD'],
                            to_eliminate=['.png', '?=', '.PNG', '.JPG', '.jpg','.docx', '.gif','.eml', '.zip', '.jpeg'])
    send_to_trash(mail.list_to_trash)

    mail.mail.close()
    # mail.mail.logout()
    print('MAIL LOGGED OUT AND CLOSED')
    print("--- %.2fs seconds ---" % (time.perf_counter() - start_time))
    new_frame = pd.concat([FRAME_T,FRAME_G,FRAME_R])
    new_frame = pretty_frame(new_frame)
    new_frame.to_csv(path_or_buf=f'{ROOT_DIRECTION}/FRAME.csv')


def get_arguments() -> tuple[str, int]:
    p = ap.ArgumentParser()
    p.add_argument("month", type=str)
    p.add_argument("year", type=str)
    args = p.parse_args()
    return str(args.month), int(args.year)


if __name__ == '__main__':
    main()