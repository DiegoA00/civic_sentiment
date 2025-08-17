import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('News Headlines')),
        body: const HeadlineList(),
      ),
    );
  }
}

class HeadlineList extends StatefulWidget {
  const HeadlineList({super.key});

  @override
  State<HeadlineList> createState() => _HeadlineListState();
}

class _HeadlineListState extends State<HeadlineList> {
  List<String> headlines = [];
  bool isLoading = true;
  String error = '';

  @override
  void initState() {
    super.initState();
    fetchHeadlines();
  }

  Future<void> fetchHeadlines() async {
    try {
      // Use your FastAPI server URL (localhost works for web)
      final response = await http.get(Uri.parse('http://localhost:8000/'));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          headlines = List<String>.from(data['message']);
          isLoading = false;
        });
      } else {
        throw Exception('Server returned ${response.statusCode}');
      }
    } catch (e) {
      setState(() {
        error = 'Failed to load: $e';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (error.isNotEmpty) {
      return Center(child: Text(error));
    }

    return ListView(
      children: [
        for (final headline in headlines) ListTile(title: Text(headline)),
      ],
    );
  }
}
