# 💉 NoSQLInsanity
<p><img src="https://i.postimg.cc/bJGrw0H6/16149.png" width="250px"></p>

#### This research for final year project
NoSQLInsanity: Tool for Security Assesment NoSQL

### Wireframe
https://whimsical.com/nosqlinsanity-F2thpyebcaNPyCQr4UBabe

<b>Researcher</b> : Roby Firnando Yusuf aka greycat aka 0x00b0<br>
<b>Supervisor</b> : Daniel Rudiaman S. S.T., M. Kom

- [Installation](#installation)
  - [from Source](#from-source)
- [Usage](#usage)
  - [Options](#options)
- [License](#license)
- [Acknowledments](#acknowledments)

### Installation
It's fairly simple to install NoSQLInsanity:
#### from Source
Clone repository and install requirements:

```
$ git clone https://github.com/robyfirnandoyusuf/NoSQLInsanity.git
$ cd NoSQLInsanity/
$ pip3 install -r requirements.txt
```

#### from PyPi
Coming Soon

### Usage
`$ python3 NoSQLInsanity.py --url "https://lab.s.he-left.me/auth/login" --platform "mongodb"`

### Options
Here are all the options it supports.
| **Argument**  	| **Description**                             	
|---------------	|---------------------------------------------
| --url    	| Vulnerable endpoint                       	| ``                                        |
| -s, --silent  	| Silent mode _(hide the time measurements)_ 

### Features
1. Dump by known a value
2. Dump by unknown value (dump all documents by specify field)
3. Multiple option algorithms (Linear and Binary Search)

## License

`NoSQLInsanity` is distributed under Apache 2.

## Acknowledments

Since this tool includes some contributions, and I'm not an asshole, I'll publically thank the following users for their supports, helps and resources:
- Daniel Roo aka BrownieInMotion (DiceGang - Redpwn)
- Fernanda Darmasaputra (Tim Petir - OurLastNight)
- and You

### TODO:
- [x] Print Info
- [x] Menu Param
- [x] Menu HTTP Method
- [x] Menu Input Payload
- [x] Engine Checker Website is UP or DOWN
- [x] Engine Vuln Test
- [x] Auto Set Success-Identifier
- [x] Engine Linear (Dump known value)
- [x] Engine Linear (Dump unknown value)
- [x] Engine Linear Count Length
- [x] Engine Binary Search (Dump known value)
- [x] Engine Binary Search (Dump unknown value)
- [x] Engine BinSearch Count Length
- [x] Research ability MongoDB to perform BinSearch
- [x] Add measurement each chars LinearSearch (Dump known value)
- [x] Add measurement each chars LinearSearch (Dump unknown value)
- [x] Add measurement each chars BinSearch (Dump known value)
- [x] Add measurement each chars BinSearch (Dump unknown value)
- [x] Log Report CSV