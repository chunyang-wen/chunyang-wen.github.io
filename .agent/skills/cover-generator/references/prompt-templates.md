# Prompt Templates

Use the same `STYLE_BLOCK` in both left and right prompts.

## STYLE_BLOCK template

```text
Style system: tech-blog illustration.
Palette (default): deep navy (#0A1020), midnight blue (#101A34), neon cyan (#36F3FF), optional magenta accent (#C45BFF).
Rendering: <flat/isometric/3d/semi-flat>.
Icon language: <line weight>, <corner style>, <shadow style>.
Lighting: <soft/medium/high contrast>.
Background: dark navy with subtle circuit-board texture, gradient glow, and soft bloom.
Mood: precise, modern, engineering-focused.
Constraint: keep dark navy/cyan dominant; use magenta sparingly for highlights.
```

## Left prompt template

```text
Create a left-side blog cover panel that visually represents this technical article.
Article title: <title>
Core topic: <topic>
Key concepts: <concept1>, <concept2>, <concept3>
Visual metaphor: <metaphor>
Constraints:
- No long text blocks
- Strong focal point
- Readable at small size

Apply this exact style block:
<STYLE_BLOCK>
```

## Right prompt template

```text
Create a right-side blog cover panel that summarizes this technical article.
Article title: <title>
Audience: <audience>
Summary bullets:
- <bullet1>
- <bullet2>
- <bullet3>
Optional bullet:
- <bullet4>
Constraints:
- Clean typography
- High readability
- Balanced whitespace

Apply this exact style block:
<STYLE_BLOCK>
```

## Regeneration rule

If left and right styles diverge, regenerate both panels using:
1. Same STYLE_BLOCK text
2. Same seed (if tool supports seed)
3. Same rendering model/version
