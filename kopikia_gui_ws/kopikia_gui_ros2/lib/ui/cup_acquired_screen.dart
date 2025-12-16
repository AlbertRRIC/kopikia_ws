import 'package:flutter/material.dart';
import '../ros/ros_connection.dart';

class CupAcquiredScreen extends StatelessWidget {
  final RosConnection? rosConnection;

  const CupAcquiredScreen({super.key, this.rosConnection});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        centerTitle: true,
        title: const Text(
          'Cup Acquired',
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
              'assets/images/cup_acquired.png',
              width: 1280,
              height: 1024,
              fit: BoxFit.contain,
            ),

            const SizedBox(height: 24),

            const Text(
              'Robot is fetching the empty cup',
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
