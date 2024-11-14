# Vine App

Opinionated application that demonstrates how to quickly build applications on top of Serra Vine.

A Serra Vine application:

- grows on what is already there
- gives back and supports growth of other applications
- is easy to cultivate

## Getting started

Note: we have to refine this section.

Fork the repository and then [detach it](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/detaching-a-fork).

Rename your app.

## Container Usage

The application is available as a Docker container:

```bash
docker pull ghcr.io/serraict/vine-app:latest
```

For detailed instructions on using the container, including environment variables, cron jobs, and deployment examples, see the [Container Documentation](docs/container.md).

## CLI Usage

The application provides a command-line interface. To see available commands:

```bash
cliapp --help
```

Example - display application information:

```bash
cliapp about
```

## Stack

Python application built on FastAPI, Typer and NiceGUI,
that allows you to quickly build command line applications, web applications and REST/RPC APIs.
