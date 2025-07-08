import 'package:westminster_standards/westminster_standards.dart';

/// Getting Started Example - The Simplest Way to Use Westminster Standards
/// This example shows the absolute basics to get you started quickly
void main() async {
  print('=== Westminster Standards Getting Started ===\n');

  // STEP 1: Create a WestminsterStandards instance
  final standards = await WestminsterStandards.create();
  print('✓ Data loaded and ready to use\n');

  // STEP 2: Get a specific question from the Shorter Catechism
  final question1 = standards.shorterCatechism.getQuestion(1);
  if (question1 != null) {
    print('Shorter Catechism Question 1:');
    print('Q${question1.number}. ${question1.question}');
    print('A. ${question1.answer}\n');
  }

  // STEP 3: Get a specific chapter from the Confession
  final chapter1 = standards.confession.getChapter(1);
  if (chapter1 != null) {
    print('Confession Chapter 1:');
    print('Chapter ${chapter1.number}. ${chapter1.title}');
    if (chapter1.sections.isNotEmpty) {
      print(
        'First section: ${chapter1.sections.first.text.substring(0, 100)}...\n',
      );
    }
  }

  // STEP 4: Get a question from the Larger Catechism
  final largerQ1 = standards.largerCatechism.getQuestion(1);
  if (largerQ1 != null) {
    print('Larger Catechism Question 1:');
    print('Q${largerQ1.number}. ${largerQ1.question}');
    print('A. ${largerQ1.answer.substring(0, 100)}...\n');
  }

  // STEP 5: Basic search functionality
  print('=== BASIC SEARCH ===');
  final godQuestions = standards.shorterCatechism.exactStr('God');
  print(
    'Questions containing "God" in Shorter Catechism: ${godQuestions.length}',
  );
  for (final q in godQuestions.take(3)) {
    print('  Q${q.number}: ${q.question}');
  }

  final graceChapters = standards.confession.exactStr('grace');
  print('Chapters containing "grace" in Confession: ${graceChapters.length}\n');

  // STEP 6: Range access
  print('=== RANGE ACCESS ===');
  final questions1to5 = standards.shorterCatechism.range(1, 5);
  print('Questions 1-5: ${questions1to5.map((q) => q.number).toList()}');

  final chapters1to3 = standards.confession.range(1, 3);
  print('Chapters 1-3: ${chapters1to3.map((c) => c.number).toList()}\n');

  // STEP 7: Working with proof texts
  print('=== PROOF TEXTS ===');
  if (question1 != null && question1.clauses.isNotEmpty) {
    print('Proof texts for Shorter Catechism Q1:');
    for (final clause in question1.clauses) {
      print('  Clause: ${clause.text}');
      if (clause.footnoteNum != null) {
        print('    Footnote ${clause.footnoteNum}:');
      }
      for (final proofText in clause.proofTexts) {
        print(
          '      ${proofText.reference}: ${proofText.text.substring(0, 50)}...',
        );
      }
    }
  }

  // STEP 8: Text-only access (without scripture references)
  print('\n=== TEXT-ONLY ACCESS ===');
  final textOnly = standards.getShorterCatechismRangeTextOnly(1, 3);
  print('Questions 1-3 (text only, first 200 chars):');
  print(textOnly.substring(0, 200) + '...');

  // STEP 9: Unified search across all documents
  print('\n=== UNIFIED SEARCH ===');
  final searchResults = standards.searchAll('God');
  print(
    'Search results for "God" across all documents: ${searchResults.length}',
  );
  for (int i = 0; i < 3 && i < searchResults.length; i++) {
    final result = searchResults[i];
    print(
      '  ${i + 1}. ${result.title} (${result.documentType.toString().split('.').last})',
    );
  }

  print(
    '\n=== That\'s it! You now have access to all Westminster Standards ===',
  );
  print('For more examples, see:');
  print('  - basic_usage_example.dart (comprehensive usage)');
  print('  - footnote_example.dart (working with footnotes)');
  print('  - extensions_example.dart (advanced features)');
}
