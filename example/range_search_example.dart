import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Example demonstrating range-based search functionality
///
/// This example shows how to:
/// - Search within ranges of catechism questions (e.g., questions 1-10)
/// - Search within ranges of confession chapters (e.g., chapters 1-5)
/// - Filter searches by specific parts (question, answer, references, etc.)
/// - Search within specific questions/chapters by numbers
/// - Use both synchronous and lazy loading approaches
void main() async {
  print('=== Westminster Standards Range Search Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();
  print('✓ Data initialized successfully\n');

  // Example 1: Search for "God" in Shorter Catechism questions 1-10
  print('1. Searching for "God" in Shorter Catechism Questions 1-10:');
  final godInFirstTen = searchWestminsterShorterCatechismRange(1, 10, 'God');
  print('   Found ${godInFirstTen.length} questions containing "God"');
  for (final question in godInFirstTen) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 2: Search for "God" in Shorter Catechism questions 1-10, questions only
  print(
    '2. Searching for "God" in Shorter Catechism Questions 1-10 (questions only):',
  );
  final godInQuestions = searchWestminsterShorterCatechismRange(
    1,
    10,
    'God',
    CatechismItemPart.question,
  );
  print(
    '   Found ${godInQuestions.length} questions with "God" in the question',
  );
  for (final question in godInQuestions) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 3: Search for "God" in Shorter Catechism questions 1-10, answers only
  print(
    '3. Searching for "God" in Shorter Catechism Questions 1-10 (answers only):',
  );
  final godInAnswers = searchWestminsterShorterCatechismRange(
    1,
    10,
    'God',
    CatechismItemPart.answer,
  );
  print('   Found ${godInAnswers.length} questions with "God" in the answer');
  for (final question in godInAnswers) {
    print('   Q${question.number}: ${question.answer}');
  }
  print('');

  // Example 4: Search for "John" in Shorter Catechism questions 1-20, references only
  print(
    '4. Searching for "John" in Shorter Catechism Questions 1-20 (references only):',
  );
  final johnInRefs = searchWestminsterShorterCatechismRange(
    1,
    20,
    'John',
    CatechismItemPart.references,
  );
  print('   Found ${johnInRefs.length} questions with "John" in references');
  for (final question in johnInRefs) {
    print(
      '   Q${question.number}: ${question.allProofTexts.where((pt) => pt.reference.contains('John')).map((pt) => pt.reference).join(', ')}',
    );
  }
  print('');

  // Example 5: Search for "salvation" in Confession chapters 1-5
  print('5. Searching for "salvation" in Confession Chapters 1-5:');
  final salvationInFirstFive = searchWestminsterConfessionRange(
    1,
    5,
    'salvation',
  );
  print(
    '   Found ${salvationInFirstFive.length} chapters containing "salvation"',
  );
  for (final chapter in salvationInFirstFive) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 6: Search for "God" in Confession chapters 1-5, titles only
  print('6. Searching for "God" in Confession Chapters 1-5 (titles only):');
  final godInTitles = searchWestminsterConfessionRange(
    1,
    5,
    'God',
    searchInTitle: true,
    searchInContent: false,
  );
  print('   Found ${godInTitles.length} chapters with "God" in the title');
  for (final chapter in godInTitles) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 7: Search for "God" in Confession chapters 1-5, content only
  print('7. Searching for "God" in Confession Chapters 1-5 (content only):');
  final godInContent = searchWestminsterConfessionRange(
    1,
    5,
    'God',
    searchInTitle: false,
    searchInContent: true,
  );
  print('   Found ${godInContent.length} chapters with "God" in the content');
  for (final chapter in godInContent) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 8: Search within specific questions by numbers
  print(
    '8. Searching for "What" in specific Shorter Catechism questions [1, 3, 5, 7]:',
  );
  final whatInSpecific = searchWestminsterShorterCatechismByNumbers(
    [1, 3, 5, 7],
    'What',
    CatechismItemPart.question,
  );
  print(
    '   Found ${whatInSpecific.length} questions with "What" in the question',
  );
  for (final question in whatInSpecific) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 9: Search within specific chapters by numbers
  print('9. Searching for "faith" in specific Confession chapters [1, 5, 10]:');
  final faithInSpecific = searchWestminsterConfessionByNumbers([
    1,
    5,
    10,
  ], 'faith');
  print('   Found ${faithInSpecific.length} chapters containing "faith"');
  for (final chapter in faithInSpecific) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 10: Using lazy loading for range search
  print(
    '10. Lazy Loading - Searching for "Christ" in Shorter Catechism Questions 10-20:',
  );
  final lazySearch = await searchWestminsterShorterCatechismRangeLazy(
    10,
    20,
    'Christ',
  );
  print('   Found ${lazySearch.length} questions containing "Christ"');
  for (final question in lazySearch) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 11: Using enhanced access through WestminsterStandards object
  print(
    '11. Enhanced Access - Searching for "sin" in Shorter Catechism Questions 15-25:',
  );
  final standards = await WestminsterStandards.create();
  final enhancedSearch = standards.shorterCatechism.searchRange(15, 25, 'sin');
  print('   Found ${enhancedSearch.length} questions containing "sin"');
  for (final question in enhancedSearch) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 12: Enhanced access for confession range search
  print(
    '12. Enhanced Access - Searching for "grace" in Confession Chapters 4-8:',
  );
  final enhancedConfessionSearch = standards.confession.searchRange(
    4,
    8,
    'grace',
    searchInTitle: true,
    searchInContent: true,
  );
  print(
    '   Found ${enhancedConfessionSearch.length} chapters containing "grace"',
  );
  for (final chapter in enhancedConfessionSearch) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 13: Search with different part combinations
  print('13. Advanced Search - "love" in Shorter Catechism Questions 1-15:');
  print('   Searching in questions and answers only:');
  final loveInQA = searchWestminsterShorterCatechismRange(
    1,
    15,
    'love',
    CatechismItemPart.questionAndAnswer,
  );
  print(
    '   Found ${loveInQA.length} questions with "love" in question or answer',
  );

  print('   Searching in questions and references only:');
  final loveInQR = searchWestminsterShorterCatechismRange(
    1,
    15,
    'love',
    CatechismItemPart.questionAndReferences,
  );
  print(
    '   Found ${loveInQR.length} questions with "love" in question or references',
  );
  print('');

  // Example 14: Performance comparison
  print('14. Performance Comparison:');
  print('   Searching entire Shorter Catechism for "God":');
  final allQuestions = getWestminsterShorterCatechism();
  final allGodResults =
      allQuestions
          .where(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          )
          .toList();
  print('   Found ${allGodResults.length} results in all questions');

  print('   Searching questions 1-10 for "God":');
  final rangeGodResults = searchWestminsterShorterCatechismRange(1, 10, 'God');
  print('   Found ${rangeGodResults.length} results in range 1-10');
  print('   Range search is more efficient for specific needs!');
  print('');

  print('=== Range Search Example Complete ===');
  print('Range-based search provides powerful filtering capabilities!');
}
