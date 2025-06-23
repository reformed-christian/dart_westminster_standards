import 'models.dart';
import 'types.dart';
import 'cache.dart';
import 'bulk_access.dart';

/// Load a specific question from the Westminster Shorter Catechism by number
/// Returns null if the question number is invalid or data is not initialized
CatechismItem? loadWestminsterShorterCatechismQuestion(int questionNumber) {
  final catechism = getWestminsterShorterCatechism();

  try {
    return catechism.firstWhere((qa) => qa.number == questionNumber);
  } catch (e) {
    return null;
  }
}

/// Load a specific question from the Westminster Larger Catechism by number
/// Returns null if the question number is invalid or data is not initialized
CatechismItem? loadWestminsterLargerCatechismQuestion(int questionNumber) {
  final catechism = getWestminsterLargerCatechism();

  try {
    return catechism.firstWhere((qa) => qa.number == questionNumber);
  } catch (e) {
    return null;
  }
}

/// Load a specific chapter from the Westminster Confession by number
/// Returns null if the chapter number is invalid or data is not initialized
ConfessionChapter? loadWestminsterConfessionChapter(int chapterNumber) {
  final confession = getWestminsterConfession();

  try {
    return confession.firstWhere((chapter) => chapter.number == chapterNumber);
  } catch (e) {
    return null;
  }
}

/// Lazy load a specific question from the Westminster Shorter Catechism by number
/// Auto-initializes data if needed
Future<CatechismItem?> loadWestminsterShorterCatechismQuestionLazy(
  int questionNumber,
) async {
  final catechism = await loadWestminsterShorterCatechismLazy();

  try {
    return catechism.firstWhere((qa) => qa.number == questionNumber);
  } catch (e) {
    return null;
  }
}

/// Lazy load a specific question from the Westminster Larger Catechism by number
/// Auto-initializes data if needed
Future<CatechismItem?> loadWestminsterLargerCatechismQuestionLazy(
  int questionNumber,
) async {
  final catechism = await loadWestminsterLargerCatechismLazy();

  try {
    return catechism.firstWhere((qa) => qa.number == questionNumber);
  } catch (e) {
    return null;
  }
}

/// Lazy load a specific chapter from the Westminster Confession by number
/// Auto-initializes data if needed
Future<ConfessionChapter?> loadWestminsterConfessionChapterLazy(
  int chapterNumber,
) async {
  final confession = await loadWestminsterConfessionLazy();

  try {
    return confession.firstWhere((chapter) => chapter.number == chapterNumber);
  } catch (e) {
    return null;
  }
}
