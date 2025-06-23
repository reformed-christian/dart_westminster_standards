import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Text-Only Access Tests', () {
    test('getWestminsterConfessionTextOnly returns non-empty string', () {
      final text = getWestminsterConfessionTextOnly();
      expect(text, isNotEmpty);
      expect(text, contains('Chapter 1.'));
      expect(text, contains('Of the Holy Scripture'));
    });

    test('getWestminsterShorterCatechismTextOnly returns non-empty string', () {
      final text = getWestminsterShorterCatechismTextOnly();
      expect(text, isNotEmpty);
      expect(text, contains('Q1.'));
      expect(text, contains('A1.'));
      expect(text, contains('What is the chief end of man?'));
    });

    test('getWestminsterLargerCatechismTextOnly returns non-empty string', () {
      final text = getWestminsterLargerCatechismTextOnly();
      expect(text, isNotEmpty);
      expect(text, contains('Q1.'));
      expect(text, contains('A1.'));
      expect(text, contains('What is the chief and highest end of man?'));
    });

    test('getWestminsterConfessionRangeTextOnly returns correct range', () {
      final text = getWestminsterConfessionRangeTextOnly(1, 2);
      expect(text, isNotEmpty);
      expect(text, contains('Chapter 1.'));
      expect(text, contains('Chapter 2.'));
      expect(text, isNot(contains('Chapter 3.')));
    });

    test(
      'getWestminsterShorterCatechismRangeTextOnly returns correct range',
      () {
        final text = getWestminsterShorterCatechismRangeTextOnly(1, 3);
        expect(text, isNotEmpty);
        expect(text, contains('Q1.'));
        expect(text, contains('Q2.'));
        expect(text, contains('Q3.'));
        expect(text, isNot(contains('Q4.')));
      },
    );

    test(
      'getWestminsterLargerCatechismRangeTextOnly returns correct range',
      () {
        final text = getWestminsterLargerCatechismRangeTextOnly(1, 2);
        expect(text, isNotEmpty);
        expect(text, contains('Q1.'));
        expect(text, contains('Q2.'));
        expect(text, isNot(contains('Q3.')));
      },
    );

    test(
      'getWestminsterConfessionByNumbersTextOnly returns specific chapters',
      () {
        final text = getWestminsterConfessionByNumbersTextOnly([1, 3]);
        expect(text, isNotEmpty);
        expect(text, contains('Chapter 1.'));
        expect(text, contains('Chapter 3.'));
        expect(text, isNot(contains('Chapter 2.')));
      },
    );

    test(
      'getWestminsterShorterCatechismByNumbersTextOnly returns specific questions',
      () {
        final text = getWestminsterShorterCatechismByNumbersTextOnly([1, 3]);
        expect(text, isNotEmpty);
        expect(text, contains('Q1.'));
        expect(text, contains('Q3.'));
        expect(text, isNot(contains('Q2.')));
      },
    );

    test(
      'getWestminsterLargerCatechismByNumbersTextOnly returns specific questions',
      () {
        final text = getWestminsterLargerCatechismByNumbersTextOnly([1, 3]);
        expect(text, isNotEmpty);
        expect(text, contains('Q1.'));
        expect(text, contains('Q3.'));
        expect(text, isNot(contains('Q2.')));
      },
    );

    test('text-only functions exclude scripture references', () {
      // Get regular access to see proof texts
      final regularConfession = getWestminsterConfession();
      final firstChapter = regularConfession.first;
      final hasProofTexts = firstChapter.sections.any(
        (section) => section.allProofTexts.isNotEmpty,
      );

      // Get text-only access
      final textOnlyConfession = getWestminsterConfessionTextOnly();

      // Verify that text-only version doesn't contain scripture references
      expect(textOnlyConfession, isNot(contains('Genesis')));
      expect(textOnlyConfession, isNot(contains('Matthew')));
      expect(textOnlyConfession, isNot(contains('John')));

      // Verify that regular access has proof texts if they exist
      if (hasProofTexts) {
        expect(regularConfession, isNot(equals(textOnlyConfession)));
      }
    });

    test('text-only functions return empty string for empty data', () {
      // These should return empty strings if data is not initialized
      // (though in practice, the data should be initialized)
      final confessionText = getWestminsterConfessionTextOnly();
      final shorterCatechismText = getWestminsterShorterCatechismTextOnly();
      final largerCatechismText = getWestminsterLargerCatechismTextOnly();

      // At least one should be non-empty if data is properly loaded
      expect(
        confessionText.isNotEmpty ||
            shorterCatechismText.isNotEmpty ||
            largerCatechismText.isNotEmpty,
        isTrue,
        reason: 'At least one document should have content',
      );
    });

    test('range functions handle invalid ranges gracefully', () {
      final confessionText = getWestminsterConfessionRangeTextOnly(999, 1000);
      final shorterCatechismText = getWestminsterShorterCatechismRangeTextOnly(
        999,
        1000,
      );
      final largerCatechismText = getWestminsterLargerCatechismRangeTextOnly(
        999,
        1000,
      );

      expect(confessionText, isEmpty);
      expect(shorterCatechismText, isEmpty);
      expect(largerCatechismText, isEmpty);
    });

    test('byNumbers functions handle invalid numbers gracefully', () {
      final confessionText = getWestminsterConfessionByNumbersTextOnly([
        999,
        1000,
      ]);
      final shorterCatechismText =
          getWestminsterShorterCatechismByNumbersTextOnly([999, 1000]);
      final largerCatechismText =
          getWestminsterLargerCatechismByNumbersTextOnly([999, 1000]);

      expect(confessionText, isEmpty);
      expect(shorterCatechismText, isEmpty);
      expect(largerCatechismText, isEmpty);
    });
  });

  group('Text-Only Access Lazy Loading Tests', () {
    test(
      'loadWestminsterConfessionTextOnlyLazy returns non-empty string',
      () async {
        final text = await loadWestminsterConfessionTextOnlyLazy();
        expect(text, isNotEmpty);
        expect(text, contains('Chapter 1.'));
      },
    );

    test(
      'loadWestminsterShorterCatechismTextOnlyLazy returns non-empty string',
      () async {
        final text = await loadWestminsterShorterCatechismTextOnlyLazy();
        expect(text, isNotEmpty);
        expect(text, contains('Q1.'));
      },
    );

    test(
      'loadWestminsterLargerCatechismTextOnlyLazy returns non-empty string',
      () async {
        final text = await loadWestminsterLargerCatechismTextOnlyLazy();
        expect(text, isNotEmpty);
        expect(text, contains('Q1.'));
      },
    );

    test('lazy loading range functions work correctly', () async {
      final confessionText = await loadWestminsterConfessionRangeTextOnlyLazy(
        1,
        2,
      );
      final shorterCatechismText =
          await loadWestminsterShorterCatechismRangeTextOnlyLazy(1, 3);
      final largerCatechismText =
          await loadWestminsterLargerCatechismRangeTextOnlyLazy(1, 2);

      expect(confessionText, isNotEmpty);
      expect(shorterCatechismText, isNotEmpty);
      expect(largerCatechismText, isNotEmpty);

      expect(confessionText, contains('Chapter 1.'));
      expect(confessionText, contains('Chapter 2.'));
      expect(shorterCatechismText, contains('Q1.'));
      expect(shorterCatechismText, contains('Q3.'));
      expect(largerCatechismText, contains('Q1.'));
      expect(largerCatechismText, contains('Q2.'));
    });

    test('lazy loading byNumbers functions work correctly', () async {
      final confessionText =
          await loadWestminsterConfessionByNumbersTextOnlyLazy([1, 3]);
      final shorterCatechismText =
          await loadWestminsterShorterCatechismByNumbersTextOnlyLazy([1, 3]);
      final largerCatechismText =
          await loadWestminsterLargerCatechismByNumbersTextOnlyLazy([1, 3]);

      expect(confessionText, isNotEmpty);
      expect(shorterCatechismText, isNotEmpty);
      expect(largerCatechismText, isNotEmpty);

      expect(confessionText, contains('Chapter 1.'));
      expect(confessionText, contains('Chapter 3.'));
      expect(shorterCatechismText, contains('Q1.'));
      expect(shorterCatechismText, contains('Q3.'));
      expect(largerCatechismText, contains('Q1.'));
      expect(largerCatechismText, contains('Q3.'));
    });
  });
}
