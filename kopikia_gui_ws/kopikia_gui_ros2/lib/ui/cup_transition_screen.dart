import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import '../ros/ros_connection.dart';

class CupTransitionScreen extends StatefulWidget {
  final RosConnection? rosConnection;

  const CupTransitionScreen({super.key, this.rosConnection});

  @override
  State<CupTransitionScreen> createState() => _CupTransitionScreenState();
}

class _CupTransitionScreenState extends State<CupTransitionScreen> {
  final AudioPlayer _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _playSound();
  }

  Future<void> _playSound() async {
    await _player.play(AssetSource('audio/CupTransition.wav'));
    // Make sure you declared assets/sounds/cup_transition.wav in pubspec.yaml
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
          'Delivering Cup',
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
              'assets/images/cup_transition.png',
              width: 1280,
              height: 949,
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 24),
            const Text(
              'Robot is delivering your drink',
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
