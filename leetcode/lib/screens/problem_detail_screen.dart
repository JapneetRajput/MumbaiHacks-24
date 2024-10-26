// lib/screens/problem_detail_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/atom-one-dark.dart';
import 'package:flutter_widget_from_html/flutter_widget_from_html.dart';
import '../models/problem.dart';

class ProblemDetailScreen extends StatelessWidget {
  final LeetCodeProblem problem;

  const ProblemDetailScreen({Key? key, required this.problem}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF1A1A1A),
      ),
      backgroundColor: const Color(0xFF0A0A0A),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween, // Distribute space between children
              children: [
                Text(
                  '${problem.problemNumber}. ${problem.title}',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                _DifficultyBadge(difficulty: problem.difficulty),
              ],
            ),
            const SizedBox(height: 24),
            const Text(
              'Description',
              style: TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            // Updated section for rendering HTML description
            HtmlWidget(
              problem.problemDescription,
              textStyle: const TextStyle(
                color: Colors.white70,
                fontSize: 16,
                height: 1.25,
              ),
              customStylesBuilder: (element) {
                if (element.localName == 'pre') {
                  return {
                    'background-color': '#1A1A1A',
                    'padding': '12px',
                    'border-radius': '8px',
                  };
                }
                return null;
              },
              customWidgetBuilder: (element) {
                if (element.localName == 'pre') {
                  return HighlightView(
                    element.text,
                    language: 'python',
                    theme: atomOneDarkTheme,
                    padding: const EdgeInsets.all(12),
                    textStyle: const TextStyle(
                      fontSize: 10,
                      height: 1.2,
                    ),
                  );
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            const Text(
              'Example Test Cases',
              style: TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            for (var testCase in problem.exampleTestCases)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Text(
                  testCase,
                  style: const TextStyle(color: Colors.white70),
                ),
              ),
            const SizedBox(height: 24),
            const Text(
              'Topic Tags',
              style: TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            for (var testCase in problem.topicTags)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Text(
                  testCase,
                  style: const TextStyle(color: Colors.white70),
                ),
              ),
            const SizedBox(height: 24),
            const Text(
              'Solution',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(8),
                color: const Color(0xFF1A1A1A),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      'Submitted on: ${_formatDate(problem.lastSubmitted)}',
                      style: const TextStyle(
                        color: Colors.white54,
                        fontSize: 10,
                      ),
                    ),
                  ),
                  HighlightView(
                    problem.latestSolution,
                    language: 'python',
                    theme: atomOneDarkTheme,
                    padding: const EdgeInsets.all(16),
                    textStyle: const TextStyle(
                      fontSize: 10,
                      height: 1.5,
                      fontFamily: 'monospace',
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Hints',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            for (var hint in problem.hints)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Text(
                  hint,
                  style: const TextStyle(color: Colors.white70),
                ),
              ),
          ],
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }
}

class _DifficultyBadge extends StatelessWidget {
  final String difficulty;

  const _DifficultyBadge({required this.difficulty});

  @override
  Widget build(BuildContext context) {
    Color color;
    switch (difficulty.toLowerCase()) {
      case 'easy':
        color = const Color(0xFF00B8A3);
        break;
      case 'medium':
        color = const Color(0xFFFFC01E);
        break;
      case 'hard':
        color = const Color(0xFFFF375F);
        break;
      default:
        color = Colors.grey;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color),
      ),
      child: Text(
        difficulty,
        style: TextStyle(
          color: color,
          fontSize: 12,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }
}
