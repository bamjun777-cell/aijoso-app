# -*- coding: utf-8 -*-
"""English edition. Legal basis: United States federal law (state law may add more).
Prompt placeholders keep the Korean keys of the master file so saved entries line up; users only see the labels."""
from _common import pr, v, st, proj, doc

LANG = 'en'
CHECKED = '2026-11-09'
PENDING = 'Pending check'

CATEGORIES = {'excel': 'Excel & Data', 'hr': 'HR & Payroll', 'admin': 'Admin & Operations', 'account': 'Accounting',
              'report': 'Reports & Email', 'gsheet': 'Google Sheets', 'sales': 'Sales & Customers', 'logistics': 'Logistics & Inventory'}
FEEDBACK = {'error': 'Report an error', 'add': 'Please add this', 'etc': 'Other'}
CHANGELOG = ['All 30 manuals are now live', 'Sentences trimmed to one line', 'Fixed numbers in the payroll example', 'A4 print preview added']
SYNONYMS = {
  'excel': ['spreadsheet', 'xlsx', 'workbook', 'sheet'], 'merge': ['combine', 'consolidate', 'append', 'join'],
  'payroll': ['salary', 'wages', 'pay', 'paycheck', 'compensation'], 'report': ['summary', 'memo', 'briefing', 'one-page'],
  'overtime': ['ot', 'extra hours', 'timesheet', 'attendance', 'hours'], 'pto': ['vacation', 'leave', 'time off', 'holiday'],
  'hiring': ['job post', 'recruit', 'job ad', 'interview'], 'notice': ['announcement', 'memo', 'promotion'],
  'minutes': ['meeting', 'meeting notes'], 'quote': ['quotation', 'vendor', 'bid', 'estimate'],
  'reconcile': ['reconciliation', 'match', 'deposit', 'bank'], 'card': ['credit card', 'expense', 'gl code', 'account code'],
  'receivable': ['ar', 'overdue', 'unpaid', 'collection', 'dunning'], 'receipt': ['expense', 'expense report', 'reimbursement'],
  'email': ['mail', 'reply', 'decline', 'apology'], 'contract': ['agreement', 'terms', 'clause'],
  'form': ['google forms', 'survey', 'responses'], 'inventory': ['stock', 'stocktake', 'reorder', 'warehouse'],
  'delivery': ['shipping', 'driver', 'courier', 'route'], 'macro': ['vba', 'automate', 'button'],
  'formula': ['function', 'vlookup', 'xlookup', 'sumifs', 'error', 'n/a'], 'compare': ['diff', 'difference', 'changes'],
  'clean': ['cleanup', 'tidy', 'format', 'duplicates'], 'pivot': ['pivot table', 'chart', 'graph'],
  'faq': ['customer questions', 'support', 'reply template'], 'sales': ['revenue', 'customers', 'ranking'],
}
MODERATION = {
  'banned': ['fuck', 'fucking', 'motherfucker', 'shit', 'bullshit', 'bitch', 'asshole', 'bastard', 'cunt', 'dickhead', 'retard', 'whore', 'slut', 'nigger', 'faggot', 'wanker', 'twat'],
  'allow': ['scunthorpe', 'cockpit', 'shitake', 'shiitake', 'assessment', 'bassist'],
}

EXCEL_RULES = ("\n\n[Calculation & print rules]\n"
  "- Put every calculated cell in as an Excel formula, not a typed number, and add a cell note explaining the calculation in plain words (visible on hover).\n"
  "- Add a 'Check' sheet that recalculates the key totals a different way and shows whether they match.\n"
  "- Print setup: Letter or A4 landscape, fit all columns on one page width, repeat the title row, page numbers in the footer.")
DOC_RULES = ("\n\n[Output rules]\n- Word (.docx), one clean page layout, standard business font\n"
  "- Don't invent anything I didn't give you (numbers, dates, promises). Mark gaps as [CHECK].")
V_EXCEL = pr('verify', 'Check: verify every calculation', 'Right after you get the file',
  "Recheck every calculated cell in the Excel file you just made.\nTable: sheet & cell / calculation in words / your recalculated value / value in the file / match?\nIf anything doesn't match, explain why and how to fix it.")
V_TEXT = pr('verify', 'Check: anything made up?', 'Right after you get the draft',
  "Recheck the text you just wrote.\nList anything that wasn't in the information I gave you (numbers, dates, promises, company policy) in a table, then give me a revised version with those removed or marked [CHECK].")

D_UP = doc('Uploading files to Claude', 'Anthropic Help Center', 'https://support.claude.com/en/articles/8241126-uploading-files-to-claude')
D_FILE = doc('Create and edit files with Claude', 'Anthropic Help Center', 'https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude')
D_PROJ = doc('What are projects?', 'Anthropic Help Center', 'https://support.claude.com/en/articles/9517075')
D_ACAD = doc('Intro to Projects (video course)', 'Claude Academy', 'https://academy.claude.com/tutorials/intro-to-projects')
D_XL = doc('XLOOKUP function', 'Microsoft Support', 'https://support.microsoft.com/office/b7fd680e-6d10-43e6-84f9-88eae8bf5929')
D_PIV = doc('Create a PivotTable', 'Microsoft Support', 'https://support.microsoft.com/office/18fb0032-b01a-4c99-9a5f-7ab09edde05a')
D_PQ = doc('Import data from a folder (Power Query)', 'Microsoft Support', 'https://support.microsoft.com/en-us/Excel/import-data-from-a-folder-with-multiple-files-power-query')
D_MAC = doc('Quick start: Create a macro', 'Microsoft Support', 'https://support.microsoft.com/en-us/office/quick-start-create-a-macro-741130ca-080d-49f5-9471-1e5fb3d581a8')
D_FORM = doc('Choose where to save form responses', 'Google Help', 'https://support.google.com/docs/answer/2917686?hl=en')
D_QUOTA = doc('Quotas for Google services (Apps Script)', 'Google for Developers', 'https://developers.google.com/apps-script/guides/services/quotas')
D_TRIG = doc('Installable triggers', 'Google for Developers', 'https://developers.google.com/apps-script/guides/triggers/installable')
D_MW = doc('Minimum Wage', 'U.S. Department of Labor', 'https://www.dol.gov/agencies/whd/minimum-wage')
D_OT = doc('FLSA overtime FAQ', 'U.S. Department of Labor', 'https://webapps.dol.gov/elaws/faq/esa/flsa/011.htm')
D_VAC = doc('Vacation Leave', 'U.S. Department of Labor', 'https://www.dol.gov/general/topic/benefits-leave/vacation_leave')

T_CF = ('Claude', "Turn on 'file creation'")
T_C = ('Claude', 'Chat is enough')
T_X = ('Excel or Google Sheets', 'Check and print results')
T_XP = ('Excel', 'Desktop Excel needed')
T_W = ('Word or Google Docs', 'Final formatting & print')
T_G = ('Google Sheets', 'Free with a Google account')

ITEMS = {}

ITEMS['excel-merge-files'] = dict(
  t='Merge branch Excel files in one go', s='Upload several files and get\na merged file plus a check sheet',
  tags=['excel', 'merge', 'consolidate', 'month-end', 'branch', 'department', 'results'],
  tools=[T_CF, T_X], p='Half a day gone copy-pasting branch files', b='Open, copy, paste, repeat', a='Upload files, send one prompt, done',
  prep=['Files to merge (up to 20)', 'Same column names and order?', 'One header row, no merged cells', 'Remove SSNs, bank and contact details', "Check your company's data rules"],
  proj=('Monthly Excel merge', "You help merge our monthly files. Output an Excel (.xlsx) file. Put calculated cells in as Excel formulas and add a cell note explaining each calculation. Put row counts and totals per source file on a 'Check' sheet, and recalculate the totals a different way on a 'Recheck' sheet. Never change values; collect suspicious rows on a 'Needs review' sheet. Print: landscape, fit to one page wide.", ['One blank standard template', 'Branch/department code list']),
  pr=[pr('main', 'Main: merge files', 'Paste in the chat with the files attached',
    "The {{파일개수}} attached Excel files are {{자료명}}. They all use the same layout, with headers in row {{머리글행}}.\n\nMake one Excel file in this order:\n"
    "1. 'Merged' sheet: stack the data from every file, add a 'Source file' column at the front, and keep the header only once.\n"
    "2. 'Check' sheet: a table of data rows and the total of '{{합계열}}' for each source file, plus the grand total.\n"
    "3. 'Needs review' sheet: blank cells, duplicate rows, text in number columns, and files whose column names differ, each with the reason.\n\n"
    "Don't change any values; only flag things that look wrong on the 'Needs review' sheet.\nName the file {{결과파일명}}.xlsx." + EXCEL_RULES,
    v('파일개수', 'Number of files', '12'), v('자료명', 'What data is it?', 'October sales by branch'), v('머리글행', 'Header row number', '1'),
    v('합계열', 'Column to total', 'Sales'), v('결과파일명', 'Output file name', 'Oct_Branch_Sales_Merged')),
    V_EXCEL,
    pr('mismatch', 'When layouts differ', 'Do this first if column names differ',
    "The attached files have slightly different column orders or names. First show me a table comparing column names by file and suggest how to match columns that mean the same thing. Use '{{기준파일}}' as the standard layout. Merge only after I confirm.",
    v('기준파일', 'Standard file name', 'Seattle.xlsx')),
    pr('powerquery', 'Monthly autopilot: Power Query', "When you can't upload to AI",
    "Walk me through, click by click, how to use Excel Power Query to automatically combine all the Excel files in one folder. My Excel version is {{엑셀버전}} and each file's sheet is named '{{시트이름}}'. Also show me how to swap in next month's files and update with Refresh.",
    v('엑셀버전', 'Excel version', 'Microsoft 365'), v('시트이름', 'Sheet name', 'Sheet1'))],
  st=[st('Remove personal data', 'Delete sensitive columns in a copy', 'Keep the original separately'), st('Turn on file creation', 'Settings > Capabilities', 'Menu name: Code execution and file creation'),
      st('Attach files', 'Upload them all with the clip (+)', 'Split into batches over 20'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Get the result', 'Download and open the Excel file', 'Check there are 4 sheets'), st('Recheck', 'Send the check prompt', 'Compare 2–3 sources by hand'),
      st('Print', 'Confirm one landscape page, then print'), st('Next month', 'Save it as a Project')],
  r=['One Excel file with 4 sheets\nMerged · Check · Needs review · Recheck', '5 branches · 716 rows · $560,380\nDifference vs sources: 0 (check matches)'],
  c=['Always compare totals with the sources', "Check your company's data rules first", 'Unmerge cells before uploading', 'The free plan has usage limits'],
  docs=[D_UP, D_FILE, D_PROJ])

ITEMS['payroll-variance-check'] = dict(
  t='Payroll check vs last month', s='Upload two payroll registers\nfor hires, exits, changes and outliers',
  tags=['payroll', 'payroll register', 'check', 'variance', 'month over month', 'minimum wage', 'labor cost'],
  tools=[T_CF, ('Excel', 'Check and print results')], p='Checking one by one still misses errors', b='Eyeballing two payroll registers', a='From causes of change to a minimum wage screen',
  prep=["Last and this period's payroll registers", "An 'Employee ID' column in both files", 'Remove SSNs, bank and home addresses', 'Notes on this period\'s staff changes', 'Confirm company rules allow uploading'],
  proj=('Payroll check', "You are a payroll review assistant. Never change data. Compare people by employee ID. Output an Excel (.xlsx) file; put calculated cells in as Excel formulas with a cell note explaining each calculation. Break the change in total pay down by cause and show on a 'Check' sheet that the causes add up. Don't make legal calls (FLSA exemption status, regular rate, state wage rules); mark them 'Check needed'. Print landscape, fit to one page wide.", ['Pay item list (item, fixed/variable, taxable/non-taxable)', 'Company allowance and bonus rules']),
  pr=[pr('main', 'Main: variance check', 'Paste in the chat with both files attached',
    "Attachment 1 is the {{전월}} payroll register and attachment 2 is the {{당월}} register. Employee ID is in the '{{사번열}}' column.\n\nPut the following in one Excel file:\n"
    "1. 'Headcount' sheet: IDs only in this period (likely hires) and IDs only in the last period (likely exits)\n"
    "2. 'Variance' sheet: for people in both, each pay item's last period, this period, change and % change\n"
    "3. 'Key changes' sheet: people whose gross pay changed by ${{기준금액}} or more or {{기준비율}}% or more, plus anyone with a pay item that appeared or disappeared\n"
    "4. 'Minimum wage' sheet: hourly-paid or non-exempt people whose base pay divided by {{소정근로시간}} hours comes out below ${{최저시급}} (a screening list only)\n"
    "5. 'Summary' sheet: 3–5 lines on the change in total gross pay and the items and headcount changes that drove it most\n\n"
    "Don't change any data; mark anything you can't judge as 'Check needed'." + EXCEL_RULES,
    v('전월', 'Last period', 'September 2026'), v('당월', 'This period', 'October 2026'), v('사번열', 'Employee ID column', 'Employee ID'),
    v('기준금액', 'Key change threshold ($)', '300'), v('기준비율', 'Key change threshold (%)', '10'),
    v('소정근로시간', 'Scheduled hours per period', '173.33'), v('최저시급', 'Minimum hourly wage ($, federal or your state)', '7.25')),
    V_EXCEL,
    pr('memo-match', 'Match against change notes', 'After the main prompt',
    "Below are this period's staff change notes. Split the people on the 'Key changes' sheet into those explained by the notes and those that aren't, in a table. The unexplained ones are what to check first.\n\n{{변동메모}}",
    v('변동메모', 'Staff change notes', 'E1023 promoted to manager 10/1, E1107 hired 10/15, E0981 left 9/30, meal allowance up $20 for everyone in October')),
    pr('approval-text', 'Approval memo wording', 'After the check is done',
    "Using the 'Summary' sheet, write 3 bullet points explaining the change from last period for the {{당월}} payroll approval memo. Use only the numbers on the sheet.",
    v('당월', 'This period', 'October 2026'))],
  st=[st('Remove personal data', 'Delete sensitive columns in a copy', 'Removing names too is safer'), st('Match ID formats', 'Make both ID columns identical', 'Otherwise hires/exits are wrong'),
      st('Attach files', 'Last period first, then this period', 'Keep file creation on'), st('Send the prompt', 'Fill blanks, copy, paste', 'Use the higher of federal or state minimum'),
      st('Check headcount', 'Compare with actual hires and exits'), st('Match change notes', 'Send the note-matching prompt', 'Start with the unexplained'),
      st('Recheck & reconcile totals', 'Check prompt + compare with payroll system', "Don't finalize if they differ"), st('Print & approve', 'Print on one landscape page', 'Memo wording via prompt too')],
  r=['Excel with 6 sheets + memo wording\nVariance, causes, outliers and check', 'Total $412,800 → $428,550\n+$15,750 (+3.8%) · causes add up'],
  c=['Payroll is sensitive: get company approval', "Don't finalize from AI output alone", 'The minimum wage screen is a guide only', 'Many states set a higher minimum wage'],
  docs=[D_FILE, D_MW, D_OT],
  legal=('Federal minimum wage is $7.25 per hour (effective July 24, 2009). Many states set higher rates; where both apply, follow the higher standard. FLSA overtime: non-exempt employees get at least 1.5× their regular rate for hours over 40 in a workweek.', CHECKED,
         'Exempt status, regular-rate and state rules need an HR or employment law professional to confirm.'))

ITEMS['one-page-exec-report'] = dict(
  t='Turn long material into a one-page report', s='Upload material and state the goal\nfor a one-pager that leads with the conclusion',
  tags=['report', 'summary', 'executive report', 'one-page', 'approval', 'memo', 'word'],
  tools=[T_CF, T_W], p='30 pages of material, the boss reads one', b='Read, extract, cut, cut again', a='Formula footnotes and likely questions too',
  prep=['Source material (Excel, PDF, email)', 'Audience and purpose in one line', "Your company's report template", 'Check rules for confidential material'],
  proj=('One-page report', "Write every report as a one-page executive brief. Lead with the conclusion. Structure: Title / Bottom line (3 lines max) / Current situation / Problem & cause / Options compared / Recommendation / Next steps. Short bullet style. Use only numbers from the attachments and footnote the calculation for any number you computed. Mark anything not in the material as [CHECK]. Date and author at top right. Word (.docx), standard business font, 2 cm / 0.8 in margins.", ['One company report template', '1–2 good example reports']),
  pr=[pr('main', 'Main: one-page draft', 'Paste in the chat with the material attached',
    "Using the attached material, write a one-page report for {{보고대상}}.\n- Purpose: {{보고목적}}\n- The question they'll care most about: {{핵심질문}}\n- Direction of the conclusion (if any): {{결론방향}}\n\n"
    "Structure: Title / Bottom line (3 lines max, conclusion first) / Current situation / Problem & cause / Options compared (table) / Recommendation / Next steps\n\nRules:\n"
    "- Short bullet style; never go over one page\n- Use only numbers in the attachments; mark anything not in them as [CHECK]\n- Put '{{작성일}}, {{작성자}}' at top right\n"
    "- Footnote the calculation for every number you computed (visible on hover in Word)\n- Word (.docx), one portrait page, 2 cm / 0.8 in margins, standard business font",
    v('보고대상', 'Audience', 'the CEO'), v('보고목적', 'Purpose', 'Decide whether to switch our office copier leasing vendor'),
    v('핵심질문', 'Their likely question', 'How much would we save a year, and what would get harder?'), v('결론방향', "Conclusion direction (or 'propose from the data')", 'Recommend switching vendors'),
    v('작성일', 'Date', '2026-11-08'), v('작성자', 'Author', 'Jane Lee, Operations')),
    pr('verify', 'Check: source for every number', 'Right after you get the draft',
    "List every number in the report in a table.\nNumber / where it comes from (file, page, cell) / calculation / recalculated value / match?\nMark any number you can't trace as 'No source'."),
    pr('qna', 'Likely executive questions', 'Right after the draft',
    "Read the report as {{보고대상}} would and give me 5 likely questions with draft answers. Use only evidence from the attachments; if there's none, write 'Needs more checking'.",
    v('보고대상', 'Audience', 'the CEO')),
    pr('shorten', 'Trim when it runs over', "When it's longer than a page",
    "Cut the bottom line to one sentence and the whole report by {{감축비율}}%. Keep the numbers and conclusion as they are, and list what you cut separately as appendix material.",
    v('감축비율', 'Cut by (%)', '20'))],
  st=[st('Gather material', 'Files and emails in one place', 'Check rules for confidential items'), st('Create a Project', 'Add the instructions and template once', 'Free plan: up to 5 projects'),
      st('Material + prompt', 'Attach in a new chat and send'), st('Check length', 'Use the trim prompt if over a page'),
      st('Check the numbers', 'Use the check prompt against sources', 'AI can make numbers up'), st('Likely questions', 'Prepare 5 questions and answers'),
      st('Print', 'Print on one portrait page', 'You make the final call')],
  r=['One-page Word report\nFormula footnotes · 5 likely questions', 'Example: saves $2,160 a year (16.7%)\nFootnotes on 12 numbers'],
  c=['Check every single number', 'You decide the conclusion and ask', "Turned off file creation? You'll get text only", 'Check rules before using confidential material'],
  docs=[D_PROJ, D_FILE, D_ACAD])

ITEMS['excel-compare-files'] = dict(
  t='Compare two files and find the differences', s='Upload two files and get just\nthe added, removed and changed rows',
  tags=['compare', 'difference', 'changes', 'excel', 'price list', 'roster'],
  tools=[T_CF, T_X], p='Comparing two lists, I always miss one', b='VLOOKUP and checking row by row', a='Matched on a key column, only the differences',
  prep=['The two files (old and new)', 'Pick a key column (employee ID, item code)', 'Match column names across files', 'Remove SSNs and contact details'],
  pr=[pr('main', 'Main: compare two files', 'Paste in the chat with both files attached',
    "Attachment 1 is {{이전파일}} and attachment 2 is {{최신파일}}. Compare them on the '{{기준열}}' column and make one Excel file.\n"
    "1. 'Summary' sheet: counts of added, removed and changed rows\n2. 'Added' sheet: rows only in the new file\n3. 'Removed' sheet: rows only in the old file\n"
    "4. 'Changed' sheet: rows in both where {{비교열}} changed (old value / new value / difference side by side; changed cells in yellow)\n"
    "5. 'Needs review' sheet: rows where the key column is blank or duplicated\nDon't change any data." + EXCEL_RULES,
    v('이전파일', 'Old file', 'September vendor price list'), v('최신파일', 'New file', 'October vendor price list'),
    v('기준열', 'Key column', 'Item code'), v('비교열', 'Columns to compare (comma-separated)', 'Unit price, Vendor')),
    V_EXCEL,
    pr('formula', 'DIY: comparison formula', "When you can't upload to AI",
    "Give me Excel formulas to compare Sheet1 (old) and Sheet2 (new) on '{{기준열}}'. I want a column next to the new sheet showing 'New/Changed/Same'. My Excel is {{엑셀버전}}. If XLOOKUP isn't available in that version, use another function.",
    v('기준열', 'Key column', 'Item code'), v('엑셀버전', 'Excel version', 'Microsoft 365'))],
  st=[st('Remove personal data', 'Delete sensitive columns in a copy', 'Keep the original separately'), st('Check the key column', 'Same format in both files', 'Watch leading zeros and spaces'),
      st('Attach files', 'Old file first, then new', 'Keep file creation on'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Review results', 'Start with the summary counts', 'Too many changes? Suspect the key'), st('Recheck', 'Compare 3–4 changes with the source', 'Use the check prompt too')],
  r=['Excel with 5 sheets\nSummary, Added, Removed, Changed, Needs review', 'Example: 1,240-row price list\n37 changed · 5 added · 2 removed'],
  c=['Different key formats flag everything as changed', 'Check a few changes against the source', 'Delete personal data before uploading', 'Over 20 columns? Name only the ones to compare'],
  docs=[D_XL, D_UP, D_FILE])

ITEMS['excel-formula'] = dict(
  t='Write Excel formulas and fix errors', s='Describe the calculation in words\nand get the formula plus a plain explanation',
  tags=['formula', 'function', 'error', 'excel', 'vlookup', 'sumifs'],
  tools=[T_C, T_X], p="I know the math but can't recall the function", b='Search, then trial and error', a='Describe it and get the formula right away',
  prep=['Column names and positions (A, B…)', '2–3 rows of sample data', 'The result you want in one line', 'Excel version (File > Account)'],
  pr=[pr('main', 'Main: write a formula', 'No file needed',
    "Write me an Excel formula.\n- Table layout: {{표구조}}\n- Result I want: {{원하는결과}}\n- Result cell: {{결과칸}}\n- Excel version: {{엑셀버전}}\n\n"
    "1. A formula I can paste in\n2. What it does, one line per part in plain words\n3. Which parts need $ locking when I fill it down\n4. When the result tends to go wrong and how to check it\n5. A fallback formula if my version lacks a function",
    v('표구조', 'Columns and positions', 'A Date, B Branch, C Item, D Sales'), v('원하는결과', 'Result you want', 'Total October sales for the Seattle branch'),
    v('결과칸', 'Result cell', 'G2'), v('엑셀버전', 'Excel version', 'Microsoft 365')),
    pr('error', 'Fix an error', 'When you see #N/A, #VALUE! etc.',
    "This formula returns a {{오류}} error. Give me the likely causes, most likely first, and a fixed formula.\nFormula: {{수식}}\nSituation: {{상황}}",
    v('오류', 'Error shown', '#N/A'), v('수식', 'Problem formula', '=VLOOKUP(A2,Sheet2!A:C,3,0)'), v('상황', 'What happened', "The ID is definitely there but it isn't found")),
    pr('explain', "Explain someone else's formula", 'For handed-over files',
    "Explain step by step, in plain words, what this formula calculates. If there's a simpler way, show me.\n{{수식}}",
    v('수식', 'Formula to explain', '=IFERROR(INDEX(C:C,MATCH(1,(A:A=F2)*(B:B=G2),0)),"")'))],
  st=[st('Note the layout', 'Jot column names and positions', 'Use sample values, not real data'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Paste the formula', 'Paste in the result cell and press Enter'), st('Check by hand', 'Work out 3–4 results yourself', "Don't skip this"),
      st('Fill down', 'Check $ locks, then copy down'), st('If it errors', 'Use the error prompt')],
  r=['A paste-ready formula + plain explanation\nIncluding when it goes wrong', 'e.g. =SUMIFS(D:D,B:B,"Seattle",\nA:A,">="&DATE(2026,10,1))'],
  c=['Always check a few results by hand', 'XLOOKUP needs Excel 2021 or 365', 'Describe with samples, not real data', 'Dates stored as text cause errors'],
  docs=[D_XL])

ITEMS['excel-clean-data'] = dict(
  t='Clean up messy data', s='Upload a messy file and get\na clean version plus a change log',
  tags=['clean', 'cleanup', 'format', 'duplicates', 'excel', 'data'],
  tools=[T_CF, T_X], p='Dates and phone numbers in every format', b='Dozens of find-and-replace runs', a='Set the rules once, cleaned in one go',
  prep=['The Excel file to clean', 'Cleanup rules (date format, etc.)', 'Delete SSNs and bank details', 'Keep the original separately'],
  pr=[pr('main', 'Main: clean the data', 'Paste in the chat with the file attached',
    "The attached file is {{자료명}}. Make a cleaned Excel file using these rules:\n{{정리규칙}}\n\n"
    "1. 'Clean' sheet: the data with the rules applied\n2. 'Change log' sheet: row / column / original value / new value\n"
    "3. 'Duplicates' sheet: rows duplicated on {{중복기준}} (flag them, don't delete)\n4. 'Needs review' sheet: values the rules can't decide\nDon't create values that aren't in the original." + EXCEL_RULES,
    v('자료명', 'What data is it?', 'Vendor list'),
    v('정리규칙', 'Cleanup rules', 'Dates as 2026-10-01, phone numbers as (555) 123-4567, trim spaces, standardize Inc./Incorporated'),
    v('중복기준', 'Column that defines a duplicate', 'Tax ID')),
    V_EXCEL,
    pr('repeat', 'Every month: Power Query', 'When the same cleanup repeats monthly',
    "I get {{자료명}} every month and want to clean it the same way. Show me, click by click, how to apply these rules with Excel Power Query so next month I just swap the file and hit Refresh.\n{{정리규칙}}",
    v('자료명', 'What data is it?', 'Vendor list'), v('정리규칙', 'Cleanup rules', 'Dates as 2026-10-01, trim spaces'))],
  st=[st('Keep the original', 'Work on a copy', "Add '_original' to the file name"), st('Set rules', 'Write each format change on a line'),
      st('Attach the file', 'Turn on file creation and attach'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Skim the change log', 'Look for odd conversions', 'Watch numbers turning into dates'), st('Recheck', 'Same row count as the original?')],
  r=['Excel with 4 sheets\nClean, Change log, Duplicates, Needs review', 'Example: 820 vendors cleaned\n312 cells changed · 9 duplicates flagged'],
  c=['Flag duplicates, never delete them', 'Check the change log for odd conversions', 'Row count should match the original', 'Delete personal data before uploading'],
  docs=[D_PQ, D_FILE])

ITEMS['excel-pivot-chart'] = dict(
  t='Summary tables (pivot) and charts', s='Say what you want to see and get\nthe summary table and chart at once',
  tags=['pivot', 'pivot table', 'chart', 'graph', 'summary', 'excel'],
  tools=[T_CF, T_X], p='Never sure where to click for a pivot', b='Find menus, drag fields, format', a='Name the breakdown, done',
  prep=['The Excel file to summarize', 'One header row, no blank rows', 'How to break it down (by branch, by month)', 'Delete personal data columns'],
  pr=[pr('main', 'Main: summary table & chart', 'Paste in the chat with the file attached',
    "Using the attached {{자료명}}, make an Excel file with a summary table and chart.\n- Rows: {{행기준}}\n- Columns: {{열기준}}\n- Values: {{값}} (sum)\n- Chart: {{차트}}\n\n"
    "1. 'Summary' sheet: the summary table (with row and column totals, thousands separators)\n2. 'Chart' sheet: a chart built from that table, with title and units\n3. 'Notes' sheet: 3 lines on what stands out, with the numbers behind them" + EXCEL_RULES,
    v('자료명', 'What data is it?', '2026 monthly sales by branch'), v('행기준', 'Rows', 'Branch'), v('열기준', 'Columns', 'Month'),
    v('값', 'Value to total', 'Sales'), v('차트', 'Chart type', 'Monthly trend line + bar by branch')),
    V_EXCEL,
    pr('howto', 'DIY: pivot click by click', 'To build it yourself in Excel',
    "Show me, click by click, how to make a PivotTable in Excel {{엑셀버전}} totaling {{값}} by {{행기준}} and {{열기준}}. Also show me how to make new source rows show up with Refresh.",
    v('엑셀버전', 'Excel version', 'Microsoft 365'), v('행기준', 'Rows', 'Branch'), v('열기준', 'Columns', 'Month'), v('값', 'Value to total', 'Sales'))],
  st=[st('Tidy the data', 'One header row, no blank rows', 'Unmerge cells'), st('Decide the breakdown', 'Note rows, columns and values'),
      st('Attach the file', 'Turn on file creation and attach'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Match totals', 'Grand total = source total?', 'Use the check prompt'), st('Print', 'Confirm one landscape page')],
  r=['Excel with 3 sheets\nSummary, Chart, Notes (3 lines)', 'Example: 8 branches × 12 months\n2 charts · 3 lines of notes'],
  c=['Compare the grand total with the source', 'Check the numbers in the notes too', 'Fix blank rows and merged cells first', 'Check the chart units ($ or $K)'],
  docs=[D_PIV, D_FILE])

ITEMS['excel-monthly-analysis'] = dict(
  t='Month-over-month results analysis', s='Upload two periods of results and get\na variance table plus comments on causes',
  tags=['variance', 'month over month', 'analysis', 'sales', 'results', 'excel'],
  tools=[T_CF, T_X], p="I have the numbers, now I have to explain why", b='A day of calculating changes and hunting causes', a='Variance table, key changes and comments in one go',
  prep=['Results files for both periods', 'Key column (branch, item, customer)', 'Notes on known reasons for changes', 'Delete personal data columns'],
  proj=('Monthly results analysis', "You help analyze monthly results. Output an Excel (.xlsx) file. Put calculated cells in as Excel formulas with a cell note explaining each calculation. Comments on causes must rest on the data and my notes; mark guesses as 'Estimate'. Put a recheck of totals on a 'Check' sheet.", ["Last month's analysis", 'Branch/item code list']),
  pr=[pr('main', 'Main: variance analysis', 'Paste in the chat with both files attached',
    "Attachment 1 is {{이전기간}} and attachment 2 is {{비교기간}} {{자료명}}. Analyze by '{{기준열}}' and make an Excel file.\n"
    "1. 'Variance' sheet: previous, current, change and % change for each key, with a total row\n2. 'Key changes' sheet: changes of ${{기준금액}} or more or {{기준비율}}% or more\n"
    "3. 'Comments' sheet: 3–5 lines on the overall change and main causes. Separate what my notes explain from what they don't.\nNotes: {{변동메모}}" + EXCEL_RULES,
    v('이전기간', 'Previous period', 'September 2026'), v('비교기간', 'Comparison period', 'October 2026'), v('자료명', 'What data is it?', 'sales by branch'),
    v('기준열', 'Key column', 'Branch'), v('기준금액', 'Key change threshold ($)', '5000'), v('기준비율', 'Key change threshold (%)', '10'),
    v('변동메모', 'Known reasons for changes', 'Dallas branch won a large new customer; Denver branch closed 10 days for remodeling')),
    V_EXCEL,
    pr('comment', '3 lines for the report', 'After the analysis',
    "Rewrite the 'Comments' sheet as 3 bullet points for a report to {{보고대상}}. Use the sheet's numbers exactly and mark guesses as 'Estimate'.",
    v('보고대상', 'Audience', 'the CEO'))],
  st=[st('Prepare files', 'Same layout for both periods', 'Same key column name'), st('Change notes', 'Write down reasons you know'),
      st('Attach files', 'Previous first, then current'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Match totals', 'Totals equal the sources?', 'Use the check prompt'), st('Check comments', 'Start with unexplained changes'), st('Report', 'Use the 3 lines in your report')],
  r=['Excel: Variance, Key changes, Comments\nPlus a 3-line summary for the report', 'Example: 8 branches, Sep → Oct\n+4.2% · 3 key changes · 1 unexplained'],
  c=['Trust only causes backed by data', "Check lines marked 'Estimate' before use", 'Compare totals with the sources', 'Different layouts? Align them first'],
  docs=[D_FILE, D_PROJ])

ITEMS['excel-vba'] = dict(
  t='Macros for repetitive tasks', s='Write down your repeated clicks\nand get a one-button macro',
  tags=['macro', 'vba', 'automate', 'repetitive', 'excel', 'button'],
  tools=[T_C, T_XP], p='The same dozens of clicks every month', b='Copy sheets, sort and format by hand', a='One macro button and done',
  prep=['Write the repeated steps in order', 'Check sheet names and column positions', 'Always use a copy of the file', 'Check whether your company blocks macros'],
  pr=[pr('main', 'Main: write a macro', 'No file needed',
    "Write me an Excel VBA macro.\n- What it does (in order): {{작업순서}}\n- Sheet name: {{시트이름}}\n- Excel version: {{엑셀버전}}\n\n"
    "1. VBA code to paste (a plain-English comment on every line)\n2. Click-by-click steps to add and run it (starting from turning on the Developer tab)\n3. Have it automatically create a backup sheet before running\n4. If the data or sheet is missing, stop and show a message\n5. Tell me how to save it (.xlsm)",
    v('작업순서', 'Steps in order', '1) Copy the Source sheet 2) Sort by column C descending 3) Thousands separators on the amount column 4) Add a total row 5) Save as PDF'),
    v('시트이름', 'Sheet name', 'Source'), v('엑셀버전', 'Excel version', 'Microsoft 365')),
    pr('error', 'Fix an error', 'When it stops while running',
    "Running this macro gives the error '{{오류메시지}}' on {{오류줄}}. Tell me the cause and give me the full fixed code.\n{{코드}}",
    v('오류메시지', 'Error message', 'Run-time error 9: Subscript out of range'), v('오류줄', 'Highlighted line', 'Sheets("Source").Copy'), v('코드', 'Full code', '(paste the code)')),
    pr('explain', 'Review a macro you received', "Before using someone else's macro",
    "Explain in plain words what this VBA code does, and check for risky actions like deleting files or sending data outside.\n{{코드}}",
    v('코드', 'Code to review', '(paste the code)'))],
  st=[st('Write the steps', 'Number each click'), st('Make a copy', 'Always use a copy', "Macros can't be undone"),
      st('Send the prompt', 'Fill blanks, copy, paste'), st('Add the code', 'Follow the click steps'),
      st('Test run', 'Run on the copy first', 'Compare with doing it by hand'), st('Save as .xlsm', 'Macro-enabled format'), st('If it errors', 'Use the error prompt')],
  r=['Commented VBA code\nHow to add, run and back up', 'Example: copy, sort, format, total\n5 steps in one button'],
  c=['Always test on a copy first', "Macro results can't be undone", 'Never run macros from unknown sources', "Won't run in Excel for the web or phones"],
  docs=[D_MAC])

ITEMS['hr-attendance-overtime'] = dict(
  t='Timesheet totals and overtime', s='Upload clock-in records and get\nweekly hours and FLSA overtime totals',
  tags=['timesheet', 'overtime', 'hours', 'attendance', 'flsa', 'payroll'],
  tools=[T_CF, T_X], p='Working out overtime from punch records is confusing', b='Adding and subtracting hours per person', a='Daily and weekly hours plus overtime screen',
  prep=['Time records (ID, date, in, out)', 'Unpaid meal break rules', 'Workweek start day', 'Remove names (keep IDs only)'],
  proj=('Monthly timesheet totals', "You help total timesheets. Under the FLSA, overtime for non-exempt employees is hours over 40 in a workweek. Put calculated cells in as Excel formulas with a cell note. Don't decide exempt status or state daily-overtime rules; mark them 'Check needed'.", ['Company work-hour and break rules', 'List of exempt / non-exempt employees']),
  pr=[pr('main', 'Main: total hours', 'Paste in the chat with the file attached',
    "The attached file is the {{기간}} time record. Clock-in is in '{{출근열}}' and clock-out in '{{퇴근열}}'.\n"
    "- Scheduled hours: {{소정근로}} per day; unpaid break {{휴게시간}}\n- Workweek starts on: {{휴일목록}}\n\n"
    "1. 'Daily' sheet: hours worked per ID and date\n2. 'Weekly' sheet: hours per ID per workweek, with hours over 40 as overtime\n"
    "3. 'Monthly' sheet: totals of regular and overtime hours per ID\n"
    "4. 'Needs review' sheet: missing punches, shifts over 24 hours, and days where the break is unclear\nCount overtime only by the workweek (over 40 hours), not by day." + EXCEL_RULES,
    v('기간', 'Period', 'October 2026'), v('출근열', 'Clock-in column', 'In'), v('퇴근열', 'Clock-out column', 'Out'),
    v('소정근로', 'Scheduled hours per day', '8'), v('휴게시간', 'Unpaid break', '12:00–12:30 (30 min)'), v('휴일목록', 'Workweek start day', 'Sunday 12:00 a.m.')),
    V_EXCEL,
    pr('pay', 'Overtime pay', 'After the hours are confirmed',
    "Add each ID's regular hourly rate (attached or the '{{시급열}}' column) to the 'Weekly' sheet and calculate overtime pay.\n"
    "Show straight-time pay (all hours × rate) and the overtime premium (overtime hours × rate × 0.5) separately. Only these people are non-exempt: {{인원}}. Mark anyone else 'Check needed'. If there are bonuses or commissions, flag that the regular rate may need adjusting.",
    v('시급열', 'Hourly rate column', 'Hourly rate'), v('인원', 'Non-exempt employees (IDs or "all")', 'all'))],
  st=[st('Remove personal data', 'Delete names, keep IDs'), st('Confirm workweek', 'Note the fixed workweek start', 'It must not change week to week'),
      st('Attach the file', 'Turn on file creation and attach'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Fix review items', 'Fill missing punches first'), st('Sample check', 'Hand-check 2–3 people', 'Use the check prompt too'), st('Overtime pay', 'Pay prompt once hours are final')],
  r=['Excel: Daily, Weekly, Monthly\nOvertime premium can be added', 'Example: 48 people · October\n612 overtime hours · 2 to review'],
  c=['Exempt employees follow different rules', 'Some states have daily overtime', 'Always hand-check 2–3 people', 'Time data is sensitive; use IDs only'],
  docs=[D_OT, D_FILE],
  legal=("FLSA: non-exempt employees must get at least 1.5× their regular rate for hours over 40 in a workweek. Where state overtime law gives more, the higher standard applies.", CHECKED,
         'Exempt status, regular-rate rules and state law need an HR or employment law professional to confirm.'))

ITEMS['hr-annual-leave'] = dict(
  t='PTO accrual, usage and balance tracker', s='Upload hire dates and time off taken\nfor accrued, used and remaining on one sheet',
  tags=['pto', 'vacation', 'leave', 'time off', 'balance', 'accrual'],
  tools=[T_CF, T_X], p='Everyone accrues differently by hire date', b='Hand counting on a calendar for each person', a='Accrued, balance and reminders, automatically',
  prep=['Employee list (ID, hire date)', 'Time off taken (ID, date, days)', 'Your PTO policy (accrual, cap, carryover)', 'Use IDs instead of names'],
  proj=('PTO tracking', "You help track paid time off. Federal law doesn't require paid vacation, so follow only the company policy I give you. Mark anything the data can't settle (leave of absence, policy exceptions) as 'Check needed'. Put calculated cells in as Excel formulas with a cell note.", ['Company PTO policy', 'Employee list']),
  pr=[pr('main', 'Main: PTO tracker', 'Paste in the chat with both files attached',
    "Attachment 1 is the employee list (ID, hire date) and attachment 2 is time off taken. Build a PTO tracker in Excel as of {{기준일}} using this policy: {{운영기준}}\n"
    "1. 'Accrued' sheet: tenure, PTO accrued and how it was calculated, per ID\n2. 'Used' sheet: days used per ID (half days as 0.5)\n"
    "3. 'Balance' sheet: accrued − used; flag anyone with {{촉진기준}} or more days left\n"
    "4. 'Needs review' sheet: missing hire dates, people who used more than they accrued, cases the policy doesn't cover" + EXCEL_RULES,
    v('기준일', 'As-of date', '2026-12-31'), v('운영기준', 'PTO policy', '1.25 days accrued per month, max 20 days, up to 5 days carry over'), v('촉진기준', 'Flag balances of (days)', '5')),
    V_EXCEL,
    pr('notice', 'Reminder to use PTO', 'For people with large balances',
    "Write a friendly reminder for the people flagged on the 'Balance' sheet. Include their remaining days and the deadline ({{사용기한}}), and ask them to send their plans by {{제출기한}}. Note that HR will confirm any carryover or payout rules.",
    v('사용기한', 'Use-by date', '2026-12-31'), v('제출기한', 'Plan due date', '2026-11-20'))],
  st=[st('Prepare data', 'IDs, hire dates, time off taken'), st('Write down the policy', 'Accrual, cap and carryover rules'),
      st('Attach files', 'List first, then time off'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Fix review items', 'Leaves of absence, policy gaps'), st('Sample check', 'One new hire and one long-tenured person', 'Use the check prompt too'), st('Remind', 'Send the reminder to big balances')],
  r=['Excel: Accrued, Used, Balance, Needs review\nPlus a reminder draft', 'Example: 48 people as of 12/31\n11 with 5+ days left'],
  c=['Follow your written PTO policy', 'Some states regulate PTO payout at exit', 'Check state and city sick leave laws', 'HR confirms carryover and payout'],
  docs=[D_VAC, D_FILE],
  legal=('The FLSA does not require payment for time not worked, such as vacations; paid vacation is a matter of agreement between employer and employee. Some states and cities have their own paid leave or payout rules.', CHECKED,
         'State and local leave laws differ. Have an HR or employment law professional confirm.'))

ITEMS['hr-job-posting'] = dict(
  t='Write job postings by role', s='Enter the role and terms and get\nthe posting plus 3 title options',
  tags=['hiring', 'job post', 'recruit', 'job ad', 'indeed'],
  tools=[T_C], p='Every posting starts from a blank page', b='Find an old posting and edit it', a='Enter the terms, get a ready posting',
  prep=['Job title and main duties', 'Requirements and nice-to-haves', 'Location, hours, pay', 'Company intro in 2–3 lines'],
  pr=[pr('main', 'Main: job posting draft', 'No file needed',
    "Write a job posting for {{플랫폼}} using the information below.\n- Company: {{회사소개}}\n- Role: {{직무}}\n- Main duties: {{주요업무}}\n- Requirements: {{자격요건}}\n- Terms: {{근무조건}}\n\n"
    "Structure: 3 title options / one-line pitch / main duties / requirements & nice-to-haves / terms / hiring process\nUse only the terms I gave you; mark anything missing as [CHECK]. Don't use wording that limits by gender, age or other protected traits.",
    v('플랫폼', 'Where it will be posted', 'Indeed'), v('회사소개', 'Company intro', 'A 120-person logistics company in New Jersey, founded 1998'), v('직무', 'Role', 'HR & Office Coordinator'),
    v('주요업무', 'Main duties', 'Payroll and benefits admin, timekeeping, office support'), v('자격요건', 'Requirements', 'Intermediate Excel; 1+ year HR experience preferred'),
    v('근무조건', 'Terms', 'Mon–Fri 9–5, $52,000+/year (negotiable), full-time')),
    V_TEXT,
    pr('check', 'Bias and wording check', 'Last check before posting',
    "Check this job posting for wording about gender, age, origin, appearance, family status or other things unrelated to the job, and for terms that could look different from reality. Give me fixed sentences.\n{{공고}}",
    v('공고', 'Posting to check', '(paste the posting)'))],
  st=[st('Settle the terms', 'Pay, hours and location'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Review', 'Use the check prompt for made-up terms'), st('Bias check', 'Use the wording check prompt'), st('Post', 'Paste into the job board form')],
  r=['Posting ready for the job board\n3 titles and the hiring process', 'Example: HR coordinator posting\n3 titles · one page'],
  c=['Terms must match reality', 'No wording that limits by protected traits', 'Fill every [CHECK] before posting', 'Some states require a pay range'],
  docs=[D_PROJ])

ITEMS['hr-interview'] = dict(
  t='Interview questions and scorecard', s='Enter the role and skills and get\na question set and scorecard',
  tags=['interview', 'questions', 'scorecard', 'hiring', 'evaluation'],
  tools=[T_CF, T_W], p="Every interviewer asks different questions, so we can't compare", b='Whatever comes to mind', a='Same questions and scoring for everyone',
  prep=['Role and main duties', '3–4 skills you most want to see', 'Interview length and number of interviewers', 'Job posting (attach if you have it)'],
  pr=[pr('main', 'Main: questions & scorecard', 'You can attach the posting',
    "Make an interview question set and scorecard for {{직무}} as a Word file.\n- Key skills: {{역량}}\n- Length: {{시간}} minutes, {{면접관}} interviewers\n\n"
    "1. Questions: 2 per skill plus follow-ups, each with an example of a strong answer\n2. Scorecard: 1–5 scale per skill (with behavior examples for each score), total and comments boxes\n3. 5 lines of guidance for interviewers\nDon't include questions unrelated to the job (marriage, family, origin, health, etc.)." + DOC_RULES,
    v('직무', 'Role', 'Warehouse Supervisor'), v('역량', 'Key skills', 'Solving floor problems, managing people, safety mindset, Excel'), v('시간', 'Length (min)', '40'), v('면접관', 'Interviewers', '3')),
    V_TEXT,
    pr('check', 'Check for off-limits questions', "Review interviewers' questions",
    "Find any questions below that are unrelated to the job or could be seen as discriminatory, explain why, and suggest replacements.\n{{질문}}",
    v('질문', 'Questions to check', 'Are you married? / Can you work late? / Where are you originally from?'))],
  st=[st('Pick the skills', '3–4 skills that matter'), st('Send the prompt', 'Attach the posting and paste'),
      st('Tailor questions', 'Adjust to your company'), st('Brief interviewers', 'Agree on scoring beforehand', 'Shared scoring is the key'), st('After interviews', 'Compare scores on the scorecard')],
  r=['Questions by skill + 1–5 scorecard\nWith interviewer guidance', 'Example: 40-min supervisor interview\n8 questions · 1-page scorecard'],
  c=['No questions unrelated to the job', 'Agree on scoring before interviews', "Don't upload candidates' personal data", 'Interviewers make the final call'],
  docs=[D_FILE])

ITEMS['hr-notice'] = dict(
  t='Staff announcements and notices', s='Enter the key points and get\na formal notice and a chat version',
  tags=['notice', 'announcement', 'promotion', 'memo', 'staff'],
  tools=[T_C], p='Even a short notice takes ages to word', b='Find an old one and edit it', a='Formal and short versions at once',
  prep=['Type (appointment, policy, event)', 'Key points and effective date', 'Who it is for', 'Contact for questions'],
  pr=[pr('main', 'Main: two versions', 'No file needed',
    "Write an internal announcement.\n- Type: {{종류}}\n- Key points: {{내용}}\n- For: {{대상}}\n- Effective: {{시행일}}\n- Questions: {{문의처}}\n\n"
    "1. Formal notice (title, body, attachments line)\n2. A chat/Slack version in 5 lines or less\nDon't add benefits or conditions I didn't give; mark gaps as [CHECK].",
    v('종류', 'Type', 'Promotion'), v('내용', 'Key points', 'John Smith promoted to Warehouse 2 Team Lead, effective 11/16'), v('대상', 'For', 'All staff'),
    v('시행일', 'Effective date', '2026-11-16'), v('문의처', 'Questions', 'HR, ext. 1234')),
    V_TEXT,
    pr('table', 'Table of appointments', 'When several people move',
    "Turn the changes below into a table for the notice (Name / Current team / New team / Title / Effective date) and write 2 lines to go above the table.\n{{발령내용}}",
    v('발령내용', 'Changes', 'John Smith Warehouse 1 → Warehouse 2 Team Lead 11/16; Emily Chen promoted to Senior Admin 11/16'))],
  st=[st('Confirm content', 'Check date and audience'), st('Send the prompt', 'Fill blanks, copy, paste'),
      st('Review', 'Use the check prompt'), st('Approval', 'Follow your sign-off process'), st('Post', 'Formal on the board, short in chat')],
  r=['Formal notice + 5-line chat version\nAppointment table on request', 'Example: promotion notice\n1 formal · 5-line chat version'],
  c=['Post appointments and policies after sign-off', 'Double-check names and teams', "Don't add benefits that don't exist", 'Keep personal matters out of notices'],
  docs=[D_PROJ])

ITEMS['admin-minutes'] = dict(
  t='Meeting notes → minutes', s='Paste your notes and get\ndecisions and action items in a table',
  tags=['minutes', 'meeting', 'meeting notes', 'action items', 'decisions'],
  tools=[T_C], p='After the meeting, writing minutes is another job', b='Retyping from notes', a='Decisions, actions and deadlines in a table',
  prep=['Meeting notes (rough is fine)', 'Meeting name, date, attendees', 'Minutes template (if any)'],
  proj=('Meeting minutes', "You write meeting minutes. Use only what's in the notes; never invent. Structure: Overview / Discussion / Decisions / Action items table (owner, due) / Parked items. If the notes lack an owner or due date, write [CHECK].", ['Company minutes template']),
  pr=[pr('main', 'Main: write the minutes', 'Paste your notes and send',
    "Turn the notes below into meeting minutes.\n- Meeting: {{회의명}}\n- Date/time: {{일시}}\n- Attendees: {{참석자}}\n\n"
    "Structure: Overview / Discussion (by topic) / Decisions / Action items table (task, owner, due) / Parked items\nDon't add anything not in the notes; if an owner or due date is missing, mark [CHECK].\n\nNotes:\n{{메모}}",
    v('회의명', 'Meeting', 'November weekly operations meeting'), v('일시', 'Date/time', '2026-11-09 10:00'), v('참석자', 'Attendees', 'Ops manager, Warehouse 1 & 2 leads, HR manager'),
    v('메모', 'Notes', '- Night shift short 2 people → HR posts job this week\n- Year-end volume expected +20%, look at temp staff\n- Safety training in November')),
    V_TEXT,
    pr('mail', 'Email to share it', 'After the minutes are done',
    "Write an email sharing these minutes with attendees. Include the action items table as is and repeat each owner's deadline. To: {{수신}}",
    v('수신', 'To', 'All attendees'))],
  st=[st('Copy your notes', 'As written in the meeting'), st('Send the prompt', 'Fill blanks and paste'),
      st('Check actions', 'Fill owners and dates marked [CHECK]'), st('Review', 'Use the check prompt for made-up content'), st('Share', 'Email prompt to send it')],
  r=['Minutes with decisions and action table\nPlus an email to share them', 'Example: 15 lines of notes\n3 decisions · 5 action items'],
  c=["Check nothing that wasn't said crept in", 'Attendees confirm owners and dates', 'Get consent before using recordings', 'Follow rules for confidential meetings'],
  docs=[D_PROJ])

ITEMS['admin-policy-form'] = dict(
  t='Draft company policies and request forms', s='Enter the purpose and content and get\na sectioned policy and request form',
  tags=['policy', 'handbook', 'form', 'rules', 'request form'],
  tools=[T_CF, T_W], p='Writing one policy starts with hunting for examples', b='Patching together samples from the web', a='A draft built on your company rules, in one go',
  prep=['Policy name and purpose', 'Who it applies to', 'Must-have points', 'Related existing policy (attach)'],
  pr=[pr('main', 'Main: policy & form draft', 'You can attach the existing policy',
    "Draft a {{규정명}} as a Word file.\n- Purpose: {{목적}}\n- Applies to: {{대상}}\n- Must include: {{주요내용}}\n\n"
    "1. Policy in numbered sections (purpose, definitions, scope, procedure, responsibilities, effective date)\n2. A matching request form (table layout, with approval boxes)\n3. Mark sections that need a legal check as [LEGAL CHECK]" + DOC_RULES,
    v('규정명', 'Policy name', 'Remote Work Policy'), v('목적', 'Purpose', 'Set rules for remote work for staff with childcare or long commutes'), v('대상', 'Applies to', 'Full-time office staff'),
    v('주요내용', 'Must include', 'Up to 2 days a week, manager approval, reachable on chat 9–5, data security pledge')),
    V_TEXT,
    pr('compare', 'Compare with the current policy', 'When revising',
    "Compare the attached current policy with the new draft and make a side-by-side table (current / proposed / reason for change). Flag any change that is less favorable to employees.")],
  st=[st('List the content', 'Write the must-have points'), st('Send the prompt', 'Attach the current policy and send'),
      st('Handle [LEGAL CHECK]', 'Review the flagged sections', 'Ask HR or counsel'), st('Comparison table', 'For revisions, compare old and new'),
      st('Gather input', 'Ask affected teams'), st('Approve & announce', 'Use the notices manual')],
  r=['Sectioned policy + request form\nSide-by-side table for revisions', 'Example: remote work policy\n9 sections · 1-page form'],
  c=['Have counsel review before adopting', 'Check state rules on required notices', 'Always review [LEGAL CHECK] sections', 'It is a draft; people make the final review'],
  docs=[D_FILE])

ITEMS['admin-quote-compare'] = dict(
  t='Compare quotes from 3 vendors', s='Upload the quotes and get\na side-by-side table on the same basis',
  tags=['quote', 'quotation', 'vendor', 'bid', 'compare', 'purchasing'],
  tools=[T_CF, T_X], p='Every vendor uses a different quote format', b='Three quotes on the desk, a table by hand', a='Tax and units aligned, plus a recommendation',
  prep=['Vendor quotes (PDF or photo OK)', 'Criteria (price, lead time, service)', 'Quantity and specs needed', 'Check quotes for personal data'],
  pr=[pr('main', 'Main: quote comparison', 'Paste in the chat with the quotes attached',
    "Compare the {{업체수}} attached quotes in an Excel file. The item is {{품목}} and we need {{수량}}.\n"
    "1. 'Comparison' sheet: unit price, quantity, subtotal, tax/fees and total per vendor (on the same tax/fee basis), plus {{비교기준}}\n"
    "2. 'Source check' sheet: each number read from the quotes and where it came from (flag hard-to-read numbers in photos)\n3. 'Recommendation' sheet: the best vendor per criterion and one overall pick, with 3 reasons" + EXCEL_RULES,
    v('업체수', 'Number of vendors', '3'), v('품목', 'Item', 'Office copier lease'), v('수량', 'Quantity', '4 units'), v('비교기준', 'Other criteria', 'Lead time, free service period, payment terms')),
    V_EXCEL,
    pr('ask', 'Questions for vendors', 'When a quote is missing details',
    "From the comparison, pick out items each vendor left out or left vague (tax, installation, delivery, service, etc.) and write a short request email per vendor.")],
  st=[st('Collect quotes', 'PDFs or clear photos'), st('Attach files', 'Turn on file creation and attach'),
      st('Send the prompt', 'Fill blanks and paste'), st('Source check', 'Verify numbers on the source sheet', 'Photos can be misread'),
      st('Recheck', 'Use the check prompt'), st('Report', 'Use the one-page report manual')],
  r=['Excel: Comparison, Source check, Recommendation\nSame tax/fee basis', 'Example: 3 copier vendors\nUp to $2,160 a year apart'],
  c=['Put tax and fees on the same basis', 'Check photo numbers against the original', 'Check units (each, box, month)', 'The buyer makes the final choice'],
  docs=[D_UP, D_FILE])

ITEMS['account-settlement'] = dict(
  t='Match customer statements to deposits', s='Upload statements and bank deposits\nto sort matched, different and unpaid',
  tags=['reconcile', 'reconciliation', 'deposit', 'statement', 'bank', 'month-end'],
  tools=[T_CF, T_X], p='Matching deposits by customer drags out month-end', b='Line by line against the bank statement', a='Matched, different and unpaid in a table',
  prep=['Customer statements (billed)', 'Bank deposit records', 'Delete account numbers', 'Standardize customer names'],
  proj=('Month-end reconciliation', "You help with month-end reconciliation. Match statements and deposits by customer and amount. Put deposits net of fees, combined payments and name mismatches on a 'Needs review' sheet. Put calculated cells in as Excel formulas with a cell note.", ['Customer name map (statement name ↔ payer name)']),
  pr=[pr('main', 'Main: reconcile', 'Paste in the chat with both files attached',
    "Attachment 1 is the {{기간}} customer statements and attachment 2 is deposits for the same period. Customer is in '{{거래처열}}' and amount in '{{금액열}}'.\n"
    "1. 'Matched' sheet: customer and amount agree\n2. 'Different' sheet: paid but a different amount (differences of ${{허용오차}} or less flagged as likely bank fees)\n"
    "3. 'Unpaid' sheet: on statements only\n4. 'Needs review' sheet: deposits from unknown payers, likely combined payments\n5. 'Summary' sheet: billed, received and difference per customer" + EXCEL_RULES,
    v('기간', 'Period', 'October 2026'), v('거래처열', 'Customer column', 'Customer'), v('금액열', 'Amount column', 'Amount billed'), v('허용오차', 'Fee tolerance ($)', '30')),
    V_EXCEL,
    pr('mail', 'Request for clarification', 'For different or unpaid customers',
    "Write a polite email to each customer on the 'Different' and 'Unpaid' sheets. Include billed, received and difference in a table; reply by {{회신기한}}.",
    v('회신기한', 'Reply by', '2026-11-14'))],
  st=[st('Remove personal data', 'Delete account numbers'), st('Standardize names', 'Prepare a name map', 'Payer names often differ'),
      st('Attach files', 'Statements first, then deposits'), st('Send the prompt', 'Fill blanks and paste'),
      st('Fix review items', 'Combined and unknown deposits'), st('Recheck', 'Total billed vs total received'), st('Send requests', 'Email the customers with differences')],
  r=['Excel with 5 sheets\nMatched, Different, Unpaid, Needs review, Summary', 'Example: 64 customers · October\n58 matched · 3 different · 3 unpaid'],
  c=['Delete account numbers before uploading', 'People decide combined payments', 'Compare totals with the bank balance', 'Recheck amounts before emailing'],
  docs=[D_UP, D_FILE, D_PROJ])

ITEMS['account-card-classify'] = dict(
  t='Code company card spending to accounts', s='Upload card transactions and get\naccount codes with reasons',
  tags=['card', 'credit card', 'expense', 'gl code', 'account code', 'coding'],
  tools=[T_CF, T_X], p='Coding hundreds of card charges wears me out', b='Typing a code for each merchant', a='Coded to your chart, only edge cases to check',
  prep=['Card transactions (Excel export)', "Your company's chart of accounts", 'Card numbers: last 4 digits only', "Last month's coding (if any)"],
  proj=('Card expense coding', "You help code company card charges. Use only accounts from the company chart of accounts. Give a reason (merchant, category) for each, and send low-confidence items to 'Needs review'. Don't make tax deductibility calls.", ['Company chart of accounts', "Last month's coding"]),
  pr=[pr('main', 'Main: code to accounts', 'Paste in the chat with the file attached',
    "The attached file is {{기간}} company card transactions. Code them using only these company accounts and make an Excel file.\nAccounts: {{계정목록}}\n\n"
    "1. 'Coded' sheet: original rows + account + reason + confidence (high/medium/low)\n2. 'Summary' sheet: count and total per account\n"
    "3. 'Needs review' sheet: low confidence, possible personal use, receipts needed\nIf it doesn't fit, don't force it; send it to 'Needs review'." + EXCEL_RULES,
    v('기간', 'Period', 'October 2026'), v('계정목록', 'Company accounts', 'Meals, Travel, Client Entertainment, Office Supplies, Vehicle, Phone & Internet, Bank Fees, Books & Training')),
    V_EXCEL,
    pr('rules', "Rules for next month", 'After coding is final',
    "Using the final coding, make a 'merchant keyword → account' rule table. Next month I'll add it to the Project to apply first.")],
  st=[st('Export transactions', 'Download as Excel', 'Last 4 digits only'), st('Prepare accounts', 'Copy your chart of accounts'),
      st('Attach the file', 'Turn on file creation and attach'), st('Send the prompt', 'Fill blanks and paste'),
      st('Fix review items', 'Check receipts and cardholders'), st('Recheck', 'Summary total = card statement'), st('Save rules', 'Add to next month\'s Project')],
  r=['Excel: Coded, Summary, Needs review\nPlus a rule table for next month', 'Example: 412 charges · October\n371 coded · 41 to review'],
  c=['Accounting confirms the final coding', 'Tax treatment is for your accountant', "Don't upload full card numbers", 'Total must match the card statement'],
  docs=[D_UP, D_FILE, D_PROJ])

ITEMS['account-receivable'] = dict(
  t='Receivables aging and payment reminders', s='Upload invoices and payments and get\nAR aging plus reminder emails',
  tags=['receivable', 'ar', 'aging', 'overdue', 'collection', 'reminder'],
  tools=[T_CF, T_X], p="I can't see at a glance who owes what", b='Working out invoices and payments per customer', a='Aging buckets and reminder emails too',
  prep=['Invoice (sales) records', 'Payment records', 'As-of date', 'Delete account numbers'],
  pr=[pr('main', 'Main: AR aging', 'Paste in the chat with both files attached',
    "Attachment 1 is invoices and attachment 2 is payments. Make an AR aging Excel file as of {{기준일}}.\n"
    "1. 'AR' sheet: invoiced, paid and open balance per customer, oldest open invoice date and days outstanding\n"
    "2. 'Aging' sheet: amounts at 0–30 / 31–60 / 61–90 / over 90 days\n3. 'Needs review' sheet: payments that can't be tied to an invoice\nApply payments to the oldest invoices first." + EXCEL_RULES,
    v('기준일', 'As-of date', '2026-10-31')),
    V_EXCEL,
    pr('mail', 'Payment reminder email', 'One per customer',
    "Write a {{단계}} payment reminder to {{거래처}}. Open balance ${{금액}}, invoice date {{청구일}}, please pay by {{기한}}. Polite but clear on dates and amounts, and ask them to tell us if they've already paid.",
    v('거래처', 'Customer', 'Brightline Supply Co.'), v('단계', 'Reminder stage', 'first friendly'), v('금액', 'Open balance ($)', '3,850'), v('청구일', 'Invoice date', '2026-08-31'), v('기한', 'Pay by', '2026-11-20'))],
  st=[st('Prepare data', 'Export invoices and payments'), st('Attach files', 'Invoices first, then payments'),
      st('Send the prompt', 'Fill blanks and paste'), st('Fix review items', 'Untied payments'),
      st('Recheck', 'Total AR = invoiced − paid'), st('Send emails', 'Reminder prompt per customer', 'Recheck amounts first')],
  r=['Excel: AR, Aging, Needs review\nReminder email per customer', 'Example: 40 customers\n2 over 90 days · $12,400'],
  c=['Compare total AR with the ledger', 'Recheck amounts before sending', 'Oldest invoices first is the default', 'Get advice before legal collection'],
  docs=[D_UP, D_FILE])

ITEMS['account-receipt'] = dict(
  t='Receipt photos → expense sheet', s='Upload receipt photos and get\nan expense sheet right away',
  tags=['receipt', 'expense', 'expense report', 'reimbursement'],
  tools=[T_CF, T_X], p='Typing in paper receipts takes longer than it should', b='Typing each receipt by hand', a='Upload photos, get a table',
  prep=['Receipt photos (up to 20 at a time)', 'Shoot in good light, text readable', "Your company's expense categories", 'Keep the paper receipts'],
  pr=[pr('main', 'Main: expense sheet', 'Paste in the chat with the photos attached',
    "Make a {{기간}} expense sheet in Excel for {{사용자}} from the attached receipt photos. Pick categories from: {{항목}}.\n"
    "1. 'Expenses' sheet: photo number, date, merchant, subtotal, tax, total, category\n2. 'Summary' sheet: total per category\n"
    "3. 'Needs review' sheet: numbers that are blurry or cut off, unclear categories\nDon't guess numbers you can't read; leave them blank." + EXCEL_RULES,
    v('기간', 'Period', 'October 2026'), v('사용자', 'Who', 'Sales Team 1'), v('항목', 'Expense categories', 'Meals, Transportation, Parking, Supplies, Other')),
    V_EXCEL],
  st=[st('Take photos', 'One at a time, bright and large', 'Flatten crumpled ones'), st('Attach files', 'Up to 20 per batch'),
      st('Send the prompt', 'Fill blanks and paste'), st('Check the originals', 'Compare every amount with the receipt', 'Photo numbers can be misread'),
      st('Fix review items', 'Fill blanks yourself'), st('Submit', 'Sheet plus original receipts')],
  r=['Excel: Expenses, Summary, Needs review\nTotals by category', 'Example: 18 receipts\nTotal $427.30 · 2 to review'],
  c=['Check every amount against the receipt', 'Type unreadable numbers yourself', 'Keep originals per company policy', 'Cover card numbers when shooting'],
  docs=[D_UP, D_FILE])

ITEMS['report-weekly'] = dict(
  t='Weekly status report template', s="Jot down what you did and get\na weekly report in your company's format",
  tags=['weekly report', 'status report', 'report', 'update', 'monthly report'],
  tools=[T_C], p='Weekly reports keep me late every Friday', b='Digging through a week of email and chat', a='Paste your notes, get the format',
  prep=['Notes on what you did this week', "Next week's plan", 'Issues and requests', "Company's weekly report template"],
  proj=('Weekly report', "You help write weekly reports. Follow the company template in Project knowledge exactly. Use short bullet points and never add results or numbers that aren't in my notes. Structure: This week / Next week / Issues & asks. Put issues needing a decision at the top.", ['Company weekly report template', "Last week's report"]),
  pr=[pr('main', 'Main: weekly report', 'Inside the Project the template applies automatically',
    "Write the weekly report for {{기간}}. Short bullets, nothing that isn't in my notes.\n\nThis week:\n{{한일}}\n\nNext week:\n{{계획}}\n\nIssues & asks:\n{{이슈}}",
    v('기간', 'Period', 'Week 2 of November (11/9–11/13)'), v('한일', 'Done this week', '- Posted night-shift job on Indeed\n- October payroll check completed\n- Safety training set for 11/20'),
    v('계획', 'Next week', '- 3 interviews\n- Review year-end temp staffing contract'), v('이슈', 'Issues & asks', '- Need budget approval for year-end temp staff')),
    V_TEXT,
    pr('monthly', 'Combine into a monthly report', 'At month-end',
    "Combine these {{개수}} weekly reports into a monthly report for {{월}}. Merge repeated items and sort into done / in progress / delayed in a table.\n\n{{주간보고}}",
    v('개수', 'Number of weekly reports', '4'), v('월', 'Month', 'November 2026'), v('주간보고', 'Paste weekly reports', '(paste the 4 weekly reports)'))],
  st=[st('Create a Project', 'Add the template once', 'Free plan: up to 5 projects'), st('Take notes', 'A line each as you go'),
      st('Send the prompt', 'Fill blanks and paste'), st('Review', 'Check nothing was made up'), st('Month-end', 'Combine into a monthly report')],
  r=["Weekly report in your company's format\nCombine into a monthly report later", 'Example: 8 lines of notes\nOne-page weekly report'],
  c=['Check no made-up results slipped in', 'Compare numbers with sources', 'Check rules for confidential content', 'Put decisions needed at the top'],
  docs=[D_PROJ])

ITEMS['report-email'] = dict(
  t='Business emails for any situation', s='Enter the situation and goal and get\nsubject and body in two versions',
  tags=['email', 'mail', 'request', 'decline', 'apology', 'reply', 'decline email', 'apology email'],
  tools=[T_C], p='Decline and apology emails stall at the first line', b='Write, delete, repeat', a='Pick from two tones',
  prep=['Recipient and relationship', 'Purpose (request, decline, apology)', 'Must-include points', 'Tone you want'],
  pr=[pr('main', 'Main: two versions', 'No file needed',
    "Write a business email.\n- To: {{받는사람}}\n- Purpose: {{목적}}\n- Must include: {{내용}}\n- Tone: {{톤}}\n\n"
    "Give subject and body in two versions (a bit softer / a bit firmer). Don't add promises, dates or amounts I didn't give.",
    v('받는사람', 'Recipient & relationship', 'Purchasing manager at a customer (3 years working together)'), v('목적', 'Purpose', 'Decline a price increase request'),
    v('내용', 'Must include', 'Prices frozen this year; can revisit in January; would consider with higher volume'), v('톤', 'Tone', 'Polite but clear')),
    V_TEXT,
    pr('reply', 'Reply to an email', 'Paste the email you received',
    "Write a reply to the email below. My position: '{{입장}}'. Answer everything they asked.\n\nTheir email:\n{{받은메일}}",
    v('입장', 'My position', "We'll send the requested files by 11/14"), v('받은메일', 'Email received', '(paste the email)'))],
  st=[st('Set the goal', 'What this email should get, in a line'), st('Send the prompt', 'Fill blanks and paste'),
      st('Pick a version', 'Choose one of the two'), st('Review', 'Recheck promises, dates, amounts'), st('Send', 'Tweak into your own voice')],
  r=['Subject + body in two versions\nReplies to received emails too', 'Example: declining a price increase\nSofter and firmer versions'],
  c=['Check promises, dates and amounts yourself', "Recheck the recipient's name and title", 'Have sensitive emails reviewed', 'Leave personal data out'],
  docs=[D_PROJ])

ITEMS['report-contract-summary'] = dict(
  t='Contract key points summary', s='Upload a contract and get\nkey terms and questions to ask',
  tags=['contract', 'agreement', 'terms', 'clause', 'summary', 'lease'],
  tools=[T_CF], p="A 30-page contract and I can't tell what matters", b='Reading every page start to finish', a='Key terms and risky clauses first',
  prep=['Contract file (PDF or Word)', 'Which party you are', 'What you most want to know', 'Check rules for confidential contracts'],
  pr=[pr('main', 'Main: contract summary', 'Paste in the chat with the contract attached',
    "Summarize the attached {{계약명}}. We are the {{입장}}.\n"
    "1. Key terms table: term, price & payment, auto-renewal, termination, penalties & damages, confidentiality, governing law & venue (with clause numbers)\n"
    "2. Clauses that may work against us, and why\n3. 5 questions to ask the other side\n4. What I most want to know: {{궁금한점}}\n"
    "Mark anything not in the contract as 'No such clause', and state at the top that this is not legal advice.",
    v('계약명', 'Contract', 'Warehouse lease agreement'), v('입장', 'Our side', 'tenant'), v('궁금한점', 'Main question', 'Cost of early termination')),
    pr('verify', 'Check: compare with the clauses', 'Right after the summary',
    "For each point in your summary, show the clause number and the original sentence side by side in a table. Flag anything summarized differently from the original or without a source.")],
  st=[st('Prepare the contract', 'Original PDF or Word'), st('Attach the file', 'Attach the contract'), st('Send the prompt', 'Fill blanks and paste'),
      st('Compare with clauses', 'Use the check prompt', "Don't trust the summary alone"), st('List questions', 'Send them to the other side'), st('Expert review', 'Lawyer for important contracts')],
  r=['Key terms table with clause numbers\nRisky clauses · 5 questions', 'Example: 28-page lease\n7 key terms · 3 to watch'],
  c=['This is not legal advice', 'Have a lawyer review important contracts', 'Always compare with the original', 'Check rules before uploading confidential contracts'],
  docs=[D_UP])

ITEMS['gsheet-form'] = dict(
  t='Auto-summary sheet for Google Forms', s='As Google Form responses come in\nthe summary sheet updates itself',
  tags=['google forms', 'form', 'survey', 'responses', 'google sheets'],
  tools=[T_G, T_C], p='Copying survey responses to count them every time', b='Download responses and count by hand', a='The summary updates with every response',
  prep=['A Google Form', 'Link responses to a sheet', 'Column names on the responses sheet', 'Consent wording if collecting personal data'],
  pr=[pr('main', 'Main: summary formulas', 'Enter your response column names',
    "Google Form responses collect on the '{{응답시트}}' sheet. Columns: {{열목록}}.\nGive me Google Sheets formulas, with cell positions, for a 'Summary' sheet that shows:\n{{원하는요약}}\n"
    "They must keep working as responses grow, and explain what each formula does in one line.",
    v('응답시트', 'Responses sheet name', 'Form Responses 1'), v('열목록', 'Column names', 'A Timestamp, B Department, C Satisfaction (1–5), D Comments'),
    v('원하는요약', 'Summary you want', 'Responses by department, average satisfaction by department, comments with satisfaction 2 or lower')),
    pr('notify', 'New-response email alert (Apps Script)', 'To hear about responses right away',
    "Write an Apps Script that emails {{받는사람}} the contents of each new Google Form response.\n"
    "1. The code (with plain-English comments)\n2. Setup: from Sheets > Extensions > Apps Script through to the 'On form submit' trigger\n3. What to click on the permission screens\n4. Daily email limits and cautions",
    v('받는사람', 'Alert email address', 'your email address')),
    pr('verify', 'Check: summary numbers', 'After adding the formulas',
    "Show me how to pick one department on my responses sheet and count responses and average satisfaction by hand, so I can compare with the summary formulas.")],
  st=[st('Link responses', 'Form > Responses > Link to Sheets'), st('Check column names', 'Copy the first row of the responses sheet'),
      st('Send the prompt', 'Fill blanks and paste'), st('Add formulas', 'Paste into the Summary sheet'),
      st('Recheck', 'Hand-check one department'), st('Alerts (optional)', 'Use the Apps Script prompt', 'Needs permission approval')],
  r=['A summary sheet that follows responses\nOptional email alert on new responses', 'Example: staff satisfaction survey\nCount and average by department, auto'],
  c=['Add consent wording when collecting personal data', 'Hand-check formula results once', 'Read scripts before granting permission', 'Consumer accounts: 100 recipients/day'],
  docs=[D_FORM, D_TRIG, D_QUOTA])

ITEMS['gsheet-auto-mail'] = dict(
  t='Automatic emails from Google Sheets', s='List recipients in a sheet and\nemails go out at a set time',
  tags=['email', 'automation', 'google sheets', 'apps script', 'scheduled'],
  tools=[T_G, T_C], p='Sending the same notice by hand every week', b='Copy-paste and send one at a time', a='Edit the sheet; mail goes out on schedule',
  prep=['A Google Sheet (recipient and content columns)', "Add a 'Sent' column", 'Test with your own email first', 'Confirm recipients agreed'],
  pr=[pr('main', 'Main: auto-send script', 'Describe your sheet',
    "Write an Apps Script that sends emails automatically from a Google Sheet.\n- Sheet name: {{시트이름}}\n- Columns: {{열목록}}\n- Subject: {{제목}}\n- When to send: {{발송시점}}\n\n"
    "1. Code (plain-English comments): send only rows where 'Sent' is blank, then record the send time\n2. A 'test mode' setting at the top: when on, every email goes only to {{시험메일}}\n"
    "3. Setup: from Extensions > Apps Script through to a time-driven trigger\n4. Permission screens, daily send limits and how to check errors",
    v('시트이름', 'Sheet name', 'Notices'), v('열목록', 'Columns', 'A Name, B Email, C Message, D Sent'),
    v('제목', 'Subject', "[Notice] This week's safety training"), v('발송시점', 'When', 'Every Monday at 9 a.m.'), v('시험메일', 'Your test email', 'your email address')),
    pr('error', 'Fix an error', 'When the execution log shows an error',
    "The Apps Script execution log shows '{{오류}}'. Tell me the cause and give me fixed code.\n{{코드}}",
    v('오류', 'Error message', 'Exception: Service invoked too many times for one day: email.'), v('코드', 'Current code', '(paste the code)')),
    pr('verify', 'Check: before going live', 'Before real sends',
    "Check my code for anything that could send twice to the same person, send for real with test mode off by mistake, or exceed limits.\n(paste the code)")],
  st=[st('Build the sheet', 'Recipient, message and Sent columns'), st('Send the prompt', 'Fill blanks and paste'),
      st('Add the code', 'Extensions > Apps Script'), st('Grant permission', 'Approve with your account', 'Read the warning screen'),
      st('Test send', 'Test mode, your email only', 'Always do this first'), st('Set the trigger', 'Add a time-driven trigger'), st('Go live', 'Turn test mode off')],
  r=['Send script with a test mode\nSetup and trigger steps', 'Example: Mondays 9 a.m.\nSafety notice to 32 people, automatically'],
  c=['Always run in test mode first', 'Consumer accounts: 100 recipients/day', 'Marketing email needs consent', "Always use the 'Sent' column to avoid repeats"],
  docs=[D_QUOTA, D_TRIG])

ITEMS['sales-faq'] = dict(
  t='Customer FAQ and reply templates', s='Collect frequent questions and get\nan FAQ with reply templates',
  tags=['faq', 'customer questions', 'support', 'reply template', 'customer service'],
  tools=[T_C], p='Writing a fresh reply to the same question every time', b='Searching old replies to copy', a='FAQ table and short reply templates',
  prep=['Collected frequent questions', 'Policies (refunds, shipping)', 'Tone you want', 'Remove customer personal data'],
  proj=('Customer replies', "You help answer customer questions. Answer only within the FAQ and company policy in Project knowledge. Never promise anything outside policy (compensation, dates, discounts); write 'We'll confirm and get back to you'. Give a short version (chat) and a formal version (email).", ['FAQ table', 'Refund and shipping policy']),
  pr=[pr('main', 'Main: build the FAQ', 'Paste the questions and send',
    "Build a customer FAQ for a {{업종}}. Our policies:\n{{정책}}\n\n"
    "1. Group similar questions into 10–15 questions\n2. For each, a short answer (2–3 lines for chat) and a formal answer (email)\n3. Put questions policy can't answer in a separate 'Needs a person' list\nTone: {{톤}}\n\nQuestions:\n{{문의}}",
    v('업종', 'Business', 'B2B parcel delivery service'), v('정책', 'Policies', 'Pickup cutoff 5 p.m.; damage claims reviewed within 7 days; returns within 3 days'),
    v('톤', 'Tone', 'Friendly and brief'), v('문의', 'Frequent questions', "- If I ship today, when will it arrive?\n- The box arrived crushed\n- Can I change my pickup time?")),
    V_TEXT,
    pr('answer', 'Draft a reply to a new question', 'After the FAQ is in the Project',
    "Draft short and formal replies to this customer question within the FAQ and policy. If policy doesn't cover it, write 'We'll confirm and get back to you'.\n{{새문의}}",
    v('새문의', 'New question', 'What I shipped yesterday still shows as not picked up'))],
  st=[st('Collect questions', 'Copy 1–2 months of questions', 'Delete names and contacts'), st('Write down policies', 'Refund and shipping rules'),
      st('Send the prompt', 'Fill blanks and paste'), st('Review', 'No answers that contradict policy'), st('Add to Project', 'Put the FAQ in knowledge'), st('Use daily', 'New-question prompt')],
  r=['FAQ table of 10–15 questions\nShort and formal answers', 'Example: 40 questions sorted\n12 FAQs · 3 need a person'],
  c=['No promises outside policy', 'Remove customer data before uploading', 'Refunds and compensation: a person confirms', 'Update the FAQ when policy changes'],
  docs=[D_PROJ])

ITEMS['sales-by-customer'] = dict(
  t='Sales by customer and ranking', s='Upload sales records and see\ncustomer ranking and share at a glance',
  tags=['sales', 'revenue', 'customers', 'ranking', 'top customers', 'analysis'],
  tools=[T_CF, T_X], p="I don't know which customers drive sales", b='Pivot, then sort the ranking separately', a='Ranking, share, change and top 20%',
  prep=['Sales records (customer, amount, date)', 'Previous period for comparison', 'Standardize customer names', 'Delete personal data columns'],
  pr=[pr('main', 'Main: customer analysis', 'Paste in the chat with the file attached',
    "Using the attached {{기간}} sales records, make a customer analysis Excel file. Customer is in '{{거래처열}}' and amount in '{{금액열}}'. Comparison period: {{비교기간}}.\n"
    "1. 'Ranking' sheet: sales, rank, share and cumulative share per customer; mark customers up to 80% cumulative\n2. 'Change' sheet: change and % change vs the comparison period; new and lost customers\n"
    "3. 'Summary' sheet: dependence on top customers and 3 notable changes (with numbers)" + EXCEL_RULES,
    v('기간', 'Period', 'Jan–Oct 2026'), v('거래처열', 'Customer column', 'Customer'), v('금액열', 'Amount column', 'Sales'), v('비교기간', 'Comparison period', 'Jan–Oct 2025')),
    V_EXCEL,
    pr('comment', 'Notes for the sales meeting', 'After the analysis',
    "Using the 'Summary' sheet, write 3 key points for the sales meeting and 3 customers that need attention, with reasons. Use the sheet's numbers exactly.")],
  st=[st('Standardize names', 'Match Inc./spacing in customer names', 'Otherwise counted as separate'), st('Attach the file', 'Turn on file creation and attach'),
      st('Send the prompt', 'Fill blanks and paste'), st('Recheck', 'Total sales = source total'), st('Notes', '3 lines for the sales meeting')],
  r=['Excel: Ranking, Change, Summary\nTop customers to 80% marked', 'Example: 214 customers\nTop 38 make 80% of sales'],
  c=['Standardize customer names first', 'Compare total sales with the source', 'Check whether returns and discounts are included', 'Match notes to sheet numbers'],
  docs=[D_PIV, D_FILE])

ITEMS['logistics-stock'] = dict(
  t='Inventory and in/out reconciliation', s='Upload movements and counts and see\ndifferences and low stock right away',
  tags=['inventory', 'stock', 'stocktake', 'cycle count', 'reorder', 'warehouse'],
  tools=[T_CF, T_X], p="Book stock and actual stock don't match", b='Adding and subtracting movements per item', a='Differences and below-safety-stock, automatically',
  prep=['Opening stock', 'Receipts and shipments', 'Physical count', 'Same item code format everywhere'],
  proj=('Weekly stock reconciliation', "You help reconcile inventory. Book stock = opening + received − shipped; compare with the physical count. Match on item code; put missing or mismatched codes on 'Needs review'. Put calculated cells in as Excel formulas with a cell note.", ['Item master (code, name, unit, safety stock)']),
  pr=[pr('main', 'Main: reconcile stock', 'Paste in the chat with the files attached',
    "Using the attached {{기간}} opening stock, receipts, shipments and physical count files, make an inventory reconciliation Excel file. Match on the '{{품목열}}' column.\n"
    "1. 'Reconcile' sheet: opening, received, shipped, book (opening + received − shipped), counted and difference per item\n2. 'Differences' sheet: items off by more than {{허용차이}}, with value if unit cost is given\n"
    "3. 'Safety stock' sheet: items counted below safety stock {{안전재고}}\n4. 'Needs review' sheet: missing codes, mixed units, shipments greater than stock" + EXCEL_RULES,
    v('기간', 'Period', 'Week 1 of November 2026'), v('품목열', 'Item code column', 'Item code'), v('허용차이', 'Allowed difference', '0 units'), v('안전재고', 'Safety stock basis', '(the Safety stock column in the item master)')),
    V_EXCEL,
    pr('order', 'Reorder list', 'When items are below safety stock',
    "Calculate reorder quantities for items on the 'Safety stock' sheet: average weekly shipments over the last {{주수}} weeks × {{리드타임}} weeks + safety stock − on hand. Show the calculation in the table.",
    v('주수', 'Weeks to average', '4'), v('리드타임', 'Lead time (weeks)', '2'))],
  st=[st('Match codes', 'Same code format in all 4 files'), st('Attach files', 'Opening, received, shipped, count'),
      st('Send the prompt', 'Fill blanks and paste'), st('Fix review items', 'Code and unit issues'),
      st('Check differences', 'Recount big differences', 'Look for missing paperwork first'), st('Recheck', 'Check prompt for total quantities'), st('Reorder', 'Reorder list prompt')],
  r=['Excel: Reconcile, Differences, Safety stock, Needs review\nReorder quantities too', 'Example: 1,180 items\n23 differences · 9 below safety stock'],
  c=['Match item code formats first', 'Mixed units (EA, BOX) cause errors', 'Check for missing paperwork first', 'The buyer decides order quantities'],
  docs=[D_FILE, D_PROJ])

ITEMS['logistics-delivery'] = dict(
  t='Delivery results by region and driver', s='Upload delivery records and get\ntotals and completion by region and driver',
  tags=['delivery', 'shipping', 'driver', 'courier', 'route', 'volume'],
  tools=[T_CF, T_X], p='Hard to see delivery results by region and driver', b='Filter and count one by one', a='Counts, completion and weekday pattern in one go',
  prep=['Delivery records file', 'Check region, driver and status columns', 'Delete driver contact details', 'Standardize status values (delivered, failed)'],
  pr=[pr('main', 'Main: delivery totals', 'Paste in the chat with the file attached',
    "Make a summary Excel file from the attached {{기간}} delivery records. Region is '{{지역열}}', driver '{{기사열}}', status '{{상태열}}', and the delivered status value is '{{완료값}}'.\n"
    "1. 'By region' sheet: total, delivered, not delivered, completion rate and daily average per region\n2. 'By driver' sheet: the same per driver, plus days worked\n"
    "3. 'By weekday' sheet: count per weekday (mark the busiest)\n4. 'Needs review' sheet: blank or odd status values\nThis may be used to evaluate people, so give numbers only; don't interpret route differences." + EXCEL_RULES,
    v('기간', 'Period', 'October 2026'), v('지역열', 'Region column', 'Zone'), v('기사열', 'Driver column', 'Driver ID'), v('상태열', 'Status column', 'Status'), v('완료값', 'Delivered value', 'Delivered')),
    V_EXCEL,
    pr('compare', 'Change vs last month', 'When you have two months',
    "I've also attached last month's file. Add month-over-month change to the 'By region' and 'By weekday' sheets, and list the 3 regions with the biggest rise or fall, with numbers.")],
  st=[st('Remove personal data', 'Driver IDs instead of names'), st('Standardize status', 'One word for delivered'),
      st('Attach the file', 'Turn on file creation and attach'), st('Send the prompt', 'Fill blanks and paste'),
      st('Recheck', 'Total = rows in the source'), st('Use it', 'Plan staffing by weekday volume')],
  r=['Excel: by region, driver and weekday\nCompletion rate and daily average', 'Example: 82,400 deliveries in October\n98.6% delivered · Monday busiest'],
  c=['Use driver IDs, not personal data', "Don't judge people on volume alone", 'Compare totals with the source', 'Standardize status values first'],
  docs=[D_PIV, D_FILE])
