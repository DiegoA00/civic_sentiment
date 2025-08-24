import 'package:flutter/material.dart';

class KeywordBars extends StatelessWidget {
  const KeywordBars({
    super.key,
    required this.title,
    required this.keywords,
    this.maxBars = 10,
  });

  final String title;
  final List<dynamic> keywords;
  final int maxBars;

  @override
  Widget build(BuildContext context) {
    final top = keywords.take(maxBars).toList();
    final maxCount = top.isNotEmpty ? (top.map((e) => (e[1] as num).toDouble()).reduce((a, b) => a > b ? a : b)) : 1.0;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        ...top.map((k) {
          final word = k[0] as String;
          final count = (k[1] as num).toDouble();
          final fraction = (count / maxCount).clamp(0.0, 1.0);
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 6.0),
            child: Row(
              children: [
                Expanded(
                  flex: 4,
                  child: Text(word, style: const TextStyle(fontSize: 14)),
                ),
                const SizedBox(width: 8),
                Expanded(
                  flex: 10,
                  child: Stack(
                    children: [
                      Container(
                        height: 22,
                        decoration: BoxDecoration(
                          color: Colors.grey.shade300,
                          borderRadius: BorderRadius.circular(4),
                        ),
                      ),
                      FractionallySizedBox(
                        widthFactor: fraction,
                        child: Container(
                          height: 22,
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.primary,
                            borderRadius: BorderRadius.circular(4),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                SizedBox(width: 40, child: Text(count.toInt().toString(), textAlign: TextAlign.right)),
              ],
            ),
          );
        }).toList(),
      ],
    );
  }
}