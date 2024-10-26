// lib/screens/problem_list_screen.dart
import 'package:flutter/material.dart';
import 'package:leetcode/screens/problem_detail_screen.dart';
import '../models/problem.dart';
import '../services/leetcode_service.dart';

class ProblemListScreen extends StatefulWidget {
  final List<LeetCodeProblem> problems;
  final LeetCodeService service;

  const ProblemListScreen({Key? key, required this.problems, required this.service})
      : super(key: key);

  @override
  _ProblemListScreenState createState() => _ProblemListScreenState();
}

class _ProblemListScreenState extends State<ProblemListScreen> {
  late List<LeetCodeProblem> _problems;
  String _sortOption = 'Problem Number';
  // bool _isRefreshing = false;

  @override
  void initState() {
    super.initState();
    _problems = widget.problems;
    _sortProblems();
  }

  void _sortProblems() {
    setState(() {
      if (_sortOption == 'Problem Number') {
        _problems.sort((a, b) => a.problemNumber.compareTo(b.problemNumber));
      } else if (_sortOption == 'Last Submitted') {
        _problems.sort((a, b) => b.lastSubmitted.compareTo(a.lastSubmitted));
      }
    });
  }

  Future<void> _refreshProblems() async {
    // setState(() {
    //   _isRefreshing = true;
    // });

    try {
      List<LeetCodeProblem> refreshedProblems = await widget.service.getProblems();
      setState(() {
        _problems = refreshedProblems;
        _sortProblems();
      });
    } catch (e) {
      print('Error refreshing problems: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Failed to refresh problems: $e'),
          backgroundColor: Colors.red,
        ));
      }
    } finally {
      // if (mounted) {
      //   setState(() {
      //     _isRefreshing = false;
      //   });
      // }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'LeetCode',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: const Color(0xFF1A1A1A),
        actions: [
          DropdownButton<String>(
            value: _sortOption,
            dropdownColor: const Color(0xFF1A1A1A),
            style: const TextStyle(color: Colors.white),
            iconEnabledColor: Colors.white,
            onChanged: (String? newValue) {
              if (newValue != null) {
                setState(() {
                  _sortOption = newValue;
                  _sortProblems();
                });
              }
            },
            items: <String>['Problem Number', 'Last Submitted']
                .map<DropdownMenuItem<String>>((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(value),
              );
            }).toList(),
          ),
        ],
      ),
      backgroundColor: const Color(0xFF0A0A0A),
      body: RefreshIndicator(
        onRefresh: _refreshProblems,
        child: Stack(
          children: [
            const SizedBox(height: 24),
            ListView.builder(
              itemCount: _problems.length,
              itemBuilder: (context, index) {
                final problem = _problems[index];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  color: const Color(0xFF1A1A1A),
                  child: InkWell(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => ProblemDetailScreen(problem: problem),
                        ),
                      );
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        children: [
                          Container(
                            width: 40,
                            alignment: Alignment.center,
                            child: Text(
                              '${problem.problemNumber}',
                              style: const TextStyle(
                                color: Colors.white70,
                                fontSize: 16,
                              ),
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  problem.title,
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 16,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Row(
                                  children: [
                                    _DifficultyBadge(difficulty: problem.difficulty),
                                    const SizedBox(width: 8),
                                    Expanded(
                                      child: Text(
                                        'Last submitted: ${_formatDate(problem.lastSubmitted)}',
                                        style: const TextStyle(
                                          color: Colors.white54,
                                          fontSize: 12,
                                        ),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                          const Icon(
                            Icons.chevron_right,
                            color: Colors.white54,
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
            // if (_isRefreshing)
            //   const Center(
            //     child: CircularProgressIndicator(),
            //   ),
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
