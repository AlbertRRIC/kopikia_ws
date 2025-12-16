import 'package:flutter/material.dart';
import '../ros/ros_connection.dart';

class GrapCupScreen extends StatelessWidget {
  final RosConnection? rosConnection;

  const GrapCupScreen({super.key, this.rosConnection});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        centerTitle: true,
        title: const Text(
          'Grab Cup',
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
              'assets/images/grap_cup.png',
              width: 1280,
              height: 1024,
              fit: BoxFit.contain,
            ),

            const SizedBox(height: 24),

            const Text(
              'Robot is grabbing the filled cup from coffee machine',
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
