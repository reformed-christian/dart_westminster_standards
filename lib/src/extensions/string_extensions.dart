/// String extensions for Westminster Standards text processing
/// Provides convenient methods for working with text content

/// Extensions for String to add Westminster Standards specific text processing
extension WestminsterTextExtensions on String {
  /// Remove scripture references from text (e.g., [Gen 1:1])
  String get withoutScriptureReferences {
    return replaceAll(RegExp(r'\[[^\]]+\]'), '').trim();
  }

  /// Extract scripture references from text
  List<String> get scriptureReferences {
    final matches = RegExp(r'\[([^\]]+)\]').allMatches(this);
    return matches.map((m) => m.group(1)!).toList();
  }

  /// Highlight search terms in text with markdown-style bold
  String highlightSearchTerm(String searchTerm) {
    final regex = RegExp(searchTerm, caseSensitive: false);
    return replaceAllMapped(regex, (match) => '**${match.group(0)}**');
  }

  /// Get a summary of the text (first 100 characters)
  String get summary {
    if (length <= 100) return this;
    return '${substring(0, 100)}...';
  }

  /// Count words in the text
  int get wordCount {
    return split(RegExp(r'\s+')).where((word) => word.isNotEmpty).length;
  }

  /// Check if text contains any scripture references
  bool get hasScriptureReferences {
    return RegExp(r'\[[^\]]+\]').hasMatch(this);
  }

  /// Get text with scripture references formatted as links
  String get withScriptureLinks {
    return replaceAllMapped(
      RegExp(r'\[([^\]]+)\]'),
      (match) => '[${match.group(1)}](scripture://${match.group(1)})',
    );
  }

  /// Clean up extra whitespace and normalize line breaks
  String get normalized {
    return replaceAll(
      RegExp(r'\s+'),
      ' ',
    ).replaceAll(RegExp(r'\n\s*\n'), '\n\n').trim();
  }

  /// Split text into sentences
  List<String> get sentences {
    return split(
      RegExp(r'[.!?]+'),
    ).map((s) => s.trim()).where((s) => s.isNotEmpty).toList();
  }

  /// Get the first sentence
  String get firstSentence {
    final sentences = this.sentences;
    return sentences.isNotEmpty ? sentences.first : this;
  }
}
