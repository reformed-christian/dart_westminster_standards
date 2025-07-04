/// Data models for Westminster Standards documents

import 'proof_text.dart';

/// Represents a clause within a section or answer with its specific proof texts
class Clause {
  final String text;
  final List<ProofText> proofTexts;
  final int? footnoteNum;

  const Clause({
    required this.text,
    required this.proofTexts,
    this.footnoteNum,
  });
}
