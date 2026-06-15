import 'dart:io';
import 'package:rosbridge/rosbridge.dart';
import 'package:flutter/widgets.dart';


class RosConnection {
  final String url;
  late final Ros ros;
  bool connected = false;

  // --- NEW: Notifier to trigger screen changes ---
  ValueNotifier<String> screenNotifier = ValueNotifier<String>('home');

  // --- NEW: Notifier for local Wi-Fi IP ---
  ValueNotifier<String> localIpNotifier = ValueNotifier<String>('Detecting...');

  // Storage for persistent subscriptions and temporary publication queue
  final List<_DeferredSubscription> _activeSubscriptions = [];
  final List<_DeferredPublication> _publicationQueue = [];

  RosConnection({this.url = 'ws://127.0.0.1:9090'}) {
    ros = Ros(url: url);
    _initLocalIp();
    _initializeStatusListener();
    _connect();
  }

  void _initLocalIp() async {
    try {
      final interfaces = await NetworkInterface.list(type: InternetAddressType.IPv4);
      for (var interface in interfaces) {
        for (var addr in interface.addresses) {
          if (!addr.isLoopback) {
            localIpNotifier.value = addr.address;
            return;
          }
        }
      }
      localIpNotifier.value = 'Offline';
    } catch (e) {
      localIpNotifier.value = 'Unknown';
    }
  }

  void _initializeStatusListener() {
    ros.statusStream.listen((status) {
      debugPrint("[ROS] Connection Status Changed: $status");
      if (status == Status.connected) {
        connected = true;
        debugPrint("[ROS] Connected! Ready to communicate on $url");

        // Re-establish all active subscriptions on (re)connection
        for (var sub in _activeSubscriptions) {
          _doSubscribe(sub.topicName, sub.onData, messageType: sub.messageType);
        }

        // Process any queued publications
        for (var pub in _publicationQueue) {
          _doPublish(pub.topic, pub.messageType, pub.msg);
        }
        _publicationQueue.clear();
      } else {
        connected = false;
        debugPrint("[ROS] Not connected (State: $status). Retrying in 5s...");
        
        // Robust retry: triggers even if initial connection failed
        Future.delayed(const Duration(seconds: 5), () {
          if (!connected && ros.status != Status.connected) {
            debugPrint("[ROS] Retrying connection to $url...");
            _connect();
          }
        });
      }
    });
  }

  void _connect() {
    try {
      debugPrint("[ROS] Connecting to $url...");
      ros.connect();
    } catch (e) {
      debugPrint("[ROS] Immediate connection error: $e");
    }
  }

  /// Subscribe safely, even if not connected yet
  void subscribe(String topicName, void Function(dynamic) onData, {String messageType = "std_msgs/String"}) {
    // Add to persistent list so we can re-subscribe on reconnect
    _activeSubscriptions.add(_DeferredSubscription(topicName, onData, messageType: messageType));
    
    if (connected) {
      _doSubscribe(topicName, onData, messageType: messageType);
    }
  }

  void _doSubscribe(String topicName, void Function(dynamic) onData, {String messageType = "std_msgs/String"}) {
    Topic topic = Topic(ros: ros, name: topicName, type: messageType);
    topic.subscribe((message) async => onData(message));
  }

  /// Publish safely, even if not connected yet
  void publish({
    required String topic,
    required String messageType,
    required Map<String, dynamic> msg,
  }) {
    if (connected) {
      _doPublish(topic, messageType, msg);
    } else {
      debugPrint("[ROS] Not connected. Queuing publish to $topic: $msg");
      _publicationQueue.add(_DeferredPublication(topic, messageType, msg));
    }
  }

  void _doPublish(String topic, String messageType, Map<String, dynamic> msg) {
    Topic t = Topic(ros: ros, name: topic, type: messageType);
    t.publish(msg);
    debugPrint("[ROS] Published to $topic: $msg");
  }


  // --- NEW: Convenience function to subscribe to telemetry and switch screens ---
void subscribeToTelemetry(String topicName) {
  subscribe(topicName, (dynamic message) {
    try {
      debugPrint("[ROS] Telemetry: $message");

      // Extract data safely
      final String data = (message is Map && message.containsKey('data'))
          ? message['data'].toString()
          : message.toString();

      final currentScreen = screenNotifier.value;

      // ---- RULE 1: Switch to fetching cup only once ----
      if (data.contains('KopiKia:getting cup')) {
        if (currentScreen != 'fetching_cup') {
          debugPrint('[UI] Switching to Getting Cup screen');
          screenNotifier.value = 'fetching_cup';
        }
        return; // stop further processing
      }

      // ---- RULE 2: Switch to cup acquired only once ----
      if (data.contains('KopiKia:cup acquired')) {
        if (currentScreen != 'cup_acquired') {
          debugPrint('[UI] Switching to Cup Acquired screen');
          screenNotifier.value = 'cup_acquired';
        }
        return; // stop further processing
      }

      // ---- RULE 3: Switch to position cup only once ----
      if (data.contains('KopiKia:position cup')) {
        if (currentScreen != 'position_cup') {
          debugPrint('[UI] Switching to Position Cup screen');
          screenNotifier.value = 'position_cup';
        }
        return; // stop further processing
      }

      // ---- RULE 4: Switch to select drink only once ----
      if (data.contains('KopiKia:select drink')) {
        if (currentScreen != 'select_drink') {
          debugPrint('[UI] Switching to Select Drink screen');
          screenNotifier.value = 'select_drink';
        }
        return; // stop further processing
      }

      // ---- RULE 5: Switch to preparing drink only once ----
      if (data.contains('KopiKia:drink started')) {
        if (currentScreen != 'drink_started') {
          debugPrint('[UI] Switching to Drink Started screen');
          screenNotifier.value = 'drink_started';
        }
        return; // stop further processing
      }      

      // ---- RULE 6: Switch to drink ready only once ----
      if (data.contains('KopiKia:drink ready')) {
        if (currentScreen != 'drink_ready') {
          debugPrint('[UI] Switching to Drink Ready screen');
          screenNotifier.value = 'drink_ready';
        }
        return; // stop further processing
      }  

      // ---- RULE 7: Switch to cup delivery only once ----
      if (data.contains('KopiKia:grap cup')) {
        if (currentScreen != 'grap_cup') {
          debugPrint('[UI] Switching to Grap Cup screen');
          screenNotifier.value = 'grap_cup';
        }
        return; // stop further processing
      }  

      // ---- RULE 8: Switch to cup delivery only once ----
      if (data.contains('KopiKia:cup transition')) {
        if (currentScreen != 'cup_transition') {
          debugPrint('[UI] Switching to Cup Transition screen');
          screenNotifier.value = 'cup_transition';
        }
        return; // stop further processing
      }  

      // ---- RULE 9: Switch to serve cup only once ----
      if (data.contains('KopiKia:serve cup')) {
        if (currentScreen != 'serve_cup') {
          debugPrint('[UI] Switching to Serve Cup screen');
          screenNotifier.value = 'serve_cup';
        }
        return; // stop further processing
      }        

      // ---- RULE 10: Only go back home on explicit message ----
      if (data.contains('KopiKia:returned home')) {
        if (currentScreen != 'home') {
          debugPrint('[UI] Returning to HOME');
          screenNotifier.value = 'home';
        }
        return;
      }

      // ---- RULE 3: Ignore everything else ----
      debugPrint('[UI] Telemetry ignored, staying on $currentScreen');
    } catch (e, st) {
      debugPrint("[ROS] Telemetry handler error: $e\n$st");
    }
  });
}


}

/// Internal classes to store deferred subscriptions and publications
class _DeferredSubscription {
  final String topicName;
  final void Function(dynamic) onData;
  final String messageType;

  _DeferredSubscription(this.topicName, this.onData, {this.messageType = "std_msgs/String"});
}

class _DeferredPublication {
  final String topic;
  final String messageType;
  final Map<String, dynamic> msg;

  _DeferredPublication(this.topic, this.messageType, this.msg);
}
