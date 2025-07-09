import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as path;
import 'asset_loader_interface.dart';

/// File system-based asset loader for pure Dart environments
class FileSystemAssetLoader {
  static AssetLoader create() {
    return (String assetPath) async {
      final possiblePaths = [
        // Current working directory (for development)
        assetPath,
        // Assets directory from current working directory
        path.join('assets', assetPath),
        // Package root directory (when installed as dependency)
        path.join(
          path.dirname(Platform.script.path),
          '..',
          '..',
          '..',
          '..',
          'assets',
          assetPath,
        ),
        // Alternative package root path
        path.join(
          path.dirname(Platform.script.path),
          '..',
          '..',
          '..',
          'assets',
          assetPath,
        ),
        // For development: try from project root
        path.join(path.current, 'assets', assetPath),
      ];

      for (final filePath in possiblePaths) {
        final file = File(filePath);
        if (await file.exists()) {
          try {
            return await file.readAsString();
          } catch (e) {
            throw AssetLoadingException('Failed to read file', assetPath, e);
          }
        }
      }

      throw AssetLoadingException(
        'Could not find asset file. Tried the following paths:\n${possiblePaths.map((p) => '  - $p').join('\n')}\nMake sure the assets are properly included in the package.',
        assetPath,
      );
    };
  }
}

/// Creates a Flutter-compatible asset loader
/// Note: This requires flutter/services.dart which is not available in pure Dart
class FlutterAssetLoader {
  static AssetLoader create({String? packageName}) {
    return (String assetPath) async {
      try {
        // This will be resolved at runtime when flutter/services is available
        final rootBundle = _getRootBundle();

        final paths = [
          if (packageName != null) 'packages/$packageName/$assetPath',
          assetPath,
        ];

        for (final fullPath in paths) {
          try {
            return await rootBundle.loadString(fullPath);
          } catch (e) {
            // Try next path
            continue;
          }
        }

        throw AssetLoadingException(
          'Failed to load asset using Flutter rootBundle. Tried paths:\n${paths.map((p) => '  - $p').join('\n')}',
          assetPath,
        );
      } catch (e) {
        throw AssetLoadingException(
          'Flutter rootBundle not available. Make sure you are running in a Flutter environment.',
          assetPath,
          e,
        );
      }
    };
  }

  // This will throw at compile time in non-Flutter environments
  // but that's okay because this loader should only be used in Flutter
  static dynamic _getRootBundle() {
    throw UnsupportedError(
      'FlutterAssetLoader can only be used in Flutter environments. Use createFlutterAssetLoader() from your Flutter app instead.',
    );
  }
}

/// HTTP-based asset loader for web environments
class HttpAssetLoader {
  final String baseUrl;

  HttpAssetLoader(this.baseUrl);

  AssetLoader create() {
    return (String assetPath) async {
      try {
        // Note: http package would need to be added as dependency for this to work
        final url = '$baseUrl/$assetPath';

        // Placeholder for HTTP loading - would use http package
        throw AssetLoadingException(
          'HTTP asset loading not implemented. Add http package dependency and implement HttpAssetLoader.create()',
          assetPath,
        );
      } catch (e) {
        throw AssetLoadingException(
          'Failed to load asset via HTTP',
          assetPath,
          e,
        );
      }
    };
  }
}

/// Memory-based asset loader for testing or embedded content
class MemoryAssetLoader {
  final Map<String, String> assets;

  MemoryAssetLoader(this.assets);

  AssetLoader create() {
    return (String assetPath) async {
      if (assets.containsKey(assetPath)) {
        return assets[assetPath]!;
      }

      throw AssetLoadingException(
        'Asset not found in memory store. Available assets: ${assets.keys.join(', ')}',
        assetPath,
      );
    };
  }
}

/// Caching wrapper for asset loaders
class CachingAssetLoader {
  final AssetLoader _baseLoader;
  final Map<String, String> _cache = {};

  CachingAssetLoader(this._baseLoader);

  AssetLoader create() {
    return (String assetPath) async {
      if (_cache.containsKey(assetPath)) {
        return _cache[assetPath]!;
      }

      final content = await _baseLoader(assetPath);
      _cache[assetPath] = content;
      return content;
    };
  }

  void clearCache() {
    _cache.clear();
  }

  void removeFromCache(String assetPath) {
    _cache.remove(assetPath);
  }
}
