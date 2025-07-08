import 'package:test/test.dart';
import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() {
  group('Range Search Tests', () {
    test('should search ranges of Westminster Standards', () async {
      final standards = await WestminsterStandards.create();

      // Test range search
      final questions = standards.shorterCatechism.searchRange(1, 5, 'God');
      expect(questions, isNotEmpty);

      final chapters = standards.confession.searchRange(1, 2, 'God');
      expect(chapters, isNotEmpty);
    });
  });
}
