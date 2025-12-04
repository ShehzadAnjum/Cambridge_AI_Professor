# Research Findings: Advanced PDF Parsing and Question Extraction

## Purpose
This research aims to identify suitable Python libraries for extracting questions and their associated marks from PDF past papers, as required by FR-002 of the Content Generation Engine specification.

## Libraries Considered

### 1. `pdfminer.six`
- **Pros**: Already installed as a dependency for `dynamic_resource_manager`. Good for basic text extraction and layout analysis. Open-source and actively maintained.
- **Cons**: Primarily designed for text extraction; extracting structured information like questions and marks often requires significant post-processing using heuristics and regular expressions. Might struggle with complex layouts or image-based text.
- **Relevance**: Useful as a starting point for raw text, but likely insufficient for robust question/mark extraction directly.

### 2. `PyPDF2` / `pypdf`
- **Pros**: Good for PDF manipulation (splitting, merging, encrypting, extracting pages). Can extract basic text.
- **Cons**: Not designed for advanced layout analysis or structured data extraction. Text extraction capabilities are often simpler than `pdfminer.six`.
- **Relevance**: More for PDF manipulation rather than content parsing.

### 3. `pdfplumber`
- **Pros**: Built on top of `pdfminer.six`, offering a higher-level, more user-friendly API for extracting text, tables, and other data. Excellent for structured data extraction if the PDFs have consistent layouts.
- **Cons**: Still relies on `pdfminer.six`'s underlying text extraction, so might face similar challenges with very complex or image-heavy PDFs.
- **Relevance**: High potential for extracting questions and marks from well-structured past papers if patterns can be identified. Tables extraction is a strong feature.

### 4. `layoutparser` + OCR libraries (e.g., `Tesseract` via `pytesseract`)
- **Pros**: `layoutparser` is a toolkit for deep learning-based document image analysis. It can detect various layout components (text, title, list, figure, table). Combined with OCR, it can handle image-based PDFs.
- **Cons**: Significantly more complex to set up and use. Requires pre-trained models or training custom models for optimal performance. OCR can be error-prone and resource-intensive.
- **Relevance**: Best solution for handling diverse, unstructured, or image-heavy PDF layouts, but involves a steep learning curve and higher computational cost.

## Conclusion & Recommendation

For the initial implementation of `FR-002`, `pdfminer.six` (already available) combined with `pdfplumber` offers the best balance of capability and ease of integration. `pdfplumber`'s structured approach to extracting text and tables, along with its ability to work with coordinates, provides a good foundation for identifying questions and marks, especially if past paper layouts are somewhat consistent.

If `pdfplumber` proves insufficient for robust question/mark extraction due to complex layouts or image-based text, then further research into `layoutparser` and OCR (e.g., `Tesseract`) will be necessary.

**Immediate Next Step**: Focus on using `pdfplumber` to implement initial question extraction logic. If issues arise, document them and revisit this research.
