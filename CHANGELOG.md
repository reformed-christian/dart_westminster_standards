## 0.0.3

* **Added lazy load functions** that automatically initialize data when needed:
  * `loadWestminsterConfessionLazy()` - Auto-initializes and returns confession data
  * `loadWestminsterShorterCatechismLazy()` - Auto-initializes and returns shorter catechism data
  * `loadWestminsterLargerCatechismLazy()` - Auto-initializes and returns larger catechism data
  * `loadWestminsterShorterCatechismQuestionLazy()` - Auto-initializes and returns specific question
  * `loadWestminsterLargerCatechismQuestionLazy()` - Auto-initializes and returns specific question
  * `loadWestminsterConfessionChapterLazy()` - Auto-initializes and returns specific chapter

## 0.0.2

* **Breaking change:** Made get methods synchronous and assume initialization
  * `getWestminsterConfession()` is now synchronous
  * `getWestminsterShorterCatechism()` is now synchronous  
  * `getWestminsterLargerCatechism()` is now synchronous
  * `loadWestminsterShorterCatechismQuestion()` is now synchronous
  * `loadWestminsterLargerCatechismQuestion()` is now synchronous
  * `loadWestminsterConfessionChapter()` is now synchronous
  * These methods now assume data has been initialized and will throw if not

## 0.0.1

* Initial release with Westminster Confession of Faith, Shorter Catechism, and Larger Catechism
* Support for loading complete documents as JSON or Dart objects
* Clause-specific proof texts for precise theological references
* Added functions to load individual items:
  * `loadWestminsterShorterCatechismQuestion(int questionNumber)` - Load specific question from Shorter Catechism
  * `loadWestminsterLargerCatechismQuestion(int questionNumber)` - Load specific question from Larger Catechism  
  * `loadWestminsterConfessionChapter(int chapterNumber)` - Load specific chapter from Confession
* **Performance improvements:**
  * Added `initializeWestminsterStandards()` for one-time initialization
  * Added `isInitialized` getter to check initialization status
  * Added efficient `get*` functions that use cached data:
    * `getWestminsterConfession()` - Get all chapters (cached)
    * `getWestminsterShorterCatechism()` - Get all questions (cached)
    * `getWestminsterLargerCatechism()` - Get all questions (cached)
  * Individual loading functions now use cached data automatically
  * Original `load*` functions maintained for backward compatibility
