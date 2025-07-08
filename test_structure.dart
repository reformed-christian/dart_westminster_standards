import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() async {
  print('=== Testing Westminster Standards Structure ===\n');

  final standards = await WestminsterStandards.create();

  // Test first question structure
  final question1 = standards.shorterCatechism.getQuestion(1);
  if (question1 != null) {
    print('Q1: ${question1.question}');
    print('Answer: ${question1.answer}');
    print('Clauses: ${question1.clauses.length}');

    for (int i = 0; i < question1.clauses.length; i++) {
      final clause = question1.clauses[i];
      print('  Clause ${i + 1}: "${clause.text}"');
      print('    Proof texts: ${clause.proofTexts.length}');
      for (int j = 0; j < clause.proofTexts.length; j++) {
        final proofText = clause.proofTexts[j];
        print('      ${j + 1}. ${proofText.reference}: ${proofText.text}');
      }
    }

    print('\nAll proof texts: ${question1.allProofTexts.length}');
    for (int i = 0; i < question1.allProofTexts.length; i++) {
      final proofText = question1.allProofTexts[i];
      print('  ${i + 1}. ${proofText.reference}: ${proofText.text}');
    }
  }

  print('\n=== Structure Test Complete ===');
}
