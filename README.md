# ScratchNLP
Tina Quach, Kara Luo, Willow Jarvis

{quacht, luok, wjarvis}@mit.edu

ScratchNLP provides a framework for someone to create [Scratch](http://scratch.mit.edu/) programs by providing a series of natural language instructions that get translated into the internal representation of [Scratch 2.0](https://en.scratch-wiki.info/wiki/Scratch_2.0) projects. 

For example, 
```
play the meow sound 10 times
```
corresponds to the script 
```
[['doRepeat', [['doRepeat:', 'times']], [['tea'], 'setVar:to:', 'tea', ['randomFrom:to:', '1', '5']]]]
```
and
```
if x is not less than three then broadcast hello thats it
```
corresponds to the script 
```
[["doIf", ["not", ["<", ["readVariable", "x"], "three"]], [["broadcast:", "hello"]]]]
```

By specifying a series of commands through the command line interface, you can construct an Scratch Project controlling a single sprite with custom variables, lists, and messages, and sound commands. With every input, you get a response about the number of parses identified in the sentence, the current state of what variables and lists exist in the program, and the script generated from the input. 

## Getting Started
- In Athena, type the following commands
```
cd /mit/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/scripts
setup 6.863
python semantic.py 
```
Running python semantic.py initiates a command line interface specifically for creating the Scratch programs with natural language. See the **Example of Creating a Project** Section for more on how to create a project.

Use the ```-h``` option on  ```semantic.py``` to learn more about usage.
```
6.863$ python semantic.py -h
usage: semantic.py [-h] [-v] [--spm] [--gui] [--batch_mode BATCH_FILE]
                   [--show_database] [--validate_output VALIDATION_FILE]

6.863 - Spring 2018 - Semantics Interpreter

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         output evaluation traces.
  --spm                 syntax parser mode (no semantic evaluation).
  --gui                 display a graphical user interface for stepping
                        through the trace of the last evaluation prior to the
                        exiting of the program
  --batch_mode BATCH_FILE
                        evaluate each sentence listed in the specified file
  --show_database       display the contents of the semantic database after
                        each evaluation
  --validate_output VALIDATION_FILE
                        check the specified input against expected output.
```

## Overview
```scripts/semantic.py``` is the entry point for the system. It launches the command line interface and manages the project creation process.  

```semanticRules.py``` defines a context free grammar and associated semantic rules. This file also stores the lexicon and code to generate and add synonyms to the lexicon. The file is compatible with the software in MIT's 6.863 Natural Language Processing software for lab 3.

```generate_vocab.py``` contains the regular expressions to parse out variable names, list names, message names that get added to the lexicon. It also adds inputted numbers to the lexicon.

```scratch_project.py``` defines the ScratchProject class which stores the state of the Scratch project specification as it changes based on user input. It also generates the json and the sb2 file.

```scratch_project_base.py``` defines the ScratchProjectBase Class which has a
basic JSON that specifies the base ScratchProject upon which the system builds.

```text2num.py``` defines the helper function to convert a word representing a number into the numerical value. 

```test_fixtures/generate_sb2_fixture_with_assets``` contains a set of asset files to be included in the generated .sb2 file. 

```systemDemos/``` contains demos of the working system. In each subdirectory, there is a file called Scripts.txt that contains the instructions used in the demo, the corresponding sb2 file generated, and a screenshot of the Scratch program when the sb2 file is loaded into Scratch.


## Example of Creating a Project

Demos of the system could be found under the directory 
```
/mit/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/systemDemos
```

To simulate the following example, you may copy and paste the following into the terminal after starting ```python semantic.py```.

```
make a variable called bananas and set bananas to 10
make a variable called strawberries
set strawberies to 5
make a list called fruit
add strawberries to fruit
add bananas to fruit
when the program starts play the cave sound thats it
when the right arrow key is pressed add 1 to bananas thats it
when the right arrow key is pressed add 5 to strawberries thats it
```

You should have the following output
```
6.863$ python semantic.py
> Loading the 6.863 Semantics REPL...
> Hello. To exit this program, enter <cr> at the prompt below.
> make a variable called bananas and set bananas to 10
[WARNING] Obtained 4 parses; selecting the first one.
{'variables': {'bananas': 0}, 'lists': {}, 'scripts': [['wait:elapsed:from:', 0.1], ['setVar:to:', 'bananas', 10]]}
> make a variable called strawberries
[WARNING] Obtained 2 parses; selecting the first one.
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {}, 'scripts': [['wait:elapsed:from:', 0.1]]}
> set strawberies to 5
[WARNING] Obtained 2 parses; selecting the first one.
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {}, 'scripts': [['setVar:to:', 'strawberies', 5]]}
> make a list called fruit
[WARNING] Obtained 2 parses; selecting the first one.
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {'fruit': []}, 'scripts': [['wait:elapsed:from:', 0.1]]}
> add strawberries to fruit
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {'fruit': []}, 'scripts': [['append:toList:', ['readVariable', 'strawberries'], 'fruit']]}
> add bananas to fruit
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {'fruit': []}, 'scripts': [['append:toList:', ['readVariable', 'bananas'], 'fruit']]}
> when the program starts play the cave sound thats it
('commandName, value', 'doPlaySoundAndWait', 'cave')
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {'fruit': []}, 'scripts': [[['whenGreenFlag'], ['doPlaySoundAndWait', 'cave']]]}
> when the right arrow key is pressed add 1 to bananas thats it
[WARNING] Obtained 2 parses; selecting the first one.
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {'fruit': []}, 'scripts': [[['whenKeyPressed', 'right arrow'], ['changeVar:by:', 'bananas', 1]]]}
> when the right arrow key is pressed add 5 to strawberries thats it
[WARNING] Obtained 2 parses; selecting the first one.
{'variables': {'strawberries': 0, 'bananas': 0}, 'lists': {'fruit': []}, 'scripts': [[['whenKeyPressed', 'right arrow'], ['changeVar:by:', 'strawberries', 5]]]}
```

You can request the project.json at any point in the process of creating a project, using the keyword "json". Note: repetitive portions of the json have been omitted and replaced with '...'
```
> json
{
  "info": {
    "spriteCount": 1,
    "scriptCount": 0,
    "flashVersion": "MAC 28,0,0,126",
    "swfVersion": "v460",
    "userAgent": "Scratch 2.0 Offline Editor",
    "videoOn": false
  },
  "penLayerID": 0,
  "tempoBPM": 60,
  "objName": "Stage",
  "sounds": [
    {
      "format": "",
      "sampleCount": 258,
      "soundName": "pop",
      "soundID": 7,
      "rate": 11025,
      "md5": "83a9787d4cb6f3b7632b4ddfebf74367.wav"
    }
  ],
  "penLayerMD5": "5c81a336fab8be57adc039a8a2b33ca9.png",
  "children": [
    {
      "direction": 90,
      "isDraggable": false,
      "indexInLibrary": 1,
      "costumes": [
        {
          "baseLayerMD5": "f9a1c175dbe2e5dee472858dd30d16bb.svg",
          "bitmapResolution": 1,
          "costumeName": "costume1",
          "baseLayerID": 1,
          "rotationCenterX": 47,
          "rotationCenterY": 55
        },
        ...
      ],
      "currentCostumeIndex": 0,
      "visible": true,
      "rotationStyle": "normal",
      "lists": [
        {
          "listName": "fruit",
          "contents": []
        }
      ],
      "scripts": [
        [5, 128, 
          [["wait:elapsed:from:", 0.1], ["setVar:to:", "bananas", 10], ["wait:elapsed:from:", 0.1], ["setVar:to:", "strawberies", 5], ["wait:elapsed:from:", 0.1], ["append:toList:", ["readVariable", "strawberries"], "fruit"], ["append:toList:", ["readVariable", "bananas"], "fruit"]]
        ],
        [5, 128, 
          [["whenGreenFlag"], ["doPlaySoundAndWait", "cave"]]], [5, 128, [["whenKeyPressed", "right arrow"], ["changeVar:by:", "bananas", 1]]
        ], 
        [5, 128, [["whenKeyPressed", "right arrow"], ["changeVar:by:", "strawberries", 5]]
        ], 
        [5, 128, []]
      ],
      "sounds": [
        {
          "format": "",
          "sampleCount": 18688,
          "soundName": "meow",
          "soundID": 0,
          "rate": 22050,
          "md5": "83c36d806dc92327b9e7049a565c6bff.wav"
        },
        ...
      ],
      "spriteInfo": {},
      "scale": 1,
      "objName": "Sprite1",
      "scratchX": 0,
      "scratchY": 0,
      "variables": [
        {
          "name": "strawberries",
          "value": 0
        },
        {
          "name": "bananas",
          "value": 0
        }
      ]
    }
  ],
  "costumes": [
    {
      "baseLayerMD5": "739b5e2a2435f6e1ec2993791b423146.png",
      "bitmapResolution": 1,
      "costumeName": "backdrop1",
      "baseLayerID": 3,
      "rotationCenterX": 240,
      "rotationCenterY": 180
    }
  ],
  "currentCostumeIndex": 0,
  "videoAlpha": 0.5
}
```

At any point, you may also type sb2 to generate an .sb2 file that can be uploaded onto the [Scratch 2.0 online editor](http://scratch.mit.edu/create) and the [Scratch 2.0 offline editor](https://scratch.mit.edu/download).
```
> sb2
  adding: 0.png (deflated 85%)
  adding: 0.wav (deflated 4%)
  adding: 1.svg (deflated 62%)
  adding: 1.wav (deflated 13%)
  adding: 2.svg (deflated 62%)
  adding: 2.wav (deflated 17%)
  adding: 3.png (deflated 85%)
  adding: 3.wav (deflated 20%)
  adding: 4.wav (deflated 10%)
  adding: 5.wav (deflated 13%)
  adding: 6.wav (deflated 17%)
  adding: 7.wav (stored 0%)
  adding: project.json (deflated 63%)
sb2_path is /afs/athena.mit.edu/course/6/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/result/scratchNLPdemo.sb2
```







