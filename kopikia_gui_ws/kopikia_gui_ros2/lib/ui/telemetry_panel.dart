import 'package:flutter/material.dart';
import '../ros/ros_connection.dart';

class TelemetryPanel extends StatefulWidget {
  final RosConnection rosConnection;

  const TelemetryPanel({super.key, required this.rosConnection});

  @override
  State<TelemetryPanel> createState() => _TelemetryPanelState();
}

class _TelemetryPanelState extends State<TelemetryPanel> {
  String latestData = "Waiting for data...";

  @override
  void initState() {
    super.initState();

    // Subscribe safely
    widget.rosConnection.subscribe("/barista/status", (data) {
      setState(() {
        latestData = data.toString();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              "Telemetry",
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(latestData),
          ],
        ),
      ),
    );
  } 
}
