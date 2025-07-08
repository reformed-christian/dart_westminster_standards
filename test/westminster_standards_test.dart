import 'package:test/test.dart';
import 'package:westminster_standards/westminster_standards.dart';

void main() {
  group('Westminster Standards Tests', () {
    test('should load Westminster Confession', () async {
      final standards = await WestminsterStandards.create();
      expect(standards.confessionList, isNotEmpty);
    });

    test('should load Westminster Shorter Catechism', () async {
      final standards = await WestminsterStandards.create();
      expect(standards.shorterCatechismList, isNotEmpty);
    });

    test('should load Westminster Larger Catechism', () async {
      final standards = await WestminsterStandards.create();
      expect(standards.largerCatechismList, isNotEmpty);
    });
  });
}
