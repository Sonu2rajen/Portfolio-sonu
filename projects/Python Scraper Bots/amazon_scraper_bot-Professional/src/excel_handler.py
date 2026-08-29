import pandas as pd
from pathlib import Path
from src.utils import today

INPUT_FILE = Path("input/SCRAP-DATA.xlsx")
OUTPUT_FILE = Path("output/SCRAP-OUTPUT.xlsx")

def read_cocoblu_asins():
    df = pd.read_excel(INPUT_FILE, sheet_name="Sheet3")
    return df["ccb"].dropna().astype(str).tolist()

def write_output(rows, sheet_prefix):
    sheet_name = f"{sheet_prefix}_{today()}"
    df = pd.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    try:
        if OUTPUT_FILE.exists():
            with pd.ExcelWriter(
                OUTPUT_FILE,
                engine="openpyxl",
                mode="a",
                if_sheet_exists="replace"
            ) as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    except PermissionError:
        print("❌ ERROR: Output Excel file is OPEN. Close Excel and run again.")
        raise