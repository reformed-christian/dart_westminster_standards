import 'models.dart';
import 'types.dart';
import 'asset_loader_interface.dart';
import 'asset_loaders.dart';
import 'json_file_loader.dart';

/// A convenient object for accessing Westminster Standards data
///
/// This class provides easy access to all Westminster Standards documents
/// and individual items. Data is loaded during creation for optimal performance.
class WestminsterStandards {
  final List<ConfessionChapter> _confession;
  final List<CatechismItem> _shorterCatechism;
  final List<CatechismItem> _largerCatechism;

  WestminsterStandards._({
    required List<ConfessionChapter> confession,
    required List<CatechismItem> shorterCatechism,
    required List<CatechismItem> largerCatechism,
  }) : _confession = confession,
       _shorterCatechism = shorterCatechism,
       _largerCatechism = largerCatechism;

  /// Create a WestminsterStandards instance from pre-loaded data
  /// This is useful for Flutter apps that need custom asset loading
  static WestminsterStandards fromData({
    required List<ConfessionChapter> confession,
    required List<CatechismItem> shorterCatechism,
    required List<CatechismItem> largerCatechism,
  }) {
    return WestminsterStandards._(
      confession: confession,
      shorterCatechism: shorterCatechism,
      largerCatechism: largerCatechism,
    );
  }

  /// Create a WestminsterStandards instance with custom asset loader
  /// This is the preferred method for Flutter apps and other custom environments
  static Future<WestminsterStandards> createWithLoader(
    AssetLoader assetLoader, [
    WestminsterDocument documents = WestminsterDocument.all,
  ]) async {
    final loader = WestminsterJsonLoader(assetLoader);

    List<ConfessionChapter> confession = [];
    List<CatechismItem> shorterCatechism = [];
    List<CatechismItem> largerCatechism = [];

    if (documents == WestminsterDocument.confession ||
        documents == WestminsterDocument.all) {
      confession = await loader.loadWestminsterConfession();
    }

    if (documents == WestminsterDocument.shorterCatechism ||
        documents == WestminsterDocument.all) {
      shorterCatechism = await loader.loadWestminsterShorterCatechism();
    }

    if (documents == WestminsterDocument.largerCatechism ||
        documents == WestminsterDocument.all) {
      largerCatechism = await loader.loadWestminsterLargerCatechism();
    }

    return WestminsterStandards._(
      confession: confession,
      shorterCatechism: shorterCatechism,
      largerCatechism: largerCatechism,
    );
  }

  /// Create a WestminsterStandards instance with default file system loader
  /// This works for pure Dart environments but will fail in Flutter
  static Future<WestminsterStandards> create([
    WestminsterDocument documents = WestminsterDocument.all,
  ]) async {
    try {
      final assetLoader = FileSystemAssetLoader.create();
      return await createWithLoader(assetLoader, documents);
    } catch (e) {
      throw AssetLoadingException(
        'Failed to load Westminster Standards using file system loader. '
            'If you are using Flutter, use createWithLoader() with a Flutter-compatible asset loader instead.',
        'create()',
        e,
      );
    }
  }

  // Enhanced access classes
  /// Enhanced access to the Westminster Confession
  Confession get confession => Confession(_confession);

  /// Enhanced access to the Westminster Shorter Catechism
  Catechism get shorterCatechism => Catechism(_shorterCatechism);

  /// Enhanced access to the Westminster Larger Catechism
  Catechism get largerCatechism => Catechism(_largerCatechism);

  // Synchronous getters for loaded data
  List<ConfessionChapter> get confessionList => _confession;
  List<CatechismItem> get shorterCatechismList => _shorterCatechism;
  List<CatechismItem> get largerCatechismList => _largerCatechism;

  // Individual item methods
  CatechismItem? getShorterCatechismQuestion(int questionNumber) {
    try {
      return _shorterCatechism.firstWhere((qa) => qa.number == questionNumber);
    } catch (e) {
      return null;
    }
  }

  CatechismItem? getLargerCatechismQuestion(int questionNumber) {
    try {
      return _largerCatechism.firstWhere((qa) => qa.number == questionNumber);
    } catch (e) {
      return null;
    }
  }

  ConfessionChapter? getConfessionChapter(int chapterNumber) {
    try {
      return _confession.firstWhere(
        (chapter) => chapter.number == chapterNumber,
      );
    } catch (e) {
      return null;
    }
  }

  // Convenience getters
  CatechismItem? get firstShorterCatechismQuestion =>
      getShorterCatechismQuestion(1);
  CatechismItem? get firstLargerCatechismQuestion =>
      getLargerCatechismQuestion(1);
  ConfessionChapter? get firstConfessionChapter => getConfessionChapter(1);

  // Proof text getters
  List<ProofText> get allShorterCatechismProofTexts {
    return _shorterCatechism.expand((qa) => qa.allProofTexts).toList();
  }

  List<ProofText> get allLargerCatechismProofTexts {
    return _largerCatechism.expand((qa) => qa.allProofTexts).toList();
  }

  List<ProofText> get allConfessionProofTexts {
    return _confession
        .expand(
          (chapter) =>
              chapter.sections.expand((section) => section.allProofTexts),
        )
        .toList();
  }

  List<ProofText> get allProofTexts {
    return [
      ...allShorterCatechismProofTexts,
      ...allLargerCatechismProofTexts,
      ...allConfessionProofTexts,
    ];
  }

  // Text-only access methods (excluding scripture references)

  /// Get the full text content of the Westminster Confession (excluding scripture references)
  String get confessionTextOnly => confession.textOnly;

  /// Get the full text content of the Westminster Shorter Catechism (excluding scripture references)
  String get shorterCatechismTextOnly => shorterCatechism.textOnly;

  /// Get the full text content of the Westminster Larger Catechism (excluding scripture references)
  String get largerCatechismTextOnly => largerCatechism.textOnly;

  /// Get text content of a range of chapters from the Westminster Confession (excluding scripture references)
  String getConfessionRangeTextOnly(int start, int end) =>
      confession.getRangeTextOnly(start, end);

  /// Get text content of a range of questions from the Westminster Shorter Catechism (excluding scripture references)
  String getShorterCatechismRangeTextOnly(int start, int end) =>
      shorterCatechism.getRangeTextOnly(start, end);

  /// Get text content of a range of questions from the Westminster Larger Catechism (excluding scripture references)
  String getLargerCatechismRangeTextOnly(int start, int end) =>
      largerCatechism.getRangeTextOnly(start, end);

  /// Get text content of specific chapters by numbers from the Westminster Confession (excluding scripture references)
  String getConfessionByNumbersTextOnly(List<int> numbers) =>
      confession.getByNumbersTextOnly(numbers);

  /// Get text content of specific questions by numbers from the Westminster Shorter Catechism (excluding scripture references)
  String getShorterCatechismByNumbersTextOnly(List<int> numbers) =>
      shorterCatechism.getByNumbersTextOnly(numbers);

  /// Get text content of specific questions by numbers from the Westminster Larger Catechism (excluding scripture references)
  String getLargerCatechismByNumbersTextOnly(List<int> numbers) =>
      largerCatechism.getByNumbersTextOnly(numbers);

  /// Get all text content from all documents (excluding scripture references)
  String get allTextOnly {
    final parts = <String>[];
    if (_confession.isNotEmpty) {
      parts.add('WESTMINSTER CONFESSION OF FAITH\n');
      parts.add(confessionTextOnly);
    }
    if (_shorterCatechism.isNotEmpty) {
      parts.add('\n\nWESTMINSTER SHORTER CATECHISM\n');
      parts.add(shorterCatechismTextOnly);
    }
    if (_largerCatechism.isNotEmpty) {
      parts.add('\n\nWESTMINSTER LARGER CATECHISM\n');
      parts.add(largerCatechismTextOnly);
    }
    return parts.join('\n');
  }

  /// Search across all Westminster Standards documents
  ///
  /// [searchString] is the text to search for
  /// [searchInTitles] if true, searches in chapter titles and question text
  /// [searchInContent] if true, searches in chapter content and answers
  /// [searchInReferences] if true, searches in proof text references
  /// Returns unified search results from all documents
  List<WestminsterSearchResult> searchAll(
    String searchString, {
    bool searchInTitles = true,
    bool searchInContent = true,
    bool searchInReferences = true,
  }) {
    final results = <WestminsterSearchResult>[];
    final lowerSearch = searchString.toLowerCase();

    // Search in Shorter Catechism
    for (final question in _shorterCatechism) {
      // Search in question text
      if (searchInTitles &&
          question.question.toLowerCase().contains(lowerSearch)) {
        results.add(
          WestminsterSearchResult(
            documentType: WestminsterDocumentType.shorterCatechism,
            number: question.number,
            title: question.question,
            content: question.answer,
            proofTexts: question.allProofTexts,
            matchedText: question.question,
            matchType: SearchMatchType.question,
          ),
        );
      }

      // Search in answer text
      if (searchInContent &&
          question.answer.toLowerCase().contains(lowerSearch)) {
        results.add(
          WestminsterSearchResult(
            documentType: WestminsterDocumentType.shorterCatechism,
            number: question.number,
            title: question.question,
            content: question.answer,
            proofTexts: question.allProofTexts,
            matchedText: question.answer,
            matchType: SearchMatchType.answer,
          ),
        );
      }

      // Search in proof text references
      if (searchInReferences) {
        for (final proofText in question.allProofTexts) {
          if (proofText.reference.toLowerCase().contains(lowerSearch)) {
            results.add(
              WestminsterSearchResult(
                documentType: WestminsterDocumentType.shorterCatechism,
                number: question.number,
                title: question.question,
                content: question.answer,
                proofTexts: question.allProofTexts,
                matchedText: proofText.reference,
                matchType: SearchMatchType.references,
              ),
            );
            break; // Only add once per question even if multiple references match
          }
        }
      }
    }

    // Search in Larger Catechism
    for (final question in _largerCatechism) {
      // Search in question text
      if (searchInTitles &&
          question.question.toLowerCase().contains(lowerSearch)) {
        results.add(
          WestminsterSearchResult(
            documentType: WestminsterDocumentType.largerCatechism,
            number: question.number,
            title: question.question,
            content: question.answer,
            proofTexts: question.allProofTexts,
            matchedText: question.question,
            matchType: SearchMatchType.question,
          ),
        );
      }

      // Search in answer text
      if (searchInContent &&
          question.answer.toLowerCase().contains(lowerSearch)) {
        results.add(
          WestminsterSearchResult(
            documentType: WestminsterDocumentType.largerCatechism,
            number: question.number,
            title: question.question,
            content: question.answer,
            proofTexts: question.allProofTexts,
            matchedText: question.answer,
            matchType: SearchMatchType.answer,
          ),
        );
      }

      // Search in proof text references
      if (searchInReferences) {
        for (final proofText in question.allProofTexts) {
          if (proofText.reference.toLowerCase().contains(lowerSearch)) {
            results.add(
              WestminsterSearchResult(
                documentType: WestminsterDocumentType.largerCatechism,
                number: question.number,
                title: question.question,
                content: question.answer,
                proofTexts: question.allProofTexts,
                matchedText: proofText.reference,
                matchType: SearchMatchType.references,
              ),
            );
            break; // Only add once per question even if multiple references match
          }
        }
      }
    }

    // Search in Confession
    for (final chapter in _confession) {
      // Search in chapter title
      if (searchInTitles && chapter.title.toLowerCase().contains(lowerSearch)) {
        results.add(
          WestminsterSearchResult(
            documentType: WestminsterDocumentType.confession,
            number: chapter.number,
            title: chapter.title,
            content: chapter.sections.map((s) => s.text).join(' '),
            proofTexts:
                chapter.sections.expand((s) => s.allProofTexts).toList(),
            matchedText: chapter.title,
            matchType: SearchMatchType.title,
          ),
        );
      }

      // Search in chapter content
      if (searchInContent) {
        for (final section in chapter.sections) {
          if (section.text.toLowerCase().contains(lowerSearch)) {
            results.add(
              WestminsterSearchResult(
                documentType: WestminsterDocumentType.confession,
                number: chapter.number,
                title: chapter.title,
                content: chapter.sections.map((s) => s.text).join(' '),
                proofTexts:
                    chapter.sections.expand((s) => s.allProofTexts).toList(),
                matchedText: section.text,
                matchType: SearchMatchType.content,
              ),
            );
            break; // Only add once per chapter even if multiple sections match
          }
        }
      }

      // Search in proof text references
      if (searchInReferences) {
        for (final section in chapter.sections) {
          for (final proofText in section.allProofTexts) {
            if (proofText.reference.toLowerCase().contains(lowerSearch)) {
              results.add(
                WestminsterSearchResult(
                  documentType: WestminsterDocumentType.confession,
                  number: chapter.number,
                  title: chapter.title,
                  content: chapter.sections.map((s) => s.text).join(' '),
                  proofTexts:
                      chapter.sections.expand((s) => s.allProofTexts).toList(),
                  matchedText: proofText.reference,
                  matchType: SearchMatchType.references,
                ),
              );
              break; // Only add once per chapter even if multiple references match
            }
          }
          break; // Only add once per chapter even if multiple sections have matching references
        }
      }
    }

    return results;
  }
}
