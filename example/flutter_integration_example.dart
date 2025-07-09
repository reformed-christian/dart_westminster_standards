import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Example showing how to use Westminster Standards with different asset loaders
/// This demonstrates the new dependency injection pattern that solves Flutter integration issues
void main() async {
  print('🔗 WESTMINSTER STANDARDS - DEPENDENCY INJECTION EXAMPLE\n');

  // Example 1: File System Loader (Pure Dart environments)
  await demonstrateFileSystemLoader();

  // Example 2: Memory Loader (Testing or embedded data)
  await demonstrateMemoryLoader();

  // Example 3: Caching Loader (Performance optimization)
  await demonstrateCachingLoader();

  // Example 4: Custom Loader (HTTP, custom protocols)
  await demonstrateCustomLoader();

  print(
    '\n🎯 For Flutter apps, copy the helper code from ASSET_LOADING_FIX.md',
  );
  print('   and use createWestminsterStandardsForFlutter() instead!');
}

/// Example 1: File System Asset Loader
Future<void> demonstrateFileSystemLoader() async {
  print('1️⃣ FILE SYSTEM LOADER (Pure Dart):');
  print('   Use this for command-line tools, server applications, etc.\n');

  try {
    // Create file system asset loader
    final assetLoader = FileSystemAssetLoader.create();

    // Create Westminster Standards with the loader
    final standards = await WestminsterStandards.createWithLoader(assetLoader);

    // Use normally
    final q1 = standards.shorterCatechism.getQuestion(1);
    print(
      '✅ Loaded ${standards.shorterCatechism.length} shorter catechism questions',
    );
    print('   Q1: ${q1?.question}');
    print('   A1: ${q1?.answer.substring(0, 50)}...\n');
  } catch (e) {
    print('❌ File system loader failed: $e\n');
  }
}

/// Example 2: Memory Asset Loader
Future<void> demonstrateMemoryLoader() async {
  print('2️⃣ MEMORY LOADER (Testing/Embedded Data):');
  print('   Use this for unit tests or when embedding data directly\n');

  try {
    // Create mock data for testing
    final mockData = {
      'assets/catechisms/shorter/westminster_shorter_catechism.json': '''[
        {
          "number": 1,
          "question": "What is the chief end of man?",
          "answer": "Man's chief end is to glorify God, and to enjoy him forever.",
          "clauses": [{"text": "Test clause", "references": []}]
        },
        {
          "number": 2,
          "question": "What rule hath God given to direct us?",
          "answer": "The Word of God contained in the Scriptures.",
          "clauses": [{"text": "Test clause", "references": []}]
        }
      ]''',
      'assets/confession/westminster_confession.json': '''{"chapters": []}''',
      'assets/catechisms/larger/westminster_larger_catechism_with_references.json':
          '''[]''',
    };

    // Create memory asset loader
    final memoryLoader = MemoryAssetLoader(mockData);
    final assetLoader = memoryLoader.create();

    // Load only shorter catechism for this example
    final standards = await WestminsterStandards.createWithLoader(
      assetLoader,
      WestminsterDocument.shorterCatechism,
    );

    print(
      '✅ Loaded ${standards.shorterCatechism.length} questions from memory',
    );
    final q1 = standards.shorterCatechism.getQuestion(1);
    final q2 = standards.shorterCatechism.getQuestion(2);
    print('   Q1: ${q1?.question}');
    print('   Q2: ${q2?.question}\n');
  } catch (e) {
    print('❌ Memory loader failed: $e\n');
  }
}

/// Example 3: Caching Asset Loader
Future<void> demonstrateCachingLoader() async {
  print('3️⃣ CACHING LOADER (Performance Optimization):');
  print('   Wrap any loader with caching for better performance\n');

  try {
    // Create base loader
    final baseLoader = FileSystemAssetLoader.create();

    // Wrap with caching
    final cachingWrapper = CachingAssetLoader(baseLoader);
    final assetLoader = cachingWrapper.create();

    print('   Loading data (first time - will cache)...');
    final standards1 = await WestminsterStandards.createWithLoader(assetLoader);

    print('   Loading data (second time - from cache)...');
    final standards2 = await WestminsterStandards.createWithLoader(assetLoader);

    print('✅ Both loads successful');
    print('   Questions loaded: ${standards1.shorterCatechism.length}');
    print(
      '   Cache is working: ${standards1.shorterCatechism.length == standards2.shorterCatechism.length}\n',
    );
  } catch (e) {
    print('❌ Caching loader failed: $e\n');
  }
}

/// Example 4: Custom Asset Loader
Future<void> demonstrateCustomLoader() async {
  print('4️⃣ CUSTOM LOADER (Your Own Implementation):');
  print('   Create your own loader for HTTP, database, etc.\n');

  try {
    // Custom loader that transforms file paths
    AssetLoader customLoader = (String assetPath) async {
      // You could load from HTTP, database, etc.
      // For this example, we'll just transform the path and use file system
      final transformedPath = assetPath.replaceFirst('assets/', 'assets/');

      // Use the file system loader as a fallback
      final fileLoader = FileSystemAssetLoader.create();
      return await fileLoader(transformedPath);
    };

    // Use the custom loader
    final standards = await WestminsterStandards.createWithLoader(
      customLoader,
      WestminsterDocument.shorterCatechism,
    );

    print('✅ Custom loader works!');
    print('   Loaded ${standards.shorterCatechism.length} questions');

    final q1 = standards.shorterCatechism.getQuestion(1);
    print('   Q1: ${q1?.question}\n');
  } catch (e) {
    print('❌ Custom loader failed: $e\n');
  }
}

/// Example showing error handling
void demonstrateErrorHandling() {
  print('5️⃣ ERROR HANDLING:');
  print(
    '   The system provides specific exceptions for different error types\n',
  );

  // AssetLoadingException - when files can't be found or loaded
  print('   AssetLoadingException: Asset files not found or inaccessible');

  // JsonParsingException - when JSON is malformed
  print('   JsonParsingException: JSON content is invalid');

  // ValidationException - when JSON structure is unexpected
  print('   ValidationException: JSON doesn\'t match expected structure');

  print(
    '\n   All exceptions include the asset path and original error for debugging\n',
  );
}
