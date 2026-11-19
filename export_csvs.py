import csv
import openpyxl

wb = openpyxl.load_workbook("KhetSathi360_2Sheet_Tracker.xlsx", data_only=False)

for name in wb.sheetnames:
    ws = wb[name]
    clean_name = name.replace(" ", "_")
    csv_file = f"{clean_name}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in ws.iter_rows(values_only=True):
            # Only write rows that have at least one non-empty value
            if any(row):
                writer.writerow([str(c or "").strip() for c in row])
    print(f"Exported {csv_file}")
