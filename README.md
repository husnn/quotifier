
# Quotifier

Turn any Tweet into a picture-quote (real or fake).

See it in action on Twitter [@Quotifier](https://twitter.com/Quotifier)

## Features

#### Common uses
| Command | Text | Author | Background Image |
| ----------- | ----------- | ----------- | ----------- |
| *@bot* this | Original tweet | Twitter username | Random, general background image |
| *@bot* this by *Name*<br>*@bot* this by *Full name* | Original tweet | *Name*<br>*Full name* | Random but related background image (if available) |

#### Arguments
| Argument | Value | Description |
| ----------- | ----------- | ----------- |
| by | Name of author | Who you want to attribute the quote to |
| --bg | *id* of the desired image | The referred image will be used as the background for the quote. The *id* can be found in *images/store.json.* |

#### Flags
| Flag(s) | Description |
| ----------- | ----------- |
| --Detach, -D | Respond to the original tweet and delete invoking mention |

## Setup

1. Create a Twitter app with read + write permissions.

2. Use pip to install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

1. Create a new .env file in the root.

2. Set these required variables inside it:

```
TWITTER_USERNAME=
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
```
3. Run the script
```
py .
```

## License

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

```
MIT License

Copyright (c) 2021 Husnain Javed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```