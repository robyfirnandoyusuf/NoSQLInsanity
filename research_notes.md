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

3. MongoDB regex itu sama dengan regex JS / PHP PCRE: 
   misal mau nyari apakah length nya itu >= 4 : http://regexr.com/79cmi, klo mau nyari exacth length cukup hapus aja "," koma nya
   dengan ability ini, memungkinkan penerapan binary search

4. funfact,undocumented feature regex mongodb itu bisa mencari rentang karakter dengan mempassing value dalam representasi hexadecimal dengan WAJIB prefix **\x** ^.[\x{HEX}-\x{HEX}]
