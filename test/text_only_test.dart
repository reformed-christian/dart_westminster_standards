import 'package:test/test.dart';
import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() {
  group('Text Only Tests', () {
    test('should provide text-only access to Westminster Standards', () async {
      final standards = await WestminsterStandards.create();

      // Test text-only access
      expect(standards.confessionTextOnly, isNotEmpty);
      expect(standards.shorterCatechismTextOnly, isNotEmpty);
      expect(standards.largerCatechismTextOnly, isNotEmpty);

      // Test that text-only content doesn't contain scripture references
      expect(standards.confessionTextOnly, isNot(contains('Gen.')));
      expect(standards.shorterCatechismTextOnly, isNot(contains('John')));
    });
  });
}
