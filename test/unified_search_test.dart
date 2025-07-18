import 'package:test/test.dart';
import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() {
  group('Unified Search Tests', () {
    test(
      'should perform unified search across all Westminster Standards',
      () async {
        final standards = await WestminsterStandards.create();

        // Test unified search
        final results = standards.searchAll('God');
        expect(results, isNotEmpty);

        // Verify results contain different document types
        final hasConfession = results.any(
          (r) => r.documentType == WestminsterDocumentType.confession,
        );
        final hasShorterCatechism = results.any(
          (r) => r.documentType == WestminsterDocumentType.shorterCatechism,
        );
        final hasLargerCatechism = results.any(
          (r) => r.documentType == WestminsterDocumentType.largerCatechism,
        );

        expect(
          hasConfession || hasShorterCatechism || hasLargerCatechism,
          isTrue,
        );
      },
    );
  });
}
