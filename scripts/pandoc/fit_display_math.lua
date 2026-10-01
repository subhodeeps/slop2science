-- Pandoc Lua filter for scripts/report_pdf.sh (LaTeX output only).
--
-- Problem: a Markdown file can have long single-line display equations (several results joined
-- by \quad, long boxed criteria) that are wider than the text block. LaTeX cannot break a
-- display, so the equation overflows the right margin in the PDF.
--
-- Fix, in the pipeline and never in the Markdown (which must stay KaTeX-readable): emit each
-- display as an amsmath equation* whose body is shrunk to the line width only if it is too wide
-- (adjustbox `max width`; narrower displays are untouched). A \tag{...} in the body moves
-- outside the box, so the equation number stays in the margin.

-- A display that is a list of equations joined by \quad / \qquad at brace depth 0 (e.g.
-- "a=...,\quad b=...,\quad c=...") is set as a centred `gathered` stack, one item per line,
-- instead of being shrunk to fit (shrinking a three-equation line made it unreadably small).
-- Only for long bodies with no environment of their own.
local SPLIT_LEN = 110
local LINE_BUDGET = 85

local function split_top_level_quads(body)
  if #body < SPLIT_LEN or body:find("\\begin{") then return nil end
  local pieces, depth, last, i = {}, 0, 1, 1
  while i <= #body do
    local c = body:sub(i, i)
    if c == "{" then depth = depth + 1
    elseif c == "}" then depth = depth - 1
    elseif c == "\\" and depth == 0 then
      local q = body:match("^\\q?quad", i)
      if q and not body:sub(i + #q, i + #q):match("%a") then
        table.insert(pieces, body:sub(last, i - 1))
        last = i + #q
        i = last - 1
      end
    end
    i = i + 1
  end
  if #pieces == 0 then return nil end
  table.insert(pieces, body:sub(last))
  -- pack pieces greedily into lines of at most LINE_BUDGET source characters; never end a
  -- line on a label ("R_{01}:") or a bare \text{...} word, which belong with what follows
  local lines, cur = {}, nil
  for _, p in ipairs(pieces) do
    p = p:gsub("^%s+", ""):gsub("%s+$", "")
    if cur == nil then cur = p
    elseif #cur + #p <= LINE_BUDGET or cur:match(":$") or cur:match("^\\text%b{}$") then
      cur = cur .. "\\quad " .. p
    else
      table.insert(lines, cur); cur = p
    end
  end
  table.insert(lines, cur)
  if #lines == 1 then return nil end
  return "\\begin{gathered}" .. table.concat(lines, "\\\\\n") .. "\\end{gathered}"
end

local function fit(el)
  if el.mathtype ~= "DisplayMath" then return nil end
  local body = el.text
  local tag = nil
  body = body:gsub("\\tag%s*(%b{})", function(t) tag = t; return "" end)
  -- a removed \tag on its own line leaves an empty line, which TeX reads as \par
  body = body:gsub("\n%s*\n", "\n"):gsub("^%s+", ""):gsub("%s+$", "")
  body = split_top_level_quads(body) or body
  -- leave room for the equation number, else a full-width box pushes it onto the next line
  local width = tag and "\\dimexpr\\linewidth-4em\\relax" or "\\linewidth"
  local out = "\\begin{equation*}\\text{\\adjustbox{max width=" .. width
      .. "}{$\\displaystyle " .. body .. "$}}"
  if tag then out = out .. "\\tag" .. tag end
  out = out .. "\\end{equation*}"
  return pandoc.RawInline("latex", out)
end

function Math(el)
  if FORMAT:match("latex") then return fit(el) end
  return nil
end
