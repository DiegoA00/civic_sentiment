import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'widgets/sentiment_pie.dart';
import 'widgets/keyword_bars.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  static const backgroundColor = Color(0xFFE5E8EB);
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Civic Sentiment',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        scaffoldBackgroundColor: backgroundColor,
        useMaterial3: true,
      ),
      home: const DashboardPage(),
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});
  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final api = ApiService(baseUrl: 'http://localhost:8000');
  bool loading = true;
  String? error;
  Map<String, int> titleCounts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
  Map<String, int> contentCounts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
  List<dynamic> positiveKeywords = [];
  List<dynamic> negativeKeywords = [];
  final _titlesKey = GlobalKey();
  final _contentsKey = GlobalKey();
  final _keywordsKey = GlobalKey();
  final _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadAll();
  }

  Future<void> _loadAll() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final titles = await api.fetchTitles(pages: 1);
      final contents = await api.fetchContents(pages: 1);
      final keywords = await api.fetchKeywords(pages: 1);
      setState(() {
        titleCounts = api.computeSentimentCountsFromTitles(titles);
        contentCounts = api.computeSentimentCountsFromContents(contents);
        positiveKeywords = keywords['positive'] ?? [];
        negativeKeywords = keywords['negative'] ?? [];
        loading = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        loading = false;
      });
    }
  }

  void _scrollTo(GlobalKey key) {
    final ctx = key.currentContext;
    if (ctx == null) return;
    Scrollable.ensureVisible(ctx, duration: const Duration(milliseconds: 400), alignment: 0.1);
  }

  @override
  Widget build(BuildContext context) {
    final navButtonStyle = TextButton.styleFrom(foregroundColor: Colors.black);
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: const Text('Civic Sentiment', style: TextStyle(color: Colors.black)),
        actions: [
          TextButton(onPressed: () => _scrollTo(_titlesKey), style: navButtonStyle, child: const Text('Titulares')),
          TextButton(onPressed: () => _scrollTo(_contentsKey), style: navButtonStyle, child: const Text('Contenidos')),
          TextButton(onPressed: () => _scrollTo(_keywordsKey), style: navButtonStyle, child: const Text('Palabras')),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadAll,
        child: loading
            ? const Center(child: CircularProgressIndicator())
            : error != null
                ? Center(child: Text('Error: $error'))
                : SingleChildScrollView(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 16),
                        Container(key: _titlesKey, child: SentimentPie(counts: titleCounts, title: 'Sentimiento en titulares')),
                        const SizedBox(height: 24),
                        Container(key: _contentsKey, child: SentimentPie(counts: contentCounts, title: 'Sentimiento en contenidos (artículos)')),
                        const SizedBox(height: 24),
                        Container(
                          key: _keywordsKey,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Palabras por sentimiento', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
                              const SizedBox(height: 12),
                              KeywordBars(title: 'Positivas', keywords: positiveKeywords),
                              const SizedBox(height: 12),
                              KeywordBars(title: 'Negativas', keywords: negativeKeywords),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _loadAll,
        child: const Icon(Icons.refresh),
      ),
    );
  }
}
