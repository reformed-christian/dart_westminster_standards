import 'package:flutter/material.dart';
import 'package:westminster_standards/westminster_standards.dart';

/// Extensions Example for Westminster Standards
/// This example demonstrates the new extension methods that provide
/// a more fluent and intuitive API for working with Westminster Standards
void main() async {
  // Initialize Flutter
  WidgetsFlutterBinding.ensureInitialized();

  print('=== Westminster Standards Extensions Example ===\n');

  // Load Westminster Standards with error handling
  final standards = await WestminsterStandards.create()
      .withErrorHandling()
      .withProgress((message) => print('Progress: $message'));

  print('1. COLLECTION EXTENSIONS:');
  print('========================');

  // Using collection extensions for more intuitive access
  print('Finding specific questions:');
  final question1 = standards.shorterCatechismList.findByNumber(1);
  final question10 = standards.shorterCatechismList.findByNumber(10);

  if (question1 != null) {
    print('  Q1: ${question1.displayString}');
    print('  Summary: ${question1.summary}');
    print('  Word count: ${question1.totalWordCount} words');
  }

  print('\nGetting ranges:');
  final questions1to5 = standards.shorterCatechismList.getRange(1, 5);
  print('  Questions 1-5: ${questions1to5.length} questions');
  for (final q in questions1to5) {
    print('    ${q.displayString}');
  }

  print('\nGetting specific numbers:');
  final specificQuestions = standards.shorterCatechismList.getByNumbers([
    1,
    5,
    10,
    15,
  ]);
  print(
    '  Specific questions: ${specificQuestions.map((q) => q.number).toList()}',
  );

  print('\n2. STRING EXTENSIONS:');
  print('====================');

  if (question1 != null) {
    print('Text processing:');
    print('  Original answer: ${question1.answer}');
    print(
      '  Without scripture references: ${question1.answer.withoutScriptureReferences}',
    );
    print('  Scripture references: ${question1.answer.scriptureReferences}');
    print('  Word count: ${question1.answer.wordCount}');
    print(
      '  Has scripture references: ${question1.answer.hasScriptureReferences}',
    );
    print('  Summary: ${question1.answer.summary}');

    // Highlight search terms
    final highlighted = question1.answer.highlightSearchTerm('God');
    print('  Highlighted "God": $highlighted');
  }

  print('\n3. NUMBER EXTENSIONS:');
  print('====================');

  // Using number extensions for validation and formatting
  final testNumbers = [1, 10, 50, 107, 108, 200];

  for (final num in testNumbers) {
    print('  $num:');
    print('    Valid Shorter Catechism: ${num.isValidShorterCatechismNumber}');
    print('    Valid Larger Catechism: ${num.isValidLargerCatechismNumber}');
    print('    Valid Confession: ${num.isValidConfessionChapterNumber}');
    print('    Document type: ${num.documentType}');
    print('    Formatted: ${num.asQuestionNumber}');
    print('    Is first: ${num.isFirst}, Is last: ${num.isLast}');
    if (num.next != null) print('    Next: ${num.next}');
    if (num.previous != null) print('    Previous: ${num.previous}');
  }

  print('\n4. MODEL EXTENSIONS:');
  print('===================');

  if (question1 != null) {
    print('Enhanced CatechismItem access:');
    print('  Display string: ${question1.displayString}');
    print('  Full text: ${question1.fullText.summary}');
    print('  Text only: ${question1.textOnly.summary}');
    print('  Contains "God": ${question1.contains("God")}');
    print('  Proof text count: ${question1.proofTextCount}');
    print('  Has proof texts: ${question1.hasProofTexts}');
    print('  Unique references: ${question1.uniqueReferences}');

    // Get proof texts grouped by reference
    final grouped = question1.proofTextsByReference;
    print('  Proof texts by reference:');
    for (final entry in grouped.entries) {
      print('    ${entry.key}: ${entry.value.length} texts');
    }
  }

  // Confession chapter extensions
  final chapter1 = standards.confessionList.findByNumber(1);
  if (chapter1 != null) {
    print('\nEnhanced ConfessionChapter access:');
    print('  Display string: ${chapter1.displayString}');
    print('  Section count: ${chapter1.sectionCount}');
    print('  Total word count: ${chapter1.totalWordCount}');
    print(
      '  Average words per section: ${chapter1.averageWordsPerSection.toStringAsFixed(1)}',
    );
    print('  Contains "God": ${chapter1.contains("God")}');
    print('  Summary: ${chapter1.summary}');
  }

  print('\n5. SEARCH EXTENSIONS:');
  print('====================');

  // Using enhanced search functionality
  final searchResults = standards.searchAll('God').sortedByRelevance;
  print('Search results for "God" (sorted by relevance):');
  print('  Total results: ${searchResults.length}');
  print('  Search summary: ${searchResults.searchSummary}');

  // Group by document type
  final byDocument = searchResults.groupedByDocument;
  for (final entry in byDocument.entries) {
    print('  ${entry.key.name}: ${entry.value.length} results');
  }

  // Group by match type
  final byMatchType = searchResults.groupedByMatchType;
  for (final entry in byMatchType.entries) {
    print('  ${entry.key.name}: ${entry.value.length} results');
  }

  // Show top 3 results
  print('\nTop 3 results:');
  for (int i = 0; i < 3 && i < searchResults.length; i++) {
    final result = searchResults[i];
    print('  ${i + 1}. ${result.displayString}');
    print(
      '     Relevance: ${(result.relevanceScore * 100).toStringAsFixed(0)}%',
    );
    print('     Content summary: ${result.contentSummary}');
  }

  print('\n6. ASYNC EXTENSIONS:');
  print('===================');

  // Using async extensions for better error handling
  try {
    final standardsWithTimeout = await WestminsterStandards.create()
        .withTimeout(const Duration(seconds: 5))
        .withRetry(maxRetries: 2);

    print('Successfully loaded with timeout and retry');

    // Using async list extensions
    final questions = standardsWithTimeout.shorterCatechismList;
    final asyncQuestions = Future.value(questions);

    final filtered = await asyncQuestions.whereAsync((q) => q.number <= 5);
    print('  Questions 1-5 (async): ${filtered.length}');

    final mapped = await asyncQuestions.mapAsync((q) => q.displayString);
    print('  Display strings (async): ${mapped.take(3).toList()}');

    final first = await asyncQuestions.firstOrNull;
    print('  First question: ${first?.displayString}');

    final length = await asyncQuestions.length;
    print('  Total questions: $length');
  } catch (e) {
    print('  Error with async extensions: $e');
  }

  print('\n7. FLUENT API EXAMPLES:');
  print('=======================');

  // Demonstrating the fluent API made possible by extensions
  print('Chaining operations:');

  // Find questions containing "God", take first 3, get their summaries
  final godQuestions = standards.shorterCatechismList
      .search('God')
      .take(3)
      .map((q) => q.summary);

  print('  Questions about God:');
  for (final summary in godQuestions) {
    print('    $summary');
  }

  // Get proof texts from first 5 questions, group by reference
  final proofTexts =
      standards.shorterCatechismList
          .getRange(1, 5)
          .getAllProofTexts()
          .groupedByReference;

  print('  Proof texts from Q1-5 (grouped by reference):');
  for (final entry in proofTexts.entries.take(3)) {
    print('    ${entry.key}: ${entry.value.length} texts');
  }

  // Search in specific parts
  final questionMatches = standards.shorterCatechismList.searchInParts(
    'God',
    CatechismItemPart.question,
  );

  final answerMatches = standards.shorterCatechismList.searchInParts(
    'God',
    CatechismItemPart.answer,
  );

  print('  Questions with "God" in question: ${questionMatches.length}');
  print('  Questions with "God" in answer: ${answerMatches.length}');

  print('\n=== Extensions Example Complete ===');
  print('The extensions provide a much more intuitive and fluent API!');

  // Run a simple Flutter app to show the results
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Westminster Standards Extensions',
      home: Scaffold(
        appBar: AppBar(title: const Text('Westminster Standards Extensions')),
        body: const Center(
          child: Text(
            'Check the console output for the extensions example results!',
            style: TextStyle(fontSize: 18),
          ),
        ),
      ),
    );
  }
}
