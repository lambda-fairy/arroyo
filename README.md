# Liana, the webhook handler

Liana is a server that accepts [GitHub webhooks].

[GitHub webhooks]: https://developer.github.com/webhooks/


## Dependencies

+ Python 3.3 or newer

+ Linux


## Setting up

1.  Start the daemon

        $ ./liana.py
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
        Added myname/myrepo to /srv/liana/secrets

4.  Tell GitHub about your hook


## systemd

A sample systemd unit file is provided in `liana.service`.


## Etymology

[Lianas] are long-stemmed, woody vines that grow by wrapping themselves
around neighboring trees.

[Lianas]: https://en.wikipedia.org/wiki/Liana


## License

AGPL version 3 or newer.
