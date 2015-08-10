#Template Client Tier

This is a template client tier for a sample Braiiin application. All application
client tiers should follow the format specified in this template, unless otherwise
stated.

## Getting Started

Here is how to setup a local instance.

1. Duplicate, not fork, this repository as `[app]-client`, and clone it.
2. Check that needed commands are accessible `source check.sh`.
3. Install `source install.sh`.
4. Run server `source activate.sh`.
5. Browse [Client Core Documentation](http://client-braiiin.readthedocs.org). (coming soon)
6. Read the [Guidelines](#guidelines) below.
7. If you are uncertain of where to start, see [How to get Working](#how-to-get-working) below.

> To update your installation of the client core, use:
 1. `git submodule foreach git reset head --hard` to remove any inadvertent changes.
 2. `git submodule foreach git pull origin master` to update the submodules.

## Guidelines

1. It is safer not to modify the core `client` submodule, which is located in the 
`client` directory from this repository. If you wish to make edits, clone the `client`
repository and make edits there.
2. Make all edits in a new branch. After creating a branch, immediately create 
a Pull Request (PR), but include `[do not merge]` in the title, so that your 
teammates can comment and collaborate on the branch.
3. Once the branch is ready, remove `[do not merge]` and alert your code partner
that it is ready for code review.
4. Do not merge your own PRs, unless it is a critical bug fix and all tests pass.
5. Conform to PEP style guidelines.
6. Rename the "template" folder in this repository's root to your application's
name.

## How It Works

**High-Level Overview**

The client core is responsible for making API calls and authenticating requests.
Each Braiiin client tier simply treats the core as a distinct, independent 
library and (1) handles user flow (redirects, template rendering, error display)
and (2) renders pages using statics and templates.

**Detailed Explanation**

This tier is quite simply a Flask application, except with a custom API instead 
of a datastore. For a primer, see [Flask documentation](http://flask.pocoo.org).

To begin, the `run.py` file, in the repository root directory, creates an instance
of the app, and then runs it. This app is defined in `template_client/__init__.py`. In
that file, a number of items are necessary for this to function:

1. Updating `sys.path` with the logic directory. This allows your application to
access the logic core as a module named `logic`.
2. In `create_template_app`, it is necessary to import views *after* the app
is instantiated.
3. In `created_template_app`, it is necessary to invoke `app.register_blueprints`
after importing the file that registers your APIs.

In the `template_client/views.py` file, "views" define output for a specific or
a set of URLs. Those URLs may inject Python values into an HTML template, using
a powerful templating language, called [Jinja](http://jinja.pocoo.org).

All objects have five default operations, matching default objects in the
logic tier: `post` (create), `get`, `put` (update), `delete`, and `get_or_create`.
Note that `get_or_create` takes only one API call.

##How to get Working

If all of the above is confusing, then simply respect the application's
abstractions and know the following. These should compartmentalize the
application enough, so that you don't need to know how the rest of it works.

1. Create a view in `view.py` with the right decorator.
2. Create a new object in `libs/sample.py` that extends `Entity`.
3. Import, instantiate and save your object.
4. Return a stringified version of your object.
5. Finally, access the URL specified for your view.