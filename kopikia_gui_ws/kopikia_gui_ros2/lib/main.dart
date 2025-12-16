import 'package:flutter/material.dart';
import 'package:kopikia_gui_ros2/ui/cup_transition_screen.dart';
import 'ros/ros_connection.dart';
import 'ui/telemetry_panel.dart';
import 'ui/fetching_cup_screen.dart';
import 'ui/cup_acquired_screen.dart';
import 'ui/serve_cup_screen.dart';
import 'ui/position_cup_screen.dart';  
import 'ui/select_drink_screen.dart';
import 'ui/drink_started_screen.dart';
import 'ui/drink_ready_screen.dart';
import 'ui/grap_cup_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Initialize RosConnection
    final rosConnection = RosConnection(url: "ws://172.26.115.102:9090");
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

class MyHomePage extends StatefulWidget {
  final String title;
  final RosConnection rosConnection;

  const MyHomePage({super.key, required this.title, required this.rosConnection});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // Configurable button size
  double buttonSize = 320;

  // Drink labels
  final List<String> labels = [
    "Espresso",
    "Americano",
    "Cappuccino",
    "Latte",
    "Milo",
    "Milo Mocha",
    "Salted Caramel Latte",
    "Matcha Latte",
    "Dirty Matcha",
  ];

  // Paths to coffee images in assets
  final List<String> images = [
    'assets/images/espresso.png',
    'assets/images/americano.png',
    'assets/images/cappuccino.png',
    'assets/images/latte.png',
    'assets/images/milo.png',
    'assets/images/mocha.png',
    'assets/images/salted_caramel_latte.png',
    'assets/images/matcha_latte.png',
    'assets/images/dirty_matcha.png',
  ];

  @override
  Widget build(BuildContext context) {
    double textSize = 36;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        centerTitle: true,
        title: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
          child: Text(
            widget.title,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              // Telemetry Panel (safe subscription)
              TelemetryPanel(rosConnection: widget.rosConnection),

              // Homepage title above the grid
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 24.0),
                child: Text(
                  'Select a Drink',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 36,
                    fontWeight: FontWeight.bold,
                    color: Colors.deepPurple,
                  ),
                ),
              ),

              // 3x3 Button Grid
              SizedBox(
                width: buttonSize * 3 + 24,
                height: buttonSize * 3 + 24,
                child: GridView.count(
                  crossAxisCount: 3,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 1,
                  physics: const NeverScrollableScrollPhysics(),
                  children: List.generate(9, (index) {
                    return SizedBox(
                      width: buttonSize,
                      height: buttonSize,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.zero,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(18),
                          ),
                        ),
                        onPressed: () {
                          debugPrint("${labels[index]} pressed");

                          widget.rosConnection.publish(
                            topic: "/barista/cmd",
                            messageType: "std_msgs/String",
                            msg: {
                              "data": labels[index]
                                  .toLowerCase()
                                  .replaceAll(' ', '_')
                            },
                          );
                        },
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            SizedBox(
                              width: buttonSize * 0.6,
                              height: buttonSize * 0.6,
                              child: Image.asset(
                                images[index],
                                fit: BoxFit.contain,
                              ),
                            ),
                            SizedBox(height: buttonSize * 0.05),
                            Text(
                              labels[index],
                              style: TextStyle(fontSize: textSize),
                              textAlign: TextAlign.center,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
