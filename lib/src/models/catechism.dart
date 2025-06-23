import 'catechism_qa.dart';
import '../types.dart';

/// Enhanced access to catechism data with search and filtering capabilities
class Catechism {
  final List<CatechismItem> _questions;

  const Catechism(this._questions);

  /// Get all questions and answers
  List<CatechismItem> get all => _questions;

  /// Get a specific question by number
  CatechismItem? getQuestion(int number) {
    try {
      return _questions.firstWhere((qa) => qa.number == number);
    } catch (e) {
      return null;
    }
  }

  /// Get the first question
  CatechismItem? get firstQuestion =>
      _questions.isNotEmpty ? _questions.first : null;

  /// Get the last question
  CatechismItem? get lastQuestion =>
      _questions.isNotEmpty ? _questions.last : null;

  /// Get the total number of questions
  int get length => _questions.length;

  /// Find questions that contain the exact string based on item part
  List<CatechismItem> exactStr(
    String searchString, [
    CatechismItemPart part = CatechismItemPart.all,
  ]) {
    final lowerSearch = searchString.toLowerCase();
    return _questions.where((qa) {
      switch (part) {
        case CatechismItemPart.question:
          return qa.question.toLowerCase().contains(lowerSearch);
        case CatechismItemPart.answer:
          return qa.answer.toLowerCase().contains(lowerSearch);
        case CatechismItemPart.references:
          return qa.allProofTexts.any(
            (proofText) =>
                proofText.reference.toLowerCase().contains(lowerSearch),
          );
        case CatechismItemPart.questionAndAnswer:
          return qa.question.toLowerCase().contains(lowerSearch) ||
              qa.answer.toLowerCase().contains(lowerSearch);
        case CatechismItemPart.questionAndReferences:
          return qa.question.toLowerCase().contains(lowerSearch) ||
              qa.allProofTexts.any(
                (proofText) =>
                    proofText.reference.toLowerCase().contains(lowerSearch),
              );
        case CatechismItemPart.answerAndReferences:
          return qa.answer.toLowerCase().contains(lowerSearch) ||
              qa.allProofTexts.any(
                (proofText) =>
                    proofText.reference.toLowerCase().contains(lowerSearch),
              );
        case CatechismItemPart.all:
          return qa.question.toLowerCase().contains(lowerSearch) ||
              qa.answer.toLowerCase().contains(lowerSearch) ||
              qa.allProofTexts.any(
                (proofText) =>
                    proofText.reference.toLowerCase().contains(lowerSearch),
              );
      }
    }).toList();
  }

  /// Find questions where the question contains the exact string
  List<CatechismItem> questionContains(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _questions.where((qa) {
      return qa.question.toLowerCase().contains(lowerSearch);
    }).toList();
  }

  /// Find questions where the answer contains the exact string
  List<CatechismItem> answerContains(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _questions.where((qa) {
      return qa.answer.toLowerCase().contains(lowerSearch);
    }).toList();
  }

  /// Find questions where any proof text reference contains the exact string
  List<CatechismItem> referencesContain(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _questions.where((qa) {
      return qa.allProofTexts.any(
        (proofText) => proofText.reference.toLowerCase().contains(lowerSearch),
      );
    }).toList();
  }

  /// Find questions that start with the given string
  List<CatechismItem> startsWith(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _questions.where((qa) {
      return qa.question.toLowerCase().startsWith(lowerSearch) ||
          qa.answer.toLowerCase().startsWith(lowerSearch);
    }).toList();
  }

  /// Find questions that end with the given string
  List<CatechismItem> endsWith(String searchString) {
    final lowerSearch = searchString.toLowerCase();
    return _questions.where((qa) {
      return qa.question.toLowerCase().endsWith(lowerSearch) ||
          qa.answer.toLowerCase().endsWith(lowerSearch);
    }).toList();
  }

  /// Get questions within a range (inclusive)
  List<CatechismItem> range(int start, int end) {
    return _questions
        .where((qa) => qa.number >= start && qa.number <= end)
        .toList();
  }

  /// Get questions by multiple numbers
  List<CatechismItem> byNumbers(List<int> numbers) {
    return _questions.where((qa) => numbers.contains(qa.number)).toList();
  }

  /// Search within a range of questions
  ///
  /// [start] and [end] define the range of questions to search (inclusive)
  /// [searchString] is the text to search for
  /// [part] specifies which part of the question to search in
  /// Returns questions within the range that match the search criteria
  List<CatechismItem> searchRange(
    int start,
    int end,
    String searchString, [
    CatechismItemPart part = CatechismItemPart.all,
  ]) {
    // First filter by range
    final rangeQuestions =
        _questions
            .where((qa) => qa.number >= start && qa.number <= end)
            .toList();

    // Then apply search filter
    return _filterBySearch(rangeQuestions, searchString, part);
  }

  /// Search within specific questions by numbers
  ///
  /// [numbers] is the list of question numbers to search in
  /// [searchString] is the text to search for
  /// [part] specifies which part of the question to search in
  /// Returns questions with the specified numbers that match the search criteria
  List<CatechismItem> searchByNumbers(
    List<int> numbers,
    String searchString, [
    CatechismItemPart part = CatechismItemPart.all,
  ]) {
    // First filter by numbers
    final specificQuestions =
        _questions.where((qa) => numbers.contains(qa.number)).toList();

    // Then apply search filter
    return _filterBySearch(specificQuestions, searchString, part);
  }

  /// Helper function to filter questions by search criteria
  List<CatechismItem> _filterBySearch(
    List<CatechismItem> questions,
    String searchString,
    CatechismItemPart part,
  ) {
    final lowerSearch = searchString.toLowerCase();

    return questions.where((qa) {
      switch (part) {
        case CatechismItemPart.question:
          return qa.question.toLowerCase().contains(lowerSearch);
        case CatechismItemPart.answer:
          return qa.answer.toLowerCase().contains(lowerSearch);
        case CatechismItemPart.references:
          return qa.allProofTexts.any(
            (proofText) =>
                proofText.reference.toLowerCase().contains(lowerSearch),
          );
        case CatechismItemPart.questionAndAnswer:
          return qa.question.toLowerCase().contains(lowerSearch) ||
              qa.answer.toLowerCase().contains(lowerSearch);
        case CatechismItemPart.questionAndReferences:
          return qa.question.toLowerCase().contains(lowerSearch) ||
              qa.allProofTexts.any(
                (proofText) =>
                    proofText.reference.toLowerCase().contains(lowerSearch),
              );
        case CatechismItemPart.answerAndReferences:
          return qa.answer.toLowerCase().contains(lowerSearch) ||
              qa.allProofTexts.any(
                (proofText) =>
                    proofText.reference.toLowerCase().contains(lowerSearch),
              );
        case CatechismItemPart.all:
          return qa.question.toLowerCase().contains(lowerSearch) ||
              qa.answer.toLowerCase().contains(lowerSearch) ||
              qa.allProofTexts.any(
                (proofText) =>
                    proofText.reference.toLowerCase().contains(lowerSearch),
              );
      }
    }).toList();
  }

  /// Get all proof texts from all questions
  List<dynamic> get allProofTexts {
    return _questions.expand((qa) => qa.allProofTexts).toList();
  }

  /// Iterator support for for-in loops
  Iterator<CatechismItem> get iterator => _questions.iterator;

  /// Index access
  CatechismItem operator [](int index) => _questions[index];

  /// Check if empty
  bool get isEmpty => _questions.isEmpty;

  /// Check if not empty
  bool get isNotEmpty => _questions.isNotEmpty;

  // Text-only access methods (excluding scripture references)

  /// Get the full text content of the catechism (excluding scripture references)
  String get textOnly {
    if (_questions.isEmpty) return '';

    return _questions
        .map((qa) {
          return 'Q${qa.number}. ${qa.question}\nA${qa.number}. ${qa.answer}';
        })
        .join('\n\n');
  }

  /// Get text content of a range of questions (excluding scripture references)
  String getRangeTextOnly(int start, int end) {
    if (_questions.isEmpty) return '';

    final rangeQuestions =
        _questions
            .where((qa) => qa.number >= start && qa.number <= end)
            .toList();

    return rangeQuestions
        .map((qa) {
          return 'Q${qa.number}. ${qa.question}\nA${qa.number}. ${qa.answer}';
        })
        .join('\n\n');
  }

  /// Get text content of specific questions by numbers (excluding scripture references)
  String getByNumbersTextOnly(List<int> numbers) {
    if (_questions.isEmpty) return '';

    final specificQuestions =
        _questions.where((qa) => numbers.contains(qa.number)).toList();

    return specificQuestions
        .map((qa) {
          return 'Q${qa.number}. ${qa.question}\nA${qa.number}. ${qa.answer}';
        })
        .join('\n\n');
  }
}
