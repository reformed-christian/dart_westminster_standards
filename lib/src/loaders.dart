import 'dart:convert';
import 'package:flutter/services.dart';
import 'models/catechism_qa.dart';
import 'models/confession_chapter.dart';
import 'models/proof_text.dart';
import 'models/clause.dart';
import 'models/confession_section.dart';

/// Load the Westminster Confession as JSON
Future<Map<String, dynamic>> loadWestminsterConfessionJson() async {
  final jsonString = await rootBundle.loadString(
    'packages/westminster_standards/assets/westminster_confession.json',
  );
  return json.decode(jsonString) as Map<String, dynamic>;
}

/// Load the Westminster Shorter Catechism as JSON
Future<Map<String, dynamic>> loadWestminsterShorterCatechismJson() async {
  final jsonString = await rootBundle.loadString(
    'packages/westminster_standards/assets/westminster_shorter_catechism.json',
  );
  return json.decode(jsonString) as Map<String, dynamic>;
}

/// Load the Westminster Larger Catechism as JSON
Future<Map<String, dynamic>> loadWestminsterLargerCatechismJson() async {
  final jsonString = await rootBundle.loadString(
    'packages/westminster_standards/assets/westminster_larger_catechism.json',
  );
  return json.decode(jsonString) as Map<String, dynamic>;
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
  final questions = json['questions'] as List;

  return questions.map((questionJson) {
    final question = questionJson as Map<String, dynamic>;
    final clauses =
        (question['clauses'] as List).map((clauseJson) {
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
            footnoteNum: clause['footnoteNum'] as int?,
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
  final questions = json['questions'] as List;

  return questions.map((questionJson) {
    final question = questionJson as Map<String, dynamic>;
    final clauses =
        (question['clauses'] as List).map((clauseJson) {
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
            footnoteNum: clause['footnoteNum'] as int?,
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
