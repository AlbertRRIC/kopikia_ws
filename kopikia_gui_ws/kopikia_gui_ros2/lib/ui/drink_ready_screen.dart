import 'package:flutter/material.dart';
import '../ros/ros_connection.dart';

class DrinkReadyScreen extends StatelessWidget {
  final RosConnection? rosConnection;

  const DrinkReadyScreen({super.key, this.rosConnection});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        centerTitle: true,
        title: const Text(
          'Drink Ready',
          style: TextStyle(
            fontSize: 36,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // BIG IMAGE
            Image.asset(
              'assets/images/drink_ready.png',
              width: 1280,
              height: 1024,
              fit: BoxFit.contain,
            ),

            const SizedBox(height: 24),

            const Text(
              'Robot detect your drink is ready',
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
