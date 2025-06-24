/// Async extensions for Westminster Standards
/// Provides convenient methods for working with async operations

import 'dart:async';
import '../westminster_standards_object.dart';

/// Custom exception for Westminster Standards operations
class WestminsterStandardsException implements Exception {
  final String message;
  final dynamic originalError;

  WestminsterStandardsException(this.message, [this.originalError]);

  @override
  String toString() => 'WestminsterStandardsException: $message';
}

/// Extensions for Future<WestminsterStandards>
extension WestminsterAsyncExtensions on Future<WestminsterStandards> {
  /// Create with error handling
  Future<WestminsterStandards> withErrorHandling() async {
    try {
      return await this;
    } catch (e) {
      throw WestminsterStandardsException(
        'Failed to load Westminster Standards: $e',
        e,
      );
    }
  }

  /// Create with timeout
  Future<WestminsterStandards> withTimeout(Duration timeout) async {
    try {
      return await this.timeout(timeout);
    } catch (e) {
      if (e is TimeoutException) {
        throw WestminsterStandardsException(
          'Operation timed out after ${timeout.inSeconds} seconds',
          e,
        );
      }
      rethrow;
    }
  }

  /// Create with retry logic
  Future<WestminsterStandards> withRetry({
    int maxRetries = 3,
    Duration delay = const Duration(milliseconds: 100),
  }) async {
    int attempts = 0;
    while (attempts < maxRetries) {
      try {
        return await this;
      } catch (e) {
        attempts++;
        if (attempts >= maxRetries) {
          throw WestminsterStandardsException(
            'Failed after $maxRetries attempts. Last error: $e',
            e,
          );
        }
        await Future.delayed(delay * attempts); // Exponential backoff
      }
    }
    throw WestminsterStandardsException('Unexpected error in retry logic');
  }

  /// Create with progress callback
  Future<WestminsterStandards> withProgress(
    void Function(String message) onProgress,
  ) async {
    onProgress('Initializing Westminster Standards...');
    try {
      final result = await this;
      onProgress('Westminster Standards loaded successfully');
      return result;
    } catch (e) {
      onProgress('Error loading Westminster Standards: $e');
      rethrow;
    }
  }
}

/// Extensions for Future<T> where T is a Westminster Standards item
extension WestminsterItemAsyncExtensions<T> on Future<T?> {
  /// Handle null results with a default value
  Future<T> withDefault(T defaultValue) async {
    final result = await this;
    return result ?? defaultValue;
  }

  /// Handle null results with an exception
  Future<T> orThrow(String errorMessage) async {
    final result = await this;
    if (result == null) {
      throw WestminsterStandardsException(errorMessage);
    }
    return result;
  }

  /// Handle null results with a custom handler
  Future<T> orElse(Future<T> Function() handler) async {
    final result = await this;
    if (result == null) {
      return await handler();
    }
    return result;
  }
}

/// Extensions for Future<List<T>> where T is a Westminster Standards item
extension WestminsterListAsyncExtensions<T> on Future<List<T>> {
  /// Filter results asynchronously
  Future<List<T>> whereAsync(bool Function(T) predicate) async {
    final list = await this;
    return list.where(predicate).toList();
  }

  /// Map results asynchronously
  Future<List<R>> mapAsync<R>(R Function(T) transform) async {
    final list = await this;
    return list.map(transform).toList();
  }

  /// Take first N results
  Future<List<T>> takeAsync(int count) async {
    final list = await this;
    return list.take(count).toList();
  }

  /// Skip first N results
  Future<List<T>> skipAsync(int count) async {
    final list = await this;
    return list.skip(count).toList();
  }

  /// Get the first result or null
  Future<T?> get firstOrNull async {
    final list = await this;
    return list.isNotEmpty ? list.first : null;
  }

  /// Get the last result or null
  Future<T?> get lastOrNull async {
    final list = await this;
    return list.isNotEmpty ? list.last : null;
  }

  /// Check if the list is empty
  Future<bool> get isEmpty async {
    final list = await this;
    return list.isEmpty;
  }

  /// Check if the list is not empty
  Future<bool> get isNotEmpty async {
    final list = await this;
    return list.isNotEmpty;
  }

  /// Get the length of the list
  Future<int> get length async {
    final list = await this;
    return list.length;
  }
}
