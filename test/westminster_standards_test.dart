import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/services.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Westminster Standards Individual Loading Tests', () {
    test('initializeWestminsterStandards loads all data by default', () async {
      clearWestminsterStandardsCache();
      await initializeWestminsterStandards();
      expect(isInitialized, isTrue);
    });

    test(
      'initializeWestminsterStandards can load specific documents',
      () async {
        clearWestminsterStandardsCache();
        // Test loading only confession
        await initializeWestminsterStandards(WestminsterDocument.confession);
        expect(isDocumentInitialized(WestminsterDocument.confession), isTrue);
        expect(
          isDocumentInitialized(WestminsterDocument.shorterCatechism),
          isFalse,
        );
        expect(
          isDocumentInitialized(WestminsterDocument.largerCatechism),
          isFalse,
        );

        // Test loading only shorter catechism
        await initializeWestminsterStandards(
          WestminsterDocument.shorterCatechism,
        );
        expect(
          isDocumentInitialized(WestminsterDocument.confession),
          isTrue,
        ); // Still loaded from previous call
        expect(
          isDocumentInitialized(WestminsterDocument.shorterCatechism),
          isTrue,
        );
        expect(
          isDocumentInitialized(WestminsterDocument.largerCatechism),
          isFalse,
        );
      },
    );

    test('isDocumentInitialized works correctly', () async {
      clearWestminsterStandardsCache();
      await initializeWestminsterStandards();
      expect(isDocumentInitialized(WestminsterDocument.all), isTrue);
      expect(isDocumentInitialized(WestminsterDocument.confession), isTrue);
      expect(
        isDocumentInitialized(WestminsterDocument.shorterCatechism),
        isTrue,
      );
      expect(
        isDocumentInitialized(WestminsterDocument.largerCatechism),
        isTrue,
      );
    });

    test(
      'loadWestminsterShorterCatechismQuestion returns correct question',
      () async {
        clearWestminsterStandardsCache();
        await initializeWestminsterStandards();
        final question = loadWestminsterShorterCatechismQuestion(1);

        expect(question, isNotNull);
        expect(question!.number, equals(1));
        expect(question.question, contains('chief end of man'));
        expect(question.answer, contains('glorify God'));
      },
    );

    test(
      'loadWestminsterShorterCatechismQuestion returns null for invalid number',
      () async {
        clearWestminsterStandardsCache();
        await initializeWestminsterStandards();
        final question = loadWestminsterShorterCatechismQuestion(999);

        expect(question, isNull);
      },
    );

    test(
      'loadWestminsterLargerCatechismQuestion returns correct question',
      () async {
        clearWestminsterStandardsCache();
        await initializeWestminsterStandards();
        final question = loadWestminsterLargerCatechismQuestion(1);

        expect(question, isNotNull);
        expect(question!.number, equals(1));
        expect(question.question, contains('chief and highest end'));
        expect(question.answer, contains('glorify God'));
      },
    );

    test(
      'loadWestminsterLargerCatechismQuestion returns null for invalid number',
      () async {
        clearWestminsterStandardsCache();
        await initializeWestminsterStandards();
        final question = loadWestminsterLargerCatechismQuestion(999);

        expect(question, isNull);
      },
    );

    test('loadWestminsterConfessionChapter returns correct chapter', () async {
      clearWestminsterStandardsCache();
      await initializeWestminsterStandards();
      final chapter = loadWestminsterConfessionChapter(1);

      expect(chapter, isNotNull);
      expect(chapter!.number, equals(1));
      expect(chapter.title, contains('Holy Scripture'));
      expect(chapter.sections, isNotEmpty);
    });

    test(
      'loadWestminsterConfessionChapter returns null for invalid number',
      () async {
        clearWestminsterStandardsCache();
        await initializeWestminsterStandards();
        final chapter = loadWestminsterConfessionChapter(999);

        expect(chapter, isNull);
      },
    );

    test('getWestminsterConfession returns cached data', () async {
      clearWestminsterStandardsCache();
      await initializeWestminsterStandards();
      final confession1 = getWestminsterConfession();
      final confession2 = getWestminsterConfession();

      expect(confession1, equals(confession2));
      expect(confession1.length, greaterThan(0));
    });

    test('getWestminsterShorterCatechism returns cached data', () async {
      clearWestminsterStandardsCache();
      await initializeWestminsterStandards();
      final catechism1 = getWestminsterShorterCatechism();
      final catechism2 = getWestminsterShorterCatechism();

      expect(catechism1, equals(catechism2));
      expect(catechism1.length, greaterThan(0));
    });

    test('getWestminsterLargerCatechism returns cached data', () async {
      clearWestminsterStandardsCache();
      await initializeWestminsterStandards();
      final catechism1 = getWestminsterLargerCatechism();
      final catechism2 = getWestminsterLargerCatechism();

      expect(catechism1, equals(catechism2));
      expect(catechism1.length, greaterThan(0));
    });

    test('functions work with selective initialization', () async {
      clearWestminsterStandardsCache();
      // Only initialize confession
      await initializeWestminsterStandards(WestminsterDocument.confession);

      // Shorter catechism should return null since it's not initialized
      final question = loadWestminsterShorterCatechismQuestion(1);
      expect(question, isNull);

      // Confession should work since it's initialized
      final chapter = loadWestminsterConfessionChapter(1);
      expect(chapter, isNotNull);

      // Now initialize shorter catechism
      await initializeWestminsterStandards(
        WestminsterDocument.shorterCatechism,
      );

      // Now it should work
      final question2 = loadWestminsterShorterCatechismQuestion(1);
      expect(question2, isNotNull);
    });

    // Lazy load function tests
    test(
      'loadWestminsterConfessionLazy auto-initializes and returns data',
      () async {
        clearWestminsterStandardsCache();
        final confession = await loadWestminsterConfessionLazy();

        expect(confession, isNotNull);
        expect(confession.length, greaterThan(0));
        expect(isDocumentInitialized(WestminsterDocument.confession), isTrue);
      },
    );

    test(
      'loadWestminsterShorterCatechismLazy auto-initializes and returns data',
      () async {
        clearWestminsterStandardsCache();
        final catechism = await loadWestminsterShorterCatechismLazy();

        expect(catechism, isNotNull);
        expect(catechism.length, greaterThan(0));
        expect(
          isDocumentInitialized(WestminsterDocument.shorterCatechism),
          isTrue,
        );
      },
    );

    test(
      'loadWestminsterLargerCatechismLazy auto-initializes and returns data',
      () async {
        clearWestminsterStandardsCache();
        final catechism = await loadWestminsterLargerCatechismLazy();

        expect(catechism, isNotNull);
        expect(catechism.length, greaterThan(0));
        expect(
          isDocumentInitialized(WestminsterDocument.largerCatechism),
          isTrue,
        );
      },
    );

    test(
      'loadWestminsterShorterCatechismQuestionLazy auto-initializes and returns question',
      () async {
        clearWestminsterStandardsCache();
        final question = await loadWestminsterShorterCatechismQuestionLazy(1);

        expect(question, isNotNull);
        expect(question!.number, equals(1));
        expect(question.question, contains('chief end of man'));
        expect(
          isDocumentInitialized(WestminsterDocument.shorterCatechism),
          isTrue,
        );
      },
    );

    test(
      'loadWestminsterLargerCatechismQuestionLazy auto-initializes and returns question',
      () async {
        clearWestminsterStandardsCache();
        final question = await loadWestminsterLargerCatechismQuestionLazy(1);

        expect(question, isNotNull);
        expect(question!.number, equals(1));
        expect(question.question, contains('chief and highest end'));
        expect(
          isDocumentInitialized(WestminsterDocument.largerCatechism),
          isTrue,
        );
      },
    );

    test(
      'loadWestminsterConfessionChapterLazy auto-initializes and returns chapter',
      () async {
        clearWestminsterStandardsCache();
        final chapter = await loadWestminsterConfessionChapterLazy(1);

        expect(chapter, isNotNull);
        expect(chapter!.number, equals(1));
        expect(chapter.title, contains('Holy Scripture'));
        expect(isDocumentInitialized(WestminsterDocument.confession), isTrue);
      },
    );

    test('lazy functions work with selective initialization', () async {
      clearWestminsterStandardsCache();

      // Lazy functions should auto-initialize and work
      final question = await loadWestminsterShorterCatechismQuestionLazy(1);
      expect(question, isNotNull);
      expect(
        isDocumentInitialized(WestminsterDocument.shorterCatechism),
        isTrue,
      );

      final chapter = await loadWestminsterConfessionChapterLazy(1);
      expect(chapter, isNotNull);
      expect(isDocumentInitialized(WestminsterDocument.confession), isTrue);
    });
  });

  group('WestminsterStandards Object Tests', () {
    test('WestminsterStandards object can be created', () async {
      final standards = await WestminsterStandards.create();
      expect(standards, isNotNull);
    });

    test('WestminsterStandards object provides enhanced access', () async {
      final standards = await WestminsterStandards.create();
      // Test enhanced accessors
      expect(standards.confession, isNotNull);
      expect(standards.shorterCatechism, isNotNull);
      expect(standards.largerCatechism, isNotNull);
      // Test enhanced search
      final godQuestions = standards.shorterCatechism.exactStr('God');
      expect(godQuestions, isNotEmpty);
      final godChapters = standards.confession.exactStr('God');
      expect(godChapters, isNotEmpty);
    });
  });
}
