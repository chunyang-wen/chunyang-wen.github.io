---
name: cover-generator
description: Generate two-panel cover images for technical blog posts from article content, including a left visual concept panel and a right summary panel with matching style. Use when creating or refreshing blog cover art, post icons, or hero images, especially when outputs must be saved under /images/posts and remain visually consistent with a tech-blog aesthetic.
---

# Cover Generator

## Overview

Generate a blog cover as two coordinated images: left for visual storytelling, right for concise summary. Keep both panels in one visual system and export final assets under `/images/posts`.

## Workflow

1. Read the target blog post content (Markdown or plain text).
2. Extract: topic, audience level, key technologies, and one strong visual metaphor.
3. Build a shared style spec before image generation:
- define color palette (default: dark navy + cyan neon, with optional magenta accent)
- define illustration mode (flat/vector/isometric/3D)
- define lighting/contrast level
- define texture/noise level
- define icon style (line thickness, corner roundness)
4. Reuse the exact same style spec in both panel prompts.

## Theme Default

1. Treat dark navy and cyan neon as the baseline visual theme for all covers.
2. Keep the background dark navy with subtle circuit textures, glow lines, or starfield/grid depth.
3. Use cyan glow and electric blue for key focal elements; allow limited magenta as secondary accent.
4. Prefer dark-mode composition unless explicitly requested otherwise.

## Left Panel Rules

1. Generate a visual representation of the blog topic.
2. Prefer concrete technical symbols (chips, code windows, network graphs, terminals, cloud nodes) over generic decoration.
3. Keep composition bold and readable at thumbnail size.
4. Avoid dense text on the left panel; visual message should dominate.

## Right Panel Rules

1. Generate a summary-focused panel based on the same post content.
2. Use short, high-signal text: title + 2-4 concise bullets.
3. Keep typography and spacing clean for readability.
4. Reuse the same palette, icon language, and rendering style as the left panel.

## Assembly And Output

1. Save intermediate images:
- `/images/posts/<slug>-left.png`
- `/images/posts/<slug>-right.png`
2. Combine side-by-side into a single cover:
- `/images/posts/<slug>-cover.png`
3. Keep both panels at equal height and aligned edges.
4. If needed, create a small icon variant in the same style:
- `/images/posts/<slug>-icon.png`

Use [Combine Images](references/combine_images.py) to combine the two images.

```bash

python references/combine_images.py \
    --left_path /images/posts/<slug>-left.png 
    --right_path /images/posts/<slug>-right.png 
    --out_path /images/posts/<slug>-cover.png
```

## Quality Checklist

1. Confirm left and right use the same visual language.
2. Confirm the right summary accurately reflects the post.
3. Confirm contrast is sufficient for mobile thumbnails.
4. Confirm files are written under `/images/posts`.
5. Confirm the final palette is dark navy/cyan dominant with controlled glow.
6. If style mismatch appears, regenerate both panels with a stricter shared style spec.

## Reference

Load [Prompt Templates](references/prompt-templates.md) when crafting generation prompts.
