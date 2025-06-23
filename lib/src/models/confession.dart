import 'confession_chapter.dart';
import 'confession_section.dart';

/// Enhanced access to confession data with search and filtering capabilities
class Confession {
  final List<ConfessionChapter> _chapters;

  const Confession(this._chapters);

  /// Get all chapters
  List<ConfessionChapter> get all => _chapters;

  /// Get a specific chapter by number
  ConfessionChapter? getChapter(int number) {
    try {
      return _chapters.firstWhere((chapter) => chapter.number == number);
    } catch (e) {
      return null;
    }
  }

  /// Get the first chapter
  ConfessionChapter? get firstChapter =>
      _chapters.isNotEmpty ? _chapters.first : null;

  /// Get the last chapter
  ConfessionChapter? get lastChapter =>
      _chapters.isNotEmpty ? _chapters.last : null;

  /// Get the total number of chapters
  int get length => _chapters.length;

  /// Find chapters that contain the exact string in title or content
  List<ConfessionChapter> exactStr(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _chapters.where((chapter) {
      // Check chapter title
      if (chapter.title.toLowerCase().contains(lowerSearch)) {
        return true;
      }
      // Check all sections in the chapter
      return chapter.sections.any((section) {
        return section.text.toLowerCase().contains(lowerSearch);
      });
    }).toList();
  }

  /// Find chapters where the title contains the exact string
  List<ConfessionChapter> titleContains(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _chapters.where((chapter) {
      return chapter.title.toLowerCase().contains(lowerSearch);
    }).toList();
  }

  /// Find chapters where any section content contains the exact string
  List<ConfessionChapter> contentContains(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _chapters.where((chapter) {
      return chapter.sections.any((section) {
        return section.text.toLowerCase().contains(lowerSearch);
      });
    }).toList();
  }

  /// Find chapters that start with the given string
  List<ConfessionChapter> startsWith(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _chapters.where((chapter) {
      return chapter.title.toLowerCase().startsWith(lowerSearch) ||
          chapter.sections.any((section) {
            return section.text.toLowerCase().startsWith(lowerSearch);
          });
    }).toList();
  }

  /// Find chapters that end with the given string
  List<ConfessionChapter> endsWith(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _chapters.where((chapter) {
      return chapter.title.toLowerCase().endsWith(lowerSearch) ||
          chapter.sections.any((section) {
            return section.text.toLowerCase().endsWith(lowerSearch);
          });
    }).toList();
  }

  /// Get chapters within a range (inclusive)
  List<ConfessionChapter> range(int start, int end) {
    return _chapters
        .where((chapter) => chapter.number >= start && chapter.number <= end)
        .toList();
  }

  /// Get chapters by multiple numbers
  List<ConfessionChapter> byNumbers(List<int> numbers) {
    return _chapters
        .where((chapter) => numbers.contains(chapter.number))
        .toList();
  }

  /// Search within a range of chapters
  ///
  /// [start] and [end] define the range of chapters to search (inclusive)
  /// [searchString] is the text to search for
  /// [searchInTitle] if true, searches in chapter titles
  /// [searchInContent] if true, searches in chapter content
  /// Returns chapters within the range that match the search criteria
  List<ConfessionChapter> searchRange(
    int start,
    int end,
    String searchString, {
    bool searchInTitle = true,
    bool searchInContent = true,
  }) {
    // First filter by range
    final rangeChapters =
        _chapters
            .where(
              (chapter) => chapter.number >= start && chapter.number <= end,
            )
            .toList();

    // Then apply search filter
    return _filterBySearch(
      rangeChapters,
      searchString,
      searchInTitle: searchInTitle,
      searchInContent: searchInContent,
    );
  }

  /// Search within specific chapters by numbers
  ///
  /// [numbers] is the list of chapter numbers to search in
  /// [searchString] is the text to search for
  /// [searchInTitle] if true, searches in chapter titles
  /// [searchInContent] if true, searches in chapter content
  /// Returns chapters with the specified numbers that match the search criteria
  List<ConfessionChapter> searchByNumbers(
    List<int> numbers,
    String searchString, {
    bool searchInTitle = true,
    bool searchInContent = true,
  }) {
    // First filter by numbers
    final specificChapters =
        _chapters.where((chapter) => numbers.contains(chapter.number)).toList();

    // Then apply search filter
    return _filterBySearch(
      specificChapters,
      searchString,
      searchInTitle: searchInTitle,
      searchInContent: searchInContent,
    );
  }

  /// Helper function to filter chapters by search criteria
  List<ConfessionChapter> _filterBySearch(
    List<ConfessionChapter> chapters,
    String searchString, {
    bool searchInTitle = true,
    bool searchInContent = true,
  }) {
    final lowerSearch = searchString.toLowerCase();

    return chapters.where((chapter) {
      // Check title if enabled
      if (searchInTitle && chapter.title.toLowerCase().contains(lowerSearch)) {
        return true;
      }

      // Check content if enabled
      if (searchInContent) {
        return chapter.sections.any((section) {
          return section.text.toLowerCase().contains(lowerSearch);
        });
      }

      return false;
    }).toList();
  }

  /// Get all sections from all chapters
  List<ConfessionSection> get allSections {
    return _chapters.expand((chapter) => chapter.sections).toList();
  }

  /// Get all proof texts from all chapters
  List<dynamic> get allProofTexts {
    return _chapters
        .expand((chapter) => chapter.sections)
        .expand((section) => section.allProofTexts)
        .toList();
  }

  /// Find sections that contain the exact string
  List<ConfessionSection> findSections(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return allSections.where((section) {
      return section.text.toLowerCase().contains(lowerSearch);
    }).toList();
  }

  /// Iterator support for for-in loops
  Iterator<ConfessionChapter> get iterator => _chapters.iterator;

  /// Index access
  ConfessionChapter operator [](int index) => _chapters[index];

  /// Check if empty
  bool get isEmpty => _chapters.isEmpty;

  /// Check if not empty
  bool get isNotEmpty => _chapters.isNotEmpty;

  // Text-only access methods (excluding scripture references)

  /// Get the full text content of the confession (excluding scripture references)
  String get textOnly {
    if (_chapters.isEmpty) return '';

    return _chapters
        .map((chapter) {
          final chapterText = StringBuffer();
          chapterText.writeln('Chapter ${chapter.number}. ${chapter.title}');
          chapterText.writeln();

          for (final section in chapter.sections) {
            chapterText.writeln('${section.number}. ${section.text}');
            chapterText.writeln();
          }

          return chapterText.toString();
        })
        .join('\n');
  }

  /// Get text content of a range of chapters (excluding scripture references)
  String getRangeTextOnly(int start, int end) {
    if (_chapters.isEmpty) return '';

    final rangeChapters =
        _chapters
            .where(
              (chapter) => chapter.number >= start && chapter.number <= end,
            )
            .toList();

    return rangeChapters
        .map((chapter) {
          final chapterText = StringBuffer();
          chapterText.writeln('Chapter ${chapter.number}. ${chapter.title}');
          chapterText.writeln();

          for (final section in chapter.sections) {
            chapterText.writeln('${section.number}. ${section.text}');
            chapterText.writeln();
          }

          return chapterText.toString();
        })
        .join('\n');
  }

  /// Get text content of specific chapters by numbers (excluding scripture references)
  String getByNumbersTextOnly(List<int> numbers) {
    if (_chapters.isEmpty) return '';

    final specificChapters =
        _chapters.where((chapter) => numbers.contains(chapter.number)).toList();

    return specificChapters
        .map((chapter) {
          final chapterText = StringBuffer();
          chapterText.writeln('Chapter ${chapter.number}. ${chapter.title}');
          chapterText.writeln();

          for (final section in chapter.sections) {
            chapterText.writeln('${section.number}. ${section.text}');
            chapterText.writeln();
          }

          return chapterText.toString();
        })
        .join('\n');
  }
}
