import 'dart:convert';
import 'asset_loader_interface.dart';
import 'models.dart';

/// Type-safe JSON file loader with dependency injection
class JsonFileLoader {
  final AssetLoader _assetLoader;
  final Map<String, dynamic> _cache = {};
  final bool _enableCaching;

  JsonFileLoader(this._assetLoader, {bool enableCaching = true})
    : _enableCaching = enableCaching;

  /// Load and parse JSON file with type safety
  Future<T> loadJson<T>(String assetPath, {T Function(dynamic)? parser}) async {
    try {
      // Check cache first
      if (_enableCaching && _cache.containsKey(assetPath)) {
        final cachedData = _cache[assetPath];
        return parser != null ? parser(cachedData) : cachedData as T;
      }

      // Load asset content
      final jsonString = await _assetLoader(assetPath);

      // Parse JSON
      final dynamic jsonData;
      try {
        jsonData = json.decode(jsonString);
      } catch (e) {
        throw JsonParsingException('Failed to parse JSON', assetPath, e);
      }

      // Cache if enabled
      if (_enableCaching) {
        _cache[assetPath] = jsonData;
      }

      // Apply parser if provided
      return parser != null ? parser(jsonData) : jsonData as T;
    } catch (e) {
      if (e is AssetLoadingException || e is JsonParsingException) {
        rethrow;
      }
      throw AssetLoadingException(
        'Unexpected error loading JSON',
        assetPath,
        e,
      );
    }
  }

  /// Load JSON with validation
  Future<Map<String, dynamic>> loadJsonWithValidation(
    String assetPath,
    bool Function(Map<String, dynamic>) validator,
  ) async {
    final data = await loadJson<Map<String, dynamic>>(assetPath);

    if (!validator(data)) {
      throw ValidationException('JSON validation failed', assetPath);
    }

    return data;
  }

  /// Clear all cached data
  void clearCache() {
    _cache.clear();
  }

  /// Remove specific file from cache
  void removeFromCache(String assetPath) {
    _cache.remove(assetPath);
  }

  /// Preload multiple files
  Future<void> preloadFiles(List<String> assetPaths) async {
    await Future.wait(assetPaths.map((path) => loadJson<dynamic>(path)));
  }

  /// Check if file is cached
  bool isCached(String assetPath) {
    return _cache.containsKey(assetPath);
  }

  /// Get cache statistics
  Map<String, dynamic> getCacheStats() {
    return {
      'cached_files': _cache.length,
      'cache_enabled': _enableCaching,
      'cached_paths': _cache.keys.toList(),
    };
  }
}

/// Westminster Standards specific loaders using JsonFileLoader
class WestminsterJsonLoader {
  final JsonFileLoader _jsonLoader;

  WestminsterJsonLoader(AssetLoader assetLoader)
    : _jsonLoader = JsonFileLoader(assetLoader);

  /// Load Westminster Confession data
  Future<List<ConfessionChapter>> loadWestminsterConfession() async {
    final data = await _jsonLoader.loadJsonWithValidation(
      'assets/confession/westminster_confession.json',
      (json) => json.containsKey('chapters') && json['chapters'] is List,
    );

    final chapters = data['chapters'] as List;
    return chapters.map((chapterJson) {
      final chapter = chapterJson as Map<String, dynamic>;
      final sections =
          (chapter['sections'] as List).map((sectionJson) {
            final section = sectionJson as Map<String, dynamic>;
            final clauses =
                (section['clauses'] as List).map((clauseJson) {
                  final clause = clauseJson as Map<String, dynamic>;
                  final proofTexts =
                      (clause['proofTexts'] as List).map((proofTextJson) {
                        final proofText = proofTextJson as Map<String, dynamic>;
                        return ProofText(
                          reference: proofText['reference'] as String,
                          text: proofText['text'] as String,
                        );
                      }).toList();

                  return Clause(
                    text: clause['text'] as String,
                    proofTexts: proofTexts,
                  );
                }).toList();

            return ConfessionSection(
              number: section['number'] as int,
              text: section['text'] as String,
              clauses: clauses,
            );
          }).toList();

      return ConfessionChapter(
        number: chapter['number'] as int,
        title: chapter['title'] as String,
        sections: sections,
      );
    }).toList();
  }

  /// Load Westminster Shorter Catechism data
  Future<List<CatechismItem>> loadWestminsterShorterCatechism() async {
    final data = await _jsonLoader.loadJson<List<dynamic>>(
      'assets/catechisms/shorter/westminster_shorter_catechism.json',
    );

    return data.map((questionJson) {
      final question = questionJson as Map<String, dynamic>;
      final clauses =
          (question['clauses'] as List).map((clauseJson) {
            final clause = clauseJson as Map<String, dynamic>;
            final proofTexts =
                (clause['references'] as List).map((proofTextJson) {
                  final proofText = proofTextJson as Map<String, dynamic>;
                  return ProofText(
                    reference: proofText['reference'] as String,
                    text: proofText['text'] as String,
                  );
                }).toList();

            return Clause(
              text: clause['text'] as String,
              proofTexts: proofTexts,
              footnoteNum: clause['footnote'] as int?,
            );
          }).toList();

      return CatechismItem(
        number: question['number'] as int,
        question: question['question'] as String,
        answer: question['answer'] as String,
        clauses: clauses,
      );
    }).toList();
  }

  /// Load Westminster Larger Catechism data
  Future<List<CatechismItem>> loadWestminsterLargerCatechism() async {
    final data = await _jsonLoader.loadJson<List<dynamic>>(
      'assets/catechisms/larger/westminster_larger_catechism_with_references.json',
    );

    return data.map((questionJson) {
      final question = questionJson as Map<String, dynamic>;
      final clauses =
          (question['clauses'] as List).map((clauseJson) {
            final clause = clauseJson as Map<String, dynamic>;
            final proofTexts =
                (clause['references'] as List).map((proofTextJson) {
                  final proofText = proofTextJson as Map<String, dynamic>;
                  return ProofText(
                    reference: proofText['reference'] as String,
                    text: proofText['text'] as String,
                  );
                }).toList();

            return Clause(
              text: clause['text'] as String,
              proofTexts: proofTexts,
              footnoteNum: clause['footnote'] as int?,
            );
          }).toList();

      return CatechismItem(
        number: question['number'] as int,
        question: question['question'] as String,
        answer: question['answer'] as String,
        clauses: clauses,
      );
    }).toList();
  }

  /// Get the underlying JsonFileLoader for advanced operations
  JsonFileLoader get jsonLoader => _jsonLoader;
}
