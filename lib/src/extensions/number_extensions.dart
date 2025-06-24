/// Number extensions for Westminster Standards validation and formatting
/// Provides convenient methods for working with chapter and question numbers

/// Extensions for int to add Westminster Standards specific validation and formatting
extension WestminsterNumberExtensions on int {
  /// Check if this is a valid Shorter Catechism question number
  bool get isValidShorterCatechismNumber => this >= 1 && this <= 107;

  /// Check if this is a valid Larger Catechism question number
  bool get isValidLargerCatechismNumber => this >= 1 && this <= 196;

  /// Check if this is a valid Confession chapter number
  bool get isValidConfessionChapterNumber => this >= 1 && this <= 33;

  /// Check if this is a valid Westminster Standards number for any document
  bool get isValidWestminsterNumber =>
      isValidShorterCatechismNumber ||
      isValidLargerCatechismNumber ||
      isValidConfessionChapterNumber;

  /// Format as a question number
  String get asQuestionNumber => 'Q$this';

  /// Format as a chapter number
  String get asChapterNumber => 'Chapter $this';

  /// Get the document type this number belongs to
  String get documentType {
    if (isValidShorterCatechismNumber) return 'Shorter Catechism';
    if (isValidLargerCatechismNumber) return 'Larger Catechism';
    if (isValidConfessionChapterNumber) return 'Confession';
    return 'Unknown';
  }

  /// Get the total count for the document type this number belongs to
  int get totalCount {
    if (isValidShorterCatechismNumber) return 107;
    if (isValidLargerCatechismNumber) return 196;
    if (isValidConfessionChapterNumber) return 33;
    return 0;
  }

  /// Check if this is the first item in its document
  bool get isFirst => this == 1;

  /// Check if this is the last item in its document
  bool get isLast {
    if (isValidShorterCatechismNumber) return this == 107;
    if (isValidLargerCatechismNumber) return this == 196;
    if (isValidConfessionChapterNumber) return this == 33;
    return false;
  }

  /// Get the next valid number in the same document
  int? get next {
    if (isLast) return null;
    if (isValidShorterCatechismNumber) return this + 1;
    if (isValidLargerCatechismNumber) return this + 1;
    if (isValidConfessionChapterNumber) return this + 1;
    return null;
  }

  /// Get the previous valid number in the same document
  int? get previous {
    if (isFirst) return null;
    if (isValidShorterCatechismNumber) return this - 1;
    if (isValidLargerCatechismNumber) return this - 1;
    if (isValidConfessionChapterNumber) return this - 1;
    return null;
  }

  /// Get a range starting from this number
  List<int> rangeTo(int end) {
    if (end < this) return [];
    return List.generate(end - this + 1, (index) => this + index);
  }

  /// Get a formatted string with validation
  String get formattedWithValidation {
    if (!isValidWestminsterNumber) {
      return '$this (Invalid Westminster Standards number)';
    }
    return '$asQuestionNumber ($documentType)';
  }
}
