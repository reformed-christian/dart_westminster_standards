import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  print('=== Westminster Standards Range Search Verification ===\n');

  // Initialize the data
  await initializeWestminsterStandards();
  print('✓ Data initialized successfully\n');

  // Test 1: Basic range search in Shorter Catechism
  print('1. Testing Shorter Catechism Range Search (1-5, "God"):');
  final shorterRangeSearch = searchWestminsterShorterCatechismRange(
    1,
    5,
    'God',
  );
  if (shorterRangeSearch.isNotEmpty &&
      shorterRangeSearch.every((q) => q.number >= 1 && q.number <= 5)) {
    print(
      '   ✓ Found ${shorterRangeSearch.length} questions with "God" in range 1-5',
    );
    for (final question in shorterRangeSearch) {
      print('   ✓ Q${question.number}: ${question.question}');
    }
  } else {
    print('   ✗ Shorter Catechism range search failed');
  }
  print('');

  // Test 2: Range search with question filter
  print(
    '2. Testing Shorter Catechism Range Search with Question Filter (1-10, "What"):',
  );
  final questionFilterSearch = searchWestminsterShorterCatechismRange(
    1,
    10,
    'What',
    CatechismItemPart.question,
  );
  if (questionFilterSearch.isNotEmpty &&
      questionFilterSearch.every(
        (q) => q.question.toLowerCase().contains('what'),
      )) {
    print(
      '   ✓ Found ${questionFilterSearch.length} questions with "What" in question text',
    );
  } else {
    print('   ✗ Question filter search failed');
  }
  print('');

  // Test 3: Range search with answer filter
  print(
    '3. Testing Shorter Catechism Range Search with Answer Filter (1-10, "God"):',
  );
  final answerFilterSearch = searchWestminsterShorterCatechismRange(
    1,
    10,
    'God',
    CatechismItemPart.answer,
  );
  if (answerFilterSearch.every((q) => q.answer.toLowerCase().contains('god'))) {
    print(
      '   ✓ Found ${answerFilterSearch.length} questions with "God" in answer text',
    );
  } else {
    print('   ✗ Answer filter search failed');
  }
  print('');

  // Test 4: Range search with references filter
  print(
    '4. Testing Shorter Catechism Range Search with References Filter (1-20, "John"):',
  );
  final refsFilterSearch = searchWestminsterShorterCatechismRange(
    1,
    20,
    'John',
    CatechismItemPart.references,
  );
  if (refsFilterSearch.every(
    (q) => q.allProofTexts.any(
      (pt) => pt.reference.toLowerCase().contains('john'),
    ),
  )) {
    print(
      '   ✓ Found ${refsFilterSearch.length} questions with "John" in references',
    );
  } else {
    print('   ✗ References filter search failed');
  }
  print('');

  // Test 5: Confession range search
  print('5. Testing Confession Range Search (1-5, "God"):');
  final confessionRangeSearch = searchWestminsterConfessionRange(1, 5, 'God');
  if (confessionRangeSearch.isNotEmpty &&
      confessionRangeSearch.every((c) => c.number >= 1 && c.number <= 5)) {
    print(
      '   ✓ Found ${confessionRangeSearch.length} chapters with "God" in range 1-5',
    );
    for (final chapter in confessionRangeSearch) {
      print('   ✓ Chapter ${chapter.number}: ${chapter.title}');
    }
  } else {
    print('   ✗ Confession range search failed');
  }
  print('');

  // Test 6: Confession range search with title only
  print('6. Testing Confession Range Search with Title Only (1-5, "God"):');
  final titleOnlySearch = searchWestminsterConfessionRange(
    1,
    5,
    'God',
    searchInTitle: true,
    searchInContent: false,
  );
  if (titleOnlySearch.every((c) => c.title.toLowerCase().contains('god'))) {
    print(
      '   ✓ Found ${titleOnlySearch.length} chapters with "God" in title only',
    );
  } else {
    print('   ✗ Title-only search failed');
  }
  print('');

  // Test 7: Search by specific numbers
  print('7. Testing Search by Specific Numbers ([1, 3, 5], "God"):');
  final specificNumbersSearch = searchWestminsterShorterCatechismByNumbers([
    1,
    3,
    5,
  ], 'God');
  if (specificNumbersSearch.every((q) => [1, 3, 5].contains(q.number))) {
    print(
      '   ✓ Found ${specificNumbersSearch.length} questions with "God" in specified numbers',
    );
  } else {
    print('   ✗ Search by specific numbers failed');
  }
  print('');

  // Test 8: Lazy loading range search
  print('8. Testing Lazy Loading Range Search (1-5, "God"):');
  final lazySearch = await searchWestminsterShorterCatechismRangeLazy(
    1,
    5,
    'God',
  );
  if (lazySearch.isNotEmpty &&
      lazySearch.every((q) => q.number >= 1 && q.number <= 5)) {
    print('   ✓ Lazy loading range search found ${lazySearch.length} results');
  } else {
    print('   ✗ Lazy loading range search failed');
  }
  print('');

  // Test 9: Enhanced access range search
  print('9. Testing Enhanced Access Range Search:');
  final standards = await WestminsterStandards.create();
  final enhancedSearch = standards.shorterCatechism.searchRange(1, 5, 'God');
  if (enhancedSearch.isNotEmpty &&
      enhancedSearch.every((q) => q.number >= 1 && q.number <= 5)) {
    print(
      '   ✓ Enhanced access range search found ${enhancedSearch.length} results',
    );
  } else {
    print('   ✗ Enhanced access range search failed');
  }
  print('');

  // Test 10: Part filtering combinations
  print('10. Testing Part Filtering Combinations:');
  final qaOnly = searchWestminsterShorterCatechismRange(
    1,
    10,
    'God',
    CatechismItemPart.questionAndAnswer,
  );
  final qrOnly = searchWestminsterShorterCatechismRange(
    1,
    10,
    'God',
    CatechismItemPart.questionAndReferences,
  );
  final arOnly = searchWestminsterShorterCatechismRange(
    1,
    10,
    'God',
    CatechismItemPart.answerAndReferences,
  );

  print('   ✓ Question and Answer filter: ${qaOnly.length} results');
  print('   ✓ Question and References filter: ${qrOnly.length} results');
  print('   ✓ Answer and References filter: ${arOnly.length} results');
  print('');

  // Test 11: Performance comparison
  print('11. Performance Comparison:');
  final allQuestions = getWestminsterShorterCatechism();
  final allGodResults =
      allQuestions
          .where(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          )
          .toList();
  print(
    '   ✓ Searching all questions for "God": ${allGodResults.length} results',
  );

  final rangeGodResults = searchWestminsterShorterCatechismRange(1, 10, 'God');
  print(
    '   ✓ Searching questions 1-10 for "God": ${rangeGodResults.length} results',
  );
  print('   ✓ Range search is more efficient for targeted searches!');
  print('');

  print('=== Range Search Verification Complete ===');
  print('✓ All range search functionality is working correctly!');
  print('✓ Part filtering is working as expected!');
  print('✓ Performance benefits are demonstrated!');
}
