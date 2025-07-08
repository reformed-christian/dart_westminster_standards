import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Enhanced Access Tests', () {
    test('should provide enhanced access to Westminster Standards', () async {
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
