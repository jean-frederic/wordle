import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() in ('--cli', '-c', 'cli'):
        import cli
        cli.main()
    else:
        import web_server
        web_server.start_server(open_browser=True)
