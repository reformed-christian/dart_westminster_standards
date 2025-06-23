/// Data models for Westminster Standards documents

import 'clause.dart';
import 'proof_text.dart';

/// Represents a catechism item (question and answer)
class CatechismItem {
  final int number;
  final String question;
  final String answer;
  final List<Clause> clauses;

  const CatechismItem({
    required this.number,
    required this.question,
    required this.answer,
    required this.clauses,
  });

  /// Get all proof texts for this item (flattened from all clauses)
  List<ProofText> get allProofTexts {
    return clauses.expand((clause) => clause.proofTexts).toList();
  }
}
