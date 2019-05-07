# word-directory-finder

This program searches through an entire file or file line by line (by extension or not), the desired word, by printing the file line and the file path.

**example :**

```shell
python3 grep_and_remove.py -w chat -p ./ -e "php txt"
```

**Result :**

```
found at line 3 in the path "./test.php"
found at line 6 in the path "./test.php"
found at line 9 in the path "./test.php"
found at line 12 in the path "./test.php"
found at line 2 in the path "./test.txt"
found at line 5 in the path "./test.txt"
found at line 8 in the path "./test.txt"
found at line 11 in the path "./test.txt"
Finish in 0.066 s
```

## Documentation :

You will find all the documentation with the -h or --help  option 

## Advices

Prefer search by extension because it is faster.
