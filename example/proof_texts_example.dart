import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  print('=== Westminster Standards Proof Texts Example ===\n');

  final standards = await WestminsterStandards.create();

  // 1. Accessing proof texts from specific questions
  print('1. Proof texts from specific questions:');

  final question1 = standards.shorterCatechism.getQuestion(1);
  if (question1 != null) {
    print('   Q1: ${question1.question}');
    print('   Proof texts: ${question1.allProofTexts.length}');
    for (final proofText in question1.allProofTexts.take(3)) {
      print('     - ${proofText.reference}');
    }
  }
  print('');

  // 2. All proof texts from each document
  print('2. Total proof texts in each document:');
  print(
    '   Shorter Catechism: ${standards.allShorterCatechismProofTexts.length}',
  );
  print(
    '   Larger Catechism: ${standards.allLargerCatechismProofTexts.length}',
  );
  print('   Confession: ${standards.allConfessionProofTexts.length}');
  print('   All documents combined: ${standards.allProofTexts.length}');
  print('');

  // 3. Finding questions with specific Bible references
  print('3. Questions with specific Bible references:');

  final johnQuestions = standards.shorterCatechism.referencesContain('John');
  print('   Questions with John references: ${johnQuestions.length}');

  final psalmsQuestions = standards.shorterCatechism.referencesContain('Psalm');
  print('   Questions with Psalm references: ${psalmsQuestions.length}');

  final romansQuestions = standards.shorterCatechism.referencesContain(
    'Romans',
  );
  print('   Questions with Romans references: ${romansQuestions.length}');
  print('');

  // 4. Proof texts from confession sections
  print('4. Proof texts from confession sections:');

  final chapter1 = standards.confession.getChapter(1);
  if (chapter1 != null) {
    print('   Chapter 1: ${chapter1.title}');
    print('   Sections: ${chapter1.sections.length}');

    for (final section in chapter1.sections.take(2)) {
      print(
        '     Section ${section.number}: ${section.allProofTexts.length} proof texts',
      );
      for (final proofText in section.allProofTexts.take(2)) {
        print('       - ${proofText.reference}');
      }
    }
  }
  print('');

  // 5. Finding all references to specific books
  print('5. Finding all references to specific books:');

  final allProofTexts = standards.allProofTexts;

  // Count references to major books
  final genesisRefs =
      allProofTexts
          .where((pt) => pt.reference.toLowerCase().contains('genesis'))
          .length;
  final exodusRefs =
      allProofTexts
          .where((pt) => pt.reference.toLowerCase().contains('exodus'))
          .length;
  final matthewRefs =
      allProofTexts
          .where((pt) => pt.reference.toLowerCase().contains('matthew'))
          .length;
  final johnRefs =
      allProofTexts
          .where((pt) => pt.reference.toLowerCase().contains('john'))
          .length;
  final romansRefs =
      allProofTexts
          .where((pt) => pt.reference.toLowerCase().contains('romans'))
          .length;

  print('   Genesis references: $genesisRefs');
  print('   Exodus references: $exodusRefs');
  print('   Matthew references: $matthewRefs');
  print('   John references: $johnRefs');
  print('   Romans references: $romansRefs');
  print('');

  // 6. Questions with most proof texts
  print('6. Questions with most proof texts:');

  final questionsWithProofTexts =
      standards.shorterCatechism.all
          .where((q) => q.allProofTexts.isNotEmpty)
          .toList();

  questionsWithProofTexts.sort(
    (a, b) => b.allProofTexts.length.compareTo(a.allProofTexts.length),
  );

  print('   Top 5 questions with most proof texts:');
  for (int i = 0; i < 5 && i < questionsWithProofTexts.length; i++) {
    final question = questionsWithProofTexts[i];
    print(
      '     Q${question.number}: ${question.allProofTexts.length} proof texts',
    );
  }
  print('');

  // 7. Proof texts from larger catechism
  print('7. Proof texts from Larger Catechism:');

  final largerQ1 = standards.largerCatechism.getQuestion(1);
  if (largerQ1 != null) {
    print('   Larger Catechism Q1: ${largerQ1.question}');
    print('   Proof texts: ${largerQ1.allProofTexts.length}');
    for (final proofText in largerQ1.allProofTexts.take(3)) {
      print('     - ${proofText.reference}');
    }
  }
  print('');

  print('=== Proof Texts Example Complete ===');
}
