import 'package:mongo_dart/mongo_dart.dart';

class LeetCodeProblem {
  final int problemNumber;
  final String title;
  final String difficulty;
  final String problemDescription;
  final List<String> exampleTestCases;
  final List<String> topicTags;
  final List<String> hints;
  final List<Submission> submissions;

  LeetCodeProblem({
    required this.problemNumber,
    required this.title,
    required this.difficulty,
    required this.problemDescription,
    required this.exampleTestCases,
    required this.topicTags,
    required this.hints,
    required this.submissions,
  });

  DateTime get lastSubmitted {
    if (submissions.isEmpty) return DateTime(1970);
    submissions.sort((a, b) => b.timestamp.compareTo(a.timestamp));
    return submissions.first.timestamp;
  }

  String get latestSolution {
    if (submissions.isEmpty) return '';
    submissions.sort((a, b) => b.timestamp.compareTo(a.timestamp));
    return submissions.first.code;
  }

  factory LeetCodeProblem.fromMongo(Map<String, dynamic> json) {
    List<Submission> submissionsList = [];
    if (json['submissions'] != null) {
      submissionsList = (json['submissions'] as List)
          .map((submissionJson) => Submission.fromJson(submissionJson))
          .toList();
    }

    return LeetCodeProblem(
      problemNumber: int.parse(json['id'] ?? '0'),
      title: json['title'] as String,
      difficulty: json['difficulty'] ?? 'Unknown',
      problemDescription: json['problemDescription'] ?? '',
      exampleTestCases: (json['example_testcases'] as String).split('\n'),
      topicTags: List<String>.from(json['topic_tags'] ?? []),
      hints: List<String>.from(json['hints'] ?? []),
      submissions: submissionsList,
    );
  }
}

class Submission {
  final DateTime timestamp;
  final String code;

  Submission({
    required this.timestamp,
    required this.code,
  });

  factory Submission.fromJson(Map<String, dynamic> json) {
    return Submission(
      timestamp: DateTime.parse(json['timestamp']),
      code: json['code'] ?? '',
    );
  }
}