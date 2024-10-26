// lib/widgets/difficulty_badge.dart
import 'package:flutter/material.dart';

class DifficultyBadge extends StatelessWidget {
  final String difficulty;

  const DifficultyBadge({Key? key, required this.difficulty}) : super(key: key);

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