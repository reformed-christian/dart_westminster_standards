import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Range Access Tests', () {
    setUpAll(() async {
      // Initialize the data for testing
      await initializeWestminsterStandards();
    });

    test('getWestminsterShorterCatechismRange returns correct range', () {
      final range = getWestminsterShorterCatechismRange(1, 5);

      expect(range, isNotEmpty);
      expect(range.length, 5);
      expect(range.first.number, 1);
      expect(range.last.number, 5);

      // Verify all numbers are in sequence
      for (int i = 0; i < range.length; i++) {
        expect(range[i].number, i + 1);
      }
    });

    test('getWestminsterLargerCatechismRange returns correct range', () {
      final range = getWestminsterLargerCatechismRange(1, 3);

      expect(range, isNotEmpty);
      expect(range.length, 3);
      expect(range.first.number, 1);
      expect(range.last.number, 3);

      // Verify all numbers are in sequence
      for (int i = 0; i < range.length; i++) {
        expect(range[i].number, i + 1);
      }
    });

    test('getWestminsterConfessionRange returns correct range', () {
      final range = getWestminsterConfessionRange(1, 3);

      expect(range, isNotEmpty);
      expect(range.length, 3);
      expect(range.first.number, 1);
      expect(range.last.number, 3);

      // Verify all numbers are in sequence
      for (int i = 0; i < range.length; i++) {
        expect(range[i].number, i + 1);
      }
    });

    test(
      'getWestminsterShorterCatechismByNumbers returns specific questions',
      () {
        final questions = getWestminsterShorterCatechismByNumbers([1, 3, 5]);

        expect(questions, isNotEmpty);
        expect(questions.length, 3);

        final numbers = questions.map((q) => q.number).toList();
        expect(numbers, containsAll([1, 3, 5]));
      },
    );

    test(
      'getWestminsterLargerCatechismByNumbers returns specific questions',
      () {
        final questions = getWestminsterLargerCatechismByNumbers([1, 2, 4]);

        expect(questions, isNotEmpty);
        expect(questions.length, 3);

        final numbers = questions.map((q) => q.number).toList();
        expect(numbers, containsAll([1, 2, 4]));
      },
    );

    test('getWestminsterConfessionByNumbers returns specific chapters', () {
      final chapters = getWestminsterConfessionByNumbers([1, 5, 10]);

      expect(chapters, isNotEmpty);
      expect(chapters.length, 3);

      final numbers = chapters.map((c) => c.number).toList();
      expect(numbers, containsAll([1, 5, 10]));
    });

    test('Invalid ranges return empty lists', () {
      final invalidRange = getWestminsterShorterCatechismRange(999, 1000);
      expect(invalidRange, isEmpty);

      final invalidChapters = getWestminsterConfessionRange(999, 1000);
      expect(invalidChapters, isEmpty);
    });

    test('Empty number lists return empty lists', () {
      final emptyQuestions = getWestminsterShorterCatechismByNumbers([]);
      expect(emptyQuestions, isEmpty);

      final emptyChapters = getWestminsterConfessionByNumbers([]);
      expect(emptyChapters, isEmpty);
    });

    test('Range functions handle edge cases', () {
      // Test with same start and end
      final singleQuestion = getWestminsterShorterCatechismRange(1, 1);
      expect(singleQuestion.length, 1);
      expect(singleQuestion.first.number, 1);

      // Test with reversed range (should still work)
      final reversedRange = getWestminsterShorterCatechismRange(5, 1);
      expect(reversedRange, isEmpty); // This is expected behavior
    });

    test('Enhanced access through WestminsterStandards object works', () async {
      final standards = await WestminsterStandards.create();

      // Test range through enhanced access
      final enhancedRange = standards.shorterCatechism.range(1, 3);
      expect(enhancedRange.length, 3);
      expect(enhancedRange.first.number, 1);
      expect(enhancedRange.last.number, 3);

      // Test byNumbers through enhanced access
      final enhancedSpecific = standards.shorterCatechism.byNumbers([1, 3, 5]);
      expect(enhancedSpecific.length, 3);

      final numbers = enhancedSpecific.map((q) => q.number).toList();
      expect(numbers, containsAll([1, 3, 5]));
    });
  });
}
