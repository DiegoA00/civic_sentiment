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
        appBar: AppBar(title: const Text('Civic Sentiment')),
        body: const HeadlineList(),
      ),
    );
  }
}

class HeadlineSentiment {
  final String headline;
  final String label;
  final String newspaper;

  HeadlineSentiment({
    required this.headline,
    required this.label,
    required this.newspaper,
  });

  factory HeadlineSentiment.fromJson(Map<String, dynamic> json) {
    return HeadlineSentiment(
      headline: json['headline'],
      label: json['label'],
      newspaper: json['newspaper'],
    );
  }
}

class HeadlineList extends StatefulWidget {
  const HeadlineList({super.key});

  @override
  State<HeadlineList> createState() => _HeadlineListState();
}

class _HeadlineListState extends State<HeadlineList> {
  List<HeadlineSentiment> headlines = [];
  bool isLoading = true;
  String error = '';

  @override
  void initState() {
    super.initState();
    fetchHeadlines();
  }

  Future<void> fetchHeadlines() async {
    try {
      final response = await http.get(Uri.parse('http://localhost:8000/'));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        setState(() {
          headlines = data
              .map((item) => HeadlineSentiment.fromJson(item))
              .toList();
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

    return ListView.builder(
      itemCount: headlines.length,
      itemBuilder: (context, index) {
        final item = headlines[index];
        return ListTile(
          title: Text(item.headline),
          subtitle: Text('${item.label} • ${item.newspaper}'),
        );
      },
    );
  }
}
