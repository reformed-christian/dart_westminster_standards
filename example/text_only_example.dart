import 'package:westminster_standards/westminster_standards.dart';

/// Example demonstrating text-only access to Westminster Standards
/// This shows how to obtain just the text content without scripture references
void main() async {
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
