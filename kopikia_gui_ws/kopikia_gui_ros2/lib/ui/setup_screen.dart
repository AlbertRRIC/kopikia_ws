import 'package:flutter/material.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:path/path.dart' as p;
import '../ros/ros_connection.dart';

class SetupScreen extends StatelessWidget {
  final RosConnection rosConnection;

  const SetupScreen({super.key, required this.rosConnection});

  Future<void> _handlePhotoImport(BuildContext context, String category) async {
    try {
      // Opens the native system dialog to select an image file
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.image,
        dialogTitle: 'Select $category Image',
      );

      if (result != null && result.files.single.path != null) {
        final String sourcePath = result.files.single.path!;
        final String fileName = result.files.single.name;
        
        // Target project directory for AI training images
        final String targetDirPath = '/home/jetsonros2/MyProject/kopikia_ws/kopikia_gui_ws/kopikia_gui_ros2/assets/photo';
        
        // Ensure the target directory exists
        await Directory(targetDirPath).create(recursive: true);
        
        final String targetPath = p.join(targetDirPath, '${category.replaceAll(' ', '_')}_$fileName');

        final File sourceFile = File(sourcePath);
        await sourceFile.copy(targetPath);

        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Successfully imported $fileName to $category.')),
          );
        }
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
        
        // Target directory for UI icons as referenced in main.dart
        final String targetDirPath = '/home/jetsonros2/MyProject/kopikia_ws/kopikia_gui_ws/kopikia_gui_ros2/assets/photo';
        
        await Directory(targetDirPath).create(recursive: true);
        
        final String targetPath = p.join(targetDirPath, targetFileName);

        final File sourceFile = File(sourcePath);
        await sourceFile.copy(targetPath);

        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Successfully updated UI icon: $targetFileName')),
          );
        }
      }
    } catch (e) {
      debugPrint("Error updating UI photo: $e");
    }
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
          onPressed: () => rosConnection.screenNotifier.value = 'home',
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
