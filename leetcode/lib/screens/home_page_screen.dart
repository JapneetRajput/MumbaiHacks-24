// lib/screens/home_page_screen.dart
import 'package:flutter/material.dart';
import 'problem_list_screen.dart';
import '../models/problem.dart';
import '../services/leetcode_service.dart';

class HomePageScreen extends StatelessWidget {
  final List<LeetCodeProblem> problems;
  final LeetCodeService service;

  const HomePageScreen({Key? key, required this.problems, required this.service})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LeetCode Home'),
        backgroundColor: const Color(0xFF1A1A1A),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          children: [
            _buildTile(context, 'Problems', Icons.code, () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ProblemListScreen(problems: problems, service: service),
                ),
              );
            }),
            _buildTile(context, 'Resources', Icons.book, () {
              // Navigate to Resources Screen (To be implemented)
            }),
            _buildTile(context, 'Roadmaps', Icons.map, () {
              // Navigate to Roadmaps Screen (To be implemented)
            }),
            _buildTile(context, 'Quiz', Icons.quiz, () {
              // Navigate to Quiz Screen (To be implemented)
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildTile(BuildContext context, String title, IconData icon, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: const Color(0xFF1A1A1A),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              spreadRadius: 2,
              blurRadius: 5,
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: Colors.white),
            const SizedBox(height: 10),
            Text(
              title,
              style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }
}
