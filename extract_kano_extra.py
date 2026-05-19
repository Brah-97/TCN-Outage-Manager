"""Read remaining rows from KANO REGION sheet that were truncated at 80 rows."""
import openpyxl
fpath = r"C:\Users\HP\OneDrive\Desktop\TCN Files\KANO REGION ISO PARAMETERS.xlsx"
wb = openpyxl.load_workbook(fpath, read_only=True, data_only=True)
ws = wb["KANO REGION"]
for i, row in enumerate(ws.iter_rows(max_col=5, values_only=True), 1):
    if i <= 80:
        continue
    cells = [str(c).strip() if c else "" for c in row]
    if all(x == "" for x in cells):
        continue
    line = " | ".join(cells)
    print(f"R{i:3d}: {line}")
wb.close()
