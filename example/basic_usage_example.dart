import 'package:flutter/material.dart';
import 'package:westminster_standards/westminster_standards.dart';

/// Basic Usage Example for Westminster Standards
/// This example shows the most common and straightforward ways to use the package
void main() async {
  // Initialize Flutter
  WidgetsFlutterBinding.ensureInitialized();

  print('=== Westminster Standards Basic Usage Example ===\n');

  // Method 1: Using the WestminsterStandards object (recommended)
  print('1. USING WESTMINSTERSTANDARDS OBJECT (Recommended):');
  print('==================================================');

  final standards = await WestminsterStandards.create();

  // Basic document information
  print('Document counts:');
  print('  Shorter Catechism: ${standards.shorterCatechism.length} questions');
  print('  Larger Catechism: ${standards.largerCatechism.length} questions');
  print('  Confession: ${standards.confession.length} chapters\n');

  // Access first items from each document
  print('First items from each document:');
  final firstShorter = standards.shorterCatechism.firstQuestion;
  final firstLarger = standards.largerCatechism.firstQuestion;
  final firstChapter = standards.confession.firstChapter;

  if (firstShorter != null) {
    print('  Shorter Catechism Q1: ${firstShorter.question}');
    print('  Answer: ${firstShorter.answer}');
  }

  if (firstLarger != null) {
    print('  Larger Catechism Q1: ${firstLarger.question}');
  }

  if (firstChapter != null) {
    print('  Confession Chapter 1: ${firstChapter.title}');
  }
  print('');

  // Access specific items by number
  print('Accessing specific items by number:');
  final question10 = standards.shorterCatechism.getQuestion(10);
  final chapter5 = standards.confession.getChapter(5);

  if (question10 != null) {
    print('  Shorter Catechism Q10: ${question10.question}');
  }

  if (chapter5 != null) {
    print('  Confession Chapter 5: ${chapter5.title}');
  }
  print('');

  // Method 2: Using individual functions (alternative approach)
  print('2. USING INDIVIDUAL FUNCTIONS (Alternative):');
  print('============================================');

  // Initialize the data
  await initializeWestminsterStandards();

  // Load specific questions and chapters
  final q1 = loadWestminsterShorterCatechismQuestion(1);
  final c1 = loadWestminsterConfessionChapter(1);

  if (q1 != null) {
    print('Shorter Catechism Q1: ${q1.question}');
    print('Answer: ${q1.answer}');
  }

  if (c1 != null) {
    print('Confession Chapter 1: ${c1.title}');
    if (c1.sections.isNotEmpty) {
      print('First section: ${c1.sections.first.text.substring(0, 100)}...');
    }
  }
  print('');

  // Method 3: Iterating through items
  print('3. ITERATING THROUGH ITEMS:');
  print('===========================');

  print('First 3 Shorter Catechism questions:');
  for (int i = 0; i < 3; i++) {
    final question = standards.shorterCatechism[i];
    print('  Q${question.number}: ${question.question}');
  }
  print('');

  print('First 3 Confession chapters:');
  for (int i = 0; i < 3; i++) {
    final chapter = standards.confession[i];
    print('  Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Method 4: Working with proof texts
  print('4. WORKING WITH PROOF TEXTS:');
  print('============================');

  final question1 = standards.shorterCatechism.getQuestion(1);
  if (question1 != null && question1.clauses.isNotEmpty) {
    print('Proof texts for Shorter Catechism Q1:');
    for (final clause in question1.clauses) {
      print('  Clause: ${clause.text}');
      if (clause.footnoteNum != null) {
        print('    Footnote ${clause.footnoteNum}:');
      }
      for (final proofText in clause.proofTexts) {
        print('      ${proofText.reference}: ${proofText.text}');
      }
    }
  }
  print('');

  // Method 5: Working with footnotes
  print('5. WORKING WITH FOOTNOTES:');
  print('==========================');

  final question2 = standards.shorterCatechism.getQuestion(2);
  if (question2 != null) {
    print('Shorter Catechism Q2 with footnotes:');
    print('Q${question2.number}. ${question2.question}');
    print('A. ${question2.answer}');

    for (final clause in question2.clauses) {
      if (clause.footnoteNum != null) {
        print('  Footnote ${clause.footnoteNum}: "${clause.text}"');
        print('    Supported by ${clause.proofTexts.length} scripture(s):');
        for (final proofText in clause.proofTexts) {
          print('      ${proofText.reference}');
        }
      }
    }
  }
  print('');

  // Method 6: Text-only access (without scripture references)
  print('6. TEXT-ONLY ACCESS (without scripture references):');
  print('==================================================');

  print('Shorter Catechism Q1-3 (text only):');
  final textOnly = standards.getShorterCatechismRangeTextOnly(1, 3);
  print(textOnly);
  print('');

  // Method 6: Search functionality
  print('6. SEARCH FUNCTIONALITY:');
  print('========================');

  final searchResults = standards.searchAll('God');
  print('Found ${searchResults.length} results for "God"');
  for (int i = 0; i < searchResults.take(3).length; i++) {
    final result = searchResults[i];
    print(
      '  ${i + 1}. ${result.documentType} #${result.number}: ${result.title}',
    );
  }
  print('');

  print('=== Basic Usage Example Complete ===');
  print('For more advanced features, see the other example files.');
  print('For footnote functionality, see footnote_example.dart');

  // Run a simple Flutter app to show the results
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Westminster Standards Basic Usage',
      home: Scaffold(
        appBar: AppBar(title: const Text('Westminster Standards')),
        body: const Center(
          child: Text(
            'Check the console output for the example results!',
            style: TextStyle(fontSize: 18),
          ),
        ),
      ),
    );
  }
}
