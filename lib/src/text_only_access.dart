import 'models.dart';
import 'bulk_access.dart';

/// Get the full text content of the Westminster Confession (excluding scripture references)
/// Returns a single string containing all the text content
String getWestminsterConfessionTextOnly() {
  final confessionChapters = getWestminsterConfession();
  final confession = Confession(confessionChapters);
  return confession.textOnly;
}

/// Get the full text content of the Westminster Shorter Catechism (excluding scripture references)
/// Returns a single string containing all the text content
String getWestminsterShorterCatechismTextOnly() {
  final catechismItems = getWestminsterShorterCatechism();
  final catechism = Catechism(catechismItems);
  return catechism.textOnly;
}

/// Get the full text content of the Westminster Larger Catechism (excluding scripture references)
/// Returns a single string containing all the text content
String getWestminsterLargerCatechismTextOnly() {
  final catechismItems = getWestminsterLargerCatechism();
  final catechism = Catechism(catechismItems);
  return catechism.textOnly;
}

/// Get text content of a range of chapters from the Westminster Confession (excluding scripture references)
/// Returns a single string containing the text content of chapters from start to end (inclusive)
String getWestminsterConfessionRangeTextOnly(int start, int end) {
  final confessionChapters = getWestminsterConfession();
  final confession = Confession(confessionChapters);
  return confession.getRangeTextOnly(start, end);
}

/// Get text content of a range of questions from the Westminster Shorter Catechism (excluding scripture references)
/// Returns a single string containing the text content of questions from start to end (inclusive)
String getWestminsterShorterCatechismRangeTextOnly(int start, int end) {
  final catechismItems = getWestminsterShorterCatechism();
  final catechism = Catechism(catechismItems);
  return catechism.getRangeTextOnly(start, end);
}

/// Get text content of a range of questions from the Westminster Larger Catechism (excluding scripture references)
/// Returns a single string containing the text content of questions from start to end (inclusive)
String getWestminsterLargerCatechismRangeTextOnly(int start, int end) {
  final catechismItems = getWestminsterLargerCatechism();
  final catechism = Catechism(catechismItems);
  return catechism.getRangeTextOnly(start, end);
}

/// Get text content of specific chapters by numbers from the Westminster Confession (excluding scripture references)
/// Returns a single string containing the text content of the specified chapters
String getWestminsterConfessionByNumbersTextOnly(List<int> numbers) {
  final confessionChapters = getWestminsterConfession();
  final confession = Confession(confessionChapters);
  return confession.getByNumbersTextOnly(numbers);
}

/// Get text content of specific questions by numbers from the Westminster Shorter Catechism (excluding scripture references)
/// Returns a single string containing the text content of the specified questions
String getWestminsterShorterCatechismByNumbersTextOnly(List<int> numbers) {
  final catechismItems = getWestminsterShorterCatechism();
  final catechism = Catechism(catechismItems);
  return catechism.getByNumbersTextOnly(numbers);
}

/// Get text content of specific questions by numbers from the Westminster Larger Catechism (excluding scripture references)
/// Returns a single string containing the text content of the specified questions
String getWestminsterLargerCatechismByNumbersTextOnly(List<int> numbers) {
  final catechismItems = getWestminsterLargerCatechism();
  final catechism = Catechism(catechismItems);
  return catechism.getByNumbersTextOnly(numbers);
}

/// Lazy load the full text content of the Westminster Confession (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterConfessionTextOnlyLazy() async {
  final confessionChapters = await loadWestminsterConfessionLazy();
  final confession = Confession(confessionChapters);
  return confession.textOnly;
}

/// Lazy load the full text content of the Westminster Shorter Catechism (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterShorterCatechismTextOnlyLazy() async {
  final catechismItems = await loadWestminsterShorterCatechismLazy();
  final catechism = Catechism(catechismItems);
  return catechism.textOnly;
}

/// Lazy load the full text content of the Westminster Larger Catechism (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterLargerCatechismTextOnlyLazy() async {
  final catechismItems = await loadWestminsterLargerCatechismLazy();
  final catechism = Catechism(catechismItems);
  return catechism.textOnly;
}

/// Lazy load text content of a range of chapters from the Westminster Confession (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterConfessionRangeTextOnlyLazy(
  int start,
  int end,
) async {
  final confessionChapters = await loadWestminsterConfessionLazy();
  final confession = Confession(confessionChapters);
  return confession.getRangeTextOnly(start, end);
}

/// Lazy load text content of a range of questions from the Westminster Shorter Catechism (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterShorterCatechismRangeTextOnlyLazy(
  int start,
  int end,
) async {
  final catechismItems = await loadWestminsterShorterCatechismLazy();
  final catechism = Catechism(catechismItems);
  return catechism.getRangeTextOnly(start, end);
}

/// Lazy load text content of a range of questions from the Westminster Larger Catechism (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterLargerCatechismRangeTextOnlyLazy(
  int start,
  int end,
) async {
  final catechismItems = await loadWestminsterLargerCatechismLazy();
  final catechism = Catechism(catechismItems);
  return catechism.getRangeTextOnly(start, end);
}

/// Lazy load text content of specific chapters by numbers from the Westminster Confession (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterConfessionByNumbersTextOnlyLazy(
  List<int> numbers,
) async {
  final confessionChapters = await loadWestminsterConfessionLazy();
  final confession = Confession(confessionChapters);
  return confession.getByNumbersTextOnly(numbers);
}

/// Lazy load text content of specific questions by numbers from the Westminster Shorter Catechism (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterShorterCatechismByNumbersTextOnlyLazy(
  List<int> numbers,
) async {
  final catechismItems = await loadWestminsterShorterCatechismLazy();
  final catechism = Catechism(catechismItems);
  return catechism.getByNumbersTextOnly(numbers);
}

/// Lazy load text content of specific questions by numbers from the Westminster Larger Catechism (excluding scripture references)
/// Auto-initializes data if needed
Future<String> loadWestminsterLargerCatechismByNumbersTextOnlyLazy(
  List<int> numbers,
) async {
  final catechismItems = await loadWestminsterLargerCatechismLazy();
  final catechism = Catechism(catechismItems);
  return catechism.getByNumbersTextOnly(numbers);
}
