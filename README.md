# Code review and feature development

## Intro

This test assignment aims to take a picture of your Python/Django coding style, taste, 
sense of good patterns, security, performance and architectural thinking. 

Don't worry, there is no highest/lowest score, no "right" or "wrong" solution, there is 
even no solution as such. Code analysis and review can take significant time and effort, 
if not limited in time. Any of 3YOURMIND's developers will approach it differently. In 
the past we had hard time reviewing each other's work until we came to some basic 
agreements.

## Description

The project is a very simple URL shortener. Users, both anonymous and authenticated, may 
add their URLs to get short aliases. All short aliases are available for redirection to 
everybody.

When users create new shortened alias, they submit their full URL and get aliased URL as 
response. URL short ids are unique randomly generated strings of constant length. When we 
generate them, we check if there is no same short_id in the table.

There is a table described in model class `main.ShortURL`, it has a foreign key field 
`author` to the model `auth.User`. Records from `main.ShortURL` have `accessed_at` and 
`times_accessed` fields, that contain the last datetime, when they were used, and how 
many times respectively. 

This is REST API service, so no frontend exists. For testing and experiments you may use 
Django REST Framework's web interface, check unit-tests or write your own tests.

## Your task

### Code review

You are supposed to show your best style, propose corrections, refactorings, fixes - 
anything you think is appropriate and important. Not everything in this codebase is bad, 
at least we want to think so :), but some parts are left "imperfect" to say the least, 
or even traps, who knows.

Add comments, refactor code to make it better. 

Please focus on the most important places and required changes, 
it is up to you how to rank them - this task has limited time to accomplish. On the 
presentation which follows this task you may mention any other minor improvement that 
you would have made. Very nice if you give insight on further development of this 
project, which new features it may have. Think beyond plain code, what needs to be done 
if it grows and needs to handle bigger amount of data.

Any of your suggestions are welcome. 

### Feature development

We don't want our DB be cluttered with stale data, it is good idea to clean anonymous 
entries, that have not been accessed for a while (longer than 30 days). The short links, 
created by authenticated users, should also be removed if they were not used for 60 days 
and had less than 2 usages. You need to write a script, that will be run periodically. 
This script should remove such "old" entries.

Additional requirement: short ids of deleted ShortURLs should not ever be reused when we 
create new ShortURLs. Most probably you will need to make changes in the database 
structure.

Fork this code repository and commit all your changes. After you've finished, share 
the code repository with your interviewers. 

## Preparation

You will need python>=3.6, packages are listed in `requirements.txt`.

If you are given this task, we assume that you already know, how to install Python 
project's requirements, run tests, create superuser and do any other related task. Use 
any DB engine of your choice. Sqlite3 is the default option and is already configured in 
Django settings.
