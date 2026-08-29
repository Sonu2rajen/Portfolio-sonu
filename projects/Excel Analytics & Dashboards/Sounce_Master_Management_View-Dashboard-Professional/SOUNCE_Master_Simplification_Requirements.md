# CBU Master Simplification — Antigravity Requirements

## 1. Objective
Create a manager-friendly Excel workbook from the supplied source workbook `UPDATED CBU MASTER_1.xlsx`.

The goal is **restructuring, organization, formatting, and readability only**. The workbook must preserve the business data exactly as supplied.

## 2. NON-NEGOTIABLE DATA PRESERVATION RULES
1. Do NOT change any existing numeric value.
2. Do NOT recalculate existing Static, Video, or Grand Total values.
3. Do NOT infer missing values.
4. Do NOT replace blanks with zero unless a new display-only summary explicitly requires it and the original value is still preserved in Source Data.
5. Do NOT reconcile or correct apparent mismatches in the source data.
6. Do NOT add formulas to replace existing values.
7. Preserve the exact existing numbers even where they appear mathematically inconsistent because some source data is incomplete.
8. Preserve source text values unless a change is strictly a presentation-safe spelling/capitalization normalization; never alter business meaning.
9. Existing final/grand-total values must remain exactly as supplied.

## 3. BUSINESS LOGIC TO PRESERVE
For each Asset Type, the source has Static and Video sections.

Static conceptually contains:
- Static Master
- Static Adapt
- Static AI
- Static Non-AI
- Static Total / applicable final value

The business expectation is that Master + Adapt corresponds conceptually to AI + Non-AI, but the source file contains missing/incomplete data. Therefore **do not calculate or correct these relationships**.

The same principle applies to Video.

## 4. REQUIRED WORKBOOK STRUCTURE
Create exactly these five sheets, in this order:

1. `01 Executive Summary`
2. `02 BU Summary`
3. `03 Brand & Asset Detail`
4. `04 Asset Type Analysis`
5. `05 Source Data`

## 5. SHEET 01 — EXECUTIVE SUMMARY
Purpose: first sheet opened by a manager; provide an immediate complete management overview.

Include:
- Workbook title: `CBU Master – Management View`
- Reporting overview / scope statement
- Overall asset figures using the source's existing values only
- Business Unit overview
- Brand overview
- Static vs Video overview where this can be presented without inventing/recalculating source values
- Clear KPI-style summary cards based on preserved source values
- One or two simple charts only if they can be generated without changing the underlying source logic

The summary must be visually clean, professional, and easy to scan.

## 6. SHEET 02 — BU SUMMARY
Purpose: summarize information by Business Unit.

Expected hierarchy:
Business Unit → Brand → Static / Video / Total overview

Display each Business Unit as a clearly separated section.

Use a consistent but subtle colour family for each BU. Current BU groups include at least:
- F&B
- B&W
- PC

Do not use overly bright colours. Use professional, readable section fills/accent colours.

The user must be able to visually distinguish BU sections immediately.

## 7. SHEET 03 — BRAND & ASSET DETAIL
Purpose: this is the **complete overview / drill-down sheet**. A manager should be able to understand the full hierarchy from one sheet without switching tabs.

Recommended structure:
Business Unit → Brand → Asset Type → Static fields → Video fields → Final / Grand Total

Include the original detailed dimensions represented in the source, such as:
- Business Unit
- Brand
- Asset Type
- Static Master
- Static Adapt
- Static AI
- Static Non-AI
- Static Total (existing source value)
- Video Master
- Video Adapt
- Video AI
- Video Non-AI
- Video Total (existing source value, if present)
- Final / Grand Total (existing source value)

Make the hierarchy visually obvious through grouping, indentation, section bands, or subtle shading.

Requirements:
- Autofilters enabled
- Freeze panes so headers and key identifying columns remain visible while scrolling
- Appropriate column widths
- Wrapped multi-line headers where needed
- Consistent number formatting
- No unnecessary merged cells inside the main data table
- Existing values preserved exactly

## 8. SHEET 04 — ASSET TYPE ANALYSIS
Purpose: make asset-type patterns easy to understand.

Organize around Asset Type (for example Social, ECOM, PMA, Other, and any other source values).

Show the existing Static and Video figures at the appropriate aggregation/display level.

Do not create new business logic. Any summary must be traceable to existing source values and must not overwrite source values.

A simple visual such as an asset-type comparison chart may be added only when the chart is based on clearly preserved source totals.

## 9. SHEET 05 — SOURCE DATA
Purpose: preserve the original source for traceability/audit.

This sheet should contain the source data in its original structure and values.

Rules:
- Do not alter numeric values.
- Do not add formulas over source data.
- Keep original row/column content intact as much as possible.
- It is acceptable to apply minimal readability formatting (such as freeze panes, filters, or widths) only if the underlying values and structure remain unchanged.

## 10. FORMATTING / UX REQUIREMENTS
Use a professional corporate Excel style.

General rules:
- Clean typography
- Strong header hierarchy
- Consistent alignment
- Subtle borders
- Good whitespace
- No decorative clutter
- Avoid excessive conditional formatting
- Avoid too many colours
- Keep negative/exception visual emphasis restrained and meaningful

Business Unit colour approach:
- Each BU should have a distinct, consistent accent colour.
- Use the same BU colour consistently wherever that BU appears.
- Prefer light section fills + dark readable text over saturated fills.

## 11. DATA CLEANING / PRESENTATION
Presentation-safe cleanup is allowed for obvious labels such as:
- `Buisness Unit` → `Business Unit`
- `Video Non-Ai` → `Video Non-AI`

But do not modify values when the change could affect business meaning.

Do not reinterpret blanks, totals, or classification values.

## 12. QUALITY CHECKS BEFORE DELIVERY
Before producing the final workbook:

1. Confirm all five sheets exist and are in the required order.
2. Confirm every source numeric value is preserved.
3. Confirm existing final/grand totals were not recalculated.
4. Confirm no missing values were invented.
5. Confirm formulas have not replaced source values.
6. Confirm the complete overview exists on `03 Brand & Asset Detail`.
7. Confirm BU colours are consistent.
8. Confirm filters and freeze panes are applied where appropriate.
9. Confirm headers are readable and columns are appropriately sized.
10. Confirm the output opens successfully as an `.xlsx` file.
11. Produce a concise validation summary stating that the source values were preserved and listing any presentation-only transformations performed.

## 13. OUTPUT
Create a ready-to-use Excel workbook named:

`CBU_Master_Management_View.xlsx`

Do not merely provide a design description. Actually create the workbook and save it in the active project/workspace.

## 14. IMPORTANT EXECUTION INSTRUCTION
First inspect the source workbook and map its existing sheet structure and column meanings.

Then create the simplified workbook using the five-sheet structure above.

If any ambiguity exists, prefer preserving the source exactly over making an assumption.

The priority order is:
1. Data preservation
2. Manager readability
3. Clear hierarchy
4. Professional visual design
5. Traceability
