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

  // La Hora data
  Map<String, int> titleCounts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
  Map<String, int> contentCounts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
  List<dynamic> positiveKeywords = [];
  List<dynamic> negativeKeywords = [];

  // Primicias data
  Map<String, int> primiciasTitleCounts = {
    'POSITIVE': 0,
    'NEGATIVE': 0,
    'NEUTRAL': 0,
  };
  Map<String, int> primiciasContentCounts = {
    'POSITIVE': 0,
    'NEGATIVE': 0,
    'NEUTRAL': 0,
  };
  List<dynamic> primiciasPositiveKeywords = [];
  List<dynamic> primiciasNegativeKeywords = [];

  // El Universo data
  Map<String, int> elUniversoTitleCounts = {
    'POSITIVE': 0,
    'NEGATIVE': 0,
    'NEUTRAL': 0,
  };
  Map<String, int> elUniversoContentCounts = {
    'POSITIVE': 0,
    'NEGATIVE': 0,
    'NEUTRAL': 0,
  };
  List<dynamic> elUniversoPositiveKeywords = [];
  List<dynamic> elUniversoNegativeKeywords = [];

  final _titlesKey = GlobalKey();
  final _contentsKey = GlobalKey();
  final _keywordsKey = GlobalKey();
  final _primiciasTitlesKey = GlobalKey();
  final _primiciasContentsKey = GlobalKey();
  final _primiciasKeywordsKey = GlobalKey();
  final _elUniversoTitlesKey = GlobalKey();
  final _elUniversoContentsKey = GlobalKey();
  final _elUniversoKeywordsKey = GlobalKey();
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
      // Load La Hora data
      final titles = await api.fetchTitles(pages: 1);
      final contents = await api.fetchContents(pages: 1);
      final keywords = await api.fetchKeywords(pages: 1);

      // Load Primicias data with error handling
      List<Map<String, dynamic>> primiciasTitles = [];
      List<Map<String, dynamic>> primiciasAnalysis = [];
      Map<String, dynamic> primiciasKeywords = {'positive': [], 'negative': []};

      try {
        primiciasTitles = await api.fetchPrimiciasTitles();
        primiciasKeywords = api.fetchPrimiciasKeywords(primiciasTitles);
      } catch (e) {
        print('Error loading Primicias titles: $e');
      }

      try {
        primiciasAnalysis = await api.fetchPrimiciasAnalysis();
      } catch (e) {
        print('Error loading Primicias analysis (usando solo títulos): $e');
        // Si falla el análisis detallado, usar datos de títulos para contenidos
        primiciasAnalysis = [];
      }

      // Load El Universo data with error handling
      List<Map<String, dynamic>> elUniversoTitles = [];
      List<Map<String, dynamic>> elUniversoAnalysis = [];
      Map<String, dynamic> elUniversoKeywords = {
        'positive': [],
        'negative': [],
      };

      try {
        elUniversoTitles = await api.fetchElUniversoTitles();
        elUniversoKeywords = api.fetchPrimiciasKeywords(elUniversoTitles);
      } catch (e) {
        print('Error loading Primicias titles: $e');
      }

      try {
        elUniversoAnalysis = await api.fetchElUniversoAnalysis();
      } catch (e) {
        print('Error loading Primicias analysis (usando solo títulos): $e');
        // Si falla el análisis detallado, usar datos de títulos para contenidos
        elUniversoAnalysis = [];
      }

      setState(() {
        // La Hora data
        titleCounts = api.computeSentimentCountsFromTitles(titles);
        contentCounts = api.computeSentimentCountsFromContents(contents);
        positiveKeywords = keywords['positive'] ?? [];
        negativeKeywords = keywords['negative'] ?? [];

        // Primicias data
        primiciasTitleCounts = api.computeSentimentCountsFromPrimicias(
          primiciasTitles,
        );
        // Si no hay análisis detallado, usar los datos de títulos para contenidos
        primiciasContentCounts = primiciasAnalysis.isNotEmpty
            ? api.computeSentimentCountsFromPrimiciasAnalysis(primiciasAnalysis)
            : api.computeSentimentCountsFromPrimicias(primiciasTitles);
        primiciasPositiveKeywords = primiciasKeywords['positive'] ?? [];
        primiciasNegativeKeywords = primiciasKeywords['negative'] ?? [];

        // El universo data

        elUniversoTitleCounts = api.computeSentimentCountsFromPrimicias(
          elUniversoTitles,
        );
        elUniversoContentCounts = elUniversoAnalysis.isNotEmpty
            ? api.computeSentimentCountsFromPrimiciasAnalysis(
                elUniversoAnalysis,
              )
            : api.computeSentimentCountsFromPrimicias(elUniversoTitles);
        elUniversoPositiveKeywords = elUniversoKeywords['positive'] ?? [];
        elUniversoNegativeKeywords = elUniversoKeywords['negative'] ?? [];

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
    Scrollable.ensureVisible(
      ctx,
      duration: const Duration(milliseconds: 400),
      alignment: 0.1,
    );
  }

  @override
  Widget build(BuildContext context) {
    final navButtonStyle = TextButton.styleFrom(foregroundColor: Colors.black);
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: const Text(
          'Civic Sentiment',
          style: TextStyle(color: Colors.black),
        ),
        actions: [
          TextButton(
            onPressed: () => _scrollTo(_titlesKey),
            style: navButtonStyle,
            child: const Text('La Hora - Titulares'),
          ),
          TextButton(
            onPressed: () => _scrollTo(_contentsKey),
            style: navButtonStyle,
            child: const Text('La Hora - Contenidos'),
          ),
          TextButton(
            onPressed: () => _scrollTo(_keywordsKey),
            style: navButtonStyle,
            child: const Text('La Hora - Palabras'),
          ),
          TextButton(
            onPressed: () => _scrollTo(_primiciasTitlesKey),
            style: navButtonStyle,
            child: const Text('Primicias - Titulares'),
          ),
          TextButton(
            onPressed: () => _scrollTo(_primiciasContentsKey),
            style: navButtonStyle,
            child: const Text('Primicias - Contenidos'),
          ),
          TextButton(
            onPressed: () => _scrollTo(_primiciasKeywordsKey),
            style: navButtonStyle,
            child: const Text('Primicias - Palabras'),
          ),
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
                    // LA HORA SECTION
                    Container(
                      key: _titlesKey,
                      child: SentimentPie(
                        counts: titleCounts,
                        title: 'Sentimiento en titulares — Política (La Hora)',
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      key: _contentsKey,
                      child: SentimentPie(
                        counts: contentCounts,
                        title:
                            'Sentimiento en contenidos (artículos) — Política (La Hora)',
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      key: _keywordsKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Palabras por sentimiento — Política (La Hora)',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 12),
                          KeywordBars(
                            title: 'Positivas',
                            keywords: positiveKeywords,
                          ),
                          const SizedBox(height: 12),
                          KeywordBars(
                            title: 'Negativas',
                            keywords: negativeKeywords,
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 40),

                    // PRIMICIAS SECTION
                    const Divider(thickness: 2, color: Colors.grey),
                    const SizedBox(height: 20),
                    Container(
                      key: _primiciasTitlesKey,
                      child: SentimentPie(
                        counts: primiciasTitleCounts,
                        title:
                            'Sentimiento en titulares — Economía (Primicias)',
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      key: _primiciasContentsKey,
                      child: SentimentPie(
                        counts: primiciasContentCounts,
                        title:
                            'Sentimiento en contenidos — Economía (Primicias)',
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      key: _primiciasKeywordsKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Palabras por sentimiento — Economía (Primicias)',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 12),
                          KeywordBars(
                            title: 'Positivas',
                            keywords: primiciasPositiveKeywords,
                          ),
                          const SizedBox(height: 12),
                          KeywordBars(
                            title: 'Negativas',
                            keywords: primiciasNegativeKeywords,
                          ),
                        ],
                      ),
                    ),

                    // el Universo
                    const Divider(thickness: 2, color: Colors.grey),
                    const SizedBox(height: 20),
                    Container(
                      key: _elUniversoTitlesKey,
                      child: SentimentPie(
                        counts: elUniversoTitleCounts,
                        title:
                            'Sentimiento en titulares — Tecnologia (El Universo)',
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      key: _elUniversoContentsKey,
                      child: SentimentPie(
                        counts: elUniversoContentCounts,
                        title:
                            'Sentimiento en contenidos — Tecnologia (El Universo)',
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      key: _elUniversoKeywordsKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Palabras por sentimiento — Tecnologia (El Universo)',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 12),
                          KeywordBars(
                            title: 'Positivas',
                            keywords: elUniversoPositiveKeywords,
                          ),
                          const SizedBox(height: 12),
                          KeywordBars(
                            title: 'Negativas',
                            keywords: elUniversoNegativeKeywords,
                          ),
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
