import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Example demonstrating unified search across all Westminster Standards
///
/// This example shows how to:
/// - Search across all documents (Confession, Shorter Catechism, Larger Catechism)
/// - Get unified results with consistent structure
/// - Filter search by different content types (titles, content, references)
/// - Analyze search results by document type and match type
void main() async {
  print('=== Westminster Standards Unified Search Example ===\n');

  // Initialize the data
  final standards = await WestminsterStandards.create();
  print('✓ Data initialized successfully\n');

  // Example 1: Basic unified search for "God"
  print('1. Unified Search for "God":');
  final godResults = standards.searchAll('God');
  print('   Found ${godResults.length} total results across all documents');

  // Group results by document type
  final godByDocument =
      <WestminsterDocumentType, List<WestminsterSearchResult>>{};
  for (final result in godResults) {
    godByDocument.putIfAbsent(result.documentType, () => []).add(result);
  }

  for (final entry in godByDocument.entries) {
    print('   ${entry.key.name}: ${entry.value.length} results');
  }
  print('');

  // Example 2: Show detailed results for first few matches
  print('2. Detailed Results (first 5):');
  for (final result in godResults.take(5)) {
    print(
      '   ${result.documentType.name.toUpperCase()} ${result.number}: ${result.title.substring(0, 50)}...',
    );
    print('     Match Type: ${result.matchType.name}');
    print('     Proof Texts: ${result.proofTexts.length}');
    print('');
  }

  // Example 3: Search for "salvation" with different filters
  print('3. Search for "salvation" with different filters:');

  // Search in titles only
  final salvationTitles = standards.searchAll(
    'salvation',
    searchInTitles: true,
    searchInContent: false,
    searchInReferences: false,
  );
  print('   Titles only: ${salvationTitles.length} results');

  // Search in content only
  final salvationContent = standards.searchAll(
    'salvation',
    searchInTitles: false,
    searchInContent: true,
    searchInReferences: false,
  );
  print('   Content only: ${salvationContent.length} results');

  // Search in references only
  final salvationReferences = standards.searchAll(
    'salvation',
    searchInTitles: false,
    searchInContent: false,
    searchInReferences: true,
  );
  print('   References only: ${salvationReferences.length} results');
  print('');

  // Example 4: Search for "grace" and analyze by match type
  print('4. Search for "grace" - Analysis by Match Type:');
  final graceResults = standards.searchAll('grace');

  final graceByMatchType = <SearchMatchType, List<WestminsterSearchResult>>{};
  for (final result in graceResults) {
    graceByMatchType.putIfAbsent(result.matchType, () => []).add(result);
  }

  for (final entry in graceByMatchType.entries) {
    print('   ${entry.key.name}: ${entry.value.length} results');
    for (final result in entry.value.take(2)) {
      print(
        '     - ${result.documentType.name.toUpperCase()} ${result.number}',
      );
    }
  }
  print('');

  // Example 5: Search for "faith" and show cross-document comparison
  print('5. Cross-Document Comparison for "faith":');
  final faithResults = standards.searchAll('faith');

  final faithByDocument =
      <WestminsterDocumentType, List<WestminsterSearchResult>>{};
  for (final result in faithResults) {
    faithByDocument.putIfAbsent(result.documentType, () => []).add(result);
  }

  for (final entry in faithByDocument.entries) {
    print('   ${entry.key.name.toUpperCase()}: ${entry.value.length} results');
    for (final result in entry.value.take(3)) {
      print('     ${result.number}: ${result.title.substring(0, 40)}...');
    }
    print('');
  }

  // Example 6: Search for Bible references
  print('6. Search for Bible References:');
  final johnResults = standards.searchAll(
    'John',
    searchInTitles: false,
    searchInContent: false,
    searchInReferences: true,
  );
  print('   References to "John": ${johnResults.length} results');

  final psalmsResults = standards.searchAll(
    'Psalm',
    searchInTitles: false,
    searchInContent: false,
    searchInReferences: true,
  );
  print('   References to "Psalm": ${psalmsResults.length} results');
  print('');

  // Example 7: Complex search analysis
  print('7. Complex Search Analysis:');
  final complexResults = standards.searchAll('justification');

  // Find questions that mention justification and have multiple proof texts
  final richQuestions =
      complexResults
          .where((r) => r.documentType != WestminsterDocumentType.confession)
          .where((r) => r.proofTexts.length >= 3)
          .toList();

  print(
    '   Questions about justification with 3+ proof texts: ${richQuestions.length}',
  );
  for (final result in richQuestions.take(3)) {
    print(
      '     ${result.documentType.name.toUpperCase()} ${result.number}: ${result.proofTexts.length} proof texts',
    );
  }
  print('');

  // Example 8: Performance comparison
  print('8. Performance Comparison:');
  final searchTerms = ['God', 'salvation', 'grace', 'faith', 'church'];

  for (final term in searchTerms) {
    final stopwatch = Stopwatch()..start();
    final results = standards.searchAll(term);
    stopwatch.stop();

    print(
      '   "$term": ${results.length} results in ${stopwatch.elapsedMicroseconds}μs',
    );
  }
  print('');

  // Example 9: Advanced filtering and sorting
  print('9. Advanced Filtering and Sorting:');
  final allResults = standards.searchAll('love');

  // Sort by document type, then by number
  allResults.sort((a, b) {
    final docComparison = a.documentType.index.compareTo(b.documentType.index);
    if (docComparison != 0) return docComparison;
    return a.number.compareTo(b.number);
  });

  print('   "love" results sorted by document and number:');
  for (final result in allResults.take(5)) {
    print(
      '     ${result.documentType.name.toUpperCase()} ${result.number}: ${result.matchType.name}',
    );
  }
  print('');

  // Example 10: Statistical analysis
  print('10. Statistical Analysis of Search Results:');
  final testResults = standards.searchAll('God');

  final docStats = <WestminsterDocumentType, int>{};
  final matchStats = <SearchMatchType, int>{};

  for (final result in testResults) {
    docStats[result.documentType] = (docStats[result.documentType] ?? 0) + 1;
    matchStats[result.matchType] = (matchStats[result.matchType] ?? 0) + 1;
  }

  print('   Document distribution:');
  for (final entry in docStats.entries) {
    print(
      '     ${entry.key.name}: ${entry.value} (${(entry.value / testResults.length * 100).toStringAsFixed(1)}%)',
    );
  }

  print('   Match type distribution:');
  for (final entry in matchStats.entries) {
    print(
      '     ${entry.key.name}: ${entry.value} (${(entry.value / testResults.length * 100).toStringAsFixed(1)}%)',
    );
  }
  print('');

  print('=== Unified Search Example Complete ===');
  print(
    'Unified search provides powerful cross-document analysis capabilities!',
  );
}
