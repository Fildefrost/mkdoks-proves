
>**for-loop** is useful to repeatedly execute a block of code.
   
```python
for letter in 'abc':
	print(letter.upper())

Output:

`A   B   C`

```



>As you can see, the for-loop repeatedly converted all the items of `'abc'` to uppercase.

> The name after `for` (e.g. `letter`) is just a variable name
  
> You can loop over **dictionary keys** as follows:

```python
phone_numbers = {"John Smith":"+37682929928","Marry Simpons":"+423998200919"}
   for value in phone_numbers.keys():
       print(value)

Output:

`John Smith`  
`Marry Simpsons`
```

> You can loop over **dictionary values**:
   
```python
phone_numbers = {"John Smith":"+37682929928","Marry Simpons":"+423998200919"}
   for value in phone_numbers.values():
       print(value)

Output:

`+37682929928`  
`+423998200919`
```


>You can loop over **dictionary items**:

```python
phone_numbers = {"John Smith":"+37682929928","Marry Simpons":"+423998200919"}
       for key, value in phone_numbers.items():
           print(key, value)
    
Output: 
    
John Smith +37682929928
Marry Simpons +423998200919
    
```

> We also have **while-loops**. The code under a while-loop will run as long as the while-loop condition is true:

```python
while datetime.datetime.now() < datetime.datetime(2090, 8, 20, 19, 30, 20):
           print("It's not yet 19:30:20 of 2090.8.20")
    
#The loop above will print out the string inside `print()` over and over again until the 20th of August, 2090.
```