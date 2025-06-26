import 'package:flutter/material.dart';
import 'package:westminster_standards/westminster_standards.dart';
import 'dart:developer' as developer;

void main() async {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Westminster Standards Example',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const WestminsterExamplePage(),
    );
  }
}

class WestminsterExamplePage extends StatefulWidget {
  const WestminsterExamplePage({super.key});

  @override
  State<WestminsterExamplePage> createState() => _WestminsterExamplePageState();
}

class _WestminsterExamplePageState extends State<WestminsterExamplePage> {
  String output = 'Loading...';
  bool isLoading = true;
  String? errorMessage;
  List<String> debugLog = [];

  @override
  void initState() {
    super.initState();
    _runExample();
  }

  void _addDebugLog(String message) {
    final timestamp = DateTime.now().toString().substring(11, 19);
    final logMessage = '$timestamp: $message';

    // Print to console for debugging
    print('🔍 DEBUG: $logMessage');
    developer.log(logMessage, name: 'WestminsterStandards');

    setState(() {
      debugLog.add(logMessage);
      if (debugLog.length > 50) {
        debugLog.removeAt(0);
      }
    });
  }

  Future<void> _runExample() async {
    try {
      _addDebugLog('Starting Westminster Standards example...');
      print('🚀 Starting Westminster Standards example...');

      final buffer = StringBuffer();

      buffer.writeln(
        '=== Westminster Standards Text-Only Access Example ===\n',
      );
      _addDebugLog('Initializing Westminster Standards data...');
      print('📚 Initializing Westminster Standards data...');

      // Initialize the data
      await initializeWestminsterStandards();
      _addDebugLog('✓ Data initialized successfully');
      print('✅ Data initialized successfully');
      buffer.writeln('✓ Data initialized and cached\n');

      // Example 1: Get full text content of the Westminster Confession
      _addDebugLog('Loading Westminster Confession text...');
      print('📖 Loading Westminster Confession text...');
      buffer.writeln(
        '1. Full Westminster Confession Text (first 500 characters):',
      );
      final confessionText = getWestminsterConfessionTextOnly();
      print('📄 Confession text loaded: ${confessionText.length} characters');
      buffer.writeln(confessionText.substring(0, 500) + '...\n');
      _addDebugLog(
        '✓ Confession text loaded (${confessionText.length} characters)',
      );

      // Example 2: Get full text content of the Westminster Shorter Catechism
      _addDebugLog('Loading Shorter Catechism text...');
      print('📖 Loading Shorter Catechism text...');
      buffer.writeln(
        '2. Full Westminster Shorter Catechism Text (first 500 characters):',
      );
      final shorterCatechismText = getWestminsterShorterCatechismTextOnly();
      print(
        '📄 Shorter Catechism text loaded: ${shorterCatechismText.length} characters',
      );
      buffer.writeln(shorterCatechismText.substring(0, 500) + '...\n');
      _addDebugLog(
        '✓ Shorter Catechism text loaded (${shorterCatechismText.length} characters)',
      );

      // Example 3: Get full text content of the Westminster Larger Catechism
      _addDebugLog('Loading Larger Catechism text...');
      print('📖 Loading Larger Catechism text...');
      buffer.writeln(
        '3. Full Westminster Larger Catechism Text (first 500 characters):',
      );
      final largerCatechismText = getWestminsterLargerCatechismTextOnly();
      print(
        '📄 Larger Catechism text loaded: ${largerCatechismText.length} characters',
      );
      buffer.writeln(largerCatechismText.substring(0, 500) + '...\n');
      _addDebugLog(
        '✓ Larger Catechism text loaded (${largerCatechismText.length} characters)',
      );

      // Example 4: Get text content of a specific range from the Confession
      _addDebugLog('Loading Confession chapters 1-3...');
      print('📖 Loading Confession chapters 1-3...');
      buffer.writeln('4. Westminster Confession Chapters 1-3 Text:');
      final confessionRangeText = getWestminsterConfessionRangeTextOnly(1, 3);
      print(
        '📄 Confession chapters 1-3 loaded: ${confessionRangeText.length} characters',
      );
      buffer.writeln(confessionRangeText);
      buffer.writeln('\n' + '=' * 50 + '\n');
      _addDebugLog('✓ Confession chapters 1-3 loaded');

      // Example 5: Get text content of a specific range from the Shorter Catechism
      _addDebugLog('Loading Shorter Catechism questions 1-5...');
      print('📖 Loading Shorter Catechism questions 1-5...');
      buffer.writeln('5. Westminster Shorter Catechism Questions 1-5 Text:');
      final shorterCatechismRangeText =
          getWestminsterShorterCatechismRangeTextOnly(1, 5);
      print(
        '📄 Shorter Catechism questions 1-5 loaded: ${shorterCatechismRangeText.length} characters',
      );
      buffer.writeln(shorterCatechismRangeText);
      buffer.writeln('\n' + '=' * 50 + '\n');
      _addDebugLog('✓ Shorter Catechism questions 1-5 loaded');

      // Example 6: Get text content of a specific range from the Larger Catechism
      _addDebugLog('Loading Larger Catechism questions 1-3...');
      print('📖 Loading Larger Catechism questions 1-3...');
      buffer.writeln('6. Westminster Larger Catechism Questions 1-3 Text:');
      final largerCatechismRangeText =
          getWestminsterLargerCatechismRangeTextOnly(1, 3);
      print(
        '📄 Larger Catechism questions 1-3 loaded: ${largerCatechismRangeText.length} characters',
      );
      buffer.writeln(largerCatechismRangeText);
      buffer.writeln('\n' + '=' * 50 + '\n');
      _addDebugLog('✓ Larger Catechism questions 1-3 loaded');

      // Example 7: Get text content of specific chapters by numbers
      _addDebugLog('Loading specific confession chapters...');
      print('📖 Loading specific confession chapters...');
      buffer.writeln(
        '7. Westminster Confession Specific Chapters (1, 3, 5) Text:',
      );
      final confessionSpecificText = getWestminsterConfessionByNumbersTextOnly([
        1,
        3,
        5,
      ]);
      print(
        '📄 Specific confession chapters loaded: ${confessionSpecificText.length} characters',
      );
      buffer.writeln(confessionSpecificText.substring(0, 800) + '...\n');
      _addDebugLog('✓ Specific confession chapters loaded');

      // Example 8: Get text content of specific questions by numbers
      _addDebugLog('Loading specific shorter catechism questions...');
      print('📖 Loading specific shorter catechism questions...');
      buffer.writeln(
        '8. Westminster Shorter Catechism Specific Questions (1, 3, 5) Text:',
      );
      final shorterCatechismSpecificText =
          getWestminsterShorterCatechismByNumbersTextOnly([1, 3, 5]);
      print(
        '📄 Specific shorter catechism questions loaded: ${shorterCatechismSpecificText.length} characters',
      );
      buffer.writeln(shorterCatechismSpecificText);
      buffer.writeln('\n' + '=' * 50 + '\n');
      _addDebugLog('✓ Specific shorter catechism questions loaded');

      // Example 9: Lazy loading examples
      _addDebugLog('Testing lazy loading...');
      print('📖 Testing lazy loading...');
      buffer.writeln('9. Lazy Loading Examples:');

      buffer.writeln('\n9a. Lazy load full Westminster Confession text:');
      final lazyConfessionText = await loadWestminsterConfessionTextOnlyLazy();
      print(
        '📄 Lazy confession text loaded: ${lazyConfessionText.length} characters',
      );
      buffer.writeln('Loaded ${lazyConfessionText.length} characters\n');
      _addDebugLog(
        '✓ Lazy confession text loaded (${lazyConfessionText.length} characters)',
      );

      buffer.writeln('9b. Lazy load Westminster Confession chapters 1-2:');
      final lazyConfessionRangeText =
          await loadWestminsterConfessionRangeTextOnlyLazy(1, 2);
      print(
        '📄 Lazy confession range loaded: ${lazyConfessionRangeText.length} characters',
      );
      buffer.writeln(lazyConfessionRangeText);
      buffer.writeln('\n' + '=' * 50 + '\n');
      _addDebugLog('✓ Lazy confession range loaded');

      // Example 10: Compare with regular access (showing scripture references are excluded)
      _addDebugLog('Comparing regular vs text-only access...');
      print('📖 Comparing regular vs text-only access...');
      buffer.writeln('10. Comparison: Regular vs Text-Only Access');

      buffer.writeln(
        '\n10a. Regular access to Confession Chapter 1 (includes scripture references):',
      );
      final regularChapter = getWestminsterConfession()[0]; // First chapter
      print(
        '📄 Regular chapter loaded: Chapter ${regularChapter.number}. ${regularChapter.title}',
      );
      buffer.writeln(
        'Chapter ${regularChapter.number}. ${regularChapter.title}',
      );
      for (final section in regularChapter.sections.take(2)) {
        // Show first 2 sections
        buffer.writeln('${section.number}. ${section.text}');
        buffer.writeln(
          'Proof texts: ${section.allProofTexts.length} references',
        );
      }
      _addDebugLog('✓ Regular chapter access completed');

      buffer.writeln(
        '\n10b. Text-only access to Confession Chapter 1 (no scripture references):',
      );
      final textOnlyChapter = getWestminsterConfessionRangeTextOnly(1, 1);
      print(
        '📄 Text-only chapter loaded: ${textOnlyChapter.length} characters',
      );
      buffer.writeln(textOnlyChapter.substring(0, 400) + '...\n');
      _addDebugLog('✓ Text-only chapter access completed');

      buffer.writeln('=== Example Complete ===');
      _addDebugLog('🎉 All examples completed successfully!');
      print('🎉 All examples completed successfully!');

      setState(() {
        output = buffer.toString();
        isLoading = false;
        errorMessage = null;
      });
    } catch (e, stackTrace) {
      final errorMsg = '❌ Error: $e';
      final stackMsg = 'Stack trace: $stackTrace';

      _addDebugLog(errorMsg);
      _addDebugLog(stackMsg);

      print('❌ ERROR: $e');
      print('📚 STACK TRACE: $stackTrace');

      setState(() {
        output = 'Error running example: $e\n\nStack trace:\n$stackTrace';
        isLoading = false;
        errorMessage = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Westminster Standards Example'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                output = 'Loading...';
                isLoading = true;
                errorMessage = null;
                debugLog.clear();
              });
              _runExample();
            },
            tooltip: 'Reload Example',
          ),
        ],
      ),
      body: Row(
        children: [
          // Main content area
          Expanded(
            flex: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (errorMessage != null)
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      margin: const EdgeInsets.only(bottom: 16),
                      decoration: BoxDecoration(
                        color: Colors.red.shade100,
                        border: Border.all(color: Colors.red),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Error Occurred:',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.red,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(errorMessage!),
                        ],
                      ),
                    ),
                  Expanded(
                    child:
                        isLoading
                            ? const Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  CircularProgressIndicator(),
                                  SizedBox(height: 16),
                                  Text('Loading Westminster Standards...'),
                                ],
                              ),
                            )
                            : SingleChildScrollView(
                              child: SelectableText(
                                output,
                                style: const TextStyle(
                                  fontFamily: 'monospace',
                                  fontSize: 12,
                                ),
                              ),
                            ),
                  ),
                ],
              ),
            ),
          ),
          // Debug log panel
          Container(
            width: 300,
            decoration: BoxDecoration(
              border: Border(left: BorderSide(color: Colors.grey.shade300)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade100,
                    border: Border(
                      bottom: BorderSide(color: Colors.grey.shade300),
                    ),
                  ),
                  child: const Text(
                    'Debug Log',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.all(8),
                    itemCount: debugLog.length,
                    itemBuilder: (context, index) {
                      final log = debugLog[index];
                      final isError = log.contains('❌');
                      final isSuccess = log.contains('✓') || log.contains('🎉');

                      return Container(
                        margin: const EdgeInsets.only(bottom: 4),
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color:
                              isError
                                  ? Colors.red.shade50
                                  : isSuccess
                                  ? Colors.green.shade50
                                  : Colors.blue.shade50,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          log,
                          style: TextStyle(
                            fontSize: 11,
                            fontFamily: 'monospace',
                            color:
                                isError
                                    ? Colors.red.shade800
                                    : isSuccess
                                    ? Colors.green.shade800
                                    : Colors.blue.shade800,
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
