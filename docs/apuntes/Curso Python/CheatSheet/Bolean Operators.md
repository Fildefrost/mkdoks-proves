
>So far, you learned how to check for one single condition:

```python
1. x = 1

3. if x == 1:
4.     print("Yes")
5. else:
6.     print("No")
```

  

>You can also check if two conditions are met at the same time using an `and` operator:

```python
1. x = 1
2. y = 1

4. if x == 1 and y==1:
5.     print("Yes")
6. else:
7.     print("No")

```
	That will return `Yes` since `x == 1` and `y ==1` are both True.

  

>You can also check if one of two conditions are met using an `or` operator:


```python
1. x = 1
2. y = 1

4. if x == 1 or y==2:
5.     print("Yes")
6. else:
7.     print("No")

```
	That will return `Yes` since at least one of the conditions is True. In this case `x == 1` is True.