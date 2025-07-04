<!--
This README describes the package. If you publish this package to pub.dev,
this README's contents appear on the landing page for your package.

For information about how to write a good package README, see the guide for
[writing package pages](https://dart.dev/tools/pub/writing-package-pages).

For general information about developing packages, see the Dart guide for
[creating packages](https://dart.dev/guides/libraries/create-packages)
and the Flutter guide for
[developing packages and plugins](https://flutter.dev/to/develop-packages).
-->

# Westminster Standards

A Flutter package providing the Westminster Confession of Faith, Westminster Shorter Catechism, and Westminster Larger Catechism with their proof texts.

## Overview

The Westminster Standards are foundational documents of Reformed theology, produced by the Westminster Assembly (1643-1649) and widely adopted by Presbyterian and Reformed churches worldwide. This package provides access to:

- **Westminster Confession of Faith** (1646) - 33 chapters of systematic theology
- **Westminster Shorter Catechism** (1647) - 107 questions and answers for instruction
- **Westminster Larger Catechism** (1648) - 196 detailed questions and answers

## Features

- Complete text of all three documents with proof texts
- **Clause-specific proof texts** - Each proof text is tied to specific clauses or phrases
- JSON storage for easy data access
- Dart objects for runtime use
- Properly formatted Scripture references
- Historical accuracy and completeness

## Usage

### Getting Started (Quick Start)

Here's the simplest way to get started with the Westminster Standards:

```dart
import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  // Initialize all documents (recommended for most apps)
  await initializeWestminsterStandards();
  
  // Get the first question from the Shorter Catechism
  final question1 = loadWestminsterShorterCatechismQuestion(1);
  if (question1 != null) {
    print('Q${question1.number}. ${question1.question}');
    print('A. ${question1.answer}');
  }
  
  // Get the first chapter from the Confession
  final chapter1 = loadWestminsterConfessionChapter(1);
  if (chapter1 != null) {
    print('Chapter ${chapter1.number}: ${chapter1.title}');
    print('First section: ${chapter1.sections.first.text}');
  }
}
```

**That's it!** This gives you access to all three Westminster documents with their proof texts. The data is cached for optimal performance.

> **📖 See `example/getting_started_example.dart` for a complete working example.**

### Quick Examples

Here are some common use cases:

**Get a specific catechism question:**
```dart
final question = loadWestminsterShorterCatechismQuestion(1);
print('Q1: ${question?.question}');
print('A: ${question?.answer}');
```

**Get a confession chapter:**
```dart
final chapter = loadWestminsterConfessionChapter(1);
print('Chapter ${chapter?.number}: ${chapter?.title}');
```

**Search for content:**
```dart
final standards = await WestminsterStandards.create();
final results = standards.searchAll('grace');
for (final result in results.take(5)) {
  print('${result.documentType} #${result.number}: ${result.title}');
}
```

**Get text without scripture references:**
```dart
final standards = await WestminsterStandards.create();
final textOnly = standards.getShorterCatechismRangeTextOnly(1, 5);
print(textOnly);
```

### Alternative: Using the WestminsterStandards Object

For more convenient access, you can use the `WestminsterStandards` object:

```dart
import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  // Create a WestminsterStandards instance
  final standards = await WestminsterStandards.create();
  
  // Access the first question from each document
  print('Q1: ${standards.shorterCatechism.firstQuestion?.question}');
  print('Chapter 1: ${standards.confession.firstChapter?.title}');
  
  // Get specific questions by number
  final question10 = standards.shorterCatechism.getQuestion(10);
  print('Q10: ${question10?.question}');
}
```

> **📖 See `example/basic_usage_example.dart` for a comprehensive basic usage example.**

### Initialization (Recommended)

For optimal performance, initialize the data once at app startup. You can choose which documents to load:

```dart
import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  // Initialize all documents (default)
  await initializeWestminsterStandards();
  
  // Or initialize specific documents only
  await initializeWestminsterStandards(WestminsterDocument.confession);
  await initializeWestminsterStandards(WestminsterDocument.shorterCatechism);
  await initializeWestminsterStandards(WestminsterDocument.largerCatechism);
  
  // Or initialize multiple documents
  await initializeWestminsterStandards(WestminsterDocument.confession);
  await initializeWestminsterStandards(WestminsterDocument.shorterCatechism);
  
  // Now all subsequent calls will use cached data
  runApp(MyApp());
}
```

You can also check which documents are initialized:

```dart
// Check if all documents are loaded
if (isInitialized) {
  print('All documents loaded');
}

// Check if specific documents are loaded
if (isDocumentInitialized(WestminsterDocument.confession)) {
  print('Confession is loaded');
}
```

### Loading as JSON

```dart
import 'package:westminster_standards/westminster_standards.dart';

// Load the Westminster Confession as JSON
final confessionJson = await loadWestminsterConfessionJson();

// Load the Shorter Catechism as JSON
final shorterCatechismJson = await loadWestminsterShorterCatechismJson();

// Load the Larger Catechism as JSON
final largerCatechismJson = await loadWestminsterLargerCatechismJson();
```

### Loading as Dart Objects

```dart
import 'package:westminster_standards/westminster_standards.dart';

// Load the Westminster Confession as Dart objects (assumes initialization)
final confession = getWestminsterConfession();
for (final chapter in confession) {
  print('Chapter ${chapter.number}: ${chapter.title}');
  for (final section in chapter.sections) {
    print('  Section ${section.number}: ${section.text}');
    for (final clause in section.clauses) {
      print('    Clause: ${clause.text}');
      for (final proofText in clause.proofTexts) {
        print('      ${proofText.reference}: ${proofText.text}');
      }
    }
  }
}

// Load the Shorter Catechism as Dart objects (assumes initialization)
final shorterCatechism = getWestminsterShorterCatechism();
for (final qa in shorterCatechism) {
  print('Q${qa.number}. ${qa.question}');
  print('A. ${qa.answer}');
  for (final clause in qa.clauses) {
    print('  Clause: ${clause.text}');
    for (final proofText in clause.proofTexts) {
      print('    ${proofText.reference}: ${proofText.text}');
    }
  }
}

// Load the Larger Catechism as Dart objects (assumes initialization)
final largerCatechism = getWestminsterLargerCatechism();
// Similar usage to Shorter Catechism
```

**Note:** The original `loadWestminsterConfession()`, `loadWestminsterShorterCatechism()`, and `loadWestminsterLargerCatechism()` functions are still available for backward compatibility, but the new `get*` functions are recommended as they use cached data when available.

### Lazy Loading (Auto-Initialization)

If you prefer functions that automatically initialize data when needed, use the lazy load functions:

```dart
import 'package:westminster_standards/westminster_standards.dart';

// Lazy load the Westminster Confession (auto-initializes if needed)
final confession = await loadWestminsterConfessionLazy();

// Lazy load the Shorter Catechism (auto-initializes if needed)
final shorterCatechism = await loadWestminsterShorterCatechismLazy();

// Lazy load the Larger Catechism (auto-initializes if needed)
final largerCatechism = await loadWestminsterLargerCatechismLazy();
```

### Loading Individual Items

You can also load specific questions or chapters by their number. These functions assume the data has been initialized and use cached data for optimal performance:

```dart
// Load a specific question from the Shorter Catechism
final question1 = loadWestminsterShorterCatechismQuestion(1);
if (question1 != null) {
  print('Q${question1.number}. ${question1.question}');
  print('A. ${question1.answer}');
}

// Load a specific question from the Larger Catechism
final largerQuestion1 = loadWestminsterLargerCatechismQuestion(1);
if (largerQuestion1 != null) {
  print('Q${largerQuestion1.number}. ${largerQuestion1.question}');
  print('A. ${largerQuestion1.answer}');
}

// Load a specific chapter from the Confession
final chapter1 = loadWestminsterConfessionChapter(1);
if (chapter1 != null) {
  print('Chapter ${chapter1.number}: ${chapter1.title}');
  for (final section in chapter1.sections) {
    print('  Section ${section.number}: ${section.text}');
  }
}
```

### Lazy Loading Individual Items

For individual items that auto-initialize when needed:

```dart
// Lazy load a specific question from the Shorter Catechism (auto-initializes if needed)
final question1 = await loadWestminsterShorterCatechismQuestionLazy(1);
if (question1 != null) {
  print('Q${question1.number}. ${question1.question}');
  print('A. ${question1.answer}');
}

// Lazy load a specific question from the Larger Catechism (auto-initializes if needed)
final largerQuestion1 = await loadWestminsterLargerCatechismQuestionLazy(1);
if (largerQuestion1 != null) {
  print('Q${largerQuestion1.number}. ${largerQuestion1.question}');
  print('A. ${largerQuestion1.answer}');
}

// Lazy load a specific chapter from the Confession (auto-initializes if needed)
final chapter1 = await loadWestminsterConfessionChapterLazy(1);
if (chapter1 != null) {
  print('Chapter ${chapter1.number}: ${chapter1.title}');
  for (final section in chapter1.sections) {
    print('  Section ${section.number}: ${section.text}');
  }
}
```

### Range-Based Access

You can get ranges of questions or chapters for efficient access to specific portions of the Westminster Standards:

```dart
// Get a range of Shorter Catechism questions (inclusive)
final questions1to5 = getWestminsterShorterCatechismRange(1, 5);
for (final question in questions1to5) {
  print('Q${question.number}: ${question.question}');
}

// Get a range of Larger Catechism questions (inclusive)
final largerQuestions1to3 = getWestminsterLargerCatechismRange(1, 3);
for (final question in largerQuestions1to3) {
  print('Q${question.number}: ${question.question}');
}

// Get a range of Confession chapters (inclusive)
final chapters1to5 = getWestminsterConfessionRange(1, 5);
for (final chapter in chapters1to5) {
  print('Chapter ${chapter.number}: ${chapter.title}');
}

// Get specific questions by numbers
final specificQuestions = getWestminsterShorterCatechismByNumbers([1, 3, 5, 7]);
for (final question in specificQuestions) {
  print('Q${question.number}: ${question.question}');
}

// Get specific chapters by numbers
final specificChapters = getWestminsterConfessionByNumbers([1, 5, 10]);
for (final chapter in specificChapters) {
  print('Chapter ${chapter.number}: ${chapter.title}');
}
```

### Lazy Loading Ranges

For range access that auto-initializes when needed:

```dart
// Lazy load ranges (auto-initializes if needed)
final lazyQuestions = await loadWestminsterShorterCatechismRangeLazy(10, 15);
final lazyChapters = await loadWestminsterConfessionRangeLazy(1, 3);

// Lazy load specific items by numbers (auto-initializes if needed)
final lazySpecificQuestions = await loadWestminsterShorterCatechismByNumbersLazy([1, 3, 5]);
final lazySpecificChapters = await loadWestminsterConfessionByNumbersLazy([1, 5, 10]);
```

**Benefits of Range Access:**
- **Performance**: Only load the data you need
- **Memory efficiency**: Avoid loading entire documents when you only need a subset
- **Flexibility**: Get any range of questions or chapters
- **Error handling**: Returns empty lists for invalid ranges instead of throwing errors

### Working with Footnotes

The Westminster Catechisms include footnote numbers that link specific parts of answers to their supporting proof texts. The `footnoteNum` field in clauses allows you to identify which parts of answers are supported by which scripture references.

```dart
// Get a catechism question and examine its footnotes
final question1 = loadWestminsterShorterCatechismQuestion(1);
if (question1 != null) {
  print('Q${question1.number}. ${question1.question}');
  print('A. ${question1.answer}');
  
  // Show clauses with their footnote numbers
  for (final clause in question1.clauses) {
    if (clause.footnoteNum != null) {
      print('  Footnote ${clause.footnoteNum}: "${clause.text}"');
      print('    Supported by:');
      for (final proofText in clause.proofTexts) {
        print('      ${proofText.reference}');
      }
    } else {
      print('  No footnote: "${clause.text}"');
    }
  }
}

// Find questions with specific footnote numbers
final standards = await WestminsterStandards.create();
final questionsWithFootnote5 = standards.shorterCatechism.all
    .where((q) => q.clauses.any((c) => c.footnoteNum == 5))
    .toList();

// Get statistics about footnotes
int totalClausesWithFootnotes = 0;
Set<int> allFootnoteNumbers = {};

for (final question in standards.shorterCatechism.all) {
  for (final clause in question.clauses) {
    if (clause.footnoteNum != null) {
      totalClausesWithFootnotes++;
      allFootnoteNumbers.add(clause.footnoteNum!);
    }
  }
}

print('Total clauses with footnotes: $totalClausesWithFootnotes');
print('Unique footnote numbers: ${allFootnoteNumbers.length}');
```

> **📖 See `example/footnote_example.dart` for a comprehensive demonstration of footnote functionality.**

### Text-Only Access (Excluding Scripture References)

For cases where you need just the text content without scripture references, the package provides text-only access functions:

```dart
// Get full text content of documents (excluding scripture references)
final confessionText = getWestminsterConfessionTextOnly();
final shorterCatechismText = getWestminsterShorterCatechismTextOnly();
final largerCatechismText = getWestminsterLargerCatechismTextOnly();

// Get text content of specific ranges (excluding scripture references)
final confessionRangeText = getWestminsterConfessionRangeTextOnly(1, 3);
final shorterCatechismRangeText = getWestminsterShorterCatechismRangeTextOnly(1, 5);
final largerCatechismRangeText = getWestminsterLargerCatechismRangeTextOnly(1, 3);

// Get text content of specific items by numbers (excluding scripture references)
final confessionSpecificText = getWestminsterConfessionByNumbersTextOnly([1, 3, 5]);
final shorterCatechismSpecificText = getWestminsterShorterCatechismByNumbersTextOnly([1, 3, 5]);
final largerCatechismSpecificText = getWestminsterLargerCatechismByNumbersTextOnly([1, 3, 5]);
```

#### Lazy Loading Text-Only Access

For auto-initialization, use the lazy loading versions:

```dart
// Lazy load full text content (auto-initializes if needed)
final lazyConfessionText = await loadWestminsterConfessionTextOnlyLazy();
final lazyShorterCatechismText = await loadWestminsterShorterCatechismTextOnlyLazy();
final lazyLargerCatechismText = await loadWestminsterLargerCatechismTextOnlyLazy();

// Lazy load text content of ranges (auto-initializes if needed)
final lazyConfessionRangeText = await loadWestminsterConfessionRangeTextOnlyLazy(1, 3);
final lazyShorterCatechismRangeText = await loadWestminsterShorterCatechismRangeTextOnlyLazy(1, 5);
final lazyLargerCatechismRangeText = await loadWestminsterLargerCatechismRangeTextOnlyLazy(1, 3);

// Lazy load text content of specific items (auto-initializes if needed)
final lazyConfessionSpecificText = await loadWestminsterConfessionByNumbersTextOnlyLazy([1, 3, 5]);
final lazyShorterCatechismSpecificText = await loadWestminsterShorterCatechismByNumbersTextOnlyLazy([1, 3, 5]);
final lazyLargerCatechismSpecificText = await loadWestminsterLargerCatechismByNumbersTextOnlyLazy([1, 3, 5]);
```

#### Text-Only Output Format

The text-only functions return formatted strings:

**Confession Format:**
```
Chapter 1. Of the Holy Scripture

1. Although the light of nature, and the works of creation and providence do so far manifest the goodness, wisdom, and power of God, as to leave men unexcusable; yet are they not sufficient to give that knowledge of God, and of his will, which is necessary unto salvation.

2. Therefore it pleased the Lord, at sundry times, and in divers manners, to reveal himself, and to declare that his will unto his church; and afterwards, for the better preserving and propagating of the truth, and for the more sure establishment and comfort of the church against the corruption of the flesh, and the malice of Satan and of the world, to commit the same wholly unto writing; which maketh the Holy Scripture to be most necessary; those former ways of God's revealing his will unto his people being now ceased.
```

**Catechism Format:**
```
Q1. What is the chief end of man?

A. Man's chief end is to glorify God, and to enjoy him for ever.

Q2. What rule hath God given to direct us how we may glorify and enjoy him?

A. The Word of God, which is contained in the Scriptures of the Old and New Testaments, is the only rule to direct us how we may glorify and enjoy him.
```

### Extensions: Fluent API

The package includes powerful Dart extensions that provide a more intuitive and fluent API for working with Westminster Standards data. These extensions make the code more readable and reduce boilerplate.

#### Collection Extensions

Extensions on collections provide convenient methods for finding, filtering, and processing Westminster Standards items:

```dart
import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  final standards = await WestminsterStandards.create();
  
  // Find specific questions by number
  final question1 = standards.shorterCatechismList.findByNumber(1);
  final question10 = standards.shorterCatechismList.findByNumber(10);
  
  // Get ranges of questions
  final questions1to5 = standards.shorterCatechismList.getRange(1, 5);
  final chapters1to3 = standards.confessionList.getRange(1, 3);
  
  // Get specific items by numbers
  final specificQuestions = standards.shorterCatechismList.getByNumbers([1, 5, 10, 15]);
  final specificChapters = standards.confessionList.getByNumbers([1, 5, 10]);
  
  // Search within collections
  final godQuestions = standards.shorterCatechismList.search('God');
  final graceChapters = standards.confessionList.search('grace');
  
  // Search in specific parts
  final questionMatches = standards.shorterCatechismList
      .searchInParts('God', CatechismItemPart.question);
  final answerMatches = standards.shorterCatechismList
      .searchInParts('God', CatechismItemPart.answer);
  
  // Get all proof texts from a collection
  final allProofTexts = standards.shorterCatechismList.getAllProofTexts();
  
  // Get text-only content
  final textOnly = standards.shorterCatechismList.textOnly;
  final rangeTextOnly = standards.shorterCatechismList.getRangeTextOnly(1, 5);
}
```

#### String Extensions

Extensions on strings provide text processing capabilities:

```dart
// Remove scripture references from text
final cleanText = originalText.withoutScriptureReferences;

// Extract scripture references
final references = text.scriptureReferences; // Returns ['Gen 1:1', 'John 3:16']

// Highlight search terms
final highlighted = text.highlightSearchTerm('God'); // Returns text with **God** highlighted

// Get text summary
final summary = text.summary; // First 100 characters

// Count words
final wordCount = text.wordCount;

// Check for scripture references
final hasRefs = text.hasScriptureReferences;

// Normalize whitespace
final normalized = text.normalized;

// Split into sentences
final sentences = text.sentences;
final firstSentence = text.firstSentence;
```

#### Number Extensions

Extensions on integers provide validation and formatting for Westminster Standards numbers:

```dart
// Validate numbers
final isValid = 1.isValidShorterCatechismNumber; // true
final isValidChapter = 33.isValidConfessionChapterNumber; // true

// Format numbers
final formatted = 1.asQuestionNumber; // "Q1"
final chapterFormatted = 1.asChapterNumber; // "Chapter 1"

// Get document information
final docType = 1.documentType; // "Shorter Catechism"
final totalCount = 1.totalCount; // 107

// Navigation
final isFirst = 1.isFirst; // true
final isLast = 107.isLast; // true
final next = 1.next; // 2
final previous = 2.previous; // 1

// Get ranges
final range = 1.rangeTo(5); // [1, 2, 3, 4, 5]
```

#### Model Extensions

Extensions on Westminster Standards models provide enhanced access:

```dart
// CatechismItem extensions
final question = standards.shorterCatechismList.first;
print(question.displayString); // "Q1: What is the chief end of man?"
print(question.fullText); // Question + answer
print(question.textOnly); // Text without scripture references
print(question.summary); // First sentence of answer
print(question.contains('God')); // true/false
print(question.proofTextCount); // Number of proof texts
print(question.uniqueReferences); // List of unique scripture references
print(question.proofTextsByReference); // Map of proof texts grouped by reference

// ConfessionChapter extensions
final chapter = standards.confessionList.first;
print(chapter.displayString); // "Chapter 1: Of the Holy Scripture"
print(chapter.sectionCount); // Number of sections
print(chapter.totalWordCount); // Total words in chapter
print(chapter.averageWordsPerSection); // Average words per section
print(chapter.contains('God')); // true/false
print(chapter.summary); // First sentence of first section
```

#### Search Extensions

Extensions on search results provide enhanced search functionality:

```dart
// Enhanced search results
final results = standards.searchAll('God').sortedByRelevance;

// Get search summary
print(results.searchSummary); // "Found 45 results (confession: 20, shorterCatechism: 15, largerCatechism: 10) - Match types: title: 5, content: 25, question: 10, answer: 5"

// Group results
final byDocument = results.groupedByDocument;
final byMatchType = results.groupedByMatchType;

// Filter results
final confessionResults = results.fromDocument(WestminsterDocumentType.confession);
final titleMatches = results.withMatchType(SearchMatchType.title);
final withProofTexts = results.withProofTexts;

// Get unique types
final docTypes = results.uniqueDocumentTypes;
final matchTypes = results.uniqueMatchTypes;

// Format results with highlighting
final formatted = results.getFormattedWithHighlight('God');
```

#### Async Extensions

Extensions on futures provide better error handling and async operations:

```dart
// Error handling
final standards = await WestminsterStandards.create()
    .withErrorHandling()
    .withTimeout(const Duration(seconds: 5))
    .withRetry(maxRetries: 3)
    .withProgress((message) => print('Progress: $message'));

// Handle null results
final question = await loadWestminsterShorterCatechismQuestionLazy(1)
    .withDefault(defaultQuestion)
    .orThrow('Question not found')
    .orElse(() => loadWestminsterShorterCatechismQuestionLazy(2));

// Async list operations
final questions = Future.value(standards.shorterCatechismList);
final filtered = await questions.whereAsync((q) => q.number <= 5);
final mapped = await questions.mapAsync((q) => q.displayString);
final first = await questions.firstOrNull;
final length = await questions.length;
```

#### Fluent API Examples

The extensions enable a fluent, chainable API:

```dart
// Find questions about God, take first 3, get their summaries
final godQuestions = standards.shorterCatechismList
    .search('God')
    .take(3)
    .map((q) => q.summary);

// Get proof texts from first 5 questions, group by reference
final proofTexts = standards.shorterCatechismList
    .getRange(1, 5)
    .getAllProofTexts()
    .groupedByReference;

// Search in specific parts and get formatted results
final results = standards.shorterCatechismList
    .searchInParts('God', CatechismItemPart.question)
    .map((q) => q.getFormattedWithHighlight('God'));

// Validate and format numbers
final validNumbers = [1, 5, 10, 15]
    .where((n) => n.isValidShorterCatechismNumber)
    .map((n) => n.asQuestionNumber);
```

> **📖 See `example/extensions_example.dart` for a comprehensive demonstration of all extension features.**

The extensions provide a much more intuitive and readable API while maintaining full backward compatibility with the existing functions.

## Data Models

### ConfessionChapter
- `number`: Chapter number
- `title`: Chapter title
- `sections`: List of ConfessionSection objects

### ConfessionSection
- `number`: Section number
- `text`: Section text
- `clauses`: List of Clause objects with specific proof texts
- `allProofTexts`: Getter that returns all proof texts (flattened)

### CatechismItem
- `number`: Question number
- `question`: Question text
- `answer`: Answer text
- `clauses`: List of Clause objects with specific proof texts
- `allProofTexts`: Getter that returns all proof texts (flattened)

### Clause
- `text`: The specific clause or phrase
- `proofTexts`: List of ProofText objects that support this clause
- `footnoteNum`: Footnote number (int?) - identifies which part of the answer this clause supports (catechisms only)

### ProofText
- `reference`: Scripture reference (e.g., "John 3:16")
- `text`: Scripture text

## JSON Structure

The JSON files are structured to show which specific clauses each proof text supports:

```json
{
  "sections": [
    {
      "number": 1,
      "text": "Full section text...",
      "clauses": [
        {
          "text": "Specific clause or phrase",
          "proofTexts": [
            {
              "reference": "John 3:16",
              "text": "For God so loved the world..."
            }
          ]
        }
      ]
    }
  ]
}
```

## Installation

Add this to your package's `pubspec.yaml` file:

```yaml
dependencies:
  westminster_standards: ^0.0.1
```

## License

This package is provided under the same license as the Westminster Standards themselves, which are in the public domain.

## Contributing

Contributions are welcome! Please ensure that any additions or modifications maintain the historical accuracy and theological integrity of the Westminster Standards.