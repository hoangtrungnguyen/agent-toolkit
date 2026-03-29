import 'dart:io';

import 'package:duplicate_file_name_cleaner/duplicate_file_name_cleaner.dart' as duplicate_file_name_cleaner;

Future<void> main(List<String> arguments) async {
  print('Arguments ${arguments.join(', ')}');
  print('---------------- Start ---------------');

  try {
    String directory = arguments[0];
    List<File> files = await duplicate_file_name_cleaner.getListFile(directory);
    files.sort((a,b){
      return b.path.compareTo(a.path);
    });
    Set<File> deletableFiles = Set();
    Set<String> existedFileNameSet = Set();

    for(int i = 0; i < files.length; i ++) {
      final file = files[i];
      print('**************** Star Loop ***********');
      String filePath = file.path;
      String rootName = filePath;
      final afterReplacedString = rootName.replaceFirst(RegExp(r'\s{1,}[0-9]{0,}\.\w{1,}$'), '');
      print('rootName $rootName');
      final nameForDistinction = afterReplacedString.split('\\').last.split('.').first.trim();
      bool added = existedFileNameSet.add(nameForDistinction);
      print('nameForDistinction ${nameForDistinction} - added ${added}');


      if(added){
        print('added to existedFileNameSet');
        print(existedFileNameSet.join('\n'));
      } else {
        deletableFiles.add(file);
      }
      print('rootName: ${rootName}');
      print('\n\n');
      print('**************** End Loop ***********');
    }

    print("existed file name set");
    print(existedFileNameSet.join('\n'));
    print("Deletable Files");
    print(deletableFiles.join('\n'));
    for(final file in deletableFiles){
      file.deleteSync();
    }

  } catch (e, trace) {
    print(e.toString());
    rethrow;
  }
  print('---------------- END ---------------');
}

String getWithoutSpaces(String s){
  String tmp = s.substring(1,s.length-1);
  while(tmp.startsWith(' ')){
    tmp = tmp.substring(1);
  }
  while(tmp.endsWith(' ')){
    tmp = tmp.substring(0,tmp.length-1);
  }

  return '('+tmp+')';
}