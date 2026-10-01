-- Pandoc Lua filter for scripts/report_pdf.sh (LaTeX output).
--
-- Problem: a table in a Markdown file often cites long inline-code paths (for example
-- `symbolic/<topic>/stage_07_elementary_solutions.wls`) next to short cells. A plain pipe table
-- has no width hints, so pandoc's LaTeX writer gives every column an equal fraction of the line.
-- A `\texttt{}` path longer than its column has no hyphenation point, overflows the column box
-- and collides with the next column.
--
-- Fix, in the pipeline and never in the Markdown: insert a zero-width space (U+200B) after each
-- '/', '_', '|' and ',' inside inline code spans in table cells. Prose has the same problem for
-- long paths, so inline code in prose gets break points too, but only when the span is not
-- short (>= LONG chars): short spans read worse with them.

local ZWSP = "\226\128\139"
local LONG = 14

local function break_code(el)
  if el.text:find(ZWSP, 1, true) then return el end  -- idempotent: tables may revisit
  el.text = el.text:gsub("([/_|,])", "%1" .. ZWSP)
  return el
end

-- Plain text: "`a`/`b`/`c`" (code spans joined by a bare slash) and identifiers such as
-- excluded_region in table cells have no break point either; allow one after '/' in prose
-- and after '/' or '_' in table cells.
function Str(el)
  if el.text:find("/", 1, true) and not el.text:find(ZWSP, 1, true) then
    el.text = el.text:gsub("/", "/" .. ZWSP)
    return el
  end
  return nil
end

local function break_str_in_cell(el)
  if el.text:find(ZWSP, 1, true) then return el end
  el.text = el.text:gsub("([/_])", "%1" .. ZWSP)
  return el
end

function Code(el)
  if #el.text >= LONG then return break_code(el) end
  return nil
end

local function break_cell(cell)
  cell.contents = pandoc.walk_block(pandoc.Div(cell.contents),
    { Code = break_code, Str = break_str_in_cell }).content
  return cell
end

-- Column widths. A pipe table whose rows are longer than pandoc's --columns gets widths from
-- the separator dashes (usually all equal); columns holding long unbreakable content (long numbers
-- in inline math, file paths) then overflow while short columns waste
-- space. When the table's natural width exceeds a line, set each column's width in proportion
-- to its longest cell (capped, with a floor), so wide content gets the room.
local LINE_CHARS = 95
local CAP, FLOOR = 60, 5

local function cell_len(cell)
  return #pandoc.utils.stringify(pandoc.Div(cell.contents))
end

local function fit_widths(tbl)
  local n = #tbl.colspecs
  local maxlen = {}
  for i = 1, n do maxlen[i] = FLOOR end
  local function scan(row)
    for i, cell in ipairs(row.cells) do
      if i <= n then maxlen[i] = math.max(maxlen[i], math.min(cell_len(cell), CAP)) end
    end
  end
  for _, row in ipairs(tbl.head.rows) do scan(row) end
  for _, body in ipairs(tbl.bodies) do for _, row in ipairs(body.body) do scan(row) end end
  local total = 0
  for i = 1, n do total = total + maxlen[i] end
  if total <= LINE_CHARS then return end
  for i = 1, n do tbl.colspecs[i][2] = maxlen[i] / total end
end

function Table(tbl)
  fit_widths(tbl)
  local function fix_row(row)
    for _, cell in ipairs(row.cells) do break_cell(cell) end
    return row
  end
  for _, row in ipairs(tbl.head.rows) do fix_row(row) end
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do fix_row(row) end
  end
  if tbl.foot then for _, row in ipairs(tbl.foot.rows) do fix_row(row) end end
  return tbl
end
