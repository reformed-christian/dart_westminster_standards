import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() async {
  print('=== Westminster Standards Search and Filter Example ===\n');

  final standards = await WestminsterStandards.create();

  // 1. Basic text search across all content
  print('1. Searching for "God" across all content:');
  final godQuestions = standards.shorterCatechism.exactStr('God');
  print(
    '   Found ${godQuestions.length} Shorter Catechism questions about God',
  );

  final godChapters = standards.confession.exactStr('God');
  print('   Found ${godChapters.length} Confession chapters about God');
  print('');

  // 2. Search specific parts of catechism questions
  print('2. Searching specific parts of catechism questions:');

  // Questions containing "What" in the question text
  final whatQuestions = standards.shorterCatechism.questionContains('What');
  print('   Questions starting with "What": ${whatQuestions.length}');

  // Questions containing "God" in the answer
  final godAnswers = standards.shorterCatechism.answerContains('God');
  print('   Questions with "God" in answer: ${godAnswers.length}');

  // Questions with specific Bible references
  final johnQuestions = standards.shorterCatechism.referencesContain('John');
  print('   Questions with John references: ${johnQuestions.length}');
  print('');

  // 3. Search confession chapters by title
  print('3. Searching confession chapters by title:');
  final godTitles = standards.confession.titleContains('God');
  print('   Chapters with "God" in title:');
  for (final chapter in godTitles) {
    print('     Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // 4. Search confession content
  print('4. Searching confession content:');
  final salvationSections = standards.confession.findSections('salvation');
  print('   Sections about salvation: ${salvationSections.length}');

  final graceSections = standards.confession.findSections('grace');
  print('   Sections about grace: ${graceSections.length}');
  print('');

  // 5. Pattern matching
  print('5. Pattern matching:');

  // Questions that start with specific words
  final whatStartsWith = standards.shorterCatechism.startsWith('What');
  print('   Questions starting with "What": ${whatStartsWith.length}');

  final howStartsWith = standards.shorterCatechism.startsWith('How');
  print('   Questions starting with "How": ${howStartsWith.length}');

  // Questions that end with specific words
  final endsWithGod = standards.shorterCatechism.endsWith('God');
  print('   Questions ending with "God": ${endsWithGod.length}');
  print('');

  // 6. Range and specific number access
  print('6. Range and specific number access:');

  // Get questions 1-5
  final firstFive = standards.shorterCatechism.range(1, 5);
  print('   Questions 1-5: ${firstFive.length} questions');

  // Get specific questions
  final specificQuestions = standards.shorterCatechism.byNumbers([
    1,
    3,
    5,
    7,
    10,
  ]);
  print(
    '   Specific questions (1, 3, 5, 7, 10): ${specificQuestions.length} questions',
  );

  // Get chapters 1-3
  final firstThreeChapters = standards.confession.range(1, 3);
  print('   Chapters 1-3: ${firstThreeChapters.length} chapters');
  print('');

  // 7. Advanced search with multiple criteria
  print('7. Advanced search examples:');

  // Find questions about sin that mention God
  final sinQuestions = standards.shorterCatechism.questionContains('sin');
  final sinAndGodQuestions =
      sinQuestions
          .where((q) => q.answer.toLowerCase().contains('god'))
          .toList();
  print(
    '   Questions about sin that mention God: ${sinAndGodQuestions.length}',
  );

  // Find chapters about Christ that mention salvation
  final christChapters = standards.confession.titleContains('Christ');
  final christSalvationChapters =
      christChapters
          .where(
            (c) => c.sections.any(
              (s) => s.text.toLowerCase().contains('salvation'),
            ),
          )
          .toList();
  print(
    '   Chapters about Christ mentioning salvation: ${christSalvationChapters.length}',
  );
  print('');

  print('=== Search and Filter Example Complete ===');
}
