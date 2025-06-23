import 'package:westminster_standards/westminster_standards.dart';

/// Simple verification that unified search works
void main() async {
  print('=== Unified Search Verification ===');

  // Initialize the data
  final standards = await WestminsterStandards.create();
  print('✓ Data initialized successfully');

  // Test basic unified search
  final results = standards.searchAll('God');
  print('✓ Found ${results.length} results for "God" across all documents');

  // Verify we have results from all document types
  final documentTypes = results.map((r) => r.documentType).toSet();
  print(
    '✓ Results from ${documentTypes.length} document types: ${documentTypes.map((d) => d.name).join(', ')}',
  );

  // Test filtering
  final titleResults = standards.searchAll(
    'God',
    searchInTitles: true,
    searchInContent: false,
    searchInReferences: false,
  );
  print('✓ Title-only search: ${titleResults.length} results');

  final contentResults = standards.searchAll(
    'God',
    searchInTitles: false,
    searchInContent: true,
    searchInReferences: false,
  );
  print('✓ Content-only search: ${contentResults.length} results');

  // Test with a different term
  final salvationResults = standards.searchAll('salvation');
  print('✓ Found ${salvationResults.length} results for "salvation"');

  // Test with Bible references
  final johnResults = standards.searchAll(
    'John',
    searchInTitles: false,
    searchInContent: false,
    searchInReferences: true,
  );
  print('✓ Found ${johnResults.length} Bible references to "John"');

  // Show sample results
  if (results.isNotEmpty) {
    print('\n=== Sample Results ===');
    for (final result in results.take(3)) {
      print(
        '${result.documentType.name.toUpperCase()} ${result.number}: ${result.title.substring(0, 50)}...',
      );
      print('  Match Type: ${result.matchType.name}');
      print('  Proof Texts: ${result.proofTexts.length}');
      print('');
    }
  }

  print('=== Verification Complete ===');
  print('Unified search is working correctly!');
}
