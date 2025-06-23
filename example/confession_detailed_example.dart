import 'package:westminster_standards/westminster_standards.dart';

void main() async {
  print('=== Westminster Confession Detailed Example ===\n');

  final standards = await WestminsterStandards.create();

  // 1. Overview of confession structure
  print('1. Confession Structure Overview:');
  print('   Total chapters: ${standards.confession.length}');
  print('   Total sections: ${standards.confession.allSections.length}');
  print('   Total proof texts: ${standards.confession.allProofTexts.length}');
  print('');

  // 2. Detailed chapter exploration
  print('2. Detailed Chapter Exploration:');

  for (int i = 1; i <= 3; i++) {
    final chapter = standards.confession.getChapter(i);
    if (chapter != null) {
      print('   Chapter ${chapter.number}: ${chapter.title}');
      print('     Sections: ${chapter.sections.length}');
      print(
        '     Proof texts: ${chapter.sections.expand((s) => s.allProofTexts).length}',
      );

      // Show first section
      if (chapter.sections.isNotEmpty) {
        final firstSection = chapter.sections.first;
        print('     First section: ${firstSection.text.substring(0, 80)}...');
      }
      print('');
    }
  }

  // 3. Searching confession content by themes
  print('3. Searching by Theological Themes:');

  final themes = [
    'salvation',
    'grace',
    'faith',
    'justification',
    'sanctification',
    'election',
    'covenant',
    'church',
    'sacraments',
    'eschatology',
  ];

  for (final theme in themes) {
    final sections = standards.confession.findSections(theme);
    print('   "$theme": ${sections.length} sections');
  }
  print('');

  // 4. Chapter titles analysis
  print('4. Chapter Titles Analysis:');

  final allTitles = standards.confession.all.map((c) => c.title).toList();
  print('   All chapter titles:');
  for (int i = 0; i < allTitles.length; i++) {
    print('     ${i + 1}. ${allTitles[i]}');
  }
  print('');

  // 5. Finding chapters by content patterns
  print('5. Finding Chapters by Content Patterns:');

  // Chapters about God
  final godChapters = standards.confession.contentContains('God');
  print('   Chapters mentioning God: ${godChapters.length}');

  // Chapters about Christ
  final christChapters = standards.confession.contentContains('Christ');
  print('   Chapters mentioning Christ: ${christChapters.length}');

  // Chapters about Holy Spirit
  final spiritChapters = standards.confession.contentContains('Holy Spirit');
  print('   Chapters mentioning Holy Spirit: ${spiritChapters.length}');
  print('');

  // 6. Section analysis
  print('6. Section Analysis:');

  final allSections = standards.confession.allSections;
  print('   Total sections: ${allSections.length}');

  // Find longest and shortest sections
  allSections.sort((a, b) => b.text.length.compareTo(a.text.length));
  print(
    '   Longest section (${allSections.first.text.length} chars): ${allSections.first.text.substring(0, 60)}...',
  );
  print(
    '   Shortest section (${allSections.last.text.length} chars): ${allSections.last.text}',
  );
  print('');

  // 7. Proof text analysis in confession
  print('7. Proof Text Analysis in Confession:');

  final confessionProofTexts = standards.confession.allProofTexts;
  print('   Total proof texts: ${confessionProofTexts.length}');

  // Most referenced books
  final bookCounts = <String, int>{};
  for (final proofText in confessionProofTexts) {
    final book = proofText.reference.split(' ').first;
    bookCounts[book] = (bookCounts[book] ?? 0) + 1;
  }

  final sortedBooks =
      bookCounts.entries.toList()..sort((a, b) => b.value.compareTo(a.value));

  print('   Top 10 most referenced books:');
  for (int i = 0; i < 10 && i < sortedBooks.length; i++) {
    print('     ${sortedBooks[i].key}: ${sortedBooks[i].value}');
  }
  print('');

  // 8. Range and specific chapter access
  print('8. Range and Specific Chapter Access:');

  // Get first 5 chapters
  final firstFiveChapters = standards.confession.range(1, 5);
  print('   First 5 chapters:');
  for (final chapter in firstFiveChapters) {
    print('     Chapter ${chapter.number}: ${chapter.title}');
  }

  // Get specific chapters
  final specificChapters = standards.confession.byNumbers([1, 5, 10, 15, 20]);
  print('   Specific chapters (1, 5, 10, 15, 20):');
  for (final chapter in specificChapters) {
    print('     Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  print('=== Confession Detailed Example Complete ===');
}
