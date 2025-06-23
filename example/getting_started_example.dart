import 'package:flutter/material.dart';
import 'package:westminster_standards/westminster_standards.dart';

/// Getting Started Example - The Simplest Way to Use Westminster Standards
/// This example shows the absolute basics to get you started quickly
void main() async {
  // Initialize Flutter
  WidgetsFlutterBinding.ensureInitialized();

  print('=== Westminster Standards Getting Started ===\n');

  // STEP 1: Initialize the data (do this once at app startup)
  await initializeWestminsterStandards();
  print('✓ Data initialized and cached\n');

  // STEP 2: Get a specific question from the Shorter Catechism
  final question1 = loadWestminsterShorterCatechismQuestion(1);
  if (question1 != null) {
    print('Shorter Catechism Question 1:');
    print('Q${question1.number}. ${question1.question}');
    print('A. ${question1.answer}\n');
  }

  // STEP 3: Get a specific chapter from the Confession
  final chapter1 = loadWestminsterConfessionChapter(1);
  if (chapter1 != null) {
    print('Confession Chapter 1:');
    print('Chapter ${chapter1.number}. ${chapter1.title}');
    if (chapter1.sections.isNotEmpty) {
      print(
        'First section: ${chapter1.sections.first.text.substring(0, 100)}...\n',
      );
    }
  }

  // STEP 4: Get a question from the Larger Catechism
  final largerQ1 = loadWestminsterLargerCatechismQuestion(1);
  if (largerQ1 != null) {
    print('Larger Catechism Question 1:');
    print('Q${largerQ1.number}. ${largerQ1.question}');
    print('A. ${largerQ1.answer.substring(0, 100)}...\n');
  }

  print('=== That\'s it! You now have access to all Westminster Standards ===');
  print('For more examples, see basic_usage_example.dart');

  // Run a simple Flutter app to show the results
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Westminster Standards Getting Started',
      home: Scaffold(
        appBar: AppBar(title: const Text('Westminster Standards')),
        body: const Center(
          child: Text(
            'Check the console output for the example results!',
            style: TextStyle(fontSize: 18),
          ),
        ),
      ),
    );
  }
}
