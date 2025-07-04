import 'package:flutter/material.dart';
import 'package:westminster_standards/westminster_standards.dart';

/// Footnote Example - Demonstrating footnote numbers in catechisms
/// This example shows how to access and use footnote numbers in the Westminster Catechisms
void main() async {
  // Initialize Flutter
  WidgetsFlutterBinding.ensureInitialized();

  print('=== Westminster Standards Footnote Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Method 1: Using the WestminsterStandards object
  print('1. USING WESTMINSTERSTANDARDS OBJECT:');
  print('=====================================');

  final standards = await WestminsterStandards.create();

  // Get Shorter Catechism Q1 and show footnote numbers
  final shorterQ1 = standards.shorterCatechism.getQuestion(1);
  if (shorterQ1 != null) {
    print('Shorter Catechism Q1: ${shorterQ1.question}');
    print('Answer: ${shorterQ1.answer}');
    print('Clauses with footnote numbers:');
    for (final clause in shorterQ1.clauses) {
      if (clause.footnoteNum != null) {
        print('  Footnote ${clause.footnoteNum}: "${clause.text}"');
        print('    Proof texts:');
        for (final proofText in clause.proofTexts) {
          print('      ${proofText.reference}');
        }
      } else {
        print('  No footnote: "${clause.text}"');
      }
    }
  }
  print('');

  // Get Larger Catechism Q1 and show footnote numbers
  final largerQ1 = standards.largerCatechism.getQuestion(1);
  if (largerQ1 != null) {
    print('Larger Catechism Q1: ${largerQ1.question}');
    print('Answer: ${largerQ1.answer}');
    print('Clauses with footnote numbers:');
    for (final clause in largerQ1.clauses) {
      if (clause.footnoteNum != null) {
        print('  Footnote ${clause.footnoteNum}: "${clause.text}"');
        print('    Proof texts:');
        for (final proofText in clause.proofTexts) {
          print('      ${proofText.reference}');
        }
      } else {
        print('  No footnote: "${clause.text}"');
      }
    }
  }
  print('');

  // Method 2: Using individual functions
  print('2. USING INDIVIDUAL FUNCTIONS:');
  print('==============================');

  final q1 = loadWestminsterShorterCatechismQuestion(1);
  if (q1 != null) {
    print('Shorter Catechism Q1 (using individual function):');
    print('Question: ${q1.question}');
    print('Answer: ${q1.answer}');

    // Count clauses with footnotes
    final clausesWithFootnotes =
        q1.clauses.where((c) => c.footnoteNum != null).length;
    final totalClauses = q1.clauses.length;
    print('Clauses with footnotes: $clausesWithFootnotes out of $totalClauses');

    // Show all footnote numbers
    final footnoteNumbers =
        q1.clauses
            .where((c) => c.footnoteNum != null)
            .map((c) => c.footnoteNum)
            .toList();
    print('Footnote numbers: $footnoteNumbers');
  }
  print('');

  // Method 3: Working with specific footnote numbers
  print('3. WORKING WITH SPECIFIC FOOTNOTE NUMBERS:');
  print('==========================================');

  // Find all clauses with footnote number 1 in first 5 questions
  print('Finding all clauses with footnote number 1 in first 5 questions:');
  for (int i = 1; i <= 5; i++) {
    final question = standards.shorterCatechism.getQuestion(i);
    if (question != null) {
      final footnote1Clauses =
          question.clauses.where((c) => c.footnoteNum == 1).toList();
      if (footnote1Clauses.isNotEmpty) {
        print(
          '  Q$i: Found ${footnote1Clauses.length} clause(s) with footnote 1',
        );
        for (final clause in footnote1Clauses) {
          print('    "${clause.text}"');
        }
      }
    }
  }
  print('');

  // Method 4: Statistics about footnotes
  print('4. FOOTNOTE STATISTICS:');
  print('=======================');

  // Shorter Catechism statistics
  int shorterTotalClauses = 0;
  int shorterClausesWithFootnotes = 0;
  Set<int> shorterFootnoteNumbers = {};

  for (final question in standards.shorterCatechism.all) {
    shorterTotalClauses += question.clauses.length;
    for (final clause in question.clauses) {
      if (clause.footnoteNum != null) {
        shorterClausesWithFootnotes++;
        shorterFootnoteNumbers.add(clause.footnoteNum!);
      }
    }
  }

  print('Shorter Catechism:');
  print('  Total clauses: $shorterTotalClauses');
  print('  Clauses with footnotes: $shorterClausesWithFootnotes');
  print('  Unique footnote numbers: ${shorterFootnoteNumbers.length}');
  print(
    '  Footnote number range: ${shorterFootnoteNumbers.isEmpty ? 'none' : '${shorterFootnoteNumbers.reduce((a, b) => a < b ? a : b)}-${shorterFootnoteNumbers.reduce((a, b) => a > b ? a : b)}'}',
  );

  // Larger Catechism statistics
  int largerTotalClauses = 0;
  int largerClausesWithFootnotes = 0;
  Set<int> largerFootnoteNumbers = {};

  for (final question in standards.largerCatechism.all) {
    largerTotalClauses += question.clauses.length;
    for (final clause in question.clauses) {
      if (clause.footnoteNum != null) {
        largerClausesWithFootnotes++;
        largerFootnoteNumbers.add(clause.footnoteNum!);
      }
    }
  }

  print('Larger Catechism:');
  print('  Total clauses: $largerTotalClauses');
  print('  Clauses with footnotes: $largerClausesWithFootnotes');
  print('  Unique footnote numbers: ${largerFootnoteNumbers.length}');
  print(
    '  Footnote number range: ${largerFootnoteNumbers.isEmpty ? 'none' : '${largerFootnoteNumbers.reduce((a, b) => a < b ? a : b)}-${largerFootnoteNumbers.reduce((a, b) => a > b ? a : b)}'}',
  );
  print('');

  // Method 5: Finding questions by footnote number
  print('5. FINDING QUESTIONS BY FOOTNOTE NUMBER:');
  print('========================================');

  // Find all questions that have a clause with footnote number 5
  print('Questions with footnote number 5:');

  // Shorter Catechism
  final shorterWithFootnote5 = <CatechismItem>[];
  for (final question in standards.shorterCatechism.all) {
    if (question.clauses.any((c) => c.footnoteNum == 5)) {
      shorterWithFootnote5.add(question);
    }
  }

  if (shorterWithFootnote5.isNotEmpty) {
    print('  Shorter Catechism:');
    for (final question in shorterWithFootnote5) {
      print('    Q${question.number}: ${question.question}');
    }
  }

  // Larger Catechism
  final largerWithFootnote5 = <CatechismItem>[];
  for (final question in standards.largerCatechism.all) {
    if (question.clauses.any((c) => c.footnoteNum == 5)) {
      largerWithFootnote5.add(question);
    }
  }

  if (largerWithFootnote5.isNotEmpty) {
    print('  Larger Catechism:');
    for (final question in largerWithFootnote5) {
      print('    Q${question.number}: ${question.question}');
    }
  }
  print('');

  print('=== Footnote Example Complete ===');
  print('The footnoteNum field allows you to identify which specific parts of');
  print('catechism answers are supported by which proof texts.');

  // Run a simple Flutter app to show the results
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Westminster Standards Footnote Example',
      home: Scaffold(
        appBar: AppBar(title: const Text('Westminster Standards Footnotes')),
        body: const Center(
          child: Text(
            'Check the console output for the footnote example results!',
            style: TextStyle(fontSize: 18),
          ),
        ),
      ),
    );
  }
}
