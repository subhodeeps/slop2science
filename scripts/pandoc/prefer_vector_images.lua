-- Pandoc Lua filter for scripts/report_pdf.sh (LaTeX output only).
--
-- Rule: prefer PDF over PNG over JPG. A Markdown file names the format that its previewer can
-- show. GitHub and VS Code cannot show a PDF in an image tag, so the Markdown names the PNG.
-- LaTeX can set a PDF as a vector graphic. For each image, this filter checks whether the same
-- file exists in a preferred format, and uses it. It keeps the named file as the fallback.
--
--   docs/figures/a.png   with docs/figures/a.pdf present  ->  a.pdf
--   docs/figures/b.png   without b.pdf                    ->  b.png (the fallback)
--   docs/figures/c.jpg   with c.png present               ->  c.png
--
-- The search follows pandoc's --resource-path, as for the image itself. Web addresses are not
-- changed.
local ORDER = { "pdf", "png", "jpg", "jpeg" }
local RANK = { pdf = 1, png = 2, jpg = 3, jpeg = 3 }

local function found(path)
  local dirs = PANDOC_STATE.resource_path
  if not dirs or #dirs == 0 then dirs = { "." } end
  for _, dir in ipairs(dirs) do
    local f = io.open(pandoc.path.join({ dir, path }), "rb")
    if f then f:close(); return true end
  end
  return false
end

function Image(el)
  if not FORMAT:match("latex") or el.src:match("^%a[%w+.-]*://") then return nil end
  local base, ext = el.src:match("^(.*)%.(%w+)$")
  local rank = ext and RANK[ext:lower()]
  if not rank then return nil end
  for _, e in ipairs(ORDER) do
    if RANK[e] < rank and found(base .. "." .. e) then
      el.src = base .. "." .. e
      return el
    end
  end
  return nil
end
