# Arroyo, the webhook handler

Arroyo is a server that accepts [GitHub webhooks].

[GitHub webhooks]: https://developer.github.com/webhooks/


## Dependencies

+ Python 3.3 or newer

+ Linux


## Setting up

1.  Start the daemon

        $ ./arroyo.py
        Started server on :8144
        Started worker thread

2.  Create a handler script

        $ mkdir -p scripts/myname
        $ cat >scripts/myname/myrepo <<EOF
        #!/bin/sh
        echo 'Hello, world!'
        EOF
        $ chmod +x scripts/myname/myrepo

3.  Generate a secret key

        $ ./add-secret myname/myrepo
        Added myname/myrepo to /srv/arroyo/secrets

4.  Tell GitHub about your hook


## systemd and Upstart

A sample systemd unit file is provided in `arroyo.service`.

A sample Upstart job file is provided in `arroyo.conf`.


## License

AGPL version 3 or newer.
