# BoLiau - A flexible and lazyness continuation tasks management framwork.

[![Build Status](https://secure.travis-ci.org/hychen/boliau.png)](http://travis-ci.org/hychen/boliau)

The project name BoLiau comes from the spelling pronunciation of 無聊
in 台灣閩南語.

Each task is a step of steps to archive a mission such as 
collecting data from website to generate a report, batch changing bug
status in Bug Tracker, etc.

A mission is composed by many tasks in sequence like a production line
in a factory.

## Composition

Every command has `boliau` prefix are like functions in function programming language
and only provide a task.

Tasks can be composted by Unix pipe line as a mission. The output of last task is 
the input of next task.

Here is a simplest composition. it only print the output of `cat /etc/apt/source.list`

```
$ cat /etc/apt/source.list | boliau-readstdin | boliau-print | wc -l
60
```

## Python!

When data is redirected to `boliau-readstdin`. it will be converted as 
a Python String Object (str).

it means you can use lovely *map*, *filter* and any built-in Python 
functions to operate data in your lovely shell.

For instance, To count u character of all urls in
/etc/apt/source.list, you can use the following instructions.

```
$ awk '{print $2}' /etc/apt/sources.list | grep http | \
  boliau-readstdin  | boliau-lines | \
  boliau-map --command "lambda e: e.count('u')" | \
  boliau-pycall sum | boliau-print
141 
```

It can be dived into 6 steps.

1. list only http url by using awk and grep
2. put the last output to Python context by using boliau-readstdin
3. split string to list by using boliau-lines
4. counting occurrences of u character of each elements of the list by
using boliau-map. 
5. boliau-pycall can apply a python function to the last ouput. In
this case, sum is used for getting all occurrences of u character. 
6. boliau-print is to print the last output to console. the data exits
Python context.

## Lazyness

There are 3 types of command in design

1. To create a mission as a container.
2. To modify a mission.
3. To do a mission.

In previous introduction, only boliau-print is third type command. the
others are used to define how many tasks need to be executed to
archive a mission.

### Some examples.

To create a mission to split source list content to list

```
$ awk '{print $2}' /etc/apt/sources.list | grep http | \
  boliau-readstdin  | boliau-lines > get_sourcelist_url.mission
```

To print the url count.

```
$ cat get_sourcelist_url.missison | boliau-pycal len | boliau-print
23
```

To create a new mission to less typing.

```
$ cat get_sourcelist_url.mission | boliau-pycal len > count_sourcelist_url.mission
$ boliau-print < count_sourcelist_url.mission
23
```

### Installation and usage

### Troubleshooting

### Development

To see what has changed in recent versions of boliau, see the [CHANGELOG](https://github.com/hychen/boliau/blob/master/CHANGELOG.md).

### Core Team Members

- Chen, Hsin-YI (hychen)

### Resources

### Other questions

Feel free to chat with the boliau core team (and many other users) on IRC in the  [#tossug](irc://irc.freenode.net/project) channel on Freenode.

### Copyright

Copyright © 2013 Chen Hsin-YI. See [LICENSE](https://github.com/hychen/boliau/blob/master/LICENSE.md) for details.

Project is a member of the [OSS Manifesto](http://ossmanifesto.org).
