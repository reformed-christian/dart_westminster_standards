/// Westminster Standards Dart Package
///
/// This package provides access to the Westminster Confession of Faith,
/// Westminster Shorter Catechism, and Westminster Larger Catechism
/// with their proof texts stored as JSON files and loaded into Dart objects.
///
/// The Westminster Standards are foundational documents of Reformed theology,
/// produced by the Westminster Assembly (1643-1649) and widely adopted
/// by Presbyterian and Reformed churches worldwide.

// Re-export catechism packages for convenience
export "package:dart_catechism/dart_catechism.dart";
export "package:dart_westminster_catechism/dart_westminster_catechism.dart"
    hide Catechism, CatechismItem, CatechismItemPart, Clause, ProofText;

export "src/models.dart";
export "src/loaders.dart";
export "src/westminster_standards_core.dart";
export "src/extensions/extensions.dart";
export "src/asset_loader_interface.dart";
export "src/asset_loaders.dart";
export "src/json_file_loader.dart";
