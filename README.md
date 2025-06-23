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

2. Under the name of Holy Scripture, or the Word of God written, are now contained all the books of the Old and New Testament, which are these:...
```

**Catechism Format:**
```
Q1. What is the chief end of man?
A1. Man's chief end is to glorify God, and to enjoy him for ever.

Q2. What rule hath God given to direct us how we may glorify and enjoy him?
A2. The Word of God, which is contained in the Scriptures of the Old and New Testaments, is the only rule to direct us how we may glorify and enjoy him.
```

**Benefits of Text-Only Access:**
- **Clean content**: Get just the theological content without scripture references
- **Simplified processing**: Easier to work with for text analysis or display
- **Consistent formatting**: Uniform output format across all documents
- **Range support**: Get text-only content for specific ranges or items
- **Memory efficient**: Returns strings instead of complex objects

### Range-Based Search

You can search within specific ranges of questions or chapters, with support for filtering by different parts:

```dart
// Search within a range of Shorter Catechism questions
final godInFirstTen = searchWestminsterShorterCatechismRange(1, 10, 'God');
for (final question in godInFirstTen) {
  print('Q${question.number}: ${question.question}');
}

// Search within a range of Larger Catechism questions
final christInRange = searchWestminsterLargerCatechismRange(25, 100, 'Christ');
for (final question in christInRange) {
  print('Q${question.number}: ${question.question}');
}

// Search within a range of Confession chapters
final salvationInChapters = searchWestminsterConfessionRange(1, 5, 'salvation');
for (final chapter in salvationInChapters) {
  print('Chapter ${chapter.number}: ${chapter.title}');
}

// Search within specific questions by numbers
final specificQuestions = searchWestminsterShorterCatechismByNumbers(
  [1, 3, 5, 7], 'What', CatechismItemPart.question,
);

// Search within specific chapters by numbers
final specificChapters = searchWestminsterConfessionByNumbers(
  [1, 5, 10], 'faith',
);
```

#### Part Filtering for Catechism Questions

You can filter searches to specific parts of catechism questions:

```dart
// Search in questions only
final questionOnly = searchWestminsterShorterCatechismRange(
  1, 10, 'God', CatechismItemPart.question,
);

// Search in answers only
final answerOnly = searchWestminsterShorterCatechismRange(
  1, 10, 'God', CatechismItemPart.answer,
);

// Search in references only
final refsOnly = searchWestminsterShorterCatechismRange(
  1, 20, 'John', CatechismItemPart.references,
);

// Search in questions and answers only
final qaOnly = searchWestminsterShorterCatechismRange(
  1, 15, 'love', CatechismItemPart.questionAndAnswer,
);

// Search in questions and references only
final qrOnly = searchWestminsterShorterCatechismRange(
  1, 15, 'love', CatechismItemPart.questionAndReferences,
);

// Search in answers and references only
final arOnly = searchWestminsterShorterCatechismRange(
  1, 15, 'love', CatechismItemPart.answerAndReferences,
);

// Search in all parts (default)
final allParts = searchWestminsterShorterCatechismRange(1, 10, 'God');
```

#### Content Filtering for Confession Chapters

You can control whether to search in titles, content, or both:

```dart
// Search in titles only
final titlesOnly = searchWestminsterConfessionRange(
  1, 5, 'God', searchInTitle: true, searchInContent: false,
);

// Search in content only
final contentOnly = searchWestminsterConfessionRange(
  1, 5, 'God', searchInTitle: false, searchInContent: true,
);

// Search in both titles and content (default)
final both = searchWestminsterConfessionRange(1, 5, 'God');
```

#### Lazy Loading Range Search

For auto-initialization, use the lazy loading versions:

```dart
// Lazy search within ranges
final lazyRangeSearch = await searchWestminsterShorterCatechismRangeLazy(
  10, 20, 'Christ',
);

// Lazy search within specific numbers
final lazySpecificSearch = await searchWestminsterShorterCatechismByNumbersLazy(
  [1, 3, 5, 7], 'What',
);

// Lazy search in confession chapters
final lazyConfessionSearch = await searchWestminsterConfessionRangeLazy(
  1, 5, 'salvation',
);
```

#### Enhanced Access Range Search

You can also use range search through the enhanced access objects:

```dart
final standards = await WestminsterStandards.create();

// Range search in Shorter Catechism
final rangeSearch = standards.shorterCatechism.searchRange(15, 25, 'sin');

// Range search in Confession
final confessionRangeSearch = standards.confession.searchRange(
  4, 8, 'grace', searchInTitle: true, searchInContent: true,
);

// Search by specific numbers
final specificSearch = standards.shorterCatechism.searchByNumbers(
  [1, 3, 5, 7], 'What', CatechismItemPart.question,
);
```

**Benefits of Range Search:**
- **Targeted searches**: Search only in the content you're interested in
- **Performance**: Faster than searching entire documents
- **Precision**: Filter by specific parts (questions, answers, references, etc.)
- **Flexibility**: Search by ranges or specific numbers
- **Part filtering**: Focus on specific aspects of the content

### Working with Clause-Specific Proof Texts

The proof texts are specifically tied to particular clauses or phrases within the Westminster texts:

```dart
// Example: Working with specific clauses
final confession = await loadWestminsterConfession();
final firstSection = confession.first.sections.first;

for (final clause in firstSection.clauses) {
  print('Clause: "${clause.text}"');
  print('Supported by:');
  for (final proofText in clause.proofTexts) {
    print('  ${proofText.reference}');
  }
  print('');
}

// Get all proof texts for a section (flattened)
final allProofTexts = firstSection.allProofTexts;
```

### Enhanced Access with WestminsterStandards Object

For more advanced access patterns, you can use the `WestminsterStandards` object which provides enhanced search and filtering capabilities:

```dart
import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  // Create Westminster Standards instance
  final standards = await WestminsterStandards.create();

  // Enhanced access to catechisms and confession
  final shorterCatechism = standards.shorterCatechism;
  final largerCatechism = standards.largerCatechism;
  final confession = standards.confession;

  // Search for questions containing specific text
  final godQuestions = standards.shorterCatechism.exactStr('God');
  for (final question in godQuestions) {
    print('Q${question.number}: ${question.question}');
  }

  // Search for confession chapters containing specific text
  final salvationChapters = standards.confession.exactStr('salvation');
  for (final chapter in salvationChapters) {
    print('Chapter ${chapter.number}: ${chapter.title}');
  }

  // Get questions in a range
  final firstTen = standards.shorterCatechism.range(1, 10);

  // Get specific questions by numbers
  final specificQuestions = standards.shorterCatechism.byNumbers([1, 3, 5, 7]);

  // Search questions by question content only
  final whatQuestions = standards.shorterCatechism.questionContains('What');

  // Search questions by answer content only
  final godAnswers = standards.shorterCatechism.answerContains('God');

  // Search confession chapters by title
  final godTitles = standards.confession.titleContains('God');

  // Find sections containing specific text
  final salvationSections = standards.confession.findSections('salvation');

  // Get all proof texts from a catechism
  final allProofTexts = standards.shorterCatechism.allProofTexts;

  // Get all sections from confession
  final allSections = standards.confession.allSections;

  // Index access
  final firstQuestion = standards.shorterCatechism[0];
  final firstChapter = standards.confession[0];
}
```

### Unified Search Across All Standards

The `WestminsterStandards` object provides a powerful unified search method that searches across all documents simultaneously:

```dart
final standards = await WestminsterStandards.create();

// Search across all documents for "God"
final allResults = standards.searchAll('God');
print('Found ${allResults.length} results across all documents');

// Analyze results by document type
for (final result in allResults) {
  print('${result.documentType.name.toUpperCase()} ${result.number}: ${result.title}');
  print('  Match Type: ${result.matchType.name}');
  print('  Proof Texts: ${result.proofTexts.length}');
}
```

#### Search Filtering Options

You can control what content to search in:

```dart
// Search in titles and questions only
final titleResults = standards.searchAll(
  'God',
  searchInTitles: true,
  searchInContent: false,
  searchInReferences: false,
);

// Search in content and answers only
final contentResults = standards.searchAll(
  'salvation',
  searchInTitles: false,
  searchInContent: true,
  searchInReferences: false,
);

// Search in proof text references only
final referenceResults = standards.searchAll(
  'John',
  searchInTitles: false,
  searchInContent: false,
  searchInReferences: true,
);
```

#### Unified Search Result Structure

The `searchAll` method returns `WestminsterSearchResult` objects with consistent structure:

```dart
class WestminsterSearchResult {
  final WestminsterDocumentType documentType; // confession, shorterCatechism, largerCatechism
  final int number; // chapter number or question number
  final String title; // chapter title or question text
  final String content; // chapter content or answer text
  final List<ProofText> proofTexts; // all proof texts for this item
  final String matchedText; // the specific text that matched
  final SearchMatchType matchType; // title, content, question, answer, references
}
```

#### Cross-Document Analysis

Unified search enables powerful cross-document analysis:

```dart
final results = standards.searchAll('faith');

// Group by document type
final byDocument = <WestminsterDocumentType, List<WestminsterSearchResult>>{};
for (final result in results) {
  byDocument.putIfAbsent(result.documentType, () => []).add(result);
}

// Group by match type
final byMatchType = <SearchMatchType, List<WestminsterSearchResult>>{};
for (final result in results) {
  byMatchType.putIfAbsent(result.matchType, () => []).add(result);
}

// Filter and sort
final catechismQuestions = results
    .where((r) => r.documentType != WestminsterDocumentType.confession)
    .where((r) => r.matchType == SearchMatchType.question)
    .toList()
  ..sort((a, b) => a.number.compareTo(b.number));
```

#### Advanced Search Patterns

```dart
// Find questions with multiple proof texts about a topic
final richQuestions = standards.searchAll('justification')
    .where((r) => r.documentType != WestminsterDocumentType.confession)
    .where((r) => r.proofTexts.length >= 3)
    .toList();

// Find Bible references across all documents
final johnReferences = standards.searchAll(
  'John',
  searchInTitles: false,
  searchInContent: false,
  searchInReferences: true,
);

// Statistical analysis
final godResults = standards.searchAll('God');
final docStats = <WestminsterDocumentType, int>{};
for (final result in godResults) {
  docStats[result.documentType] = (docStats[result.documentType] ?? 0) + 1;
}
```

**Benefits of Unified Search:**
- **Cross-document analysis**: Search all standards simultaneously
- **Consistent results**: Unified result structure for all documents
- **Rich metadata**: Know exactly what matched and where
- **Flexible filtering**: Control what content to search in
- **Performance**: Efficient single-method search across all data
- **Analysis ready**: Easy to group, filter, and analyze results

#### Enhanced Access Methods

The enhanced access classes provide the following methods:

**Catechism Class:**
- `exactStr(String searchString)` - Find questions containing the string in question or answer
- `questionContains(String searchString)` - Find questions where the question contains the string
- `answerContains(String searchString)` - Find questions where the answer contains the string
- `startsWith(String searchString)` - Find questions that start with the string
- `endsWith(String searchString)` - Find questions that end with the string
- `range(int start, int end)` - Get questions within a range (inclusive)
- `byNumbers(List<int> numbers)` - Get questions by specific numbers
- `getQuestion(int number)` - Get a specific question by number
- `allProofTexts` - Get all proof texts from all questions

**Confession Class:**
- `exactStr(String searchString)` - Find chapters containing the string in title or content
- `titleContains(String searchString)` - Find chapters where the title contains the string
- `contentContains(String searchString)` - Find chapters where any section contains the string
- `startsWith(String searchString)` - Find chapters that start with the string
- `endsWith(String searchString)` - Find chapters that end with the string
- `range(int start, int end)` - Get chapters within a range (inclusive)
- `byNumbers(List<int> numbers)` - Get chapters by specific numbers
- `getChapter(int number)` - Get a specific chapter by number
- `findSections(String searchString)` - Find sections containing the string
- `allSections` - Get all sections from all chapters
- `allProofTexts` - Get all proof texts from all chapters

**Both Classes:**
- `all` - Get all items as a list
- `firstQuestion`/`firstChapter` - Get the first item
- `lastQuestion`/`lastChapter` - Get the last item
- `length` - Get the total number of items
- `isEmpty`/`isNotEmpty` - Check if empty
- `iterator` - Support for iteration
- `operator []` - Index access

#### Text-Only Access (Excluding Scripture References)

The enhanced access classes and `WestminsterStandards` object provide methods to obtain just the text content without scripture references:

**WestminsterStandards Object:**
```dart
// Full document text-only access
final confessionText = standards.confessionTextOnly;
final shorterCatechismText = standards.shorterCatechismTextOnly;
final largerCatechismText = standards.largerCatechismTextOnly;
final allText = standards.allTextOnly;

// Range-based text-only access
final confessionRangeText = standards.getConfessionRangeTextOnly(1, 3);
final shorterCatechismRangeText = standards.getShorterCatechismRangeTextOnly(1, 10);
final largerCatechismRangeText = standards.getLargerCatechismRangeTextOnly(1, 5);

// Specific numbers text-only access
final confessionSpecificText = standards.getConfessionByNumbersTextOnly([1, 3, 5]);
final shorterCatechismSpecificText = standards.getShorterCatechismByNumbersTextOnly([1, 3, 5]);
final largerCatechismSpecificText = standards.getLargerCatechismByNumbersTextOnly([1, 3, 5]);
```

**Enhanced Access Classes:**
```dart
// Full document text-only access
final confessionText = standards.confession.textOnly;
final shorterCatechismText = standards.shorterCatechism.textOnly;
final largerCatechismText = standards.largerCatechism.textOnly;

// Range-based text-only access
final confessionRangeText = standards.confession.getRangeTextOnly(1, 3);
final shorterCatechismRangeText = standards.shorterCatechism.getRangeTextOnly(1, 10);
final largerCatechismRangeText = standards.largerCatechism.getRangeTextOnly(1, 5);

// Specific numbers text-only access
final confessionSpecificText = standards.confession.getByNumbersTextOnly([1, 3, 5]);
final shorterCatechismSpecificText = standards.shorterCatechism.getByNumbersTextOnly([1, 3, 5]);
final largerCatechismSpecificText = standards.largerCatechism.getByNumbersTextOnly([1, 3, 5]);
```

**Benefits of Text-Only Access:**
- **Clean content**: Get just the doctrinal text without scripture references
- **Consistent formatting**: Uniform text structure across all documents
- **Range flexibility**: Get text for specific chapters or questions
- **Multiple access patterns**: Full documents, ranges, or specific numbers
- **Performance**: Efficient text extraction without processing proof texts
- **Use cases**: Perfect for text analysis, printing, or content extraction

### Backward Compatibility

All existing access methods remain available for backward compatibility:

```dart
// Original methods still work
final confession = getWestminsterConfession();
final shorterCatechism = getWestminsterShorterCatechism();
final largerCatechism = getWestminsterLargerCatechism();

// Enhanced access provides additional functionality
final standards = await WestminsterStandards.create();
final enhancedConfession = standards.confession;
final enhancedShorterCatechism = standards.shorterCatechism;
final enhancedLargerCatechism = standards.largerCatechism;
```

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