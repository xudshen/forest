# forest

restful api generator using XPath

## Scopes
```
├── api
│   ├── meta.api.json
│   └── user.api.json
├── controller
│   └── user.controller.json
├── model
│   ├── books.model.json
│   └── user.model.json
├── sample-books.xml
└── sample-table.html
```

## Todos
- [ ] scope 
- [ ] parse html into json object
  - [ ] html tables to array ```<table>```
  - [ ] html lists to array ```<ol> <ul> <li> <dl> <dt> <dd>```
  - [ ] regular list to array
  - [ ] provide json template
- [ ] browser plugin


[sample]:http://nodejs.org


## LICENSE

The MIT License (MIT)

Copyright (c) 2014 Xudong Shen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
