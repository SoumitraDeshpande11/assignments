import 'package:flutter/material.dart';

void main() => runApp(const ProductApp());

class Product {
  const Product({
    required this.name,
    required this.category,
    required this.price,
    required this.rating,
    required this.emoji,
  });

  final String name;
  final String category;
  final double price;
  final double rating;
  final String emoji;
}

class ProductApp extends StatelessWidget {
  const ProductApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Product Catalog',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.white,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2D6A4F)),
      ),
      home: const CatalogScreen(),
    );
  }
}

class CatalogScreen extends StatefulWidget {
  const CatalogScreen({super.key});

  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  static const String _all = 'All';

  final TextEditingController _searchController = TextEditingController();

  final List<Product> _products = const [
    Product(name: 'Wireless Headphones', category: 'Electronics', price: 79.99, rating: 4.6, emoji: '🎧'),
    Product(name: 'Smart Watch', category: 'Electronics', price: 129.00, rating: 4.3, emoji: '⌚'),
    Product(name: 'Bluetooth Speaker', category: 'Electronics', price: 45.50, rating: 4.1, emoji: '🔊'),
    Product(name: 'Denim Jacket', category: 'Clothing', price: 59.99, rating: 4.4, emoji: '🧥'),
    Product(name: 'Running Shoes', category: 'Clothing', price: 89.95, rating: 4.7, emoji: '👟'),
    Product(name: 'Cotton T-Shirt', category: 'Clothing', price: 19.99, rating: 4.0, emoji: '👕'),
    Product(name: 'Organic Coffee Beans', category: 'Grocery', price: 14.50, rating: 4.8, emoji: '☕'),
    Product(name: 'Green Tea Box', category: 'Grocery', price: 9.99, rating: 4.2, emoji: '🍵'),
    Product(name: 'Almond Butter', category: 'Grocery', price: 11.25, rating: 4.5, emoji: '🥜'),
    Product(name: 'The Silent River', category: 'Books', price: 16.99, rating: 4.6, emoji: '📖'),
    Product(name: 'Atomic Notes', category: 'Books', price: 21.00, rating: 4.9, emoji: '📘'),
    Product(name: 'Cooking Made Simple', category: 'Books', price: 27.50, rating: 4.4, emoji: '📗'),
  ];

  String _searchQuery = '';
  String _selectedCategory = _all;

  List<String> get _categories =>
      [_all, ..._products.map((p) => p.category).toSet()];

  List<Product> get _filteredProducts {
    final query = _searchQuery.toLowerCase();
    return _products.where((p) {
      final matchesSearch =
          query.isEmpty || p.name.toLowerCase().contains(query);
      final matchesCategory =
          _selectedCategory == _all || p.category == _selectedCategory;
      return matchesSearch && matchesCategory;
    }).toList();
  }

  void _onSearchChanged(String value) {
    setState(() {
      _searchQuery = value;
    });
  }

  void _onCategorySelected(String category) {
    setState(() {
      _selectedCategory = category;
    });
  }

  void _clearSearch() {
    setState(() {
      _searchQuery = '';
      _searchController.clear();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final filtered = _filteredProducts;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Product Catalog'),
        backgroundColor: const Color(0xFF2D6A4F),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: TextField(
              controller: _searchController,
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                hintText: 'Search products...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchQuery.isEmpty
                    ? null
                    : IconButton(
                        icon: const Icon(Icons.close),
                        onPressed: _clearSearch,
                      ),
                filled: true,
                fillColor: const Color(0xFFF4F6F5),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
          SizedBox(
            height: 48,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              itemCount: _categories.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final category = _categories[index];
                final selected = category == _selectedCategory;
                return ChoiceChip(
                  label: Text(category),
                  selected: selected,
                  onSelected: (_) => _onCategorySelected(category),
                  selectedColor: const Color(0xFF2D6A4F),
                  labelStyle: TextStyle(
                    color: selected ? Colors.white : Colors.black87,
                  ),
                  backgroundColor: const Color(0xFFF4F6F5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                    side: BorderSide.none,
                  ),
                  showCheckmark: false,
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Align(
              alignment: Alignment.centerLeft,
              child: Text(
                '${filtered.length} of ${_products.length} products',
                style: const TextStyle(color: Colors.grey),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: filtered.isEmpty
                ? const Center(
                    child: Text(
                      'No products match your search.',
                      style: TextStyle(color: Colors.grey),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    itemCount: filtered.length,
                    itemBuilder: (context, index) {
                      final product = filtered[index];
                      return Card(
                        elevation: 0,
                        color: const Color(0xFFF4F6F5),
                        margin: const EdgeInsets.only(bottom: 8),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: Colors.white,
                            child: Text(
                              product.emoji,
                              style: const TextStyle(fontSize: 20),
                            ),
                          ),
                          title: Text(product.name),
                          subtitle: Row(
                            children: [
                              const Icon(Icons.star,
                                  size: 14, color: Colors.amber),
                              const SizedBox(width: 4),
                              Text('${product.rating} · ${product.category}'),
                            ],
                          ),
                          trailing: Text(
                            '\$${product.price.toStringAsFixed(2)}',
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF2D6A4F),
                              fontSize: 15,
                            ),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
