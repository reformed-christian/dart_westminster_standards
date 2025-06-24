/// Collection extensions for Westminster Standards data
/// Provides convenient methods for working with collections of Westminster Standards items

import '../models.dart';
import '../types.dart';

/// Extensions for collections of CatechismItem
extension CatechismItemsIterable on Iterable<CatechismItem> {
  /// Find a catechism question by number
  CatechismItem? findByNumber(int number) {
    try {
      return firstWhere((item) => item.number == number);
    } catch (e) {
      return null;
    }
  }

  /// Get questions in a range (inclusive)
  List<CatechismItem> getRange(int start, int end) {
    return where((item) => item.number >= start && item.number <= end).toList()
      ..sort((a, b) => a.number.compareTo(b.number));
  }

  /// Get questions by specific numbers
  List<CatechismItem> getByNumbers(List<int> numbers) {
    return where((item) => numbers.contains(item.number)).toList()
      ..sort((a, b) => a.number.compareTo(b.number));
  }

  /// Search within questions and answers
  List<CatechismItem> search(String query) {
    final lowerQuery = query.toLowerCase();
    return where(
      (item) =>
          item.question.toLowerCase().contains(lowerQuery) ||
          item.answer.toLowerCase().contains(lowerQuery),
    ).toList();
  }

  /// Search in specific parts of catechism items
  List<CatechismItem> searchInParts(String query, CatechismItemPart part) {
    final lowerQuery = query.toLowerCase();
    return where((item) {
      switch (part) {
        case CatechismItemPart.question:
          return item.question.toLowerCase().contains(lowerQuery);
        case CatechismItemPart.answer:
          return item.answer.toLowerCase().contains(lowerQuery);
        case CatechismItemPart.references:
          return item.allProofTexts.any(
            (pt) => pt.reference.toLowerCase().contains(lowerQuery),
          );
        case CatechismItemPart.questionAndAnswer:
          return item.question.toLowerCase().contains(lowerQuery) ||
              item.answer.toLowerCase().contains(lowerQuery);
        case CatechismItemPart.questionAndReferences:
          return item.question.toLowerCase().contains(lowerQuery) ||
              item.allProofTexts.any(
                (pt) => pt.reference.toLowerCase().contains(lowerQuery),
              );
        case CatechismItemPart.answerAndReferences:
          return item.answer.toLowerCase().contains(lowerQuery) ||
              item.allProofTexts.any(
                (pt) => pt.reference.toLowerCase().contains(lowerQuery),
              );
        case CatechismItemPart.all:
          return item.question.toLowerCase().contains(lowerQuery) ||
              item.answer.toLowerCase().contains(lowerQuery) ||
              item.allProofTexts.any(
                (pt) => pt.reference.toLowerCase().contains(lowerQuery),
              );
      }
    }).toList();
  }

  /// Get all proof texts from all items
  List<ProofText> getAllProofTexts() {
    return expand((item) => item.allProofTexts).toList();
  }

  /// Get text-only content (without scripture references)
  String get textOnly {
    return map(
      (item) => 'Q${item.number}. ${item.question}\n\n${item.answer}',
    ).join('\n\n');
  }

  /// Get range text-only content
  String getRangeTextOnly(int start, int end) {
    return getRange(start, end)
        .map((item) => 'Q${item.number}. ${item.question}\n\n${item.answer}')
        .join('\n\n');
  }

  /// Get by numbers text-only content
  String getByNumbersTextOnly(List<int> numbers) {
    return getByNumbers(numbers)
        .map((item) => 'Q${item.number}. ${item.question}\n\n${item.answer}')
        .join('\n\n');
  }
}

/// Extensions for collections of ConfessionChapter
extension ConfessionChaptersIterable on Iterable<ConfessionChapter> {
  /// Find a chapter by number
  ConfessionChapter? findByNumber(int number) {
    try {
      return firstWhere((chapter) => chapter.number == number);
    } catch (e) {
      return null;
    }
  }

  /// Get chapters in a range (inclusive)
  List<ConfessionChapter> getRange(int start, int end) {
    return where(
        (chapter) => chapter.number >= start && chapter.number <= end,
      ).toList()
      ..sort((a, b) => a.number.compareTo(b.number));
  }

  /// Get chapters by specific numbers
  List<ConfessionChapter> getByNumbers(List<int> numbers) {
    return where((chapter) => numbers.contains(chapter.number)).toList()
      ..sort((a, b) => a.number.compareTo(b.number));
  }

  /// Search within chapter titles and content
  List<ConfessionChapter> search(String query) {
    final lowerQuery = query.toLowerCase();
    return where(
      (chapter) =>
          chapter.title.toLowerCase().contains(lowerQuery) ||
          chapter.sections.any(
            (section) => section.text.toLowerCase().contains(lowerQuery),
          ),
    ).toList();
  }

  /// Search in chapter titles only
  List<ConfessionChapter> searchInTitles(String query) {
    final lowerQuery = query.toLowerCase();
    return where(
      (chapter) => chapter.title.toLowerCase().contains(lowerQuery),
    ).toList();
  }

  /// Search in chapter content only
  List<ConfessionChapter> searchInContent(String query) {
    final lowerQuery = query.toLowerCase();
    return where(
      (chapter) => chapter.sections.any(
        (section) => section.text.toLowerCase().contains(lowerQuery),
      ),
    ).toList();
  }

  /// Get all proof texts from all chapters
  List<ProofText> getAllProofTexts() {
    return expand(
      (chapter) => chapter.sections.expand((section) => section.allProofTexts),
    ).toList();
  }

  /// Get text-only content (without scripture references)
  String get textOnly {
    return map(
      (chapter) =>
          'Chapter ${chapter.number}. ${chapter.title}\n\n${chapter.sections.map((s) => s.text).join('\n\n')}',
    ).join('\n\n');
  }

  /// Get range text-only content
  String getRangeTextOnly(int start, int end) {
    return getRange(start, end)
        .map(
          (chapter) =>
              'Chapter ${chapter.number}. ${chapter.title}\n\n${chapter.sections.map((s) => s.text).join('\n\n')}',
        )
        .join('\n\n');
  }

  /// Get by numbers text-only content
  String getByNumbersTextOnly(List<int> numbers) {
    return getByNumbers(numbers)
        .map(
          (chapter) =>
              'Chapter ${chapter.number}. ${chapter.title}\n\n${chapter.sections.map((s) => s.text).join('\n\n')}',
        )
        .join('\n\n');
  }
}

/// Extensions for collections of ProofText
extension ProofTextsIterable on Iterable<ProofText> {
  /// Search in proof text references
  List<ProofText> searchInReferences(String query) {
    final lowerQuery = query.toLowerCase();
    return where(
      (pt) => pt.reference.toLowerCase().contains(lowerQuery),
    ).toList();
  }

  /// Search in proof text content
  List<ProofText> searchInContent(String query) {
    final lowerQuery = query.toLowerCase();
    return where((pt) => pt.text.toLowerCase().contains(lowerQuery)).toList();
  }

  /// Get unique references
  List<String> get uniqueReferences {
    return map((pt) => pt.reference).toSet().toList()..sort();
  }

  /// Group by reference
  Map<String, List<ProofText>> get groupedByReference {
    final grouped = <String, List<ProofText>>{};
    for (final pt in this) {
      grouped.putIfAbsent(pt.reference, () => []).add(pt);
    }
    return grouped;
  }
}
