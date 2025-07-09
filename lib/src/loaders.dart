import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as path;
import 'models/catechism_qa.dart';
import 'models/confession_chapter.dart';
import 'models/proof_text.dart';
import 'models/clause.dart';
import 'models/confession_section.dart';

/// Try to find and load a file from multiple possible locations
Future<String> _loadAssetFile(String relativePath) async {
  final possiblePaths = [
    // Current working directory (for development)
    relativePath,
    // Assets directory from current working directory
    path.join('assets', relativePath),
    // Package root directory (when installed as dependency)
    path.join(
      path.dirname(Platform.script.path),
      '..',
      '..',
      '..',
      '..',
      'assets',
      relativePath,
    ),
    // Alternative package root path
    path.join(
      path.dirname(Platform.script.path),
      '..',
      '..',
      '..',
      'assets',
      relativePath,
    ),
    // For development: try from project root
    path.join(path.current, 'assets', relativePath),
  ];

  for (final filePath in possiblePaths) {
    final file = File(filePath);
    if (await file.exists()) {
      return await file.readAsString();
    }
  }

  throw FileSystemException(
    'Could not find asset file: $relativePath\n'
    'Tried the following paths:\n${possiblePaths.map((p) => '  - $p').join('\n')}\n'
    'Make sure the assets are properly included in the package.',
    relativePath,
  );
}

/// Load the Westminster Confession as JSON
Future<Map<String, dynamic>> loadWestminsterConfessionJson() async {
  final jsonString = await _loadAssetFile(
    'confession/westminster_confession.json',
  );
  return json.decode(jsonString) as Map<String, dynamic>;
}

/// Load the Westminster Shorter Catechism as JSON
Future<List<dynamic>> loadWestminsterShorterCatechismJson() async {
  final jsonString = await _loadAssetFile(
    'catechisms/shorter/westminster_shorter_catechism.json',
  );
  return json.decode(jsonString) as List<dynamic>;
}

/// Load the Westminster Larger Catechism as JSON
Future<List<dynamic>> loadWestminsterLargerCatechismJson() async {
  final jsonString = await _loadAssetFile(
    'catechisms/larger/westminster_larger_catechism_with_references.json',
  );
  return json.decode(jsonString) as List<dynamic>;
}

/// Load the Westminster Confession as Dart objects
Future<List<ConfessionChapter>> loadWestminsterConfession() async {
  final json = await loadWestminsterConfessionJson();
  final chapters = json['chapters'] as List;

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

/// Load the Westminster Shorter Catechism as Dart objects
Future<List<CatechismItem>> loadWestminsterShorterCatechism() async {
  final json = await loadWestminsterShorterCatechismJson();
  final questions = json as List;

  return questions.map((questionJson) {
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

/// Load the Westminster Larger Catechism as Dart objects
Future<List<CatechismItem>> loadWestminsterLargerCatechism() async {
  final json = await loadWestminsterLargerCatechismJson();
  final questions = json as List;

  return questions.map((questionJson) {
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
