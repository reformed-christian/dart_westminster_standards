/// Types and enums for Westminster Standards

// Re-export generic catechism types
export 'package:dart_catechism/dart_catechism.dart' show CatechismItemPart;

/// Enum for selecting which Westminster Standards documents to initialize
enum WestminsterDocument { confession, shorterCatechism, largerCatechism, all }

/// Document types for unified search results
enum WestminsterDocumentType { confession, shorterCatechism, largerCatechism }

/// Types of search matches for unified search results
enum SearchMatchType { title, content, question, answer, references }

/// Unified search result for searching across all Westminster Standards
class WestminsterSearchResult {
  /// The type of document this result comes from
  final WestminsterDocumentType documentType;

  /// The number (chapter number or question number)
  final int number;

  /// The title (chapter title or question text)
  final String title;

  /// The content (chapter content or answer text)
  final String content;

  /// All proof texts associated with this item
  final List<dynamic> proofTexts;

  /// The specific text that matched the search
  final String matchedText;

  /// Where the match was found
  final SearchMatchType matchType;

  const WestminsterSearchResult({
    required this.documentType,
    required this.number,
    required this.title,
    required this.content,
    required this.proofTexts,
    required this.matchedText,
    required this.matchType,
  });

  @override
  String toString() {
    return 'WestminsterSearchResult(documentType: $documentType, number: $number, title: "$title", matchType: $matchType)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is WestminsterSearchResult &&
        other.documentType == documentType &&
        other.number == number &&
        other.title == title &&
        other.content == content &&
        other.matchedText == matchedText &&
        other.matchType == matchType;
  }

  @override
  int get hashCode {
    return Object.hash(
      documentType,
      number,
      title,
      content,
      matchedText,
      matchType,
    );
  }
}
