import 'models.dart';
import 'types.dart';
import 'cache.dart';
import 'bulk_access.dart';

/// Search within a range of Shorter Catechism questions
///
/// [start] and [end] define the range of questions to search (inclusive)
/// [searchString] is the text to search for
/// [part] specifies which part of the question to search in
/// Returns questions within the range that match the search criteria
List<CatechismItem> searchWestminsterShorterCatechismRange(
  int start,
  int end,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) {
  final catechism = getWestminsterShorterCatechism();

  if (catechism.isEmpty) return [];

  // First filter by range
  final rangeQuestions =
      catechism.where((qa) => qa.number >= start && qa.number <= end).toList();

  // Then apply search filter
  return _filterCatechismBySearch(rangeQuestions, searchString, part);
}

/// Search within a range of Larger Catechism questions
///
/// [start] and [end] define the range of questions to search (inclusive)
/// [searchString] is the text to search for
/// [part] specifies which part of the question to search in
/// Returns questions within the range that match the search criteria
List<CatechismItem> searchWestminsterLargerCatechismRange(
  int start,
  int end,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) {
  final catechism = getWestminsterLargerCatechism();

  if (catechism.isEmpty) return [];

  // First filter by range
  final rangeQuestions =
      catechism.where((qa) => qa.number >= start && qa.number <= end).toList();

  // Then apply search filter
  return _filterCatechismBySearch(rangeQuestions, searchString, part);
}

/// Search within a range of Confession chapters
///
/// [start] and [end] define the range of chapters to search (inclusive)
/// [searchString] is the text to search for
/// [searchInTitle] if true, searches in chapter titles
/// [searchInContent] if true, searches in chapter content
/// Returns chapters within the range that match the search criteria
List<ConfessionChapter> searchWestminsterConfessionRange(
  int start,
  int end,
  String searchString, {
  bool searchInTitle = true,
  bool searchInContent = true,
}) {
  final confession = getWestminsterConfession();

  if (confession.isEmpty) return [];

  // First filter by range
  final rangeChapters =
      confession
          .where((chapter) => chapter.number >= start && chapter.number <= end)
          .toList();

  // Then apply search filter
  return _filterConfessionBySearch(
    rangeChapters,
    searchString,
    searchInTitle: searchInTitle,
    searchInContent: searchInContent,
  );
}

/// Search within specific Shorter Catechism questions by numbers
///
/// [numbers] is the list of question numbers to search in
/// [searchString] is the text to search for
/// [part] specifies which part of the question to search in
/// Returns questions with the specified numbers that match the search criteria
List<CatechismItem> searchWestminsterShorterCatechismByNumbers(
  List<int> numbers,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) {
  final catechism = getWestminsterShorterCatechism();

  if (catechism.isEmpty) return [];

  // First filter by numbers
  final specificQuestions =
      catechism.where((qa) => numbers.contains(qa.number)).toList();

  // Then apply search filter
  return _filterCatechismBySearch(specificQuestions, searchString, part);
}

/// Search within specific Larger Catechism questions by numbers
///
/// [numbers] is the list of question numbers to search in
/// [searchString] is the text to search for
/// [part] specifies which part of the question to search in
/// Returns questions with the specified numbers that match the search criteria
List<CatechismItem> searchWestminsterLargerCatechismByNumbers(
  List<int> numbers,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) {
  final catechism = getWestminsterLargerCatechism();

  if (catechism.isEmpty) return [];

  // First filter by numbers
  final specificQuestions =
      catechism.where((qa) => numbers.contains(qa.number)).toList();

  // Then apply search filter
  return _filterCatechismBySearch(specificQuestions, searchString, part);
}

/// Search within specific Confession chapters by numbers
///
/// [numbers] is the list of chapter numbers to search in
/// [searchString] is the text to search for
/// [searchInTitle] if true, searches in chapter titles
/// [searchInContent] if true, searches in chapter content
/// Returns chapters with the specified numbers that match the search criteria
List<ConfessionChapter> searchWestminsterConfessionByNumbers(
  List<int> numbers,
  String searchString, {
  bool searchInTitle = true,
  bool searchInContent = true,
}) {
  final confession = getWestminsterConfession();

  if (confession.isEmpty) return [];

  // First filter by numbers
  final specificChapters =
      confession.where((chapter) => numbers.contains(chapter.number)).toList();

  // Then apply search filter
  return _filterConfessionBySearch(
    specificChapters,
    searchString,
    searchInTitle: searchInTitle,
    searchInContent: searchInContent,
  );
}

/// Lazy loading versions of range search functions
/// These auto-initialize data if needed

/// Lazy search within a range of Shorter Catechism questions
Future<List<CatechismItem>> searchWestminsterShorterCatechismRangeLazy(
  int start,
  int end,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) async {
  final catechism = await loadWestminsterShorterCatechismLazy();

  if (catechism.isEmpty) return [];

  // First filter by range
  final rangeQuestions =
      catechism.where((qa) => qa.number >= start && qa.number <= end).toList();

  // Then apply search filter
  return _filterCatechismBySearch(rangeQuestions, searchString, part);
}

/// Lazy search within a range of Larger Catechism questions
Future<List<CatechismItem>> searchWestminsterLargerCatechismRangeLazy(
  int start,
  int end,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) async {
  final catechism = await loadWestminsterLargerCatechismLazy();

  if (catechism.isEmpty) return [];

  // First filter by range
  final rangeQuestions =
      catechism.where((qa) => qa.number >= start && qa.number <= end).toList();

  // Then apply search filter
  return _filterCatechismBySearch(rangeQuestions, searchString, part);
}

/// Lazy search within a range of Confession chapters
Future<List<ConfessionChapter>> searchWestminsterConfessionRangeLazy(
  int start,
  int end,
  String searchString, {
  bool searchInTitle = true,
  bool searchInContent = true,
}) async {
  final confession = await loadWestminsterConfessionLazy();

  if (confession.isEmpty) return [];

  // First filter by range
  final rangeChapters =
      confession
          .where((chapter) => chapter.number >= start && chapter.number <= end)
          .toList();

  // Then apply search filter
  return _filterConfessionBySearch(
    rangeChapters,
    searchString,
    searchInTitle: searchInTitle,
    searchInContent: searchInContent,
  );
}

/// Lazy search within specific Shorter Catechism questions by numbers
Future<List<CatechismItem>> searchWestminsterShorterCatechismByNumbersLazy(
  List<int> numbers,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) async {
  final catechism = await loadWestminsterShorterCatechismLazy();

  if (catechism.isEmpty) return [];

  // First filter by numbers
  final specificQuestions =
      catechism.where((qa) => numbers.contains(qa.number)).toList();

  // Then apply search filter
  return _filterCatechismBySearch(specificQuestions, searchString, part);
}

/// Lazy search within specific Larger Catechism questions by numbers
Future<List<CatechismItem>> searchWestminsterLargerCatechismByNumbersLazy(
  List<int> numbers,
  String searchString, [
  CatechismItemPart part = CatechismItemPart.all,
]) async {
  final catechism = await loadWestminsterLargerCatechismLazy();

  if (catechism.isEmpty) return [];

  // First filter by numbers
  final specificQuestions =
      catechism.where((qa) => numbers.contains(qa.number)).toList();

  // Then apply search filter
  return _filterCatechismBySearch(specificQuestions, searchString, part);
}

/// Lazy search within specific Confession chapters by numbers
Future<List<ConfessionChapter>> searchWestminsterConfessionByNumbersLazy(
  List<int> numbers,
  String searchString, {
  bool searchInTitle = true,
  bool searchInContent = true,
}) async {
  final confession = await loadWestminsterConfessionLazy();

  if (confession.isEmpty) return [];

  // First filter by numbers
  final specificChapters =
      confession.where((chapter) => numbers.contains(chapter.number)).toList();

  // Then apply search filter
  return _filterConfessionBySearch(
    specificChapters,
    searchString,
    searchInTitle: searchInTitle,
    searchInContent: searchInContent,
  );
}

/// Helper function to filter catechism questions by search criteria
List<CatechismItem> _filterCatechismBySearch(
  List<CatechismItem> questions,
  String searchString,
  CatechismItemPart part,
) {
  final lowerSearch = searchString.toLowerCase();

  return questions.where((qa) {
    switch (part) {
      case CatechismItemPart.question:
        return qa.question.toLowerCase().contains(lowerSearch);
      case CatechismItemPart.answer:
        return qa.answer.toLowerCase().contains(lowerSearch);
      case CatechismItemPart.references:
        return qa.allProofTexts.any(
          (proofText) =>
              proofText.reference.toLowerCase().contains(lowerSearch),
        );
      case CatechismItemPart.questionAndAnswer:
        return qa.question.toLowerCase().contains(lowerSearch) ||
            qa.answer.toLowerCase().contains(lowerSearch);
      case CatechismItemPart.questionAndReferences:
        return qa.question.toLowerCase().contains(lowerSearch) ||
            qa.allProofTexts.any(
              (proofText) =>
                  proofText.reference.toLowerCase().contains(lowerSearch),
            );
      case CatechismItemPart.answerAndReferences:
        return qa.answer.toLowerCase().contains(lowerSearch) ||
            qa.allProofTexts.any(
              (proofText) =>
                  proofText.reference.toLowerCase().contains(lowerSearch),
            );
      case CatechismItemPart.all:
        return qa.question.toLowerCase().contains(lowerSearch) ||
            qa.answer.toLowerCase().contains(lowerSearch) ||
            qa.allProofTexts.any(
              (proofText) =>
                  proofText.reference.toLowerCase().contains(lowerSearch),
            );
    }
  }).toList();
}

/// Helper function to filter confession chapters by search criteria
List<ConfessionChapter> _filterConfessionBySearch(
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
