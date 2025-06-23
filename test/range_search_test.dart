import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Range Search Tests', () {
    setUpAll(() async {
      // Initialize the data for testing
      await initializeWestminsterStandards();
    });

    group('Shorter Catechism Range Search', () {
      test(
        'searchWestminsterShorterCatechismRange returns correct results',
        () {
          final results = searchWestminsterShorterCatechismRange(1, 5, 'God');

          expect(results, isNotEmpty);
          expect(results.every((q) => q.number >= 1 && q.number <= 5), isTrue);
          expect(
            results.every(
              (q) =>
                  q.question.toLowerCase().contains('god') ||
                  q.answer.toLowerCase().contains('god'),
            ),
            isTrue,
          );
        },
      );

      test('searchWestminsterShorterCatechismRange with question filter', () {
        final results = searchWestminsterShorterCatechismRange(
          1,
          10,
          'What',
          CatechismItemPart.question,
        );

        expect(results, isNotEmpty);
        expect(results.every((q) => q.number >= 1 && q.number <= 10), isTrue);
        expect(
          results.every((q) => q.question.toLowerCase().contains('what')),
          isTrue,
        );
      });

      test('searchWestminsterShorterCatechismRange with answer filter', () {
        final results = searchWestminsterShorterCatechismRange(
          1,
          10,
          'God',
          CatechismItemPart.answer,
        );

        expect(results, isNotEmpty);
        expect(results.every((q) => q.number >= 1 && q.number <= 10), isTrue);
        expect(
          results.every((q) => q.answer.toLowerCase().contains('god')),
          isTrue,
        );
      });

      test('searchWestminsterShorterCatechismRange with references filter', () {
        final results = searchWestminsterShorterCatechismRange(
          1,
          20,
          'John',
          CatechismItemPart.references,
        );

        expect(results.every((q) => q.number >= 1 && q.number <= 20), isTrue);
        // Check that at least one reference contains 'John'
        expect(
          results.every(
            (q) => q.allProofTexts.any(
              (pt) => pt.reference.toLowerCase().contains('john'),
            ),
          ),
          isTrue,
        );
      });

      test(
        'searchWestminsterShorterCatechismRange returns empty for no matches',
        () {
          final results = searchWestminsterShorterCatechismRange(
            1,
            5,
            'nonexistentword',
          );

          expect(results, isEmpty);
        },
      );

      test(
        'searchWestminsterShorterCatechismRange returns empty for invalid range',
        () {
          final results = searchWestminsterShorterCatechismRange(
            1000,
            2000,
            'God',
          );

          expect(results, isEmpty);
        },
      );
    });

    group('Larger Catechism Range Search', () {
      test('searchWestminsterLargerCatechismRange returns correct results', () {
        final results = searchWestminsterLargerCatechismRange(1, 10, 'God');

        expect(results, isNotEmpty);
        expect(results.every((q) => q.number >= 1 && q.number <= 10), isTrue);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          ),
          isTrue,
        );
      });

      test('searchWestminsterLargerCatechismRange with question filter', () {
        final results = searchWestminsterLargerCatechismRange(
          1,
          10,
          'What',
          CatechismItemPart.question,
        );

        expect(results.every((q) => q.number >= 1 && q.number <= 10), isTrue);
        expect(
          results.every((q) => q.question.toLowerCase().contains('what')),
          isTrue,
        );
      });
    });

    group('Confession Range Search', () {
      test('searchWestminsterConfessionRange returns correct results', () {
        final results = searchWestminsterConfessionRange(1, 5, 'God');

        expect(results, isNotEmpty);
        expect(results.every((c) => c.number >= 1 && c.number <= 5), isTrue);
        expect(
          results.every(
            (c) =>
                c.title.toLowerCase().contains('god') ||
                c.sections.any((s) => s.text.toLowerCase().contains('god')),
          ),
          isTrue,
        );
      });

      test('searchWestminsterConfessionRange with title only', () {
        final results = searchWestminsterConfessionRange(
          1,
          5,
          'God',
          searchInTitle: true,
          searchInContent: false,
        );

        expect(results.every((c) => c.number >= 1 && c.number <= 5), isTrue);
        expect(
          results.every((c) => c.title.toLowerCase().contains('god')),
          isTrue,
        );
      });

      test('searchWestminsterConfessionRange with content only', () {
        final results = searchWestminsterConfessionRange(
          1,
          5,
          'God',
          searchInTitle: false,
          searchInContent: true,
        );

        expect(results.every((c) => c.number >= 1 && c.number <= 5), isTrue);
        expect(
          results.every(
            (c) => c.sections.any((s) => s.text.toLowerCase().contains('god')),
          ),
          isTrue,
        );
      });
    });

    group('Search by Numbers', () {
      test(
        'searchWestminsterShorterCatechismByNumbers returns correct results',
        () {
          final results = searchWestminsterShorterCatechismByNumbers([
            1,
            3,
            5,
          ], 'God');

          expect(results, isNotEmpty);
          expect(results.every((q) => [1, 3, 5].contains(q.number)), isTrue);
          expect(
            results.every(
              (q) =>
                  q.question.toLowerCase().contains('god') ||
                  q.answer.toLowerCase().contains('god'),
            ),
            isTrue,
          );
        },
      );

      test('searchWestminsterConfessionByNumbers returns correct results', () {
        final results = searchWestminsterConfessionByNumbers([1, 5], 'God');

        expect(results, isNotEmpty);
        expect(results.every((c) => [1, 5].contains(c.number)), isTrue);
        expect(
          results.every(
            (c) =>
                c.title.toLowerCase().contains('god') ||
                c.sections.any((s) => s.text.toLowerCase().contains('god')),
          ),
          isTrue,
        );
      });
    });

    group('Lazy Loading Range Search', () {
      test(
        'searchWestminsterShorterCatechismRangeLazy works correctly',
        () async {
          final results = await searchWestminsterShorterCatechismRangeLazy(
            1,
            5,
            'God',
          );

          expect(results, isNotEmpty);
          expect(results.every((q) => q.number >= 1 && q.number <= 5), isTrue);
          expect(
            results.every(
              (q) =>
                  q.question.toLowerCase().contains('god') ||
                  q.answer.toLowerCase().contains('god'),
            ),
            isTrue,
          );
        },
      );

      test('searchWestminsterConfessionRangeLazy works correctly', () async {
        final results = await searchWestminsterConfessionRangeLazy(1, 5, 'God');

        expect(results, isNotEmpty);
        expect(results.every((c) => c.number >= 1 && c.number <= 5), isTrue);
        expect(
          results.every(
            (c) =>
                c.title.toLowerCase().contains('god') ||
                c.sections.any((s) => s.text.toLowerCase().contains('god')),
          ),
          isTrue,
        );
      });
    });

    group('Enhanced Access Range Search', () {
      test('Catechism searchRange method works correctly', () async {
        final standards = await WestminsterStandards.create();
        final results = standards.shorterCatechism.searchRange(1, 5, 'God');

        expect(results, isNotEmpty);
        expect(results.every((q) => q.number >= 1 && q.number <= 5), isTrue);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          ),
          isTrue,
        );
      });

      test('Confession searchRange method works correctly', () async {
        final standards = await WestminsterStandards.create();
        final results = standards.confession.searchRange(1, 5, 'God');

        expect(results, isNotEmpty);
        expect(results.every((c) => c.number >= 1 && c.number <= 5), isTrue);
        expect(
          results.every(
            (c) =>
                c.title.toLowerCase().contains('god') ||
                c.sections.any((s) => s.text.toLowerCase().contains('god')),
          ),
          isTrue,
        );
      });

      test('Catechism searchByNumbers method works correctly', () async {
        final standards = await WestminsterStandards.create();
        final results = standards.shorterCatechism.searchByNumbers([
          1,
          3,
          5,
        ], 'God');

        expect(results, isNotEmpty);
        expect(results.every((q) => [1, 3, 5].contains(q.number)), isTrue);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          ),
          isTrue,
        );
      });

      test('Confession searchByNumbers method works correctly', () async {
        final standards = await WestminsterStandards.create();
        final results = standards.confession.searchByNumbers([1, 5], 'God');

        expect(results, isNotEmpty);
        expect(results.every((c) => [1, 5].contains(c.number)), isTrue);
        expect(
          results.every(
            (c) =>
                c.title.toLowerCase().contains('god') ||
                c.sections.any((s) => s.text.toLowerCase().contains('god')),
          ),
          isTrue,
        );
      });
    });

    group('Part Filtering Combinations', () {
      test('questionAndAnswer filter works correctly', () {
        final results = searchWestminsterShorterCatechismRange(
          1,
          10,
          'God',
          CatechismItemPart.questionAndAnswer,
        );

        expect(results.every((q) => q.number >= 1 && q.number <= 10), isTrue);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          ),
          isTrue,
        );
        // Should not include matches only in references
        expect(
          results.every(
            (q) =>
                !(q.question.toLowerCase().contains('god') == false &&
                    q.answer.toLowerCase().contains('god') == false &&
                    q.allProofTexts.any(
                      (pt) => pt.reference.toLowerCase().contains('god'),
                    )),
          ),
          isTrue,
        );
      });

      test('questionAndReferences filter works correctly', () {
        final results = searchWestminsterShorterCatechismRange(
          1,
          20,
          'John',
          CatechismItemPart.questionAndReferences,
        );

        expect(results.every((q) => q.number >= 1 && q.number <= 20), isTrue);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('john') ||
                q.allProofTexts.any(
                  (pt) => pt.reference.toLowerCase().contains('john'),
                ),
          ),
          isTrue,
        );
      });

      test('answerAndReferences filter works correctly', () {
        final results = searchWestminsterShorterCatechismRange(
          1,
          10,
          'God',
          CatechismItemPart.answerAndReferences,
        );

        expect(results.every((q) => q.number >= 1 && q.number <= 10), isTrue);
        expect(
          results.every(
            (q) =>
                q.answer.toLowerCase().contains('god') ||
                q.allProofTexts.any(
                  (pt) => pt.reference.toLowerCase().contains('god'),
                ),
          ),
          isTrue,
        );
      });
    });
  });
}
