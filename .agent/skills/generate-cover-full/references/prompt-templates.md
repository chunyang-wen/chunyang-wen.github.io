# Prompt Templates (generate-cover-full)

Use this structure when crafting your dual prompts for `generate_comfyui.py`. The script will generate the left and right panels separately and then combine them side-by-side into a single 1200x600 image. Focus on educational technical content and detailed diagrams. Ensure the style instructions are identical for both to maintain cohesion.

## Left Panel Template (Technical Diagram)

```text
A unified technical blog cover image, left panel. Create a detailed technical diagram showing [SPECIFIC TECHNICAL CONCEPT: e.g. microservices architecture with multiple interconnected services, API gateways, databases, and data flow arrows]. Include multiple related components: servers, databases, network connections, data structures, or system components. Show clear relationships between elements with connecting lines, arrows, or flow indicators. The diagram should be educational and technically accurate.
Overall style: Solid dark navy background covering the entire layout. Cyan and magenta glowing accents, high-contrast, futuristic tech-blog aesthetic. Multiple technical elements with clear visual hierarchy, isometric 3D perspective preferred for depth.
```

## Right Panel Template (Educational Breakdown)

```text
A unified technical blog cover image, right panel. Create a clean educational breakdown showing '[SHORT TITLE]' prominently at the top in large, clear English text. Below, show 3 simple, well-spaced technical diagrams that explain key concepts or process steps. Use plenty of white space between elements for readability. All text must be in English only. Keep the layout clean and uncluttered - avoid overwhelming the viewer with too much information.
Overall style: Solid dark navy background covering the entire layout. Cyan and magenta glowing accents, high-contrast, futuristic tech-blog aesthetic, cohesive design. Ensure the background seamlessly matches the left panel. Emphasize readability and clean spacing.

## Technical Diagram Fallback (When Complexity Is Too High)

```text
A unified technical blog cover image, right panel. Simplified technical breakdown with title '[SHORT TITLE]' in large, clear English text and 2-3 core technical diagrams below. Focus on the most essential concepts with generous white space between elements. Show clear technical relationships with simple connecting elements. All text must be in English only. Prioritize clarity over complexity.
Overall style: Solid dark navy background covering the entire layout. Cyan and magenta glowing accents, high-contrast, futuristic tech-blog aesthetic, cohesive design. Ensure the background seamlessly matches the left panel. Emphasize clean, readable layout.
```

## Language and Layout Guidelines

**CRITICAL REQUIREMENTS:**
- **English Only**: All text, labels, and annotations must be in English to avoid encoding issues
- **Clean Spacing**: Use generous white space between elements to prevent overwhelming layouts
- **Readability First**: Prioritize clear, readable content over complex technical details
- **3-Element Rule**: Limit right panel to 3 main elements maximum for better visual hierarchy

## Example (C++ Data Structures)

**Left Panel (`prompt_left`)**:
```text
A unified technical blog cover image, left panel. Create a detailed technical diagram showing C++ STL container architecture with multiple data structures: stack (LIFO visualization with push/pop arrows), queue (FIFO with enqueue/dequeue flow), and deque (double-ended with bidirectional access). Include memory layout representations, pointer connections, and data flow indicators. Show internal structure with array segments, linked components, and access patterns.
Overall style: Solid dark navy background spanning the entire canvas. Cyan neon grid lines and glowing connection paths, futuristic tech-blog aesthetic, isometric 3D perspective with technical depth.
```

**Right Panel (`prompt_right`)**:
```text
A unified technical blog cover image, right panel. Create an educational breakdown showing 'C++ STL Containers' as the title, followed by detailed technical illustrations: 1) Stack operations diagram with LIFO principle, 2) Queue operations with FIFO flow, 3) Deque bidirectional access patterns, 4) Performance comparison chart or memory layout differences. Include technical annotations and operational arrows.
Overall style: Solid dark navy background spanning the entire canvas. Cyan neon grid lines and glowing connection paths, futuristic tech-blog aesthetic, cohesive design matching the left panel.
```
