import 'dart:io';

int calculate() {
  return 6 * 7;
}


Future<List<File>> getListFile(String directory) async {
  final dir = Directory(directory);
  final List<FileSystemEntity> entities = await dir.list().toList();
  return entities.whereType<File>().toList();
}