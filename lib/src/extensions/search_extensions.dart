/// Search extensions for Westminster Standards search results
/// Provides convenient methods for working with search results

import '../types.dart';
import 'string_extensions.dart';

/// Extensions for WestminsterSearchResult
extension WestminsterSearchResultExtensions on WestminsterSearchResult {
  /// Get a formatted summary
  String get summary {
    switch (documentType) {
      case WestminsterDocumentType.shorterCatechism:
        return 'Shorter Catechism Q$number';
      case WestminsterDocumentType.largerCatechism:
        return 'Larger Catechism Q$number';
      case WestminsterDocumentType.confession:
        return 'Confession Chapter $number';
    }
  }

  /// Get a detailed summary with title
  String get detailedSummary {
    return '${summary}: $title';
  }

  /// Get highlighted matched text
  String get highlightedMatch {
    // This would need the original search term to highlight properly
    // For now, return the matched text as is
    return matchedText;
  }

  /// Get content summary (first 100 characters)
  String get contentSummary => content.summary;

  /// Get the word count of the content
  int get contentWordCount => content.wordCount;

  /// Check if this result has proof texts
  bool get hasProofTexts => proofTexts.isNotEmpty;

  /// Get the number of proof texts
  int get proofTextCount => proofTexts.length;

  /// Get a formatted display string
  String get displayString {
    final matchTypeStr = matchType.name.toUpperCase();
    return '${summary} [$matchTypeStr]: ${title.summary}';
  }

  /// Get a relevance score (simple implementation)
  double get relevanceScore {
    // Simple scoring based on match type
    switch (matchType) {
      case SearchMatchType.title:
        return 1.0; // Highest relevance
      case SearchMatchType.question:
        return 0.9;
      case SearchMatchType.content:
        return 0.7;
      case SearchMatchType.answer:
        return 0.8;
      case SearchMatchType.references:
        return 0.5; // Lowest relevance
    }
  }

  /// Get a formatted result with highlighted search term
  String getFormattedWithHighlight(String searchTerm) {
    final highlightedTitle = title.highlightSearchTerm(searchTerm);
    final highlightedContent = content.highlightSearchTerm(searchTerm);
    return '${summary}\n$highlightedTitle\n\n$highlightedContent';
  }
}

/// Extensions for collections of WestminsterSearchResult
extension WestminsterSearchResultsIterable
    on Iterable<WestminsterSearchResult> {
  /// Sort results by relevance score
  List<WestminsterSearchResult> get sortedByRelevance {
    final results = toList();
    results.sort((a, b) => b.relevanceScore.compareTo(a.relevanceScore));
    return results;
  }

  /// Group results by document type
  Map<WestminsterDocumentType, List<WestminsterSearchResult>>
  get groupedByDocument {
    final grouped = <WestminsterDocumentType, List<WestminsterSearchResult>>{};
    for (final result in this) {
      grouped.putIfAbsent(result.documentType, () => []).add(result);
    }
    return grouped;
  }

  /// Group results by match type
  Map<SearchMatchType, List<WestminsterSearchResult>> get groupedByMatchType {
    final grouped = <SearchMatchType, List<WestminsterSearchResult>>{};
    for (final result in this) {
      grouped.putIfAbsent(result.matchType, () => []).add(result);
    }
    return grouped;
  }

  /// Get results from a specific document type
  List<WestminsterSearchResult> fromDocument(
    WestminsterDocumentType documentType,
  ) {
    return where((result) => result.documentType == documentType).toList();
  }

  /// Get results with a specific match type
  List<WestminsterSearchResult> withMatchType(SearchMatchType matchType) {
    return where((result) => result.matchType == matchType).toList();
  }

  /// Get results that have proof texts
  List<WestminsterSearchResult> get withProofTexts {
    return where((result) => result.hasProofTexts).toList();
  }

  /// Get results without proof texts
  List<WestminsterSearchResult> get withoutProofTexts {
    return where((result) => !result.hasProofTexts).toList();
  }

  /// Get unique document types in the results
  List<WestminsterDocumentType> get uniqueDocumentTypes {
    return map((result) => result.documentType).toSet().toList();
  }

  /// Get unique match types in the results
  List<SearchMatchType> get uniqueMatchTypes {
    return map((result) => result.matchType).toSet().toList();
  }

  /// Get a summary of the search results
  String get searchSummary {
    final total = length;
    final byDoc = groupedByDocument;
    final byMatch = groupedByMatchType;

    final docSummary = byDoc.entries
        .map((e) => '${e.key.name}: ${e.value.length}')
        .join(', ');
    final matchSummary = byMatch.entries
        .map((e) => '${e.key.name}: ${e.value.length}')
        .join(', ');

    return 'Found $total results ($docSummary) - Match types: $matchSummary';
  }

  /// Get formatted results with highlighted search term
  List<String> getFormattedWithHighlight(String searchTerm) {
    return map(
      (result) => result.getFormattedWithHighlight(searchTerm),
    ).toList();
  }
}
