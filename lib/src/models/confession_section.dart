/// Data models for Westminster Standards documents

import 'clause.dart';
import 'proof_text.dart';

/// Represents a section within a chapter of the Westminster Confession
class ConfessionSection {
  final int number;
  final String text;
  final List<Clause> clauses;

  const ConfessionSection({
    required this.number,
    required this.text,
    required this.clauses,
  });

  /// Get all proof texts for this section (flattened from all clauses)
  List<ProofText> get allProofTexts {
    return clauses.expand((clause) => clause.proofTexts).toList();
  }
}
