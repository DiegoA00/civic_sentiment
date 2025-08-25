import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  ApiService({
    required this.baseUrl,
    this.timeoutSeconds = 30, // Aumentado de 10 a 30 segundos para Primicias
  });

  final String baseUrl;
  final int timeoutSeconds;
  final Map<String, String> lastFetchSource = {};

  Future<List<Map<String, dynamic>>> fetchTitles({int pages = 1}) async {
    final uri = Uri.parse('$baseUrl/lahora/politica/titles-sentiment')
        .replace(queryParameters: {'num_pages': pages.toString()});
    try {
      final respBody = await _get(uri);
      lastFetchSource['titles'] = 'backend';
      final dynamic jsonBody = jsonDecode(respBody);
      final List<dynamic> rawList = _extractList(jsonBody, 'titles');
      return rawList.map((e) => Map<String, dynamic>.from(e as Map)).toList();
    } catch (e) {
      lastFetchSource['titles'] = 'error';
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> fetchContents({int pages = 1}) async {
    final uri = Uri.parse('$baseUrl/lahora/politica/content-sentiment')
        .replace(queryParameters: {'num_pages': pages.toString()});
    try {
      final respBody = await _get(uri);
      lastFetchSource['contents'] = 'backend';
      final dynamic jsonBody = jsonDecode(respBody);
      final List<dynamic> rawList = _extractList(jsonBody, 'contents');
      return rawList.map((e) => Map<String, dynamic>.from(e as Map)).toList();
    } catch (e) {
      lastFetchSource['contents'] = 'error';
      rethrow;
    }
  }

  Future<Map<String, dynamic>> fetchKeywords({int pages = 1}) async {
    final candidates = <Uri>[
      Uri.parse('$baseUrl/lahora/politica/keywords-by-sentiment')
          .replace(queryParameters: {'num_pages': pages.toString()}),
      Uri.parse('$baseUrl/lahora/politica/keywords_by_sentiment')
          .replace(queryParameters: {'num_pages': pages.toString()}),
    ];

    for (final uri in candidates) {
      try {
        final respBody = await _get(uri);
        final dynamic jsonBody = jsonDecode(respBody);
        if (jsonBody is Map) {
          lastFetchSource['keywords'] = 'backend';
          return Map<String, dynamic>.from(jsonBody);
        }
      } catch (_) {}
    }

    try {
      final titles = await fetchTitles(pages: pages);
      final positiveWords = <String>[];
      final negativeWords = <String>[];

      final stopwords = <String>{
        'de','la','que','el','en','y','a','los','del','se','las','por','un','para','con','no','una',
        'su','al','lo','como','más','pero','sus','o','este','sí','porque','esta','entre','cuando','muy',
        'sin','sobre','también','me','hasta','hay','todo','uno','ni','otros','ese','eso','ante','ellos'
      };

      final wordRe = RegExp(r'\w+', unicode: true);

      for (final t in titles) {
        final text = (t['text'] ?? t['title'] ?? '').toString().toLowerCase();
        final sentiment = (t['sentiment'] ?? '').toString().toUpperCase();
        final words = wordRe
            .allMatches(text)
            .map((m) => m.group(0)!)
            .where((w) => !stopwords.contains(w))
            .toList();
        if (sentiment.contains('POS')) positiveWords.addAll(words);
        else if (sentiment.contains('NEG')) negativeWords.addAll(words);
      }

      Map<String,int> countMap(List<String> words) {
        final m = <String,int>{};
        for (final w in words) m[w] = (m[w] ?? 0) + 1;
        return m;
      }

      final posCounts = countMap(positiveWords);
      final negCounts = countMap(negativeWords);

      List<List<dynamic>> toListOfPairs(Map<String,int> m) {
        final entries = m.entries.toList()..sort((a,b) => b.value.compareTo(a.value));
        return entries.map((e) => [e.key, e.value]).toList();
      }

      lastFetchSource['keywords'] = 'computed_from_titles';
      return {
        'positive': toListOfPairs(posCounts),
        'negative': toListOfPairs(negCounts),
      };
    } catch (e) {
      lastFetchSource['keywords'] = 'error';
      throw Exception('Failed to fetch keywords: tried ${candidates.length} endpoints and fallback failed: $e');
    }
  }

  // Nuevos métodos para Primicias
  Future<List<Map<String, dynamic>>> fetchPrimiciasTitles() async {
    final uri = Uri.parse('$baseUrl/primicias/economia/titles');
    try {
      final respBody = await _get(uri);
      lastFetchSource['primicias_titles'] = 'backend';
      final dynamic jsonBody = jsonDecode(respBody);
      final List<dynamic> rawList = _extractList(jsonBody, 'titles');
      return rawList.map((e) => Map<String, dynamic>.from(e as Map)).toList();
    } catch (e) {
      lastFetchSource['primicias_titles'] = 'error';
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> fetchPrimiciasAnalysis() async {
    final uri = Uri.parse('$baseUrl/primicias/economia/analysis');
    try {
      final respBody = await _get(uri);
      lastFetchSource['primicias_analysis'] = 'backend';
      final dynamic jsonBody = jsonDecode(respBody);
      if (jsonBody is List) {
        return jsonBody.map((e) => Map<String, dynamic>.from(e as Map)).toList();
      }
      throw Exception('Expected analysis response to be a list.');
    } catch (e) {
      lastFetchSource['primicias_analysis'] = 'error';
      rethrow;
    }
  }

  Map<String, dynamic> fetchPrimiciasKeywords(List<Map<String, dynamic>> titles) {
    final positiveWords = <String>[];
    final negativeWords = <String>[];

    final stopwords = <String>{
      'de','la','que','el','en','y','a','los','del','se','las','por','un','para','con','no','una',
      'su','al','lo','como','más','pero','sus','o','este','sí','porque','esta','entre','cuando','muy',
      'sin','sobre','también','me','hasta','hay','todo','uno','ni','otros','ese','eso','ante','ellos',
      'tommy','wright','corporación','favorita','supermaxi','ecuador','quito','economía','primicias'
    };

    final wordRe = RegExp(r'\w+', unicode: true);

    for (final t in titles) {
      final text = (t['text'] ?? '').toString().toLowerCase();
      final sentimentObj = t['sentiment'] as Map<String, dynamic>?;
      final sentiment = (sentimentObj?['label'] ?? '').toString().toUpperCase();
      
      final words = wordRe
          .allMatches(text)
          .map((m) => m.group(0)!)
          .where((w) => w.length > 3 && !stopwords.contains(w))
          .toList();
      
      if (sentiment.contains('POS')) positiveWords.addAll(words);
      else if (sentiment.contains('NEG')) negativeWords.addAll(words);
    }

    Map<String,int> countMap(List<String> words) {
      final m = <String,int>{};
      for (final w in words) m[w] = (m[w] ?? 0) + 1;
      return m;
    }

    final posCounts = countMap(positiveWords);
    final negCounts = countMap(negativeWords);

    List<List<dynamic>> toListOfPairs(Map<String,int> m) {
      final entries = m.entries.toList()..sort((a,b) => b.value.compareTo(a.value));
      return entries.take(10).map((e) => [e.key, e.value]).toList(); // Top 10
    }

    return {
      'positive': toListOfPairs(posCounts),
      'negative': toListOfPairs(negCounts),
    };
  }

  Map<String, int> computeSentimentCountsFromPrimicias(List<Map<String, dynamic>> titles) {
    final counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
    for (final t in titles) {
      final sentimentObj = t['sentiment'] as Map<String, dynamic>?;
      final sentiment = (sentimentObj?['label'] ?? '').toString().toUpperCase();
      
      if (sentiment.contains('POS')) counts['POSITIVE'] = counts['POSITIVE']! + 1;
      else if (sentiment.contains('NEG')) counts['NEGATIVE'] = counts['NEGATIVE']! + 1;
      else counts['NEUTRAL'] = counts['NEUTRAL']! + 1;
    }
    return counts;
  }

  Map<String, int> computeSentimentCountsFromPrimiciasAnalysis(List<Map<String, dynamic>> analysis) {
    final counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
    for (final item in analysis) {
      final citas = item['citas'] as List<dynamic>?;
      final emociones = item['emociones'] as List<dynamic>?;
      
      if (citas != null && emociones != null) {
        for (final emocion in emociones) {
          if (emocion is Map<String, dynamic>) {
            final sentiment = (emocion['label'] ?? '').toString().toUpperCase();
            if (sentiment.contains('POS')) counts['POSITIVE'] = counts['POSITIVE']! + 1;
            else if (sentiment.contains('NEG')) counts['NEGATIVE'] = counts['NEGATIVE']! + 1;
            else counts['NEUTRAL'] = counts['NEUTRAL']! + 1;
          }
        }
      }
    }
    return counts;
  }

  Future<String> _get(Uri uri) async {
    try {
      final response = await http
          .get(uri, headers: {'Accept': 'application/json'})
          .timeout(Duration(seconds: timeoutSeconds));
      if (response.statusCode != 200) {
        throw Exception('HTTP ${response.statusCode} ${response.reasonPhrase}: ${response.body}');
      }
      return response.body;
    } catch (e) {
      throw Exception('Request to $uri failed: $e');
    }
  }

  List<dynamic> _extractList(dynamic jsonBody, String keyName) {
    if (jsonBody is Map && jsonBody.containsKey(keyName)) {
      final val = jsonBody[keyName];
      if (val is List) return val;
      throw Exception('Expected "$keyName" to be a list in response.');
    } else if (jsonBody is List) {
      return jsonBody;
    } else {
      throw Exception('Unexpected JSON shape: expected map with "$keyName" or a list.');
    }
  }

  Map<String, int> computeSentimentCountsFromTitles(List<Map<String, dynamic>> titles) {
    final counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
    for (final t in titles) {
      final s = (t['sentiment'] ?? '').toString().toUpperCase();
      if (s.contains('POS')) counts['POSITIVE'] = counts['POSITIVE']! + 1;
      else if (s.contains('NEG')) counts['NEGATIVE'] = counts['NEGATIVE']! + 1;
      else counts['NEUTRAL'] = counts['NEUTRAL']! + 1;
    }
    return counts;
  }

  Map<String, int> computeSentimentCountsFromContents(List<Map<String, dynamic>> contents) {
    final counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0};
    for (final c in contents) {
      final s = (c['sentiment'] ?? '').toString().toUpperCase();
      if (s.contains('POS')) counts['POSITIVE'] = counts['POSITIVE']! + 1;
      else if (s.contains('NEG')) counts['NEGATIVE'] = counts['NEGATIVE']! + 1;
      else counts['NEUTRAL'] = counts['NEUTRAL']! + 1;
    }
    return counts;
  }
}