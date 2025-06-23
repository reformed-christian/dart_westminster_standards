import 'models.dart';
import 'types.dart';
import 'cache.dart';

/// Get all chapters from the Westminster Confession (uses cached data)
List<ConfessionChapter> getWestminsterConfession() {
  return cachedConfession!;
}

/// Get all questions from the Westminster Shorter Catechism (uses cached data)
List<CatechismItem> getWestminsterShorterCatechism() {
  return cachedShorterCatechism!;
}

/// Get all questions from the Westminster Larger Catechism (uses cached data)
List<CatechismItem> getWestminsterLargerCatechism() {
  return cachedLargerCatechism!;
}

/// Lazy load all chapters from the Westminster Confession (initializes if needed)
Future<List<ConfessionChapter>> loadWestminsterConfessionLazy() async {
  if (!isDocumentInitialized(WestminsterDocument.confession)) {
    await initializeWestminsterStandards(WestminsterDocument.confession);
  }
  return cachedConfession!;
}

/// Lazy load all questions from the Westminster Shorter Catechism (initializes if needed)
Future<List<CatechismItem>> loadWestminsterShorterCatechismLazy() async {
  if (!isDocumentInitialized(WestminsterDocument.shorterCatechism)) {
    await initializeWestminsterStandards(WestminsterDocument.shorterCatechism);
  }
  return cachedShorterCatechism!;
}

/// Lazy load all questions from the Westminster Larger Catechism (initializes if needed)
Future<List<CatechismItem>> loadWestminsterLargerCatechismLazy() async {
  if (!isDocumentInitialized(WestminsterDocument.largerCatechism)) {
    await initializeWestminsterStandards(WestminsterDocument.largerCatechism);
  }
  return cachedLargerCatechism!;
}
