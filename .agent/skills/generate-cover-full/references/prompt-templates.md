# Prompt Templates (generate-cover-full)

Use this structure when crafting your dual prompts for `generate_comfyui.py`. The script will generate the left and right panels separately and then combine them side-by-side into a single 1200x600 image. Ensure the style instructions are identical for both to maintain cohesion.

## Left Panel Template (Visual Concept)

```text
A unified technical blog cover image, left panel. The visual composition features [SINGLE, STRONG VISUAL CONCEPT: e.g. An isometric 3D glowing neon server rack with data streams representing high load]. The artwork should be clean, bold, and uncluttered. Do not include any text, letters, numbers, or symbols on this panel.
Overall style: Solid dark navy background covering the entire layout. Cyan and magenta glowing accents, high-contrast, futuristic tech-blog aesthetic. One clear focal object, minimal secondary elements, cohesive design.
```

## Right Panel Template (Icon‑Heavy Summary)

```text
A unified technical blog cover image, right panel. Create a summary card layout dominated by pictorial icons/tiles. Include a small title text reading EXACTLY '[SHORT TITLE]' at the top. Below, show 3-4 icon tiles/mini diagrams that represent key concepts. No bullet lists, no captions, minimal text.
Overall style: Solid dark navy background covering the entire layout. Cyan and magenta glowing accents, high-contrast, futuristic tech-blog aesthetic, cohesive design. Ensure the background seamlessly matches the left panel.

## Minimal‑Text Fallback (When Text Is Messy)

```text
A unified technical blog cover image, right panel. Icon‑heavy summary panel with title only. Use a small title reading EXACTLY '[SHORT TITLE]' and 3-4 icon tiles below. No bullet text, no captions, no extra words.
Overall style: Solid dark navy background covering the entire layout. Cyan and magenta glowing accents, high-contrast, futuristic tech-blog aesthetic, cohesive design. Ensure the background seamlessly matches the left panel.
```
```

## Example (Software Architecture)

**Left Panel (`prompt_left`)**:
```text
A unified technical blog cover image, left panel. The composition features a bold, high-contrast flat vector illustration of interlocking glowing puzzle pieces and gears, symbolizing microservices Architecture and decoupling. The artwork should be clean and powerful. Do not include any text on this panel.
Overall style: Solid dark navy background spanning the entire canvas. Subtle cyan neon grid lines, futuristic tech-blog aesthetic, cohesive design.
```

**Right Panel (`prompt_right`)**:
```text
A unified technical blog cover image, right panel. The composition features ONLY large, prominent typography reading EXACTLY 'Microservices vs Monoliths'.
Overall style: Solid dark navy background spanning the entire canvas. Subtle cyan neon grid lines, futuristic tech-blog aesthetic, cohesive design.
```
