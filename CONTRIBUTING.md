Clone/Fork the repo and run setup.py

    cd glustertool
    sudo python setup.py develop

Used "develop" instead of "install" for setup. With this setup the
changes made in repo will directly reflects when we run
`glustertool`. See
[here](http://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install)
for more details about `setup.py install vs develop`

### Adding new Tool

Adding tool is as simple as running one command!

    ./newtool hello

And run the tool using `glustertool hello`.

`newtool` is tool to generate tool, this command only to generate initial
code for the tool as required. Once created.

Above command generates a Python file called `hello.py` in
glustertool/plugins directory. hello.py will have two functions
definitions pre populated, add your stuff and complete the tool.

function cmdargs receives a parser object, which is a `argparse`
object. Add your arguments to the parser using `parser.add_argument`.
For example, if your tool accepts a positional parameter and a
optional parameter then,

    def cmdargs(parser):
        parser.add_argument("name", help="Your Name")
        parser.add_argument("--email", help="Your Email")

And implement the `run` function by using the `args`.

    def run(args):
        print ("Hello %s" % args.name)
        if args.email:
            print ("Your email is %s" % args.email)

Read [here](http://docs.python.org/2/library/argparse.html) for more
details about Python argparse library.

If your tool is having more than one Python files then create it as
module instead of single python file.

    ./newtool hello2 --type pymodule

It will create the directory inside plugins directory as shown below.

    glustertool/plugins
        - hello2/
            - __init__.py

What if it is not the Python tool?

We have a solution for such tools too. Create your tool with
`--type=exec` and specify the `--bin` and `--prog`.

Where bin is the path of binary relative to the plugins directory and
prog is name of program which is used to execute the script. Leave it
blank if the script/binary can be executed without any prefix.

For example, if you want to add myscript.sh as a tool then,

    ./newtool myscript --type=exec --bin=myscript.sh --prog=bash

If you make myscript.sh as executable(`chmod +x myscript.sh`) then,

    ./newtool myscript --type=exec --bin=myscript.sh

Once the above command is run, copy your script to
`glustertool/plugins/myscript` directory.

Above command creates a directory for your tool inside plugins
directory and also adds two files `doc.txt` and `tool.json`. Add your
tool documentation in doc.txt.

`tool.json` will have two keys `bin` and `prog`. Example,

    {
        "bin": "myscript.sh", 
        "prog": "bash"
    }


## Utilities libraries

If you are writing the plugin using Python language then you can
use the utility functions provided by the glustertool.

For example, if you want to use CliTable library then just import and
use it inside your tool.

    from glustertool.utils import clitable

For Examples refer `examples/` directory.


**Submit pull request with your tool!**
