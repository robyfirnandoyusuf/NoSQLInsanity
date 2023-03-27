## Research Notes
### Semua catatan hasil eksplorasi lingkup MongoDB

1. di mongoDB itu ada function substr untuk memotong karakter, ex:
```
db.users.find({ 
    "$where": function() {
        (this.username.substr(0,1) > "x") && (this.password.substr(0,1) > "y") 
    }} 
)
```
jadi memungkinkan untuk dilakukan optimasi, syaratnya web yg vulnerable mengirim arbitrary JS pada parameternya

2. di mongoDB tidak perlu function ascii, karena dia mampu melakukan compare secara langsung dari setiap karakter, ex:
```
[
  {
    "thing": "alphabet"
  },
  {
    "thing": "bravo"
  },
  {
    "thing": "charlie"
  }
]

https://mongoplayground.net/p/WTnItnWx7D9.
```

3. MongoDB regex itu sama dengan regex JS / PHP PCRE (ref: https://www.oreilly.com/library/view/mongodb-the-definitive/9781449344795/ch04.html): 
   misal mau nyari apakah length nya itu >= 4 : http://regexr.com/79cmi, klo mau nyari exacth length cukup hapus aja "," koma nya
   dengan ability ini, memungkinkan penerapan binary search

4. funfact,undocumented feature regex mongodb itu bisa mencari rentang karakter dengan mempassing value dalam representasi hexadecimal dengan WAJIB prefix **\x** ^.[\x{HEX}-\x{HEX}]

5. untuk passing repr hexa via protocol http regex harus dirubah menjadi [\x{HEX VALUE}], kalau query langsung di mongodb bisa langsung [\xHEX VALUE]
### Approach untuk dump data tanpa diketahui sama sekali salah satu value col

1. cari prefix
2. cari length
3. cari index setelah prefix pke within regex
4. masih diprefix yg sama dipastikan lgi 


#### Coretan
$regex: /^(?!.*admin)(?!.*nando).*.{12}[\x{006b}-\x{006f}].*$/ 
^(?!.*abcdefghijklm).*a{1}[\x63-\x67].{7}(?!.{13}$).* = bkan abcdefghijklm, second char 63-67, pjg length bkan 13
^(?!.*abcdefghijklm)(?!.{13}$).*a.{5,}.*

^(?!.*abcdefghijklm)(?!.{13}$)(?!.*\badminxyz\b)(?!.8$).*a.* = ini regex buat include yg udah diexclude
^(?!.*jsmith)(?!.{6}$).*j([u])
^(?!.*\babcdefghijklm\b)(?!.{13}$)(?!.*\badminxxyz\b)(?!.{9}$).{6}[i].{0}

kasus dump abcdefghijklm
^a.{0}[b].{10} = kalau ada prefix
^.{1}[b].{11} = kalau g ada prefix
^abc([\x62-\x64]).{9}$ 
^(?!.*jsmith)(?!.{6}$)^j([a-s])
a bcdefghijklm

