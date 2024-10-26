// lib/services/leetcode_service.dart
import 'package:mongo_dart/mongo_dart.dart';
import '../models/problem.dart';

class LeetCodeService {
  final String mongoUri;
  Db? _db;

  LeetCodeService({required this.mongoUri});

  Future<List<LeetCodeProblem>> getProblems() async {
    try {
      _db ??= await Db.create(mongoUri);

      if (!(_db?.isConnected ?? false)) {
        await _db?.open();
      }

      final collection = _db?.collection('problems');
      final List<Map<String, dynamic>> problemsData =
          await collection?.find().toList() ?? [];

      return problemsData.map((data) => LeetCodeProblem.fromMongo(data)).toList();
    } catch (e) {
      print('Error fetching problems: $e');
      rethrow;
    }
  }

  Future<void> close() async {
    await _db?.close();
  }
}
