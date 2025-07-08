import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Extensions Example for Westminster Standards
/// This example demonstrates the extension methods that provide
/// a more fluent and intuitive API for working with Westminster Standards
void main() async {
  print('=== Westminster Standards Extensions Example ===\n');

  // Create WestminsterStandards instance
  final standards = await WestminsterStandards.create();

  print('1. COLLECTION EXTENSIONS:');
  print('========================');

  // Using collection extensions for more intuitive access
  print('Finding specific questions:');
  final question1 = standards.shorterCatechism.getQuestion(1);
  final question10 = standards.shorterCatechism.getQuestion(10);

  if (question1 != null) {
    print('  Q1: ${question1.question}');
    print('  Answer: ${question1.answer}');
    print('  Word count: ${question1.answer.split(' ').length} words');
  }

  print('\nGetting ranges:');
  final questions1to5 = standards.shorterCatechism.range(1, 5);
  print('  Questions 1-5: ${questions1to5.length} questions');
  for (final q in questions1to5) {
    print('    Q${q.number}: ${q.question}');
  }

  print('\nGetting specific numbers:');
  final specificQuestions = standards.shorterCatechism.byNumbers([
    1,
    5,
    10,
    15,
  ]);
  print(
    '  Specific questions: ${specificQuestions.map((q) => q.number).toList()}',
  );

  print('\n2. SEARCH FUNCTIONALITY:');
  print('=======================');

  // Search within collections
  final godQuestions = standards.shorterCatechism.exactStr('God');
  print('Questions containing "God": ${godQuestions.length}');
  for (final q in godQuestions.take(3)) {
    print('  Q${q.number}: ${q.question}');
  }

  final graceChapters = standards.confession.exactStr('grace');
  print('Chapters containing "grace": ${graceChapters.length}');

  print('\n3. PROOF TEXT ACCESS:');
  print('=====================');

  if (question1 != null) {
    print('Proof texts for Q1:');
    for (final clause in question1.clauses) {
      print('  Clause: "${clause.text}"');
      for (final proofText in clause.proofTexts) {
        print(
          '    ${proofText.reference}: ${proofText.text.substring(0, 50)}...',
        );
      }
    }
  }

  print('\n4. TEXT-ONLY ACCESS:');
  print('===================');

  // Get text-only content (without scripture references)
  final textOnly = standards.shorterCatechismTextOnly;
  print('Shorter Catechism text-only (first 200 chars):');
  print(textOnly.substring(0, 200) + '...');

  final rangeTextOnly = standards.getShorterCatechismRangeTextOnly(1, 3);
  print('\nQuestions 1-3 text-only (first 200 chars):');
  print(rangeTextOnly.substring(0, 200) + '...');

  print('\n5. UNIFIED SEARCH:');
  print('==================');

  // Search across all documents
  final searchResults = standards.searchAll('God');
  print(
    'Search results for "God" across all documents: ${searchResults.length}',
  );

  // Group by document type
  final byDocument = <String, int>{};
  for (final result in searchResults) {
    final docType = result.documentType.toString().split('.').last;
    byDocument[docType] = (byDocument[docType] ?? 0) + 1;
  }

  for (final entry in byDocument.entries) {
    print('  ${entry.key}: ${entry.value} results');
  }

  // Show top 3 results
  print('\nTop 3 results:');
  for (int i = 0; i < 3 && i < searchResults.length; i++) {
    final result = searchResults[i];
    print('  ${i + 1}. ${result.title}');
    print('     Document: ${result.documentType.toString().split('.').last}');
    print('     Number: ${result.number}');
  }

  print('\n6. RANGE SEARCH:');
  print('================');

  // Search within specific ranges
  final rangeResults = standards.shorterCatechism.searchRange(1, 10, 'God');
  print('Questions 1-10 containing "God": ${rangeResults.length}');
  for (final q in rangeResults) {
    print('  Q${q.number}: ${q.question}');
  }

  print('\n7. FLUENT API EXAMPLES:');
  print('=======================');

  // Demonstrating the fluent API
  print('Chaining operations:');

  // Find questions containing "God", take first 3
  final godQuestionsLimited = standards.shorterCatechism
      .exactStr('God')
      .take(3);
  print('  First 3 questions about God:');
  for (final q in godQuestionsLimited) {
    print('    Q${q.number}: ${q.question}');
  }

  // Get proof texts from first 5 questions
  final first5Questions = standards.shorterCatechism.range(1, 5);
  final allProofTexts = first5Questions.expand((q) => q.allProofTexts).toList();
  print('  Proof texts from Q1-5: ${allProofTexts.length} total');

  // Group proof texts by reference
  final groupedByReference = <String, List<ProofText>>{};
  for (final proofText in allProofTexts) {
    groupedByReference
        .putIfAbsent(proofText.reference, () => [])
        .add(proofText);
  }

  print('  Proof texts grouped by reference:');
  for (final entry in groupedByReference.entries.take(3)) {
    print('    ${entry.key}: ${entry.value.length} texts');
  }

  print('\n=== Extensions Example Complete ===');
  print('The extensions provide a more intuitive and fluent API!');
}
