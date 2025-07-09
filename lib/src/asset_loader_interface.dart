/// Asset loader interface for dependency injection
/// This allows the package to work with different loading strategies
/// (Flutter assets, file system, web, etc.)
typedef AssetLoader = Future<String> Function(String assetPath);

/// Custom exceptions for asset loading
class AssetLoadingException implements Exception {
  final String message;
  final String assetPath;
  final Object? originalError;

  const AssetLoadingException(
    this.message,
    this.assetPath, [
    this.originalError,
  ]);

  @override
  String toString() {
    if (originalError != null) {
      return 'AssetLoadingException: $message (Asset: $assetPath, Original: $originalError)';
    }
    return 'AssetLoadingException: $message (Asset: $assetPath)';
  }
}

/// JSON parsing exception
class JsonParsingException implements Exception {
  final String message;
  final String assetPath;
  final Object originalError;

  const JsonParsingException(this.message, this.assetPath, this.originalError);

  @override
  String toString() {
    return 'JsonParsingException: $message (Asset: $assetPath, Original: $originalError)';
  }
}

/// Validation exception
class ValidationException implements Exception {
  final String message;
  final String assetPath;

  const ValidationException(this.message, this.assetPath);

  @override
  String toString() {
    return 'ValidationException: $message (Asset: $assetPath)';
  }
}
