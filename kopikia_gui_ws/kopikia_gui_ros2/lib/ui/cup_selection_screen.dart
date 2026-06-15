import 'package:flutter/material.dart';
import '../ros/ros_connection.dart';

class CupSelectionScreen extends StatelessWidget {
  final String title;
  final RosConnection rosConnection;

  const CupSelectionScreen({super.key, required this.title, required this.rosConnection});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white, size: 32),
          onPressed: () => rosConnection.screenNotifier.value = 'home',
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: Center(
              child: ValueListenableBuilder<String>(
                valueListenable: rosConnection.localIpNotifier,
                builder: (context, ip, _) => Text(
                  'IP: $ip',
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
              ),
            ),
          ),
        ],
        centerTitle: true,
        title: Text(
          title,
          style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Select Your Cup Type',
              style: TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Colors.deepPurple),
            ),
            const SizedBox(height: 80),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildCupButton('Cup 1', 'assets/photo/cup1.png'),
                _buildCupButton('Cup 2', 'assets/photo/cup2.png'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCupButton(String label, String imagePath) {
    return GestureDetector(
      onTap: () {
        debugPrint("$label selected");
        rosConnection.screenNotifier.value = 'drink_selection';
      },
      child: Column(
        children: [
          Container(
            width: 300,
            height: 300,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 10,
                  spreadRadius: 5,
                ),
              ],
            ),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Image.asset(imagePath, fit: BoxFit.contain),
            ),
          ),
          const SizedBox(height: 20),
          Text(
            label,
            style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}