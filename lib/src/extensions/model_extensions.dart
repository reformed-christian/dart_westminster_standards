/// Model extensions for Westminster Standards data models
/// Provides convenient methods for working with Westminster Standards objects

import '../models.dart';
import '../types.dart';
import 'string_extensions.dart';

/// Extensions for CatechismItem
extension CatechismItemExtensions on CatechismItem {
  /// Get the full text (question + answer)
  String get fullText => '$question $answer';

  /// Get text without scripture references
  String get textOnly => fullText.withoutScriptureReferences;

  /// Check if this item contains a specific search term
  bool contains(String searchTerm) {
    final lowerTerm = searchTerm.toLowerCase();
    return question.toLowerCase().contains(lowerTerm) ||
        answer.toLowerCase().contains(lowerTerm) ||
        allProofTexts.any(
          (pt) => pt.reference.toLowerCase().contains(lowerTerm),
        );
  }

  /// Get a formatted display string
  String get displayString => 'Q$number: $question';

  /// Get a short summary (first sentence of answer)
  String get summary => answer.firstSentence;

  /// Get the number of proof texts
  int get proofTextCount => allProofTexts.length;

  /// Check if this item has proof texts
  bool get hasProofTexts => allProofTexts.isNotEmpty;

  /// Get unique scripture references
  List<String> get uniqueReferences {
    return allProofTexts.map((pt) => pt.reference).toSet().toList()..sort();
  }

  /// Get proof texts grouped by reference
  Map<String, List<ProofText>> get proofTextsByReference {
    final grouped = <String, List<ProofText>>{};
    for (final pt in allProofTexts) {
      grouped.putIfAbsent(pt.reference, () => []).add(pt);
    }
    return grouped;
  }

  /// Get a formatted text with highlighted search terms
  String getFormattedWithHighlight(String searchTerm) {
    final highlightedQuestion = question.highlightSearchTerm(searchTerm);
    final highlightedAnswer = answer.highlightSearchTerm(searchTerm);
    return 'Q$number: $highlightedQuestion\n\n$highlightedAnswer';
  }

  /// Get the word count of the answer
  int get answerWordCount => answer.wordCount;

  /// Get the word count of the question
  int get questionWordCount => question.wordCount;

  /// Get the total word count
  int get totalWordCount => questionWordCount + answerWordCount;
}

/// Extensions for ConfessionChapter
extension ConfessionChapterExtensions on ConfessionChapter {
  /// Get all text from all sections
  String get fullText => sections.map((s) => s.text).join(' ');

  /// Get text without scripture references
  String get textOnly => fullText.withoutScriptureReferences;

  /// Get a formatted display string
  String get displayString => 'Chapter $number: $title';

  /// Check if this chapter contains a specific search term
  bool contains(String searchTerm) {
    final lowerTerm = searchTerm.toLowerCase();
    return title.toLowerCase().contains(lowerTerm) ||
        sections.any(
          (section) => section.text.toLowerCase().contains(lowerTerm),
        );
  }

  /// Get a short summary (first sentence of first section)
  String get summary {
    if (sections.isEmpty) return title;
    return sections.first.text.firstSentence;
  }

  /// Get the number of sections
  int get sectionCount => sections.length;

  /// Get all proof texts from all sections
  List<ProofText> get allProofTexts {
    return sections.expand((section) => section.allProofTexts).toList();
  }

  /// Get the number of proof texts
  int get proofTextCount => allProofTexts.length;

  /// Check if this chapter has proof texts
  bool get hasProofTexts => allProofTexts.isNotEmpty;

  /// Get unique scripture references
  List<String> get uniqueReferences {
    return allProofTexts.map((pt) => pt.reference).toSet().toList()..sort();
  }

  /// Get proof texts grouped by reference
  Map<String, List<ProofText>> get proofTextsByReference {
    final grouped = <String, List<ProofText>>{};
    for (final pt in allProofTexts) {
      grouped.putIfAbsent(pt.reference, () => []).add(pt);
    }
    return grouped;
  }

  /// Get a formatted text with highlighted search terms
  String getFormattedWithHighlight(String searchTerm) {
    final highlightedTitle = title.highlightSearchTerm(searchTerm);
    final highlightedSections = sections
        .map((s) => s.text.highlightSearchTerm(searchTerm))
        .join('\n\n');
    return 'Chapter $number: $highlightedTitle\n\n$highlightedSections';
  }

  /// Get the word count of all sections
  int get totalWordCount =>
      sections.fold(0, (sum, s) => sum + s.text.wordCount);

  /// Get the average word count per section
  double get averageWordsPerSection {
    if (sections.isEmpty) return 0;
    return totalWordCount / sections.length;
  }
}

/// Extensions for ConfessionSection
extension ConfessionSectionExtensions on ConfessionSection {
  /// Get text without scripture references
  String get textOnly => text.withoutScriptureReferences;

  /// Check if this section contains a specific search term
  bool contains(String searchTerm) {
    final lowerTerm = searchTerm.toLowerCase();
    return text.toLowerCase().contains(lowerTerm) ||
        allProofTexts.any(
          (pt) => pt.reference.toLowerCase().contains(lowerTerm),
        );
  }

  /// Get a short summary (first sentence)
  String get summary => text.firstSentence;

  /// Get the number of proof texts
  int get proofTextCount => allProofTexts.length;

  /// Check if this section has proof texts
  bool get hasProofTexts => allProofTexts.isNotEmpty;

  /// Get unique scripture references
  List<String> get uniqueReferences {
    return allProofTexts.map((pt) => pt.reference).toSet().toList()..sort();
  }

  /// Get the word count
  int get wordCount => text.wordCount;

  /// Get a formatted text with highlighted search terms
  String getFormattedWithHighlight(String searchTerm) {
    return text.highlightSearchTerm(searchTerm);
  }
}

/// Extensions for ProofText
extension ProofTextExtensions on ProofText {
  /// Get text without scripture references
  String get textOnly => text.withoutScriptureReferences;

  /// Check if this proof text contains a specific search term
  bool contains(String searchTerm) {
    final lowerTerm = searchTerm.toLowerCase();
    return reference.toLowerCase().contains(lowerTerm) ||
        text.toLowerCase().contains(lowerTerm);
  }

  /// Get a short summary (first sentence)
  String get summary => text.firstSentence;

  /// Get the word count
  int get wordCount => text.wordCount;

  /// Get a formatted display string
  String get displayString => '$reference: $text';

  /// Get a formatted text with highlighted search terms
  String getFormattedWithHighlight(String searchTerm) {
    final highlightedReference = reference.highlightSearchTerm(searchTerm);
    final highlightedText = text.highlightSearchTerm(searchTerm);
    return '$highlightedReference: $highlightedText';
  }
}
