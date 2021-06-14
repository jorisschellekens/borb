# 1. Markdown Support in pText
## 1.1 Lists

### 1.1.1 Asterisk Sign

This list was formatted using the '*' sign.

  * One
  * Two
  * Three
  * Four

### 1.1.2 Minus Sign

This list was formatted using the '-' sign.
  
  - One
  - Two
  - Three
  - Four
  
### 1.1.3 Plus Sign  

This list was formatted using the '+' sign.
  
  + One
  + Two
  + Three
  + Four
  
### 1.1.4 Numbered List
  
  1. One
  2. Two
  3. Three
  4. Four

### 1.1.5 Numbered List (Wrong)

This numbered list has non-sequential numbers.
pText automatically corrects this list to ensure the numbers are sequential.
  
  1. One
  3. Two
  5. Three
  6. Four
  
## 1.2 Blockquotes

> Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
> sed do eiusmod tempor incididunt ut labore et dolore magna. 
> Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut 
> aliquip ex ea commodo consequat. 
> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
> eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
> sunt in culpa qui officia deserunt mollit anim id est laborum. 

## 1.3 Code Snippet

### 1.3.1 Code Snippet By Indent

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut 

### 1.3.2 Code Snippet By Fencing

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut 
```

## 1.4 Horizontal Rule

---

## 1.5 Paragraphs

### 1.5.1 Homogeneous Paragraphs

Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut

aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### 1.5.2 Heterogeneous Paragraphs

Lorem ipsum dolor sit **amet**, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut _labore et dolore_ magna.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut

**aliquip ex ea commodo consequat**. Duis aute irure `dolor` in reprehenderit in voluptate velit esse cillum dolore 
eu fugiat nulla pariatur. __Excepteur sint occaecat__ cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.


## 1.6 Tables

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |
| zebra stripes | are neat      |    $1 |

## 1.7 Images

![Image Alt Text](https://images.unsplash.com/photo-1617235641226-4ebf93095678?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2134&q=80 "Zero Take") 