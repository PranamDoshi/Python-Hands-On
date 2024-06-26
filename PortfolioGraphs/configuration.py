from pathlib import Path
parent_path = Path(Path(__file__).parent).as_posix().replace('/', '\\')

LOGS_FOLDER = f"{parent_path}\logs"

NSE_BSE_Stocks_Details_File = f"{parent_path}\BSE_NSE_Code.csv"
