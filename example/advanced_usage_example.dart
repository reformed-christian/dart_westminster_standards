import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() async {
  print('=== Westminster Standards Advanced Usage Example ===\n');

  // 1. Loading specific documents only
  print('1. Loading Specific Documents:');

  // Load only confession
  final confessionOnly = await WestminsterStandards.create(
    WestminsterDocument.confession,
  );
  print('   Confession only: ${confessionOnly.confession.length} chapters');
  print(
    '   Shorter Catechism: ${confessionOnly.shorterCatechism.length} questions (not loaded)',
  );
  print('');

  // Load only catechisms (alternative approach)
  final shorterOnly = await WestminsterStandards.create(
    WestminsterDocument.shorterCatechism,
  );
  final largerOnly = await WestminsterStandards.create(
    WestminsterDocument.largerCatechism,
  );
  print(
    '   Shorter Catechism: ${shorterOnly.shorterCatechism.length} questions',
  );
  print('   Larger Catechism: ${largerOnly.largerCatechism.length} questions');
  print('   Confession: not loaded');
  print('');

  // 2. Complex search patterns
  print('2. Complex Search Patterns:');

  final standards = await WestminsterStandards.create();

  // Find questions about salvation that mention grace and have multiple proof texts
  final salvationQuestions = standards.shorterCatechism.exactStr('salvation');
  final salvationGraceQuestions =
      salvationQuestions
          .where((q) => q.answer.toLowerCase().contains('grace'))
          .toList();
  final complexQuestions =
      salvationGraceQuestions
          .where((q) => q.allProofTexts.length >= 3)
          .toList();

  print(
    '   Questions about salvation mentioning grace with 3+ proof texts: ${complexQuestions.length}',
  );
  for (final question in complexQuestions.take(2)) {
    print('     Q${question.number}: ${question.question}');
    print('       Proof texts: ${question.allProofTexts.length}');
  }
  print('');

  // 3. Cross-document analysis
  print('3. Cross-Document Analysis:');

  // Find all references to specific theological concepts across all documents
  final concepts = ['justification', 'sanctification', 'election', 'covenant'];

  for (final concept in concepts) {
    final confessionChapters = standards.confession.exactStr(concept);
    final shorterQuestions = standards.shorterCatechism.exactStr(concept);
    final largerQuestions = standards.largerCatechism.exactStr(concept);

    print('   "$concept":');
    print('     Confession chapters: ${confessionChapters.length}');
    print('     Shorter Catechism questions: ${shorterQuestions.length}');
    print('     Larger Catechism questions: ${largerQuestions.length}');
    print(
      '     Total: ${confessionChapters.length + shorterQuestions.length + largerQuestions.length}',
    );
  }
  print('');

  // 4. Statistical analysis
  print('4. Statistical Analysis:');

  // Word count analysis
  final allShorterAnswers = standards.shorterCatechism.all
      .map((q) => q.answer.split(' ').length)
      .reduce((a, b) => a + b);

  final allLargerAnswers = standards.largerCatechism.all
      .map((q) => q.answer.split(' ').length)
      .reduce((a, b) => a + b);

  final allConfessionText = standards.confession.allSections
      .map((s) => s.text.split(' ').length)
      .reduce((a, b) => a + b);

  print('   Total word count:');
  print('     Shorter Catechism answers: $allShorterAnswers words');
  print('     Larger Catechism answers: $allLargerAnswers words');
  print('     Confession sections: $allConfessionText words');
  print(
    '     Total: ${allShorterAnswers + allLargerAnswers + allConfessionText} words',
  );
  print('');

  // 5. Finding questions by complexity
  print('5. Finding Questions by Complexity:');

  // Questions with longest answers
  final sortedByLength =
      standards.shorterCatechism.all.toList()
        ..sort((a, b) => b.answer.length.compareTo(a.answer.length));

  print('   Shorter Catechism questions with longest answers:');
  for (int i = 0; i < 3; i++) {
    final question = sortedByLength[i];
    print('     Q${question.number}: ${question.answer.length} characters');
  }

  // Questions with most proof texts
  final sortedByProofTexts =
      standards.shorterCatechism.all.toList()..sort(
        (a, b) => b.allProofTexts.length.compareTo(a.allProofTexts.length),
      );

  print('   Shorter Catechism questions with most proof texts:');
  for (int i = 0; i < 3; i++) {
    final question = sortedByProofTexts[i];
    print(
      '     Q${question.number}: ${question.allProofTexts.length} proof texts',
    );
  }
  print('');

  // 6. Pattern analysis
  print('6. Pattern Analysis:');

  // Find questions that follow specific patterns
  final whatQuestions = standards.shorterCatechism.questionContains('What');
  final howQuestions = standards.shorterCatechism.questionContains('How');
  final whyQuestions = standards.shorterCatechism.questionContains('Why');
  final whenQuestions = standards.shorterCatechism.questionContains('When');
  final whereQuestions = standards.shorterCatechism.questionContains('Where');

  print('   Question patterns:');
  print('     "What" questions: ${whatQuestions.length}');
  print('     "How" questions: ${howQuestions.length}');
  print('     "Why" questions: ${whyQuestions.length}');
  print('     "When" questions: ${whenQuestions.length}');
  print('     "Where" questions: ${whereQuestions.length}');
  print('');

  // 7. Bible book analysis
  print('7. Bible Book Analysis:');

  final allProofTexts = standards.allProofTexts;
  final bookCounts = <String, int>{};

  for (final proofText in allProofTexts) {
    final book = proofText.reference.split(' ').first;
    bookCounts[book] = (bookCounts[book] ?? 0) + 1;
  }

  final sortedBooks =
      bookCounts.entries.toList()..sort((a, b) => b.value.compareTo(a.value));

  print('   Most referenced Bible books across all documents:');
  for (int i = 0; i < 10 && i < sortedBooks.length; i++) {
    print('     ${sortedBooks[i].key}: ${sortedBooks[i].value}');
  }
  print('');

  // 8. Theological theme analysis
  print('8. Theological Theme Analysis:');

  final themes = {
    'God': 'theology proper',
    'Christ': 'christology',
    'Holy Spirit': 'pneumatology',
    'salvation': 'soteriology',
    'church': 'ecclesiology',
    'eschatology': 'eschatology',
    'covenant': 'covenant theology',
    'law': 'law and gospel',
    'grace': 'grace',
    'faith': 'faith',
  };

  for (final entry in themes.entries) {
    final keyword = entry.key;
    final theme = entry.value;

    final confessionCount = standards.confession.exactStr(keyword).length;
    final shorterCount = standards.shorterCatechism.exactStr(keyword).length;
    final largerCount = standards.largerCatechism.exactStr(keyword).length;

    print('   $theme ($keyword):');
    print('     Confession: $confessionCount');
    print('     Shorter Catechism: $shorterCount');
    print('     Larger Catechism: $largerCount');
  }
  print('');

  print('=== Advanced Usage Example Complete ===');
}
