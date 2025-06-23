import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  print('=== Westminster Catechisms Comparison Example ===\n');

  final standards = await WestminsterStandards.create();

  // 1. Basic comparison
  print('1. Basic Comparison:');
  print('   Shorter Catechism: ${standards.shorterCatechism.length} questions');
  print('   Larger Catechism: ${standards.largerCatechism.length} questions');
  print(
    '   Ratio: ${(standards.largerCatechism.length / standards.shorterCatechism.length).toStringAsFixed(2)}:1',
  );
  print('');

  // 2. Comparing first questions
  print('2. Comparing First Questions:');

  final shorterQ1 = standards.shorterCatechism.getQuestion(1);
  final largerQ1 = standards.largerCatechism.getQuestion(1);

  if (shorterQ1 != null && largerQ1 != null) {
    print('   Shorter Catechism Q1:');
    print('     Question: ${shorterQ1.question}');
    print('     Answer length: ${shorterQ1.answer.length} characters');
    print('     Proof texts: ${shorterQ1.allProofTexts.length}');

    print('   Larger Catechism Q1:');
    print('     Question: ${largerQ1.question}');
    print('     Answer length: ${largerQ1.answer.length} characters');
    print('     Proof texts: ${largerQ1.allProofTexts.length}');
  }
  print('');

  // 3. Comparing questions about the same topic
  print('3. Comparing Questions About the Same Topic:');

  // Find questions about God in both catechisms
  final shorterGodQuestions = standards.shorterCatechism.exactStr('God');
  final largerGodQuestions = standards.largerCatechism.exactStr('God');

  print('   Questions about God:');
  print('     Shorter Catechism: ${shorterGodQuestions.length}');
  print('     Larger Catechism: ${largerGodQuestions.length}');

  // Show first few examples
  print('   Shorter Catechism examples:');
  for (final question in shorterGodQuestions.take(3)) {
    print('     Q${question.number}: ${question.question}');
  }

  print('   Larger Catechism examples:');
  for (final question in largerGodQuestions.take(3)) {
    print('     Q${question.number}: ${question.question}');
  }
  print('');

  // 4. Comparing answer lengths
  print('4. Comparing Answer Lengths:');

  final shorterAvgLength =
      standards.shorterCatechism.all
          .map((q) => q.answer.length)
          .reduce((a, b) => a + b) /
      standards.shorterCatechism.length;

  final largerAvgLength =
      standards.largerCatechism.all
          .map((q) => q.answer.length)
          .reduce((a, b) => a + b) /
      standards.largerCatechism.length;

  print('   Average answer length:');
  print(
    '     Shorter Catechism: ${shorterAvgLength.toStringAsFixed(1)} characters',
  );
  print(
    '     Larger Catechism: ${largerAvgLength.toStringAsFixed(1)} characters',
  );
  print(
    '     Ratio: ${(largerAvgLength / shorterAvgLength).toStringAsFixed(2)}:1',
  );
  print('');

  // 5. Comparing proof text usage
  print('5. Comparing Proof Text Usage:');

  final shorterProofTexts = standards.allShorterCatechismProofTexts;
  final largerProofTexts = standards.allLargerCatechismProofTexts;

  print('   Total proof texts:');
  print('     Shorter Catechism: ${shorterProofTexts.length}');
  print('     Larger Catechism: ${largerProofTexts.length}');
  print(
    '     Ratio: ${(largerProofTexts.length / shorterProofTexts.length).toStringAsFixed(2)}:1',
  );

  print('   Average proof texts per question:');
  print(
    '     Shorter Catechism: ${(shorterProofTexts.length / standards.shorterCatechism.length).toStringAsFixed(2)}',
  );
  print(
    '     Larger Catechism: ${(largerProofTexts.length / standards.largerCatechism.length).toStringAsFixed(2)}',
  );
  print('');

  // 6. Finding corresponding questions
  print('6. Finding Corresponding Questions:');

  // Look for questions with similar content
  final shorterSinQuestions = standards.shorterCatechism.questionContains(
    'sin',
  );
  final largerSinQuestions = standards.largerCatechism.questionContains('sin');

  print('   Questions about sin:');
  print('     Shorter Catechism: ${shorterSinQuestions.length}');
  print('     Larger Catechism: ${largerSinQuestions.length}');

  // Show examples
  if (shorterSinQuestions.isNotEmpty && largerSinQuestions.isNotEmpty) {
    print(
      '   Shorter example: Q${shorterSinQuestions.first.number}: ${shorterSinQuestions.first.question}',
    );
    print(
      '   Larger example: Q${largerSinQuestions.first.number}: ${largerSinQuestions.first.question}',
    );
  }
  print('');

  // 7. Question patterns comparison
  print('7. Question Patterns Comparison:');

  // Questions starting with "What"
  final shorterWhat = standards.shorterCatechism.questionContains('What');
  final largerWhat = standards.largerCatechism.questionContains('What');

  print('   Questions starting with "What":');
  print('     Shorter Catechism: ${shorterWhat.length}');
  print('     Larger Catechism: ${largerWhat.length}');

  // Questions starting with "How"
  final shorterHow = standards.shorterCatechism.questionContains('How');
  final largerHow = standards.largerCatechism.questionContains('How');

  print('   Questions starting with "How":');
  print('     Shorter Catechism: ${shorterHow.length}');
  print('     Larger Catechism: ${largerHow.length}');
  print('');

  // 8. Bible reference comparison
  print('8. Bible Reference Comparison:');

  // Count references to major books
  final books = [
    'Genesis',
    'Exodus',
    'Matthew',
    'John',
    'Romans',
    'Revelation',
  ];

  for (final book in books) {
    final shorterRefs =
        standards.shorterCatechism.referencesContain(book).length;
    final largerRefs = standards.largerCatechism.referencesContain(book).length;

    print('   $book references:');
    print('     Shorter Catechism: $shorterRefs');
    print('     Larger Catechism: $largerRefs');
  }
  print('');

  print('=== Catechisms Comparison Example Complete ===');
}
