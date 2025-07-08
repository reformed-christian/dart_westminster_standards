import 'dart:io';
import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main(List<String> args) async {
  if (args.isEmpty) {
    print('Usage: dart run_example.dart <example_name>');
    print('Available examples:');
    print('  text_only');
    print('  basic_usage');
    print('  getting_started');
    print('  enhanced_access');
    print('  error_handling');
    print('  performance');
    print('  proof_texts');
    print('  catechism_comparison');
    print('  confession_detailed');
    print('  extensions');
    print('  advanced_usage');
    return;
  }

  final example = args[0];

  switch (example) {
    case 'text_only':
      await runTextOnlyExample();
      break;
    case 'basic_usage':
      await runBasicUsageExample();
      break;
    case 'getting_started':
      await runGettingStartedExample();
      break;
    case 'enhanced_access':
      await runEnhancedAccessExample();
      break;
    case 'error_handling':
      await runErrorHandlingExample();
      break;
    case 'performance':
      await runPerformanceExample();
      break;
    case 'proof_texts':
      await runProofTextsExample();
      break;
    case 'catechism_comparison':
      await runCatechismComparisonExample();
      break;
    case 'confession_detailed':
      await runConfessionDetailedExample();
      break;
    case 'extensions':
      await runExtensionsExample();
      break;
    case 'advanced_usage':
      await runAdvancedUsageExample();
      break;
    default:
      print('Unknown example: $example');
      print('Run without arguments to see available examples.');
  }
}

Future<void> runTextOnlyExample() async {
  print('=== Westminster Standards Text-Only Access Example ===\n');

  // Example 1: Get full text content of the Westminster Confession
  print('1. Full Westminster Confession Text (first 500 characters):');
  final confessionText = getWestminsterConfessionTextOnly();
  print(confessionText.substring(0, 500) + '...\n');

  // Example 2: Get full text content of the Westminster Shorter Catechism
  print('2. Full Westminster Shorter Catechism Text (first 500 characters):');
  final shorterCatechismText = getWestminsterShorterCatechismTextOnly();
  print(shorterCatechismText.substring(0, 500) + '...\n');

  // Example 3: Get full text content of the Westminster Larger Catechism
  print('3. Full Westminster Larger Catechism Text (first 500 characters):');
  final largerCatechismText = getWestminsterLargerCatechismTextOnly();
  print(largerCatechismText.substring(0, 500) + '...\n');

  // Example 4: Get text content of a specific range from the Confession
  print('4. Westminster Confession Chapters 1-3 Text:');
  final confessionRangeText = getWestminsterConfessionRangeTextOnly(1, 3);
  print(confessionRangeText);
  print('\n' + '=' * 50 + '\n');

  // Example 5: Get text content of a specific range from the Shorter Catechism
  print('5. Westminster Shorter Catechism Questions 1-5 Text:');
  final shorterCatechismRangeText = getWestminsterShorterCatechismRangeTextOnly(
    1,
    5,
  );
  print(shorterCatechismRangeText);
  print('\n' + '=' * 50 + '\n');

  // Example 6: Get text content of a specific range from the Larger Catechism
  print('6. Westminster Larger Catechism Questions 1-3 Text:');
  final largerCatechismRangeText = getWestminsterLargerCatechismRangeTextOnly(
    1,
    3,
  );
  print(largerCatechismRangeText);
  print('\n' + '=' * 50 + '\n');

  // Example 7: Get text content of specific chapters by numbers
  print('7. Westminster Confession Specific Chapters (1, 3, 5) Text:');
  final confessionSpecificText = getWestminsterConfessionByNumbersTextOnly([
    1,
    3,
    5,
  ]);
  print(confessionSpecificText.substring(0, 800) + '...\n');

  // Example 8: Get text content of specific questions by numbers
  print('8. Westminster Shorter Catechism Specific Questions (1, 3, 5) Text:');
  final shorterCatechismSpecificText =
      getWestminsterShorterCatechismByNumbersTextOnly([1, 3, 5]);
  print(shorterCatechismSpecificText);
  print('\n' + '=' * 50 + '\n');

  // Example 9: Lazy loading examples
  print('9. Lazy Loading Examples:');

  print('\n9a. Lazy load full Westminster Confession text:');
  final lazyConfessionText = await loadWestminsterConfessionTextOnlyLazy();
  print('Loaded ${lazyConfessionText.length} characters\n');

  print('9b. Lazy load Westminster Confession chapters 1-2:');
  final lazyConfessionRangeText =
      await loadWestminsterConfessionRangeTextOnlyLazy(1, 2);
  print(lazyConfessionRangeText);
  print('\n' + '=' * 50 + '\n');

  // Example 10: Compare with regular access (showing scripture references are excluded)
  print('10. Comparison: Regular vs Text-Only Access');

  print(
    '\n10a. Regular access to Confession Chapter 1 (includes scripture references):',
  );
  final regularChapter = getWestminsterConfession()[0]; // First chapter
  print('Chapter ${regularChapter.number}. ${regularChapter.title}');
  for (final section in regularChapter.sections.take(2)) {
    // Show first 2 sections
    print('${section.number}. ${section.text}');
    print('Proof texts: ${section.allProofTexts.length} references');
  }

  print(
    '\n10b. Text-only access to Confession Chapter 1 (no scripture references):',
  );
  final textOnlyChapter = getWestminsterConfessionRangeTextOnly(1, 1);
  print(textOnlyChapter.substring(0, 400) + '...\n');

  print('=== Example Complete ===');
}

Future<void> runBasicUsageExample() async {
  print('=== Westminster Standards Basic Usage Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();
  print('✓ Data initialized and cached\n');

  // Get a specific question from the Shorter Catechism
  final question1 = loadWestminsterShorterCatechismQuestion(1);
  if (question1 != null) {
    print('Shorter Catechism Question 1:');
    print('Q${question1.number}. ${question1.question}');
    print('A. ${question1.answer}\n');
  }

  // Get a specific chapter from the Confession
  final chapter1 = loadWestminsterConfessionChapter(1);
  if (chapter1 != null) {
    print('Confession Chapter 1:');
    print('Chapter ${chapter1.number}. ${chapter1.title}');
    if (chapter1.sections.isNotEmpty) {
      print(
        'First section: ${chapter1.sections.first.text.substring(0, 100)}...\n',
      );
    }
  }

  // Get a question from the Larger Catechism
  final largerQ1 = loadWestminsterLargerCatechismQuestion(1);
  if (largerQ1 != null) {
    print('Larger Catechism Question 1:');
    print('Q${largerQ1.number}. ${largerQ1.question}');
    print('A. ${largerQ1.answer.substring(0, 100)}...\n');
  }

  print('=== Example Complete ===');
}

Future<void> runGettingStartedExample() async {
  print('=== Westminster Standards Getting Started Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();
  print('✓ Data initialized and cached\n');

  // Get a specific question from the Shorter Catechism
  final question1 = loadWestminsterShorterCatechismQuestion(1);
  if (question1 != null) {
    print('Shorter Catechism Question 1:');
    print('Q${question1.number}. ${question1.question}');
    print('A. ${question1.answer}\n');
  }

  // Get a specific chapter from the Confession
  final chapter1 = loadWestminsterConfessionChapter(1);
  if (chapter1 != null) {
    print('Confession Chapter 1:');
    print('Chapter ${chapter1.number}. ${chapter1.title}');
    if (chapter1.sections.isNotEmpty) {
      print(
        'First section: ${chapter1.sections.first.text.substring(0, 100)}...\n',
      );
    }
  }

  // Get a question from the Larger Catechism
  final largerQ1 = loadWestminsterLargerCatechismQuestion(1);
  if (largerQ1 != null) {
    print('Larger Catechism Question 1:');
    print('Q${largerQ1.number}. ${largerQ1.question}');
    print('A. ${largerQ1.answer.substring(0, 100)}...\n');
  }

  print('=== Example Complete ===');
}

Future<void> runEnhancedAccessExample() async {
  print('=== Westminster Standards Enhanced Access Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Get all chapters from the Confession
  final confession = getWestminsterConfession();
  print('Total confession chapters: ${confession.length}');

  // Get all questions from the Shorter Catechism
  final shorterCatechism = getWestminsterShorterCatechism();
  print('Total shorter catechism questions: ${shorterCatechism.length}');

  // Get all questions from the Larger Catechism
  final largerCatechism = getWestminsterLargerCatechism();
  print('Total larger catechism questions: ${largerCatechism.length}');

  // Get specific chapters by numbers
  final specificChapters = getWestminsterConfessionByNumbers([1, 3, 5]);
  print('\nSpecific confession chapters (1, 3, 5):');
  for (final chapter in specificChapters) {
    print('Chapter ${chapter.number}: ${chapter.title}');
  }

  // Get specific questions by numbers
  final specificQuestions = getWestminsterShorterCatechismByNumbers([1, 3, 5]);
  print('\nSpecific shorter catechism questions (1, 3, 5):');
  for (final question in specificQuestions) {
    print('Q${question.number}: ${question.question}');
  }

  print('=== Example Complete ===');
}

Future<void> runErrorHandlingExample() async {
  print('=== Westminster Standards Error Handling Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Try to get a non-existent question
  final nonExistentQuestion = loadWestminsterShorterCatechismQuestion(999);
  if (nonExistentQuestion == null) {
    print('✓ Correctly handled non-existent question (999)');
  }

  // Try to get a non-existent chapter
  final nonExistentChapter = loadWestminsterConfessionChapter(999);
  if (nonExistentChapter == null) {
    print('✓ Correctly handled non-existent chapter (999)');
  }

  // Try to get range with invalid parameters
  try {
    final invalidRange = getWestminsterConfessionRange(10, 5); // start > end
    print('Invalid range returned ${invalidRange.length} results');
  } catch (e) {
    print('✓ Correctly handled invalid range parameters: $e');
  }

  print('=== Example Complete ===');
}

Future<void> runPerformanceExample() async {
  print('=== Westminster Standards Performance Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Measure range access performance
  final stopwatch = Stopwatch();

  stopwatch.start();
  final rangeResults = getWestminsterConfessionRange(1, 10);
  stopwatch.stop();

  print(
    'Getting confession chapters 1-10 took ${stopwatch.elapsedMilliseconds}ms',
  );
  print('Retrieved ${rangeResults.length} chapters');

  // Measure individual access performance
  stopwatch.reset();
  stopwatch.start();
  for (int i = 1; i <= 10; i++) {
    loadWestminsterShorterCatechismQuestion(i);
  }
  stopwatch.stop();

  print(
    'Loading 10 individual shorter catechism questions took ${stopwatch.elapsedMilliseconds}ms',
  );

  print('=== Example Complete ===');
}

Future<void> runProofTextsExample() async {
  print('=== Westminster Standards Proof Texts Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Get a chapter with proof texts
  final chapter1 = loadWestminsterConfessionChapter(1);
  if (chapter1 != null) {
    print('Chapter ${chapter1.number}: ${chapter1.title}');
    print('Total sections: ${chapter1.sections.length}');

    for (final section in chapter1.sections.take(2)) {
      print('\nSection ${section.number}:');
      print('Text: ${section.text.substring(0, 100)}...');
      print('Proof texts: ${section.allProofTexts.length} references');

      for (final proofText in section.allProofTexts.take(3)) {
        print(
          '  - ${proofText.reference}: ${proofText.text.substring(0, 50)}...',
        );
      }
    }
  }

  print('=== Example Complete ===');
}

Future<void> runCatechismComparisonExample() async {
  print('=== Westminster Standards Catechism Comparison Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Compare the same question number in both catechisms
  final shorterQ1 = loadWestminsterShorterCatechismQuestion(1);
  final largerQ1 = loadWestminsterLargerCatechismQuestion(1);

  if (shorterQ1 != null && largerQ1 != null) {
    print('Question 1 Comparison:');
    print('\nShorter Catechism:');
    print('Q${shorterQ1.number}. ${shorterQ1.question}');
    print('A. ${shorterQ1.answer}');

    print('\nLarger Catechism:');
    print('Q${largerQ1.number}. ${largerQ1.question}');
    print('A. ${largerQ1.answer.substring(0, 200)}...');

    print('\nShorter answer length: ${shorterQ1.answer.length} characters');
    print('Larger answer length: ${largerQ1.answer.length} characters');
  }

  print('=== Example Complete ===');
}

Future<void> runConfessionDetailedExample() async {
  print('=== Westminster Standards Confession Detailed Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Get detailed information about a specific chapter
  final chapter1 = loadWestminsterConfessionChapter(1);
  if (chapter1 != null) {
    print('Chapter ${chapter1.number}: ${chapter1.title}');
    print('Total sections: ${chapter1.sections.length}');
    print(
      'Total proof texts: ${chapter1.sections.fold(0, (sum, section) => sum + section.allProofTexts.length)}',
    );

    print('\nSections:');
    for (final section in chapter1.sections) {
      print('  ${section.number}. ${section.text.substring(0, 100)}...');
      print('    Proof texts: ${section.allProofTexts.length}');
    }
  }

  print('=== Example Complete ===');
}

Future<void> runExtensionsExample() async {
  print('=== Westminster Standards Extensions Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Use collection extensions
  final confession = getWestminsterConfession();
  final chaptersWithGod = confession.where(
    (chapter) =>
        chapter.title.toLowerCase().contains('god') ||
        chapter.sections.any(
          (section) => section.text.toLowerCase().contains('god'),
        ),
  );

  print('Chapters containing "God":');
  for (final chapter in chaptersWithGod.take(3)) {
    print('  Chapter ${chapter.number}: ${chapter.title}');
  }

  // Use string extensions
  final shorterCatechism = getWestminsterShorterCatechism();
  final longQuestions = shorterCatechism.where((q) => q.question.length > 100);
  print('\nQuestions with long titles (${longQuestions.length} found):');
  for (final question in longQuestions.take(2)) {
    print('  Q${question.number}: ${question.question}');
  }

  print('=== Example Complete ===');
}

Future<void> runAdvancedUsageExample() async {
  print('=== Westminster Standards Advanced Usage Example ===\n');

  // Initialize the data
  await initializeWestminsterStandards();

  // Complex search and filtering
  final confession = getWestminsterConfession();

  // Find chapters with the most proof texts
  final chaptersByProofTexts =
      confession.map((chapter) {
        final totalProofTexts = chapter.sections.fold(
          0,
          (sum, section) => sum + section.allProofTexts.length,
        );
        return {'chapter': chapter, 'proofTexts': totalProofTexts};
      }).toList();

  chaptersByProofTexts.sort(
    (a, b) => (b['proofTexts'] as int).compareTo(a['proofTexts'] as int),
  );

  print('Chapters with most proof texts:');
  for (int i = 0; i < 3; i++) {
    final chapter = chaptersByProofTexts[i]['chapter'] as dynamic;
    final proofTexts = chaptersByProofTexts[i]['proofTexts'] as int;
    print(
      '  Chapter ${chapter.number}: ${chapter.title} (${proofTexts} proof texts)',
    );
  }

  // Find questions with specific patterns
  final shorterCatechism = getWestminsterShorterCatechism();
  final questionsAboutSin = shorterCatechism.where(
    (q) =>
        q.question.toLowerCase().contains('sin') ||
        q.answer.toLowerCase().contains('sin'),
  );

  print('\nQuestions about sin:');
  for (final question in questionsAboutSin.take(3)) {
    print('  Q${question.number}: ${question.question}');
  }

  print('=== Example Complete ===');
}
