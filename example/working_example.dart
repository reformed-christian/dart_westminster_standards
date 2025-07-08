import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Comprehensive example showing how to use the Westminster Standards package
/// This example demonstrates various ways to access and work with the data
void main() async {
  print('🏛️  Westminster Standards Package Example\n');

  try {
    // Load all Westminster Standards documents
    final standards = await WestminsterStandards.create();

    print('✅ Successfully loaded all Westminster Standards documents!\n');

    // 1. Basic Data Access
    print('📊 BASIC DATA ACCESS:');
    print(
      '• Westminster Confession: ${standards.confessionList.length} chapters',
    );
    print(
      '• Shorter Catechism: ${standards.shorterCatechismList.length} questions',
    );
    print(
      '• Larger Catechism: ${standards.largerCatechismList.length} questions\n',
    );

    // 2. Individual Item Access
    print('🔍 INDIVIDUAL ITEM ACCESS:');

    // Get specific confession chapter
    final chapter1 = standards.getConfessionChapter(1);
    if (chapter1 != null) {
      print(
        '• Chapter 1: "${chapter1.title}" (${chapter1.sections.length} sections)',
      );
    }

    // Get specific catechism questions
    final scQ1 = standards.getShorterCatechismQuestion(1);
    if (scQ1 != null) {
      print('• Shorter Catechism Q1: "${scQ1.question}"');
      print('  A: "${scQ1.answer}"');
    }

    final lcQ1 = standards.getLargerCatechismQuestion(1);
    if (lcQ1 != null) {
      print('• Larger Catechism Q1: "${lcQ1.question}"');
      print('  A: "${lcQ1.answer}"\n');
    }

    // 3. Enhanced Access Methods
    print('🚀 ENHANCED ACCESS METHODS:');

    // Range access using the list directly
    final scQuestions1to3 =
        standards.shorterCatechismList
            .where((q) => q.number >= 1 && q.number <= 3)
            .toList();
    print('• Shorter Catechism Q1-Q3: ${scQuestions1to3.length} questions');

    // Search functionality
    final searchResults = standards.searchAll('grace', searchInContent: true);
    print('• Search for "grace": ${searchResults.length} results found');

    // Text-only access (without scripture references)
    final confessionText = standards.confessionTextOnly;
    print(
      '• Confession text-only length: ${confessionText.length} characters\n',
    );

    // 4. Proof Texts
    print('📖 PROOF TEXTS:');
    final allProofTexts = standards.allProofTexts;
    print('• Total proof texts across all documents: ${allProofTexts.length}');

    if (allProofTexts.isNotEmpty) {
      final sampleProofText = allProofTexts.first;
      print('• Sample proof text: "${sampleProofText.reference}"');
      print('  Text: "${sampleProofText.text.substring(0, 50)}..."\n');
    }

    // 5. Bulk Operations
    print('📚 BULK OPERATIONS:');

    // Get all questions with "God" in them
    final godQuestions =
        standards.shorterCatechismList
            .where(
              (q) =>
                  q.question.toLowerCase().contains('god') ||
                  q.answer.toLowerCase().contains('god'),
            )
            .toList();
    print(
      '• Shorter Catechism questions mentioning "God": ${godQuestions.length}',
    );

    // Get all confession chapters with "faith" in the title
    final faithChapters =
        standards.confessionList
            .where((c) => c.title.toLowerCase().contains('faith'))
            .toList();
    print(
      '• Confession chapters with "faith" in title: ${faithChapters.length}\n',
    );

    // 6. Performance Demonstration
    print('⚡ PERFORMANCE DEMONSTRATION:');

    final stopwatch = Stopwatch()..start();

    // Multiple operations
    for (int i = 1; i <= 10; i++) {
      standards.getShorterCatechismQuestion(i);
      standards.getConfessionChapter(i);
    }

    stopwatch.stop();
    print(
      '• 20 individual item lookups completed in ${stopwatch.elapsedMilliseconds}ms',
    );

    print('\n🎉 All examples completed successfully!');
    print(
      'The Westminster Standards package is working correctly with proper asset loading.',
    );
  } catch (e) {
    print('❌ Error occurred:');
    print(e.toString());
  }
}
