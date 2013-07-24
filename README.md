# BoLiau - A flexible and lazyness continuation tasks management framwork.

[![Build Status](https://secure.travis-ci.org/hychen/boliau.png)](http://travis-ci.org/hychen/boliau)

The project name BoLiau comes from the spelling pronunciation of 無聊
in 台灣閩南語, because the author Chen Hsin-Yi developed when he was
trying to eliminate tedious repetition actions.

Those actions has two kind: Task and Mission.

Each task is a step of steps to archive a mission such as 
collecting data from website to generate a report, batch changing bug
status in Bug Tracker, etc.

And, a  mission is composed by many tasks in sequence like a production line
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

## Python

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
  boliau-py-call sum | boliau-print
141 
```

It can be dived into 6 steps.

1. list only http url by using awk and grep
2. put the last output to Python context by using boliau-readstdin
3. split string to list by using boliau-lines
4. counting occurrences of u character of each elements of the list by
using boliau-map. 
5. boliau-py-call can apply a python function to the last ouput. In
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

### Examples

To create a mission to split source list content to list

```
$ awk '{print $2}' /etc/apt/sources.list | grep http | \
  boliau-readstdin  | boliau-lines > get_sourcelist_url.mission
```

To print the url count.

```
$ cat get_sourcelist_url.missison | boliau-py-call len | boliau-print
23
```

To create a new mission to less typing.

```
$ cat get_sourcelist_url.mission | boliau-py-call len > count_sourcelist_url.mission
$ boliau-print < count_sourcelist_url.mission
23
```

To create a Python object from json string and print its type 

```
$ boliau-py-obj --from-string '{"a":1}' | boliau-py-call type | boliau-print
<type 'dict'>
```

## To operate more data types with plugins.

### Examples

To display Launchpad bug information.

```
$ boliau-lp-get bug 1 | boliau-lp-format buginfo | boliau-print 
Title: (LP:# 1) Microsoft has a majority market share
Created: 2004-08-20 00:00:00+00:00
Last updated: 2013-01-04 00:12:18.967847+00:00
URL: https://bugs.launchpad.net/bugs/1
```

To statistic status of launchpad bugtasks of people ossug-hychen and print to
console in yaml format.

```
$ boliau-lp-findbugtasks people ossug-hychen > bugtasks.mission
$ cat bugtasks.mission | boliau-lp-format today_bugtask_status | boliau-lp-format toyaml | boliau-print 
{date: !!timestamp '2013-01-06 05:04:10.091141', fix-committed: 4, fix-released: 8,
  in-progress: 2, todo: 4, wont-fix: 3}
```

To store the collected data to mongodb.

```
$ cat bugtasks.mission | boliau-lp-format today_bugtask_status | boliau-mongo-insert testdb test
50e95ae8f101ad1bb2000000
```

Get collected data from mongodb and convert to json format.

```
boliau-mongo-find testdb test  | boliau-py-call list | boliau-lp-format tojson | boliau-print 
[{"wont-fix": 3, "fix-committed": 4, "in-progress": 2, "fix-released": 8, "date": "2013-01-06T19:07:20.704000", "_id": null, "todo": 4}]
```

Update google spread sheet data.

```
$ boliau-py-obj --from-string '[[1,2,3],[4,5,8]]' | boliau-gspread-upsert hychentestdb --email some@email.com --worksheet sheet1
```

### Installation and usage

Dependency
- nosetest
- mock
- launchpadlib
- ucltip
- mako
- gspread

### Development

1. Fork the git repository [here](https://github.com/hychen/boliau/fork_select).
2. Hacking...
3. Make sure all changes pass unittest.
4. Send pull request.

```
$ source setdevenv
$ nosetest
```

To see what has changed in recent versions of boliau, see the [CHANGELOG](https://github.com/hychen/boliau/blob/master/CHANGELOG.md).

### Core Team Members

- Chen, Hsin-Yi (hychen)

### Resources

The project is inspired by many ideas in functional programming. 

- [Lambda Function](http://en.wikipedia.org/wiki/Anonymous_function)
- [Closure](http://en.wikipedia.org/wiki/Closure_(computer_science))
- [Function Composition](http://en.wikipedia.org/wiki/Function_composition_(computer_science))
- [Haskell/Understanding arrows](http://en.wikibooks.org/wiki/Haskell/Understanding_arrows#.2A.2A.2A)

### Ideas pool

#### Core
- A commad to display or execute last mission. called boliau-it

```
$ boliau-lp-findpackages ppa:ossug-hychen/ppa | boliau-print
$ boliau-it --show
boliau-lp-findpackages ppa:ossug-hychen/ppa | boliau-print
```

- simple ui for data selection

```
boliau-lp-findpackages ppa:ossug-hychen/ppa | boliau-ui-selection --onlyone | boliau-print
```

- Type check

```
$ boliau-lp-findpackages ppa:ossug-hychen/ppa | boliau-py-call list | boliau-concat | boliau-typecheck
link: None -> Mission -> Mission -> None
data: None -> PublishedSourcePackage -> list -> str 
```
- Computation Composition
same as b(a()) + c(a())

```
$ boliau-arr-split a.mission | boliau-arr-unsplit b.mission c.mission | boliau-print
```

### Other questions

Feel free to chat with the boliau core team (and many other users) on IRC in the  [#tossug](irc://irc.freenode.net/project) channel on Freenode.

### Copyright

Copyright © 2013 Chen Hsin-YI. See [LICENSE](https://github.com/hychen/boliau/blob/master/LICENSE.md) for details.

Project is a member of the [OSS Manifesto](http://ossmanifesto.org).
