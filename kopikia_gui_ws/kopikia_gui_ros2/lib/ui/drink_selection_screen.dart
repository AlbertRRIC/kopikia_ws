import 'package:flutter/material.dart';
import '../ros/ros_connection.dart';

class DrinkSelectionScreen extends StatefulWidget {
  final String title;
  final RosConnection rosConnection;

  const DrinkSelectionScreen({super.key, required this.title, required this.rosConnection});

  @override
  State<DrinkSelectionScreen> createState() => _DrinkSelectionScreenState();
}

class _DrinkSelectionScreenState extends State<DrinkSelectionScreen> {
  // Configurable button size
  double buttonSize = 240;

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
    double textSize = 28;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white, size: 32),
          onPressed: () {
            widget.rosConnection.screenNotifier.value = 'home';
          },
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: Center(
              child: ValueListenableBuilder<String>(
                valueListenable: widget.rosConnection.localIpNotifier,
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
          ),
        ],
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
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 8.0),
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
                              "data": labels[index].toLowerCase().replaceAll(' ', '_')
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