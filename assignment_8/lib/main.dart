import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(const FetcherApp());

class Post {
  const Post({required this.id, required this.title, required this.body});

  final int id;
  final String title;
  final String body;

  factory Post.fromJson(Map<String, dynamic> json) =>
      Post(id: json['id'], title: json['title'], body: json['body']);

  Map<String, dynamic> toJson() => {'id': id, 'title': title, 'body': body};
}

class FetchResult {
  const FetchResult({
    required this.posts,
    required this.fromCache,
    required this.fetchedAt,
  });

  final List<Post> posts;
  final bool fromCache;
  final DateTime fetchedAt;
}

class PostsRepository {
  static const String _cacheKey = 'posts_cache';
  static const String _cacheTimeKey = 'posts_cache_time';
  static const String _apiUrl =
      'https://jsonplaceholder.typicode.com/posts?_limit=12';

  Future<FetchResult> loadPosts() async {
    try {
      final response = await http.get(Uri.parse(_apiUrl));
      if (response.statusCode != 200) {
        throw Exception('HTTP ${response.statusCode}');
      }
      final posts = (jsonDecode(response.body) as List)
          .map((e) => Post.fromJson(e))
          .toList();
      await _saveCache(posts);
      return FetchResult(posts: posts, fromCache: false, fetchedAt: DateTime.now());
    } catch (e) {
      final cached = await _readCache();
      if (cached != null) return cached;
      rethrow;
    }
  }

  Future<void> _saveCache(List<Post> posts) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(
        _cacheKey, jsonEncode(posts.map((p) => p.toJson()).toList()));
    await prefs.setString(_cacheTimeKey, DateTime.now().toIso8601String());
  }

  Future<FetchResult?> _readCache() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_cacheKey);
    if (raw == null) return null;
    final posts =
        (jsonDecode(raw) as List).map((e) => Post.fromJson(e)).toList();
    final time = DateTime.tryParse(prefs.getString(_cacheTimeKey) ?? '') ??
        DateTime.now();
    return FetchResult(posts: posts, fromCache: true, fetchedAt: time);
  }
}

class FetcherApp extends StatelessWidget {
  const FetcherApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'API Fetcher',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.white,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2D6A4F)),
      ),
      home: const PostsScreen(),
    );
  }
}

class PostsScreen extends StatefulWidget {
  const PostsScreen({super.key});

  @override
  State<PostsScreen> createState() => _PostsScreenState();
}

class _PostsScreenState extends State<PostsScreen> {
  final PostsRepository _repository = PostsRepository();
  late Future<FetchResult> _future;

  @override
  void initState() {
    super.initState();
    _future = _repository.loadPosts();
  }

  void _refresh() {
    setState(() {
      _future = _repository.loadPosts();
    });
  }

  String _formatTime(DateTime t) {
    String two(int n) => n.toString().padLeft(2, '0');
    return '${two(t.hour)}:${two(t.minute)}:${two(t.second)}';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('JSONPlaceholder Posts'),
        backgroundColor: const Color(0xFF2D6A4F),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh',
            onPressed: _refresh,
          ),
        ],
      ),
      body: FutureBuilder<FetchResult>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(color: Color(0xFF2D6A4F)),
                  SizedBox(height: 12),
                  Text('Fetching posts...',
                      style: TextStyle(color: Colors.grey)),
                ],
              ),
            );
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.cloud_off,
                        size: 48, color: Colors.redAccent),
                    const SizedBox(height: 12),
                    const Text('Could not load posts',
                        style: TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 4),
                    Text('${snapshot.error}',
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: Colors.grey)),
                    const SizedBox(height: 16),
                    FilledButton.icon(
                      onPressed: _refresh,
                      style: FilledButton.styleFrom(
                          backgroundColor: const Color(0xFF2D6A4F)),
                      icon: const Icon(Icons.refresh),
                      label: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            );
          }

          final result = snapshot.data!;
          return Column(
            children: [
              Container(
                width: double.infinity,
                margin: const EdgeInsets.all(16),
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                decoration: BoxDecoration(
                  color: result.fromCache
                      ? const Color(0xFFFFF4E0)
                      : const Color(0xFFE9F2EE),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  children: [
                    Icon(
                      result.fromCache ? Icons.offline_pin : Icons.cloud_done,
                      size: 18,
                      color: const Color(0xFF2D6A4F),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        result.fromCache
                            ? 'Offline — cached data from ${_formatTime(result.fetchedAt)}'
                            : 'Live data · fetched at ${_formatTime(result.fetchedAt)}',
                        style: const TextStyle(fontSize: 13),
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: result.posts.length,
                  itemBuilder: (context, index) {
                    final post = result.posts[index];
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
                            '${post.id}',
                            style: const TextStyle(
                                fontSize: 13, color: Color(0xFF2D6A4F)),
                          ),
                        ),
                        title: Text(
                          post.title,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontWeight: FontWeight.w600),
                        ),
                        subtitle: Text(
                          post.body,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
