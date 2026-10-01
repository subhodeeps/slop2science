-- Pandoc Lua filter for scripts/report_pdf.sh (LaTeX output only).
--
-- Problem: a README often centres its figures with raw HTML, for example
--   <p align="center"><img src="docs/figures/a.png" width="49%" alt="..."></p>
-- pandoc passes raw HTML through only to HTML output. For LaTeX it drops the tags, and each
-- figure silently disappears from the PDF.
--
-- Fix, in the pipeline and never in the Markdown: turn each <img> into a pandoc Image, with
-- its src, width (a percentage becomes a fraction of the line) and alt text. Turn <p
-- align="center"> and </p> into a centred block. Drop other layout-only tags (<div>, <br>,
-- <picture>, <source>) and keep their content.

local function attrs(tag)
  local a = {}
  for k, v in tag:gmatch('([%w%-]+)%s*=%s*"([^"]*)"') do a[k:lower()] = v end
  return a
end

local function image_from(tag)
  local a = attrs(tag)
  if not a.src then return nil end
  local kv = {}
  if a.width then table.insert(kv, { "width", a.width }) end
  if a.height then table.insert(kv, { "height", a.height }) end
  local alt = a.alt and { pandoc.Str(a.alt) } or {}
  return pandoc.Image(alt, a.src, "", pandoc.Attr("", {}, kv))
end

function RawInline(el)
  if el.format ~= "html" then return nil end
  if el.text:match("^<img[%s/>]") then return image_from(el.text) end
  if el.text:match("^</?br") then return pandoc.LineBreak() end
  if el.text:match("^</?[%w]+") then return {} end        -- any other tag: keep the content
  return nil
end

function RawBlock(el)
  if el.format ~= "html" then return nil end
  local text = el.text
  local low = text:lower()
  local opens = low:match("^%s*<p[%s>]") or low:match("^%s*<div[%s>]")
  local centred = opens and low:find('align%s*=%s*"center"')
  local out = {}
  -- A CommonMark HTML block runs to the next blank line, so it can hold the open tag, the
  -- images and the close tag together, or only one of them. Handle each case.
  local images = {}
  for tag in text:gmatch("<img[^>]*>") do
    local img = image_from(tag)
    if img then table.insert(images, img); table.insert(images, pandoc.Space()) end
  end
  local rest = text:gsub("<img[^>]*>", ""):gsub("<!%-%-.-%-%->", ""):gsub("<[^>]*>", "")
  rest = rest:gsub("^%s+", ""):gsub("%s+$", "")
  if centred then table.insert(out, pandoc.RawBlock("latex", "\\begin{center}")) end
  if #images > 0 then table.insert(out, pandoc.Para(images)) end
  if rest ~= "" then table.insert(out, pandoc.Para({ pandoc.Str(rest) })) end
  local closes = low:match("</p>%s*$") or low:match("</div>%s*$")
  if closes and (centred or low:match("^%s*</")) then
    table.insert(out, pandoc.RawBlock("latex", "\\end{center}"))
  end
  return out
end
