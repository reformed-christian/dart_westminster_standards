import 'package:westminster_standards/westminster_standards.dart';

/// Footnote Example - Demonstrating footnote numbers in catechisms
/// This example shows how to access and use footnote numbers in the Westminster Catechisms
void main() async {
  print('=== Westminster Standards Footnote Example ===\n');

  // Create a WestminsterStandards instance
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

  // Working with specific footnote numbers
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

  // Statistics about footnotes
  print('=== FOOTNOTE STATISTICS ===');

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
  if (shorterFootnoteNumbers.isNotEmpty) {
    final minFootnote = shorterFootnoteNumbers.reduce((a, b) => a < b ? a : b);
    final maxFootnote = shorterFootnoteNumbers.reduce((a, b) => a > b ? a : b);
    print('  Footnote number range: $minFootnote-$maxFootnote');
  }

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
  if (largerFootnoteNumbers.isNotEmpty) {
    final minFootnote = largerFootnoteNumbers.reduce((a, b) => a < b ? a : b);
    final maxFootnote = largerFootnoteNumbers.reduce((a, b) => a > b ? a : b);
    print('  Footnote number range: $minFootnote-$maxFootnote');
  }
  print('');

  // Finding questions by footnote number
  print('=== QUESTIONS WITH FOOTNOTE NUMBER 5 ===');

  // Shorter Catechism
  final shorterWithFootnote5 = <CatechismItem>[];
  for (final question in standards.shorterCatechism.all) {
    if (question.clauses.any((c) => c.footnoteNum == 5)) {
      shorterWithFootnote5.add(question);
    }
  }

  if (shorterWithFootnote5.isNotEmpty) {
    print('Shorter Catechism:');
    for (final question in shorterWithFootnote5) {
      print('  Q${question.number}: ${question.question}');
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
    print('Larger Catechism:');
    for (final question in largerWithFootnote5) {
      print('  Q${question.number}: ${question.question}');
    }
  }
  print('');

  print('=== Footnote Example Complete ===');
  print('The footnoteNum field allows you to identify which specific parts of');
  print('catechism answers are supported by which proof texts.');
}
