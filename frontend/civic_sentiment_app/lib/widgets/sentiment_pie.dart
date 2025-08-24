import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class SentimentPie extends StatelessWidget {
  const SentimentPie({super.key, required this.counts, required this.title});

  final Map<String, int> counts;
  final String title;

  @override
  Widget build(BuildContext context) {
    final total = counts.values.fold<int>(0, (s, v) => s + v);
    final titleStyle = TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: Colors.black87);
    if (total == 0) {
      return Column(
        children: [
          Center(child: Text(title, style: titleStyle)),
          const SizedBox(height: 20),
          const Text('No hay datos')
        ],
      );
    }

    final sections = <PieChartSectionData>[];
    final colors = {
      'POSITIVE': Colors.green,
      'NEGATIVE': Colors.red,
      'NEUTRAL': Colors.grey,
    };

    counts.forEach((k, v) {
      if (v <= 0) return;
      final value = v.toDouble();
      final pct = ((value / total) * 100).toStringAsFixed(0) + '%';
      sections.add(PieChartSectionData(
        color: colors[k],
        value: value,
        title: '$k\n$pct',
        titleStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
        radius: 60,
      ));
    });

    return Column(
      children: [
        Center(child: Text(title, style: titleStyle)),
        const SizedBox(height: 24),
        SizedBox(
          height: 160,
          child: Center(
            child: PieChart(
              PieChartData(
                sections: sections,
                sectionsSpace: 4,
                centerSpaceRadius: 24,
              ),
            ),
          ),
        ),
      ],
    );
  }
}