[![contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/robyfirnandoyusuf/NoSQLInsanity/issues)

# 💉 NoSQLInsanity
<p><img src="https://i.postimg.cc/bJGrw0H6/16149.png" width="250px"></p>

#### This research for final year project
NoSQLInsanity: Tool for Security Assesment NoSQL

### Whitepaper and Slide
Paper : https://jurnal.ubhinus.ac.id/index.php/J-INTECH/article/view/980/686<br>
Slide : https://docs.google.com/presentation/d/1pQpXUFeMGmT3h4KhPl9n71Ma-cI4FGDIWuzd37F3kC8/edit?slide=id.g1f87997393_0_782#slide=id.g1f87997393_0_782

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
#### from Docker
Pull the Docker image by running:

```bash
$ docker pull robyfirnando/nosqlinsanity:v2.0.1
```

#### from PyPi
Coming Soon

### Usage
Simply,
```bash
# from source
$ python3 NoSQLInsanity.py --url "https://lab.s.he-left.me/auth/login" --platform "mongodb"
# from docker
$ docker run -it robyfirnando/nosqlinsanity:v2.0.1 --url "https://lab.s.he-left.me/auth/login" --platform "mongodb"
```

<img src="https://i.postimg.cc/WzCBctnB/Screenshot-214.png">

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
- Daniel Lu aka BrownieInMotion (DiceGang - Redpwn)
- Fernanda Darmasaputra (Tim Petir - OurLastNight)
- Pavel Sorokin (BI.ZONE Security Researcher)
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
