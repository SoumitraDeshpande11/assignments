import 'package:flutter/material.dart';

void main() => runApp(const DashboardApp());

class DashboardApp extends StatelessWidget {
  const DashboardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Responsive Dashboard',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.white,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2D6A4F)),
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  static const stats = [
    ('Revenue', '₹4.2L', Icons.payments_outlined),
    ('Orders', '1,284', Icons.shopping_bag_outlined),
    ('Customers', '856', Icons.people_outline),
    ('Refunds', '12', Icons.undo),
    ('Conversion', '3.4%', Icons.trending_up),
    ('Avg. Order', '₹327', Icons.receipt_long_outlined),
    ('Sessions', '9,410', Icons.bolt_outlined),
    ('Bounce Rate', '41%', Icons.exit_to_app),
  ];

  static const activity = [
    ('Priya placed order #1284', '2 min ago'),
    ('Refund issued for order #1201', '18 min ago'),
    ('New customer signup: Arjun', '44 min ago'),
    ('Order #1279 shipped', '1 hr ago'),
    ('Weekly report generated', '3 hrs ago'),
    ('Inventory alert: low stock', '5 hrs ago'),
    ('Payment settled: ₹18,240', 'Yesterday'),
  ];

  @override
  Widget build(BuildContext context) {
    // MediaQuery: pick the layout from the current screen width.
    final width = MediaQuery.of(context).size.width;
    final columns = width >= 900
        ? 4
        : width >= 600
        ? 3
        : 2;
    final isWide = width >= 900;

    final statsGrid = GridView.builder(
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: columns,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.4,
      ),
      itemCount: stats.length,
      itemBuilder: (context, i) =>
          StatCard(title: stats[i].$1, value: stats[i].$2, icon: stats[i].$3),
    );

    final activityList = ListView.separated(
      itemCount: activity.length,
      separatorBuilder: (_, __) => const Divider(height: 1),
      itemBuilder: (context, i) => ListTile(
        dense: true,
        leading: const Icon(Icons.circle, size: 8, color: Color(0xFF2D6A4F)),
        title: Text(activity[i].$1),
        trailing: Text(
          activity[i].$2,
          style: const TextStyle(color: Colors.grey, fontSize: 12),
        ),
      ),
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('Store Dashboard'),
        backgroundColor: Colors.white,
        surfaceTintColor: Colors.transparent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header summary row: Expanded splits the space evenly.
            Row(
              children: const [
                Expanded(
                  child: SummaryChip(label: 'Today', value: '₹12,480'),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: SummaryChip(label: 'This week', value: '₹86,120'),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: SummaryChip(label: 'This month', value: '₹4.2L'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const SectionTitle('Overview'),
            const SizedBox(height: 8),
            // Flexible/Expanded: the grid and list share the remaining space.
            Expanded(
              child: isWide
                  ? Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Flexible(flex: 2, child: statsGrid),
                        const SizedBox(width: 16),
                        Flexible(
                          flex: 1,
                          child: ActivityPanel(child: activityList),
                        ),
                      ],
                    )
                  : Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(flex: 3, child: statsGrid),
                        const SizedBox(height: 16),
                        const SectionTitle('Recent activity'),
                        const SizedBox(height: 8),
                        Expanded(flex: 2, child: activityList),
                      ],
                    ),
            ),
          ],
        ),
      ),
    );
  }
}

class StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;

  const StatCard({
    super.key,
    required this.title,
    required this.value,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFF4F6F5),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Icon(icon, size: 20, color: const Color(0xFF2D6A4F)),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                value,
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                ),
              ),
              Text(
                title,
                style: const TextStyle(color: Colors.grey, fontSize: 12),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class SummaryChip extends StatelessWidget {
  final String label;
  final String value;

  const SummaryChip({super.key, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 14),
      decoration: BoxDecoration(
        color: const Color(0xFF2D6A4F),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(color: Colors.white70, fontSize: 12),
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}

class ActivityPanel extends StatelessWidget {
  final Widget child;

  const ActivityPanel({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFF4F6F5),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.fromLTRB(16, 14, 16, 4),
            child: SectionTitle('Recent activity'),
          ),
          Expanded(child: child),
        ],
      ),
    );
  }
}

class SectionTitle extends StatelessWidget {
  final String text;

  const SectionTitle(this.text, {super.key});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
    );
  }
}
