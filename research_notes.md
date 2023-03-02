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
