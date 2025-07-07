# Westminster Standards Assets

This directory contains the organized JSON data files for the Westminster Standards.

## Quick Overview

```
assets/
├── catechisms/
│   ├── larger/     ← Larger Catechism files
│   └── shorter/    ← Shorter Catechism files
├── confessions/    ← Westminster Confession
└── references/     ← Future reference files
```

## Directory Structure

### `/catechisms/`
Contains catechism-related files organized by type:

#### `/catechisms/larger/`
- **`westminster_larger_catechism_with_references.json`** - **FINAL VERSION** - Complete Larger Catechism with all references integrated
- `westminster_larger_catechism_no_references.json` - Base Larger Catechism without references
- `westminster_larger_catechism_references.json` - Reference lookup table for Larger Catechism

#### `/catechisms/shorter/`
- **`westminster_shorter_catechism.json`** - **FINAL VERSION** - Complete Shorter Catechism with references
- `westminster_shorter_catechism_references.json` - Reference lookup table for Shorter Catechism

### `/confessions/`
Contains confession-related files:

- `westminster_confession.json` - Complete Westminster Confession of Faith

### `/references/`
Currently empty - reserved for future reference-related files

## File Descriptions

### Final Production Files
- **`catechisms/larger/westminster_larger_catechism_with_references.json`** - Use this for the Larger Catechism
- **`catechisms/shorter/westminster_shorter_catechism.json`** - Use this for the Shorter Catechism  
- **`confessions/westminster_confession.json`** - Use this for the Confession

### Working Files
The other files are intermediate/working files used during the data processing pipeline.

## Usage

For production applications, use the files marked as "FINAL VERSION" or "Use this for..." as they contain the complete, processed data with all references properly integrated. 