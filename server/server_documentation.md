# ScratchNLP Application Programming Interface (API)
ScratchNLP provides a framework for someone to create [Scratch](http://scratch.mit.edu/) programs by providing a series of natural language instructions that get translated into the internal representation of [Scratch 2.0](https://en.scratch-wiki.info/wiki/Scratch_2.0) projects. Programs that wish to access ScratchNLP functionality programmaticaly may use this API.

TODO(tquach): Implement/change specification "The ScratchNLP API uses JSON as its communication format, and standard HTTP methods like GET, PUT, POST and DELETE."

## Getting Started
The ScratchNLP Server maintains a database of projects and is implemented as a Flask application.

### API Endpoints
| Endpoint | Description |
| --- | --- |
| `/project/<project_name>` | Get information about the entire project |
| `/project/<project_name>/script/<raw_instruction>` | Create or update a specific project with an instruction |
| `/allprojects` | Get list of all projects |
| `/translate/<instruction>` | Get Scratch 2.0 nested array representation of the instruction |

## Example of Creating a Project
Using the API, you may want to build up a project in the database by providing each raw_instruction to add to the program. Alternatively, You may want to manage the program state and development on the client side. In this case, you would make individual queries to the translate API endpoint and have an own method of bringing those results together into a cohesive program.







