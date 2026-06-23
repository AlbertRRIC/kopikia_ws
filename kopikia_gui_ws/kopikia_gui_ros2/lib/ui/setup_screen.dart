import 'package:flutter/material.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:path/path.dart' as p;
import '../ros/ros_connection.dart';

class SetupScreen extends StatefulWidget {
  final RosConnection rosConnection;

  const SetupScreen({super.key, required this.rosConnection});

  @override
  State<SetupScreen> createState() => _SetupScreenState();
}

class TrainingState {
  final String log;
  final bool isTraining;
  const TrainingState({required this.log, this.isTraining = false});
}

class _SetupScreenState extends State<SetupScreen> {
  final ValueNotifier<TrainingState> _trainingState = ValueNotifier<TrainingState>(TrainingState(log: ''));

  Future<void> _signalContinue() async {
    final signalFile = File('/home/jetsonros2/MyProject/kopikia_ws/src/kopikia_vision/.continue_training');
    await signalFile.writeAsString('continue');
  }

  Future<void> _handlePhotoImport(BuildContext context, String category) async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.image,
        dialogTitle: 'Select $category Images',
        allowMultiple: true,
      );

      if (result == null || result.files.isEmpty) return;

      String targetDirPath;
      String baseFileName;

      if (category == "Cup 1 Design") {
        targetDirPath = '/home/jetsonros2/MyProject/kopikia_ws/src/kopikia_vision/assets/cup1';
        baseFileName = 'cup1';
      } else if (category == "Cup 2 Design") {
        targetDirPath = '/home/jetsonros2/MyProject/kopikia_ws/src/kopikia_vision/assets/cup2';
        baseFileName = 'cup2';
      } else {
        return;
      }

      await Directory(targetDirPath).create(recursive: true);

      final Directory dir = Directory(targetDirPath);
      final List<FileSystemEntity> files = await dir.list().toList();

      int highestNumber = 0;
      final RegExp regExp = RegExp(r'^' + baseFileName + r'_(\d+)\.');

      for (var file in files) {
        if (file is File) {
          final String fileName = p.basename(file.path);
          final Match? match = regExp.firstMatch(fileName);
          if (match != null) {
            final int number = int.parse(match.group(1)!);
            if (number > highestNumber) {
              highestNumber = number;
            }
          }
        }
      }

      for (final file in result.files) {
        if (file.path == null) continue;

        final String sourcePath = file.path!;
        final String fileName = file.name;
        final String fileExtension = p.extension(fileName);

        int newNumber = highestNumber + 1;
        final String newFileName = '${baseFileName}_${newNumber.toString().padLeft(3, '0')}$fileExtension';
        final String targetPath = p.join(targetDirPath, newFileName);

        await File(sourcePath).copy(targetPath);
        highestNumber = newNumber;
      }

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Successfully imported ${result.files.length} images to $category.')),
        );
      }
    } catch (e) {
      debugPrint("Error importing photo: $e");
    }
  }

  Future<void> _handleUIPhotoImport(BuildContext context, String targetFileName) async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.image,
        dialogTitle: 'Select UI Image ($targetFileName)',
      );

      if (result != null && result.files.single.path != null) {
        final String sourcePath = result.files.single.path!;

        final String targetDirPath = '/home/jetsonros2/MyProject/kopikia_ws/kopikia_gui_ws/kopikia_gui_ros2/assets/photo';

        await Directory(targetDirPath).create(recursive: true);

        final String targetPath = p.join(targetDirPath, targetFileName);

        final File sourceFile = File(sourcePath);
        await sourceFile.copy(targetPath);

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Successfully updated UI icon: $targetFileName')),
          );
        }
      }
    } catch (e) {
      debugPrint("Error updating UI photo: $e");
    }
  }

  Future<void> _runYoloClassification() async {
    final String scriptPath = '/home/jetsonros2/MyProject/kopikia_ws/src/kopikia_vision/train_classification.py';
    _trainingState.value = TrainingState(log: 'Starting training...\n', isTraining: true);

    final Process process = await Process.start('python3', [scriptPath]);

    String stderrBuffer = '';

    process.stdout.transform(const SystemEncoding().decoder).listen((data) {
      _trainingState.value = TrainingState(
        log: _trainingState.value.log + data,
        isTraining: true,
      );
    });

    process.stderr.transform(const SystemEncoding().decoder).listen((data) {
      stderrBuffer += data;
      _trainingState.value = TrainingState(
        log: _trainingState.value.log + '\nErrors:\n' + stderrBuffer,
        isTraining: true,
      );
    });

    final int exitCode = await process.exitCode;

    String finalMessage = '';
    if (exitCode == 0) {
      finalMessage = 'YOLO training completed successfully.';
    } else {
      finalMessage = 'Training failed with exit code $exitCode.';
    }

    _trainingState.value = TrainingState(
      log: _trainingState.value.log + '\n$finalMessage\n',
      isTraining: false,
    );

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(finalMessage)),
      );
    }
  }

  Future<void> _runYoloDetection() async {
    final String scriptPath = '/home/jetsonros2/MyProject/kopikia_ws/src/kopikia_vision/train_detection.py';
    _trainingState.value = TrainingState(log: 'Starting training...\n', isTraining: true);

    final Process process = await Process.start('python3', [scriptPath]);

    String stderrBuffer = '';

    process.stdout.transform(const SystemEncoding().decoder).listen((data) {
      _trainingState.value = TrainingState(
        log: _trainingState.value.log + data,
        isTraining: true,
      );
    });

    process.stderr.transform(const SystemEncoding().decoder).listen((data) {
      stderrBuffer += data;
      _trainingState.value = TrainingState(
        log: _trainingState.value.log + '\nErrors:\n' + stderrBuffer,
        isTraining: true,
      );
    });

    final int exitCode = await process.exitCode;

    String finalMessage = '';
    if (exitCode == 0) {
      finalMessage = 'YOLO training completed successfully.';
    } else {
      finalMessage = 'Training failed with exit code $exitCode.';
    }

    _trainingState.value = TrainingState(
      log: _trainingState.value.log + '\n$finalMessage\n',
      isTraining: false,
    );

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(finalMessage)),
      );
    }
  }

  void _showClassificationDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext dialogContext) {
        return ValueListenableBuilder<TrainingState>(
          valueListenable: _trainingState,
          builder: (context, trainingState, child) {
            final showContinueButton = trainingState.log.contains('ACTION REQUIRED') || trainingState.log.contains('Continue button');
            return AlertDialog(
              title: const Text('YOLO Classification Training Log'),
              content: Container(
                width: double.maxFinite,
                height: 400,
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(8),
                ),
                padding: const EdgeInsets.all(12),
                child: SingleChildScrollView(
                  reverse: true,
                  child: Text(
                    trainingState.log,
                    style: const TextStyle(
                      color: Colors.green,
                      fontFamily: 'monospace',
                      fontSize: 12,
                    ),
                  ),
                ),
              ),
              actions: <Widget>[
                if (showContinueButton)
                  TextButton(
                    onPressed: () async {
                      await _signalContinue();
                    },
                    child: const Text('Continue'),
                  ),
                TextButton(
                  onPressed: trainingState.isTraining ? null : () {
                    Navigator.of(dialogContext).pop();
                  },
                  child: const Text('Close'),
                ),
              ],
            );
          },
        );
      },
    );
    _runYoloClassification();
  }

  void _showDetectionDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext dialogContext) {
        return ValueListenableBuilder<TrainingState>(
          valueListenable: _trainingState,
          builder: (context, trainingState, child) {
            final showContinueButton = trainingState.log.contains('ACTION REQUIRED') || trainingState.log.contains('Continue button');
            return AlertDialog(
              title: const Text('YOLO Detection Training Log'),
              content: Container(
                width: double.maxFinite,
                height: 400,
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(8),
                ),
                padding: const EdgeInsets.all(12),
                child: SingleChildScrollView(
                  reverse: true,
                  child: Text(
                    trainingState.log,
                    style: const TextStyle(
                      color: Colors.green,
                      fontFamily: 'monospace',
                      fontSize: 12,
                    ),
                  ),
                ),
              ),
              actions: <Widget>[
                if (showContinueButton)
                  TextButton(
                    onPressed: () async {
                      await _signalContinue();
                    },
                    child: const Text('Continue'),
                  ),
                TextButton(
                  onPressed: trainingState.isTraining ? null : () {
                    Navigator.of(dialogContext).pop();
                  },
                  child: const Text('Close'),
                ),
              ],
            );
          },
        );
      },
    );
    _runYoloDetection();
  }

  @override
  void dispose() {
    _trainingState.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text(
          "Setup / Settings",
          style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
        ),
        centerTitle: true,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white, size: 32),
          onPressed: () => widget.rosConnection.screenNotifier.value = 'home',
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                "Import Cup Photographs for AI Training",
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.deepPurple),
              ),
              const SizedBox(height: 40),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildImportTile(
                    label: "Cup 1 Design",
                    icon: Icons.camera_enhance,
                    onPressed: () => _handlePhotoImport(context, "Cup 1 Design"),
                  ),
                  const SizedBox(width: 100),
                  _buildImportTile(
                    label: "Cup 2 Design",
                    icon: Icons.add_photo_alternate,
                    onPressed: () => _handlePhotoImport(context, "Cup 2 Design"),
                  ),
                  const SizedBox(width: 100),
                  _buildImportTile(
                    label: "Train Detector",
                    icon: Icons.construction,
                    onPressed: () => _showDetectionDialog(),
                  ),
                ],
              ),
              const SizedBox(height: 60),
              const Text(
                "Replace Main Screen UI Icons",
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.deepPurple),
              ),
              const SizedBox(height: 40),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildImportTile(
                    label: "UI Cup 1",
                    icon: Icons.photo,
                    onPressed: () => _handleUIPhotoImport(context, "cup1.png"),
                  ),
                  const SizedBox(width: 100),
                  _buildImportTile(
                    label: "UI Cup 2",
                    icon: Icons.photo_library,
                    onPressed: () => _handleUIPhotoImport(context, "cup2.png"),
                  ),
                ],
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildImportTile({required String label, required IconData icon, required VoidCallback onPressed}) {
    return GestureDetector(
      onTap: onPressed,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(32),
            decoration: BoxDecoration(
              color: Colors.deepPurple.withOpacity(0.1),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Icon(icon, size: 100, color: Colors.deepPurple),
          ),
          const SizedBox(height: 16),
          Text(
            label,
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}