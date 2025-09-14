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

```
$ todo                                     - Show current list of TODOs
$ todo new "TODO description"              - Create a new TODO
$ todo remove <TODO_ID>                    - Remove a TODO
$ todo update <TODO_ID> "New description"  - Update TODO description
$ todo <TODO_ID> completed                 - Mark TODO as completed
$ todo all completed                       - Mark all TODOs as completed
$ todo clear                               - Clear all TODOs
```

_Examples:_

``` 
$ todo new "Go get groceries" 
$ todo update 1 "Go buy batteries" 
$ todo 1 completed 
$ todo clear 
```
