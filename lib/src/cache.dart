import 'models.dart';
import 'types.dart';
import 'loaders.dart';

// Cached data for efficient access
List<ConfessionChapter>? _cachedConfession;
List<CatechismItem>? _cachedShorterCatechism;
List<CatechismItem>? _cachedLargerCatechism;

// Initialization flags
bool _isConfessionInitialized = false;
bool _isShorterCatechismInitialized = false;
bool _isLargerCatechismInitialized = false;

/// Initialize the Westminster Standards data
/// Call this once at app startup for optimal performance
/// [documents] specifies which documents to load (defaults to all)
Future<void> initializeWestminsterStandards([
  WestminsterDocument documents = WestminsterDocument.all,
]) async {
  switch (documents) {
    case WestminsterDocument.confession:
      _cachedConfession = await loadWestminsterConfession();
      _isConfessionInitialized = true;
      break;
    case WestminsterDocument.shorterCatechism:
      _cachedShorterCatechism = await loadWestminsterShorterCatechism();
      _isShorterCatechismInitialized = true;
      break;
    case WestminsterDocument.largerCatechism:
      _cachedLargerCatechism = await loadWestminsterLargerCatechism();
      _isLargerCatechismInitialized = true;
      break;
    case WestminsterDocument.all:
      _cachedConfession = await loadWestminsterConfession();
      _cachedShorterCatechism = await loadWestminsterShorterCatechism();
      _cachedLargerCatechism = await loadWestminsterLargerCatechism();
      _isConfessionInitialized = true;
      _isShorterCatechismInitialized = true;
      _isLargerCatechismInitialized = true;
      break;
  }
}

/// Check if all documents are initialized
bool get isInitialized {
  return _isConfessionInitialized &&
      _isShorterCatechismInitialized &&
      _isLargerCatechismInitialized;
}

/// Check if a specific document is initialized
bool isDocumentInitialized(WestminsterDocument document) {
  switch (document) {
    case WestminsterDocument.confession:
      return _isConfessionInitialized;
    case WestminsterDocument.shorterCatechism:
      return _isShorterCatechismInitialized;
    case WestminsterDocument.largerCatechism:
      return _isLargerCatechismInitialized;
    case WestminsterDocument.all:
      return isInitialized;
  }
}

/// Clear all cached data and reset initialization flags
void clearWestminsterStandardsCache() {
  _cachedConfession = null;
  _cachedShorterCatechism = null;
  _cachedLargerCatechism = null;
  _isConfessionInitialized = false;
  _isShorterCatechismInitialized = false;
  _isLargerCatechismInitialized = false;
}

/// Set cached data for confession
void setCachedConfession(List<ConfessionChapter> confession) {
  _cachedConfession = confession;
  _isConfessionInitialized = true;
}

/// Set cached data for shorter catechism
void setCachedShorterCatechism(List<CatechismItem> catechism) {
  _cachedShorterCatechism = catechism;
  _isShorterCatechismInitialized = true;
}

/// Set cached data for larger catechism
void setCachedLargerCatechism(List<CatechismItem> catechism) {
  _cachedLargerCatechism = catechism;
  _isLargerCatechismInitialized = true;
}

/// Get cached confession data
List<ConfessionChapter>? get cachedConfession => _cachedConfession;

/// Get cached shorter catechism data
List<CatechismItem>? get cachedShorterCatechism => _cachedShorterCatechism;

/// Get cached larger catechism data
List<CatechismItem>? get cachedLargerCatechism => _cachedLargerCatechism;
