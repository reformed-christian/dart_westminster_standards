import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Unified Search Tests', () {
    late WestminsterStandards standards;

    setUpAll(() async {
      // Initialize the data for testing
      standards = await WestminsterStandards.create();
    });

    group('Basic SearchAll Functionality', () {
      test('searchAll returns results from all documents', () {
        final results = standards.searchAll('God');

        expect(results, isNotEmpty);
        expect(results.every((r) => r is WestminsterSearchResult), isTrue);

        // Should have results from all document types
        final documentTypes = results.map((r) => r.documentType).toSet();
        expect(
          documentTypes.contains(WestminsterDocumentType.confession),
          isTrue,
        );
        expect(
          documentTypes.contains(WestminsterDocumentType.shorterCatechism),
          isTrue,
        );
        expect(
          documentTypes.contains(WestminsterDocumentType.largerCatechism),
          isTrue,
        );
      });

      test('searchAll returns empty list for non-existent term', () {
        final results = standards.searchAll('nonexistentword12345');
        expect(results, isEmpty);
      });

      test('searchAll is case insensitive', () {
        final lowerResults = standards.searchAll('god');
        final upperResults = standards.searchAll('GOD');
        final mixedResults = standards.searchAll('God');

        expect(lowerResults.length, equals(upperResults.length));
        expect(lowerResults.length, equals(mixedResults.length));
      });
    });

    group('Search Filtering', () {
      test('searchInTitles filter works correctly', () {
        final allResults = standards.searchAll('God');
        final titleResults = standards.searchAll(
          'God',
          searchInTitles: true,
          searchInContent: false,
          searchInReferences: false,
        );

        expect(titleResults.length, lessThanOrEqualTo(allResults.length));
        expect(
          titleResults.every(
            (r) =>
                r.matchType == SearchMatchType.title ||
                r.matchType == SearchMatchType.question,
          ),
          isTrue,
        );
      });

      test('searchInContent filter works correctly', () {
        final allResults = standards.searchAll('God');
        final contentResults = standards.searchAll(
          'God',
          searchInTitles: false,
          searchInContent: true,
          searchInReferences: false,
        );

        expect(contentResults.length, lessThanOrEqualTo(allResults.length));
        expect(
          contentResults.every(
            (r) =>
                r.matchType == SearchMatchType.content ||
                r.matchType == SearchMatchType.answer,
          ),
          isTrue,
        );
      });

      test('searchInReferences filter works correctly', () {
        final allResults = standards.searchAll('John');
        final referenceResults = standards.searchAll(
          'John',
          searchInTitles: false,
          searchInContent: false,
          searchInReferences: true,
        );

        expect(referenceResults.length, lessThanOrEqualTo(allResults.length));
        expect(
          referenceResults.every(
            (r) => r.matchType == SearchMatchType.references,
          ),
          isTrue,
        );
      });

      test('all filters disabled returns empty results', () {
        final results = standards.searchAll(
          'God',
          searchInTitles: false,
          searchInContent: false,
          searchInReferences: false,
        );

        expect(results, isEmpty);
      });
    });

    group('Result Structure', () {
      test('WestminsterSearchResult has correct structure', () {
        final results = standards.searchAll('God');
        expect(results, isNotEmpty);

        final firstResult = results.first;
        expect(firstResult.documentType, isA<WestminsterDocumentType>());
        expect(firstResult.number, isA<int>());
        expect(firstResult.number, greaterThan(0));
        expect(firstResult.title, isA<String>());
        expect(firstResult.title, isNotEmpty);
        expect(firstResult.content, isA<String>());
        expect(firstResult.content, isNotEmpty);
        expect(firstResult.proofTexts, isA<List>());
        expect(firstResult.matchedText, isA<String>());
        expect(firstResult.matchedText, isNotEmpty);
        expect(firstResult.matchType, isA<SearchMatchType>());
      });

      test('Catechism results have correct document type', () {
        final results = standards.searchAll('What');

        final catechismResults =
            results
                .where(
                  (r) =>
                      r.documentType ==
                          WestminsterDocumentType.shorterCatechism ||
                      r.documentType == WestminsterDocumentType.largerCatechism,
                )
                .toList();

        for (final result in catechismResults) {
          expect(result.title, contains('What'));
          expect(
            result.matchType == SearchMatchType.question ||
                result.matchType == SearchMatchType.answer,
            isTrue,
          );
        }
      });

      test('Confession results have correct document type', () {
        final results = standards.searchAll('God');

        final confessionResults =
            results
                .where(
                  (r) => r.documentType == WestminsterDocumentType.confession,
                )
                .toList();

        for (final result in confessionResults) {
          expect(
            result.matchType == SearchMatchType.title ||
                result.matchType == SearchMatchType.content ||
                result.matchType == SearchMatchType.references,
            isTrue,
          );
        }
      });
    });

    group('Match Type Validation', () {
      test('Question matches are from catechisms', () {
        final results = standards.searchAll('What');
        final questionMatches =
            results
                .where((r) => r.matchType == SearchMatchType.question)
                .toList();

        for (final result in questionMatches) {
          expect(
            result.documentType == WestminsterDocumentType.shorterCatechism ||
                result.documentType == WestminsterDocumentType.largerCatechism,
            isTrue,
          );
        }
      });

      test('Answer matches are from catechisms', () {
        final results = standards.searchAll('God');
        final answerMatches =
            results
                .where((r) => r.matchType == SearchMatchType.answer)
                .toList();

        for (final result in answerMatches) {
          expect(
            result.documentType == WestminsterDocumentType.shorterCatechism ||
                result.documentType == WestminsterDocumentType.largerCatechism,
            isTrue,
          );
        }
      });

      test('Title matches are from confession', () {
        final results = standards.searchAll('God');
        final titleMatches =
            results.where((r) => r.matchType == SearchMatchType.title).toList();

        for (final result in titleMatches) {
          expect(
            result.documentType == WestminsterDocumentType.confession,
            isTrue,
          );
        }
      });

      test('Content matches are from confession', () {
        final results = standards.searchAll('salvation');
        final contentMatches =
            results
                .where((r) => r.matchType == SearchMatchType.content)
                .toList();

        for (final result in contentMatches) {
          expect(
            result.documentType == WestminsterDocumentType.confession,
            isTrue,
          );
        }
      });

      test('Reference matches can be from any document', () {
        final results = standards.searchAll('John');
        final referenceMatches =
            results
                .where((r) => r.matchType == SearchMatchType.references)
                .toList();

        expect(referenceMatches, isNotEmpty);
        for (final result in referenceMatches) {
          expect(result.matchedText.toLowerCase(), contains('john'));
        }
      });
    });

    group('Cross-Document Analysis', () {
      test('can analyze results by document type', () {
        final results = standards.searchAll('faith');

        final byDocument =
            <WestminsterDocumentType, List<WestminsterSearchResult>>{};
        for (final result in results) {
          byDocument.putIfAbsent(result.documentType, () => []).add(result);
        }

        expect(byDocument.keys.length, greaterThan(0));
        expect(byDocument.values.every((list) => list.isNotEmpty), isTrue);
      });

      test('can analyze results by match type', () {
        final results = standards.searchAll('grace');

        final byMatchType = <SearchMatchType, List<WestminsterSearchResult>>{};
        for (final result in results) {
          byMatchType.putIfAbsent(result.matchType, () => []).add(result);
        }

        expect(byMatchType.keys.length, greaterThan(0));
        expect(byMatchType.values.every((list) => list.isNotEmpty), isTrue);
      });

      test('can filter and sort results', () {
        final results = standards.searchAll('love');

        // Filter to catechism questions only
        final catechismQuestions =
            results
                .where(
                  (r) =>
                      r.documentType != WestminsterDocumentType.confession &&
                      r.matchType == SearchMatchType.question,
                )
                .toList();

        // Sort by document type, then by number
        catechismQuestions.sort((a, b) {
          final docComparison = a.documentType.index.compareTo(
            b.documentType.index,
          );
          if (docComparison != 0) return docComparison;
          return a.number.compareTo(b.number);
        });

        expect(catechismQuestions, isNotEmpty);
        expect(
          catechismQuestions.every(
            (r) => r.matchType == SearchMatchType.question,
          ),
          isTrue,
        );
      });
    });

    group('Performance and Edge Cases', () {
      test('handles empty search string', () {
        final results = standards.searchAll('');
        expect(results, isEmpty);
      });

      test('handles single character search', () {
        final results = standards.searchAll('a');
        expect(results, isNotEmpty);
      });

      test('handles very long search string', () {
        final longString = 'a' * 1000;
        final results = standards.searchAll(longString);
        expect(results, isEmpty);
      });

      test('performance is reasonable', () {
        final stopwatch = Stopwatch()..start();
        final results = standards.searchAll('God');
        stopwatch.stop();

        expect(results, isNotEmpty);
        expect(
          stopwatch.elapsedMilliseconds,
          lessThan(1000),
        ); // Should complete in under 1 second
      });
    });

    group('Data Integrity', () {
      test('all results have valid proof texts', () {
        final results = standards.searchAll('God');

        for (final result in results) {
          expect(result.proofTexts, isA<List>());
          // Proof texts should be non-null (can be empty but not null)
          expect(result.proofTexts, isNotNull);
        }
      });

      test('matched text contains search term', () {
        final results = standards.searchAll('salvation');

        for (final result in results) {
          expect(result.matchedText.toLowerCase(), contains('salvation'));
        }
      });

      test('content field is not empty for valid results', () {
        final results = standards.searchAll('God');

        for (final result in results) {
          expect(result.content, isNotEmpty);
        }
      });

      test('title field is not empty for valid results', () {
        final results = standards.searchAll('God');

        for (final result in results) {
          expect(result.title, isNotEmpty);
        }
      });
    });
  });
}
