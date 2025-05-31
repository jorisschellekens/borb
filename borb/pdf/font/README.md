### PDF Font Types Hierarchy

Understanding the hierarchy of font types in PDFs is crucial for working with text in the `borb` library. This section provides a detailed overview of font classifications, their properties, and how they interact with the PDF rendering process.

### Font Hierarchy Overview

PDFs support a variety of font types, organized into a hierarchy that defines their structure and usage. Below is a visual representation of this hierarchy:

```mermaid
---
title: PDF Font Types Hierarchy
---
classDiagram
    Font <|-- SimpleFont
    Font <|-- CompositeFont

    %% Simple Fonts
    SimpleFont <|-- Type1Font
    SimpleFont <|-- Type3Font
    SimpleFont <|-- TrueTypeFont
    Type1Font <|-- StandardType1Font

    %% Composite Fonts
    CompositeFont <|-- CIDFont
    CIDFont <|-- CIDType0Font
    CIDFont <|-- CIDType2Font

    %% Base Classes and Components
    class Font {
        +Type
        +Subtype
    }
    class SimpleFont {
    }
    class CompositeFont {
        +CMap
        +CIDSystemInfo
    }
    class Type1Font {
        +BaseFont
        +Encoding
        +FirstChar
        +FontDescriptor
        +LastChar
        +Name
        +ToUnicode
        +Widths
    }
    class Type3Font {
        +CharProcs
        +Encoding
        +FirstChar
        +FontBBox
        +FontDescriptor
        +FontMatrix
        +LastChar
        +Resources
        +ToUnicode
        +Widths
    }
    class StandardType1Font {
    }
    class TrueTypeFont {
        +CMap
    }
    class CIDFont {
        +CIDToGIDMap
        +VerticalMetrics (Optional)
    }
    class CIDType0Font {
        +CFF Glyph Data
    }
    class CIDType2Font {
        +TrueType Glyph Data
    }
```

### Key Concepts

- **Simple Fonts**: Represent basic fonts that map characters directly to glyphs. Examples: Type 1, Type 3, and TrueType fonts.

- **Composite Fonts**: Support large character sets and complex mappings. Examples: CIDType0Font and CIDType2Font.

- **Font Properties**: Fonts define various attributes, such as encoding, glyph data, and additional resources for rendering text accurately.

### Operations on Font Objects

Working with fonts in borb involves two primary operations:

- Reading text encoded with a specific font.
- Writing text using the appropriate font type and encoding.

#### Reading Text in a Given Font

When reading text from a PDF, borb decodes content bytes using font-specific properties. The process involves multiple decision points, as outlined below:

```mermaid
flowchart TD
    ContentBytes["Content Bytes"] --> ValueBytes
    ValueBytes["Value Bytes"] --> SimpleFontChoice
    SimpleFontChoice{"Simple Font?"} --> SimpleFontYes
    SimpleFontChoice{"Simple Font?"} --> e00["TODO"]
    
    SimpleFontYes["Yes"] --> TrueTypeFontChoice
    TrueTypeFontChoice{TrueType Font?} --> TrueTypeYes
    TrueTypeFontChoice{TrueType Font?} --> TrueTypeNo
    TrueTypeYes["Yes"] --> e01["Use the CMap"]
    TrueTypeNo["No"] --> Standard14FontChoice
    
    Standard14FontChoice{"Standard 14?"} --> Standard14FontYes
    Standard14FontChoice{"Standard 14?"} --> Standard14FontNo
    
    Standard14FontYes["Yes"] --> e02["Encoding defined"]
    Standard14FontNo["No"] --> ToUnicodeChoice
    
    ToUnicodeChoice{"/ToUnicode?"} --> ToUnicodeYes
    ToUnicodeChoice{"/ToUnicode?"} --> ToUnicodeNo

    ToUnicodeYes["Yes"] --> e03["Use /ToUnicode \n to decode characters"]
    ToUnicodeNo["No"] --> DifferencesChoice
    
    DifferencesChoice{"/Differences?"} --> DifferencesYes
    DifferencesChoice{"/Differences?"} --> DifferencesNo
    
    DifferencesYes["Yes"] --> BaseEncodingChoice
    DifferencesNo["No"] --> EncodingChoice
    
    BaseEncodingChoice{"/Encoding /BaseEncoding?"} --> BaseEncodingYes
    BaseEncodingChoice{"/Encoding /BaseEncoding?"} --> BaseEncodingNo
    
    BaseEncodingYes["Yes"] --> e04["Use /Encoding /BaseEncoding"]
    BaseEncodingNo["No"] --> e05["Use implied \n /Encoding /BaseEncoding"]
    
    EncodingChoice{"/Encoding?"} --> e06["Use /Encoding"]    
    EncodingChoice{"/Encoding?"} --> e07["Use implied \n /Encoding"]
```

### Key Steps in Text Decoding

- **Content Bytes**:  
  Raw data from the PDF’s content stream, typically compressed.

- **Value Bytes**:  
  Content bytes after special characters are unescaped (e.g., `\\(` becomes `(`).

- **Font Decision Points**:  
  - Determine whether the font is a simple or composite font.  
  - Identify the specific type (e.g., TrueType, Standard 14).

- **Encoding Mechanisms**:  
  - `/ToUnicode`: Use a Unicode mapping for character decoding.  
  - `/Differences`: Map specific character codes to glyphs.  
  - `/BaseEncoding`: Specify the base encoding (e.g., StandardEncoding, MacRoman).
