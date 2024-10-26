// lib/main.dart
import 'package:flutter/material.dart';
import 'models/problem.dart';
import 'screens/problem_list_screen.dart';
import 'screens/home_page_screen.dart';
import 'services/leetcode_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LeetCode',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0A0A0A),
        primaryColor: const Color(0xFF1A1A1A),
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final LeetCodeService _service = LeetCodeService(
    mongoUri: 'mongodb+srv://arjun:empathyarjun@empathy.nuqkypk.mongodb.net/leetcode',
  );

  late Future<List<LeetCodeProblem>> _problemsFuture;

  @override
  void initState() {
    super.initState();
    _problemsFuture = _service.getProblems();
  }

  @override
  void dispose() {
    _service.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<LeetCodeProblem>>(
      future: _problemsFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        } else if (snapshot.hasError) {
          return Scaffold(
            body: Center(
              child: Text(
                'Error: ${snapshot.error}',
                style: const TextStyle(color: Colors.white),
              ),
            ),
          );
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const Scaffold(
            body: Center(
              child: Text(
                'No problems found',
                style: TextStyle(color: Colors.white),
              ),
            ),
          );
        }

        // Pass the problems and the service to HomePageScreen
        return HomePageScreen(problems: snapshot.data!, service: _service);
      },
    );
  }
}
