Simple CLI TODO manager written in Python for Linux (Ubuntu). For storing/managing TODOs, SQLite3 is used.

### Requirements

- Python 3.10+

### Installation

1) Clone the repo

2) Add symbolic link of the shell script to bin directory:

```
$ sudo ln -s ~/path/to/todo.sh /bin/todo
```

### Usage

_Available commands:_

Show current list of TODOs
``` todo ```

Create a new TODO
``` todo new "TODO description" ``` 

Remove a TODO
``` todo remove <TODO_ID> ``` 

Update TODO description
``` todo update <TODO_ID> "New description" ``` 

Mark TODO as completed
``` todo <TODO_ID> completed ``` 

Mark all TODOs as completed
``` todo all completed ``` 

Clear all TODOs
``` todo clear ``` 

_Examples:_

``` todo new "Go get groceries" ```
``` todo update 1 "Go buy batteries" ```
``` todo 1 completed ```
``` todo clear ```
