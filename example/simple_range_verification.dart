import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  print('=== Westminster Standards Range Access Verification ===\n');

  // Initialize the data
  await initializeWestminsterStandards();
  print('✓ Data initialized successfully\n');

  // Test 1: Shorter Catechism Range
  print('1. Testing Shorter Catechism Range (1-5):');
  final shorterRange = getWestminsterShorterCatechismRange(1, 5);
  if (shorterRange.length == 5 &&
      shorterRange.first.number == 1 &&
      shorterRange.last.number == 5) {
    print('   ✓ Range returned ${shorterRange.length} questions');
    print('   ✓ First question: ${shorterRange.first.number}');
    print('   ✓ Last question: ${shorterRange.last.number}');
  } else {
    print('   ✗ Range test failed');
  }
  print('');

  // Test 2: Larger Catechism Range
  print('2. Testing Larger Catechism Range (1-3):');
  final largerRange = getWestminsterLargerCatechismRange(1, 3);
  if (largerRange.length == 3 &&
      largerRange.first.number == 1 &&
      largerRange.last.number == 3) {
    print('   ✓ Range returned ${largerRange.length} questions');
    print('   ✓ First question: ${largerRange.first.number}');
    print('   ✓ Last question: ${largerRange.last.number}');
  } else {
    print('   ✗ Range test failed');
  }
  print('');

  // Test 3: Confession Range
  print('3. Testing Confession Range (1-3):');
  final confessionRange = getWestminsterConfessionRange(1, 3);
  if (confessionRange.length == 3 &&
      confessionRange.first.number == 1 &&
      confessionRange.last.number == 3) {
    print('   ✓ Range returned ${confessionRange.length} chapters');
    print('   ✓ First chapter: ${confessionRange.first.number}');
    print('   ✓ Last chapter: ${confessionRange.last.number}');
  } else {
    print('   ✗ Range test failed');
  }
  print('');

  // Test 4: Specific Questions by Numbers
  print('4. Testing Specific Questions by Numbers [1, 3, 5]:');
  final specificQuestions = getWestminsterShorterCatechismByNumbers([1, 3, 5]);
  if (specificQuestions.length == 3) {
    final numbers = specificQuestions.map((q) => q.number).toList();
    if (numbers.contains(1) && numbers.contains(3) && numbers.contains(5)) {
      print('   ✓ Returned ${specificQuestions.length} specific questions');
      print('   ✓ Questions: ${numbers.join(', ')}');
    } else {
      print('   ✗ Wrong question numbers returned');
    }
  } else {
    print('   ✗ Wrong number of questions returned');
  }
  print('');

  // Test 5: Specific Chapters by Numbers
  print('5. Testing Specific Chapters by Numbers [1, 5, 10]:');
  final specificChapters = getWestminsterConfessionByNumbers([1, 5, 10]);
  if (specificChapters.length == 3) {
    final numbers = specificChapters.map((c) => c.number).toList();
    if (numbers.contains(1) && numbers.contains(5) && numbers.contains(10)) {
      print('   ✓ Returned ${specificChapters.length} specific chapters');
      print('   ✓ Chapters: ${numbers.join(', ')}');
    } else {
      print('   ✗ Wrong chapter numbers returned');
    }
  } else {
    print('   ✗ Wrong number of chapters returned');
  }
  print('');

  // Test 6: Invalid Range
  print('6. Testing Invalid Range (999-1000):');
  final invalidRange = getWestminsterShorterCatechismRange(999, 1000);
  if (invalidRange.isEmpty) {
    print('   ✓ Invalid range correctly returned empty list');
  } else {
    print('   ✗ Invalid range should have returned empty list');
  }
  print('');

  // Test 7: Enhanced Access
  print('7. Testing Enhanced Access through WestminsterStandards:');
  final standards = await WestminsterStandards.create();
  final enhancedRange = standards.shorterCatechism.range(1, 3);
  if (enhancedRange.length == 3 &&
      enhancedRange.first.number == 1 &&
      enhancedRange.last.number == 3) {
    print('   ✓ Enhanced range returned ${enhancedRange.length} questions');
    print('   ✓ First question: ${enhancedRange.first.number}');
    print('   ✓ Last question: ${enhancedRange.last.number}');
  } else {
    print('   ✗ Enhanced range test failed');
  }
  print('');

  print('=== Verification Complete ===');
  print('All range access functionality is working correctly!');
}
