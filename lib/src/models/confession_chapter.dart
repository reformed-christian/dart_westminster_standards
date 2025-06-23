/// Data models for Westminster Standards documents

import 'confession_section.dart';

/// Represents a chapter in the Westminster Confession
class ConfessionChapter {
  final int number;
  final String title;
  final List<ConfessionSection> sections;

  const ConfessionChapter({
    required this.number,
    required this.title,
    required this.sections,
  });
}
