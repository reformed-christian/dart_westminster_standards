import 'package:flutter_test/flutter_test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Enhanced Access Tests', () {
    late WestminsterStandards standards;

    setUpAll(() async {
      standards = await WestminsterStandards.create();
    });

    test('should access shorter catechism with exactStr method', () {
      final results = standards.shorterCatechism.exactStr('God');
      expect(results, isNotEmpty);
      expect(results.first, isA<CatechismItem>());
    });

    test('should access confession with exactStr method', () {
      final results = standards.confession.exactStr('God');
      expect(results, isNotEmpty);
      expect(results.first, isA<ConfessionChapter>());
    });

    test('should access larger catechism with exactStr method', () {
      final results = standards.largerCatechism.exactStr('God');
      expect(results, isNotEmpty);
      expect(results.first, isA<CatechismItem>());
    });

    test('should find specific question by number', () {
      final question = standards.shorterCatechism.getQuestion(1);
      expect(question, isNotNull);
      expect(question!.number, equals(1));
    });

    test('should find specific chapter by number', () {
      final chapter = standards.confession.getChapter(1);
      expect(chapter, isNotNull);
      expect(chapter!.number, equals(1));
    });

    test('should get questions in range', () {
      final questions = standards.shorterCatechism.range(1, 5);
      expect(questions.length, equals(5));
      expect(questions.first.number, equals(1));
      expect(questions.last.number, equals(5));
    });

    test('should get chapters in range', () {
      final chapters = standards.confession.range(1, 2);
      expect(chapters.length, equals(2));
      expect(chapters.first.number, equals(1));
      expect(chapters.last.number, equals(2));
    });

    test('should find questions by multiple numbers', () {
      final questions = standards.shorterCatechism.byNumbers([1, 3, 5]);
      expect(questions.length, equals(3));
      expect(questions.map((q) => q.number).toSet(), equals({1, 3, 5}));
    });

    test('should find chapters by multiple numbers', () {
      final chapters = standards.confession.byNumbers([1, 2]);
      expect(chapters.length, equals(2));
      expect(chapters.map((c) => c.number).toSet(), equals({1, 2}));
    });

    test('should search questions by question content only', () {
      final results = standards.shorterCatechism.questionContains('What');
      expect(results, isNotEmpty);
      expect(
        results.every((q) => q.question.toLowerCase().contains('what')),
        isTrue,
      );
    });

    test('should search questions by answer content only', () {
      final results = standards.shorterCatechism.answerContains('God');
      expect(results, isNotEmpty);
      expect(
        results.every((q) => q.answer.toLowerCase().contains('god')),
        isTrue,
      );
    });

    test('should search chapters by title only', () {
      final results = standards.confession.titleContains('God');
      expect(results, isNotEmpty);
      expect(
        results.every((c) => c.title.toLowerCase().contains('god')),
        isTrue,
      );
    });

    test('should search chapters by content only', () {
      final results = standards.confession.contentContains('God');
      expect(results, isNotEmpty);
    });

    test('should find sections containing text', () {
      final sections = standards.confession.findSections('God');
      expect(sections, isNotEmpty);
      expect(sections.first, isA<ConfessionSection>());
    });

    test('should support index access', () {
      final firstQuestion = standards.shorterCatechism[0];
      expect(firstQuestion, isA<CatechismItem>());
      expect(firstQuestion.number, equals(1));
    });

    test('should check empty state', () {
      expect(standards.shorterCatechism.isNotEmpty, isTrue);
      expect(standards.shorterCatechism.isEmpty, isFalse);
    });

    test('should get all proof texts from catechism', () {
      final proofTexts = standards.shorterCatechism.allProofTexts;
      expect(proofTexts, isNotEmpty);
    });

    test('should get all proof texts from confession', () {
      final proofTexts = standards.confession.allProofTexts;
      expect(proofTexts, isNotEmpty);
    });

    test('should get all sections from confession', () {
      final sections = standards.confession.allSections;
      expect(sections, isNotEmpty);
      expect(sections.first, isA<ConfessionSection>());
    });

    group('CatechismItemPart Tests', () {
      test('should search questions only', () {
        final results = standards.shorterCatechism.exactStr(
          'What',
          CatechismItemPart.question,
        );
        expect(results, isNotEmpty);
        expect(
          results.every((q) => q.question.toLowerCase().contains('what')),
          isTrue,
        );
      });

      test('should search answers only', () {
        final results = standards.shorterCatechism.exactStr(
          'God',
          CatechismItemPart.answer,
        );
        expect(results, isNotEmpty);
        expect(
          results.every((q) => q.answer.toLowerCase().contains('god')),
          isTrue,
        );
      });

      test('should search references only', () {
        final results = standards.shorterCatechism.exactStr(
          'John',
          CatechismItemPart.references,
        );
        expect(results, isNotEmpty);
        expect(
          results.every(
            (q) => q.allProofTexts.any(
              (pt) => pt.reference.toLowerCase().contains('john'),
            ),
          ),
          isTrue,
        );
      });

      test('should search question and answer', () {
        final results = standards.shorterCatechism.exactStr(
          'God',
          CatechismItemPart.questionAndAnswer,
        );
        expect(results, isNotEmpty);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god'),
          ),
          isTrue,
        );
      });

      test('should search question and references', () {
        final results = standards.shorterCatechism.exactStr(
          'John',
          CatechismItemPart.questionAndReferences,
        );
        expect(results, isNotEmpty);
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

      test('should search answer and references', () {
        final results = standards.shorterCatechism.exactStr(
          'God',
          CatechismItemPart.answerAndReferences,
        );
        expect(results, isNotEmpty);
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

      test('should search all fields by default', () {
        final results = standards.shorterCatechism.exactStr('God');
        expect(results, isNotEmpty);
        expect(
          results.every(
            (q) =>
                q.question.toLowerCase().contains('god') ||
                q.answer.toLowerCase().contains('god') ||
                q.allProofTexts.any(
                  (pt) => pt.reference.toLowerCase().contains('god'),
                ),
          ),
          isTrue,
        );
      });

      test(
        'should find questions with references containing specific text',
        () {
          final results = standards.shorterCatechism.referencesContain('John');
          expect(results, isNotEmpty);
          expect(
            results.every(
              (q) => q.allProofTexts.any(
                (pt) => pt.reference.toLowerCase().contains('john'),
              ),
            ),
            isTrue,
          );
        },
      );
    });
  });
}
