import 'package:flutter/material.dart';
import 'package:kopikia_gui_ros2/ui/cup_transition_screen.dart';
import 'ros/ros_connection.dart';

import 'ui/fetching_cup_screen.dart';
import 'ui/cup_acquired_screen.dart';
import 'ui/serve_cup_screen.dart';
import 'ui/position_cup_screen.dart';  
import 'ui/select_drink_screen.dart';
import 'ui/drink_started_screen.dart';
import 'ui/drink_ready_screen.dart';
import 'ui/grap_cup_screen.dart';
import 'ui/setup_screen.dart';
import 'ui/cup_selection_screen.dart';
import 'ui/drink_selection_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Initialize RosConnection
    final rosConnection = RosConnection(url: "ws://127.0.0.1:9090");
    rosConnection.subscribeToTelemetry('/barista/status'); // Subscribe to telemetry

    // Debug listener to verify notifier updates
    rosConnection.screenNotifier.addListener(() {
      debugPrint("[UI] ScreenNotifier updated: ${rosConnection.screenNotifier.value}");
    });

    return MaterialApp(
      title: 'Kopi Kia Robot Barista',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: ValueListenableBuilder<String>(
        valueListenable: rosConnection.screenNotifier,
        builder: (context, screen, child) {
          switch (screen) {
            case 'fetching_cup':
              return FetchCupScreen(rosConnection: rosConnection);
            case 'cup_acquired':
              return CupAcquiredScreen(rosConnection: rosConnection);
            case 'position_cup':
              return PositionCupScreen(rosConnection: rosConnection);
            case 'select_drink':
              return SelectDrinkScreen(rosConnection: rosConnection);
            case 'drink_started':
              return DrinkStartedScreen(rosConnection: rosConnection);
            case 'drink_ready':
              return DrinkReadyScreen(rosConnection: rosConnection);
            case 'grap_cup':
              return GrapCupScreen(rosConnection: rosConnection);
            case 'cup_transition':  
              return CupTransitionScreen(rosConnection: rosConnection);
            case 'drink_selection':
              return DrinkSelectionScreen(
                title: 'Kopi Kia Robot Barista',
                rosConnection: rosConnection,
              );
            case 'cup_selection':
              return CupSelectionScreen(
                title: 'Kopi Kia Robot Barista',
                rosConnection: rosConnection,
              );
            case 'setup':
              return SetupScreen(rosConnection: rosConnection);
            case 'serve_cup':
              return ServeCupScreen(rosConnection: rosConnection);      
            case 'home':
            default:
              return MyHomePage(
                title: 'Kopi Kia Robot Barista',
                rosConnection: rosConnection,
              );
          }
        },
      ),
    );
  }
}

class MyHomePage extends StatelessWidget {
  final String title;
  final RosConnection rosConnection;

  const MyHomePage({super.key, required this.title, required this.rosConnection});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        leadingWidth: 200,
        leading: Center(
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
        actions: [
          IconButton(
            icon: const Icon(Icons.settings, color: Colors.white, size: 32),
            onPressed: () {
              rosConnection.screenNotifier.value = 'setup';
            },
          ),
          const SizedBox(width: 16),
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
            const Icon(Icons.info_outline, size: 120, color: Colors.deepPurple),
            const SizedBox(height: 40),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 60),
              child: Text(
                'Please place the two different cup designs onto the cup holder.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 42,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
            ),
            const SizedBox(height: 60),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 60, vertical: 25),
                backgroundColor: Colors.deepPurple,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(40),
                ),
              ),
              onPressed: () {
                rosConnection.screenNotifier.value = 'cup_selection';
              },
              child: const Text(
                'Start Selection',
                style: TextStyle(fontSize: 28, color: Colors.white, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }
}