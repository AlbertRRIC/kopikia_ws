import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import '../ros/ros_connection.dart';

class FetchCupScreen extends StatefulWidget {
  final RosConnection? rosConnection;

  const FetchCupScreen({super.key, this.rosConnection});

  @override
  State<FetchCupScreen> createState() => _FetchCupScreenState();
}

class _FetchCupScreenState extends State<FetchCupScreen> {
  final AudioPlayer _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _playSound();
  }

  Future<void> _playSound() async {
    await _player.play(AssetSource('audio/FetchCup.wav')); 
    // Make sure you declared assets/sounds/fetching.wav in pubspec.yaml
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
          'Fetching Cup',
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
              'assets/images/fetching_cup.png',
              width: 1280,
              height: 949,
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 24),
            const Text(
              'Robot is moving towards the cup holder',
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
