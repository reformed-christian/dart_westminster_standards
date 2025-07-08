import 'dart:convert';
import 'dart:io';
import 'models/catechism_qa.dart';
import 'models/confession_chapter.dart';
import 'models/proof_text.dart';
import 'models/clause.dart';
import 'models/confession_section.dart';

/// Load the Westminster Confession as JSON
Future<Map<String, dynamic>> loadWestminsterConfessionJson() async {
  final file = File('assets/confession/westminster_confession.json');
  final jsonString = await file.readAsString();
  return json.decode(jsonString) as Map<String, dynamic>;
}

/// Load the Westminster Shorter Catechism as JSON
Future<List<dynamic>> loadWestminsterShorterCatechismJson() async {
  final file = File(
    'assets/catechisms/shorter/westminster_shorter_catechism.json',
  );
  final jsonString = await file.readAsString();
  return json.decode(jsonString) as List<dynamic>;
}

/// Load the Westminster Larger Catechism as JSON
Future<List<dynamic>> loadWestminsterLargerCatechismJson() async {
  final file = File(
    'assets/catechisms/larger/westminster_larger_catechism_with_references.json',
  );
  final jsonString = await file.readAsString();
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
