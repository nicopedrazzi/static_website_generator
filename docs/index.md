# Markdown Guide for This Site

Welcome to the demo content for the static site generator. Each page is written in Markdown and stored in `docs/`.

## File layout

- Pages live in `docs/<path>/index.md`
- The URL maps to the folder path. Example: `docs/blog/glorfindel/index.md` -> `/blog/glorfindel`
- Every page should start with a single H1 heading (`# Title`)

## Paragraphs and line breaks

Write paragraphs with blank lines between them. Line breaks inside a paragraph are joined.

## Emphasis and inline code

Use **bold**, _italic_, and `inline code`.

## Links and images

[External link](https://www.example.com)
![Example image](/images/tolkien.png)

## Lists

- Unordered list item
- Another item

1. Ordered list item
2. Next item (must be sequential for this generator)

## Quotes

> This is a blockquote.

## Code blocks

```python
print("Hello from a code block")
```

## Starter template

```md
# Page Title

Intro paragraph with **bold** and _italic_ text.

- Bullet
- Bullet

[Link text](https://example.com)
```

## Example pages

- [Example blog post](/blog/glorfindel)
- [Contact page](/contact)
