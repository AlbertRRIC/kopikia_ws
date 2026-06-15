import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import '../ros/ros_connection.dart';

class GrapCupScreen extends StatefulWidget {
  final RosConnection? rosConnection;

  const GrapCupScreen({super.key, this.rosConnection});

  @override
  State<GrapCupScreen> createState() => _GrapCupScreenState();
}

class _GrapCupScreenState extends State<GrapCupScreen> {
  final AudioPlayer _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _playSound();
  }

  Future<void> _playSound() async {
    await _player.play(AssetSource('audio/GrapCup.wav'));
    // Make sure you declared assets/sounds/grap_cup.wav in pubspec.yaml
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
            Image.asset(
              'assets/images/grap_cup.png',
              width: 1280,
              height: 949,
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
