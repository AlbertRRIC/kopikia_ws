import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import '../ros/ros_connection.dart';

class ServeCupScreen extends StatefulWidget {
  final RosConnection? rosConnection;

  const ServeCupScreen({super.key, this.rosConnection});

  @override
  State<ServeCupScreen> createState() => _ServeCupScreenState();
}

class _ServeCupScreenState extends State<ServeCupScreen> {
  final AudioPlayer _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _playSound();
  }

  Future<void> _playSound() async {
    await _player.play(AssetSource('audio/ServedCup.wav'));
    // Make sure you declared assets/sounds/serve_cup.wav in pubspec.yaml
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        centerTitle: true,
        title: const Text(
          'Serve Cup',
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
            Image.asset(
              'assets/images/serve_cup.png',
              width: 1280,
              height: 949,
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 24),
            const Text(
              'Robot served your cup! Please take your drink.',
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
