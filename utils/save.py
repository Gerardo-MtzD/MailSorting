import pandas as pd
from pathlib import Path


class save_file:
    control: str
    year: int

    def __init__(self, path: Path, control: str, year: int) -> None:
        self.full_path = Path(path / f'{control}.xlsx')
        self.writer = pd.ExcelWriter(self.full_path, engine='xlsxwriter')
        # self.write_to_excel(FRAME_T, name='TCS')
        # self.write_to_excel(FRAME_G, name='GM')
        # self.write_to_excel(FRAME_R, name='RD')
        # self.writer.save()

    def get_frame(self, frame: pd.DataFrame, name: str) -> None:
        self.write_to_excel(frame=frame, name=name)

    def write_to_excel(self, frame: pd.DataFrame, name: str) -> None:
        if isinstance(frame, pd.DataFrame):
            frame = frame.drop('XML_PATH', axis=1)
            frame = frame.drop_duplicates(subset=['FOLIO'],keep='first')
            frame = frame.reset_index(drop=True)
            frame = frame.style.set_properties(**{
                'font-size': '9pt',
            })
            frame.to_excel(self.writer, sheet_name=name)
        else:
            pd.DataFrame().to_excel(self.writer, sheet_name=name)

    def close(self):
        self.writer.save()
