import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Range Access Tests', () {
    test('should access ranges of Westminster Standards', () async {
      final standards = await WestminsterStandards.create();

      // Test range access
      final questions = standards.shorterCatechism.range(1, 5);
      expect(questions.length, equals(5));
      expect(questions.first.number, equals(1));
      expect(questions.last.number, equals(5));

      final chapters = standards.confession.range(1, 2);
      expect(chapters.length, equals(2));
      expect(chapters.first.number, equals(1));
      expect(chapters.last.number, equals(2));
    });
  });
}
