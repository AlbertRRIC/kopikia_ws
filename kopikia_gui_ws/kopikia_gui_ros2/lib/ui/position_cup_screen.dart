import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import '../ros/ros_connection.dart';

class PositionCupScreen extends StatefulWidget {
  final RosConnection? rosConnection;

  const PositionCupScreen({super.key, this.rosConnection});

  @override
  State<PositionCupScreen> createState() => _PositionCupScreenState();
}

class _PositionCupScreenState extends State<PositionCupScreen> {
  final AudioPlayer _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _playSound();
  }

  Future<void> _playSound() async {
    await _player.play(AssetSource('audio/PositionCup.wav'));
    // Make sure you declared assets/sounds/position_cup.wav in pubspec.yaml
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
          'Position Cup',
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
              'assets/images/position_cup.png',
              width: 1280,
              height: 949,
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 24),
            const Text(
              'Robot is transferring empty cup to coffee machine',
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
