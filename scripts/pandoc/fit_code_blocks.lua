-- Pandoc Lua filter for scripts/report_pdf.sh (LaTeX output only).
--
-- Problem: a fenced code block with long lines (a directory listing in two columns, a long
-- command) wraps with a continuation arrow when it is wider than the text block. The wrap
-- breaks the alignment of a listing.
--
-- Fix, in the pipeline and never in the Markdown: set a block in the largest font size at which
-- its longest line still fits. Blocks that fit at the body size are not changed. A block that
-- is wider than the smallest size wraps (report_header.tex sets breaklines).
--
-- The capacities are for a 6.5 in text block and a 11 pt body with DejaVu Sans Mono at scale
-- 0.85 (0.51 em per character), as report_pdf.sh sets them.
local SIZES = {
  { 83, nil },                  -- \normalsize
  { 91, "\\small" },
  { 102, "\\footnotesize" },
  { 114, "\\scriptsize" },
}

function CodeBlock(el)
  local longest = 0
  for line in (el.text .. "\n"):gmatch("([^\n]*)\n") do
    longest = math.max(longest, utf8.len(line) or #line)
  end
  local size = SIZES[#SIZES][2]
  for _, s in ipairs(SIZES) do
    if longest <= s[1] then size = s[2]; break end
  end
  if not size then return nil end
  return { pandoc.RawBlock("latex", "\\begingroup" .. size), el,
           pandoc.RawBlock("latex", "\\endgroup") }
end
