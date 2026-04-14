---
name: excel-report-styler
description: "Transform plain or raw Excel reports into polished, presentation-ready workbooks with warm vivid color scales, conditional formatting, data bars, frozen panes, and annotated headers. Use this skill whenever the user uploads an .xlsx file and asks to make it 'colorful', 'impactful', 'presentation-ready', 'annotated', 'formatted', 'polished', or wants outliers to stand out. Also trigger when the user says 'add color scales', 'highlight outliers', 'make it pop', 'style this spreadsheet', 'beautify this Excel', or 'format for leadership'. Works on any multi-sheet Excel workbook. Does NOT create new analysis or change data -- only applies visual formatting on top of existing content."
---

# Excel Report Styler

Transform raw Excel workbooks into polished, presentation-ready reports using warm vivid formatting, color scales, conditional highlighting, data bars, and structural polish. The goal is to make outliers visually obvious and the report scannable at a glance -- bold enough to read at a distance, warm enough not to feel harsh.

## When to Use

- User uploads an .xlsx and wants it visually improved
- Phrases like "make it colorful", "add spark", "highlight outliers", "presentation-ready"
- Any request to apply conditional formatting, color scales, or data bars to an existing workbook
- When leadership or business stakeholders need to review raw data exports

## Core Principles

1. **Never alter data.** Only add formatting, conditional rules, and structural polish.
2. **Auto-detect structure.** Scan each sheet for header rows, data ranges, numeric vs. text columns, and flag/status columns.
3. **Warm vivid color scales on metrics.** Apply 3-color gradient scales (warm green - golden - terracotta) to numeric KPI columns.
4. **Conditional highlights on flags/status.** Color-code status values with warm fills (rose, sage, sand, honey, lavender).
5. **Data bars for magnitude.** Add data bars (warm steel blue) to high-variance numeric columns for instant visual weight.
6. **Structural polish.** Freeze panes, auto-filters, tab colors, cream-tinted alternating rows, professional header styling.
7. **Skip list per sheet.** Exclude columns that don't need color scales (supporting metrics, IDs, etc.) via the SKIP_COLORING config.

## Workflow

### Step 1: Analyze the Workbook

Read the uploaded .xlsx file. For each sheet, identify:

- The header row (usually row 1 or row 3 if row 1 is a title/banner)
- Column data types: numeric, date, text, percentage, currency, flag/status
- Which numeric columns are "higher is better" vs "lower is better"
- Which text columns contain categorical statuses or flags
- Which columns should be skipped from coloring (IDs, supporting metrics)
- Total row count (to decide styling depth for large sheets)

### Step 2: Apply Formatting

Run the Python script `style_excel.py`:

```bash
python style_excel.py "input.xlsx" "output_styled.xlsx"
```

The script auto-detects headers, classifies columns, and applies the warm vivid palette. Columns listed in SKIP_COLORING get font/border/banding but no color scales or data bars.

### Step 3: Manual Adjustments

After running the script, review the output. Common customizations:

- Update SKIP_COLORING dict to add/remove columns per sheet
- Adjust which columns get color scales based on the specific report's meaning
- Add domain-specific conditional formatting (e.g., target status colors for pharma)
- Tune the color palette if the user has brand colors

## Formatting Reference

### Color Palette (Warm Vivid)

| Element | Color | Hex |
|---------|-------|-----|
| Header background | Warm indigo-navy | `2C3E6B` |
| Header text | White | `FFFFFF` |
| Title banner | Warm indigo-navy | `2C3E6B` |
| Data bars | Warm steel blue | `5B8DB8` |
| Alternating rows | Warm cream | `F5F2EE` |
| Good/high values | Warm green | `6BAF5B` |
| Warning/medium | Warm golden | `F5C342` |
| Bad/low/flagged | Warm terracotta | `D96B4F` |
| Flag fill (bad) | Warm rose | `F5D0CB` |
| Flag fill (warning) | Warm sand | `FAE0C3` |
| Flag fill (good) | Warm sage | `C5DFAA` |
| Flag fill (info) | Warm sky | `B8D4E8` |
| Flag fill (special) | Warm lavender | `D4BFE0` |
| Flag fill (neutral) | Warm honey | `FAEAB8` |
| Body text | Warm charcoal | `2D2D2D` |
| Borders | Warm taupe | `C0B8B0` |

### Color Scale Rules

Use 3-color scales with min/percentile-50/max anchors:

- **Higher is better** (calls, hours, attendance): warm green(high) - golden(mid) - terracotta(low)
  `start=D96B4F, mid=F5C342, end=6BAF5B`
- **Lower is better** (cost, flags, errors): warm green(low) - golden(mid) - terracotta(high)
  `start=6BAF5B, mid=F5C342, end=D96B4F`

### Conditional Formatting Patterns

- **Status columns:** Map known values to warm fills (e.g., "Attended" - sage, "No show" - rose, "Canceled" - sand)
- **Flag columns:** Any non-empty cell - warm rose fill
- **Target/tier columns:** Distinct warm color per tier (A=sage, B=sky, C=sand, etc.)
- **Percentage columns:** Color scale from terracotta(0%) through golden(50%) to warm green(100%)

### Column Skip List (SKIP_COLORING)

Per-sheet dict of column headers to exclude from color scales and data bars. These columns still get font, borders, and alt-row banding -- just no color gradients. Typical skips:

- **IDs:** Event ID, NPI, Account ID
- **Supporting metrics:** Phone, Email, Video, Other, GPS %, Bus Miles
- **Financial fields on summary tabs:** Grand Total, Speaker Expenses, etc. (keep on detail tabs)

### Structural Elements

- **Frozen panes:** Freeze below headers and to the right of identifier columns (typically columns A-C)
- **Auto-filters:** Apply to the full header row range on every data sheet
- **Tab colors:** Warm vivid rotation (indigo, olive, sienna, plum, teal, gold)
- **Row height:** Headers = 30px, title rows = 40px
- **Column width:** Auto-fit based on content, min 10, max 35
- **Header font:** Arial Bold 11pt white on warm indigo-navy
- **Body font:** Arial 10pt warm charcoal

### Performance Notes

- For sheets with >5,000 rows, apply cell-level font/border/fill styling only to the first 500 rows. Conditional formatting rules (color scales, data bars, cell-is rules) still apply to the full range since they're rule-based, not cell-by-cell.
- Data bars and color scales are lightweight -- apply freely to any range size.
- Always test that the output opens without corruption.

## Dependencies

- Python 3 with `openpyxl` (install: `pip install openpyxl`)
