---
name: generate-cover-full
description: Generate a 1200x600 combined cover from two 600x600 panels for technical blog posts from article content. The prompt_left should describe the left visual concept panel and prompt_right should describe the right text summary panel. Use when creating or refreshing blog cover art, especially when outputs must be saved under /images/posts and you want the cover generated entirely via ComfyUI (qwen-image model or flux).
---

# Generate Cover Full

## Overview

Generate a blog cover as a combined 1200x600 image composed of two 600x600 panels via ComfyUI (local). The cover should visually present a conceptual illustration on the left and a concise typography-driven summary on the right. Both panels must be generated with a consistent style.

## Workflow

1. Read the target blog post content (Markdown or plain text).
2. Extract: topic, audience level, key technologies, and one strong visual metaphor.
3. Determine a short display title for the cover (aim 2-5 words). If the post title is long or contains punctuation, shorten it for typography reliability and move details into bullets.
3. Build a shared style spec for the entire image:
- define color palette (default: dark navy + cyan neon, with optional magenta accent)
- define illustration mode (flat/vector/isometric/3D)
4. Craft two cohesive prompts: `prompt_left` for the conceptual illustration, and `prompt_right` for an icon‑heavy summary panel (short title + pictorial tiles). Emphasize a unifying dark background for both to ensure they blend seamlessly when stitched.
5. Prefer a single strong focal object on the left, avoid clutter and avoid any text, glyphs, or symbols.

## Image Generation

1. Generate the left panel:
```bash
python .agent/skills/generate-cover-full/references/generate_comfyui.py --prompt "<left_visual_prompt>" --out_path /images/posts/<slug>-left.png
```

2. Generate the right panel:
```bash
python .agent/skills/generate-cover-full/references/generate_comfyui.py --prompt "<right_text_prompt>" --out_path /images/posts/<slug>-right.png
```

## Assembly And Output

1. Combine the panels side-by-side into a single cover using `references/combine_images.py`:
```bash
python .agent/skills/generate-cover-full/references/combine_images.py \
    /images/posts/<slug>-left.png \
    /images/posts/<slug>-right.png \
    /images/posts/<slug>-cover.png
```

## Quality Checklist

1. Confirm the `prompt_left` clearly articulates the visuals and `prompt_right` articulates the typography.
2. Confirm files are written under `/images/posts` with dimensions 1200x600.
3. If text is misspelled or messy, shorten the title further and regenerate the right panel with even less text (title only).
4. If style mismatch appears, re-run both panels with identical palette + lighting terms and an explicit background description.

## Reference

Load [Prompt Templates](references/prompt-templates.md) when crafting generation prompts.
