import 'models.dart';
import 'types.dart';
import 'cache.dart';
import 'bulk_access.dart';

/// Get a range of questions from the Westminster Shorter Catechism (inclusive)
/// Returns questions with numbers from start to end (inclusive)
/// Returns empty list if range is invalid or data is not initialized
List<CatechismItem> getWestminsterShorterCatechismRange(int start, int end) {
  final catechism = getWestminsterShorterCatechism();

  if (catechism.isEmpty) return [];

  return catechism
      .where((qa) => qa.number >= start && qa.number <= end)
      .toList();
}

/// Get a range of questions from the Westminster Larger Catechism (inclusive)
/// Returns questions with numbers from start to end (inclusive)
/// Returns empty list if range is invalid or data is not initialized
List<CatechismItem> getWestminsterLargerCatechismRange(int start, int end) {
  final catechism = getWestminsterLargerCatechism();

  if (catechism.isEmpty) return [];

  return catechism
      .where((qa) => qa.number >= start && qa.number <= end)
      .toList();
}

/// Get a range of chapters from the Westminster Confession (inclusive)
/// Returns chapters with numbers from start to end (inclusive)
/// Returns empty list if range is invalid or data is not initialized
List<ConfessionChapter> getWestminsterConfessionRange(int start, int end) {
  final confession = getWestminsterConfession();

  if (confession.isEmpty) return [];

  return confession
      .where((chapter) => chapter.number >= start && chapter.number <= end)
      .toList();
}

/// Get specific questions by numbers from the Westminster Shorter Catechism
/// Returns questions with the specified numbers
/// Returns empty list if any number is invalid or data is not initialized
List<CatechismItem> getWestminsterShorterCatechismByNumbers(List<int> numbers) {
  final catechism = getWestminsterShorterCatechism();

  if (catechism.isEmpty) return [];

  return catechism.where((qa) => numbers.contains(qa.number)).toList();
}

/// Get specific questions by numbers from the Westminster Larger Catechism
/// Returns questions with the specified numbers
/// Returns empty list if any number is invalid or data is not initialized
List<CatechismItem> getWestminsterLargerCatechismByNumbers(List<int> numbers) {
  final catechism = getWestminsterLargerCatechism();

  if (catechism.isEmpty) return [];

  return catechism.where((qa) => numbers.contains(qa.number)).toList();
}

/// Get specific chapters by numbers from the Westminster Confession
/// Returns chapters with the specified numbers
/// Returns empty list if any number is invalid or data is not initialized
List<ConfessionChapter> getWestminsterConfessionByNumbers(List<int> numbers) {
  final confession = getWestminsterConfession();

  if (confession.isEmpty) return [];

  return confession
      .where((chapter) => numbers.contains(chapter.number))
      .toList();
}

/// Lazy load a range of questions from the Westminster Shorter Catechism (inclusive)
/// Auto-initializes data if needed
Future<List<CatechismItem>> loadWestminsterShorterCatechismRangeLazy(
  int start,
  int end,
) async {
  final catechism = await loadWestminsterShorterCatechismLazy();

  if (catechism.isEmpty) return [];

  return catechism
      .where((qa) => qa.number >= start && qa.number <= end)
      .toList();
}

/// Lazy load a range of questions from the Westminster Larger Catechism (inclusive)
/// Auto-initializes data if needed
Future<List<CatechismItem>> loadWestminsterLargerCatechismRangeLazy(
  int start,
  int end,
) async {
  final catechism = await loadWestminsterLargerCatechismLazy();

  if (catechism.isEmpty) return [];

  return catechism
      .where((qa) => qa.number >= start && qa.number <= end)
      .toList();
}

/// Lazy load a range of chapters from the Westminster Confession (inclusive)
/// Auto-initializes data if needed
Future<List<ConfessionChapter>> loadWestminsterConfessionRangeLazy(
  int start,
  int end,
) async {
  final confession = await loadWestminsterConfessionLazy();

  if (confession.isEmpty) return [];

  return confession
      .where((chapter) => chapter.number >= start && chapter.number <= end)
      .toList();
}

/// Lazy load specific questions by numbers from the Westminster Shorter Catechism
/// Auto-initializes data if needed
Future<List<CatechismItem>> loadWestminsterShorterCatechismByNumbersLazy(
  List<int> numbers,
) async {
  final catechism = await loadWestminsterShorterCatechismLazy();

  if (catechism.isEmpty) return [];

  return catechism.where((qa) => numbers.contains(qa.number)).toList();
}

/// Lazy load specific questions by numbers from the Westminster Larger Catechism
/// Auto-initializes data if needed
Future<List<CatechismItem>> loadWestminsterLargerCatechismByNumbersLazy(
  List<int> numbers,
) async {
  final catechism = await loadWestminsterLargerCatechismLazy();

  if (catechism.isEmpty) return [];

  return catechism.where((qa) => numbers.contains(qa.number)).toList();
}

/// Lazy load specific chapters by numbers from the Westminster Confession
/// Auto-initializes data if needed
Future<List<ConfessionChapter>> loadWestminsterConfessionByNumbersLazy(
  List<int> numbers,
) async {
  final confession = await loadWestminsterConfessionLazy();

  if (confession.isEmpty) return [];

  return confession
      .where((chapter) => numbers.contains(chapter.number))
      .toList();
}
