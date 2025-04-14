
>Lists, strings, and tuples have a **positive index** system:

```python
1. ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2.    0      1      2      3      4      5      6
```


  
>And they have a **negative index** system as well:
   
```python
1. ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2.   -7     -6     -5     -4     -3     -2     -1

```

  
>In a list, the **2nd**, **3rd**, and **4th** items can be accessed with:
   
```python
1. days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2. days[1:4]
3. Output: ['Tue', 'Wed', 'Thu']

```
  
>**First three items of a list**:
   
```python
1. days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2. days[:3]
3. Output:['Mon', 'Tue', 'Wed'] 

```
  
>**Last three items of a list**:
   
```python
1. days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2. days[-3:]
3. Output: ['Fri', 'Sat', 'Sun']

```
>**Everything but the last**:
   
```python
1. days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2. days[:-1] 
3. Output: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] 

```
>**Everything but the last two**:
  
```python
1. days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
2. days[:-2] 
3. Output: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'] 

```
  
>A dictionary **value** can be accessed using its corresponding dictionary **key**:
   
```python
1. phone_numbers = {"John":"+37682929928","Marry":"+423998200919"}
2. phone_numbers["Marry"]
3. Output: '+423998200919'
```