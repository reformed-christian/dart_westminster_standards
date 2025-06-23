/// Data models for Westminster Standards documents

/// Represents a proof text reference
class ProofText {
  final String reference;
  final String text;

  const ProofText({required this.reference, required this.text});

  @override
  String toString() => '$reference: $text';
}
