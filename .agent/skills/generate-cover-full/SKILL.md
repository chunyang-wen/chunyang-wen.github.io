---
name: generate-cover-full
description: Generate a 1200x600 combined cover from two 600x600 panels for technical blog posts with educational, diagram-heavy content. The prompt_left should describe detailed technical diagrams and prompt_right should describe complementary educational breakdowns. Focus on technical accuracy and educational value over marketing aesthetics. Use when creating educational blog cover art that must be saved under /images/posts and generated via ComfyUI (flux model optimized for technical diagrams).
---

# Generate Cover Full

## Overview

Generate a blog cover as a combined 1200x600 image composed of two 600x600 panels via ComfyUI (local). The cover should present educational technical diagrams on the left and detailed concept visualization on the right. Focus on technical accuracy and educational value over marketing aesthetics. Both panels must be generated with a consistent style.

## Workflow

1. Read the target blog post content (Markdown or plain text).
2. Extract: topic, audience level, key technologies, technical concepts, and architectural patterns.
3. Identify 3-4 core technical concepts that can be visualized as diagrams or technical illustrations.
4. Build a shared style spec for the entire image:
- define color palette (default: dark navy + cyan neon, with optional magenta accent)
- define illustration mode (isometric/3D technical diagrams preferred for educational content)
- define technical diagram style (flowcharts, architecture diagrams, data structures, etc.)
5. Craft two educational prompts: `prompt_left` for detailed technical diagrams showing system architecture, data flow, or core concepts, and `prompt_right` for complementary technical visualization with key points or process steps.
6. Focus on technical accuracy and educational value - include multiple related elements, technical symbols, and clear visual relationships between components.

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

1. Confirm the `prompt_left` clearly articulates technical diagrams and `prompt_right` shows complementary educational content.
2. Confirm files are written under `/images/posts` with dimensions 1200x600.
3. Verify both panels contain educational technical content - avoid purely decorative elements.
4. Ensure technical accuracy in diagrams - components should be recognizable and properly connected.
5. If diagrams are unclear or oversimplified, regenerate with more specific technical terminology and architectural details.
6. If style mismatch appears, re-run both panels with identical palette + lighting terms and explicit technical diagram styling.

## Reference

Load [Prompt Templates](references/prompt-templates.md) when crafting generation prompts.
