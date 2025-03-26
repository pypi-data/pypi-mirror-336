# Run DMARC Milter with Postfix

## Steps

1. Install pydmarc, e.g. like this from sources:

   ```console
   $ git clone https://gitlab.com/duobradovic/pydmarc.git
   $ cd pydmarc

   # N.B. You may want to create and activate a Python virtualenv at this point.

   # This installs the package at the current location (`.`) with the `milter` option
   # to indicate extra dependencies to be installed.
   $ python -m pip install -e .[milter]
   ```

2. Run `dmarc.milter` module, bound to the loopback interface.

   ```console
   $ python -m dmarc.milter \
       --bind-host 127.0.0.1 \
       --bind-port 9000 \
       --log-level=INFO
   ```
  
   💡 Add `--config-file` parameter to load configuration file,
   see -- [`conf/`](conf/dmarcmilter.toml).
   
   💡 Change `--log-level=INFO` to `--log-level=DEBUG` and be ready to get a lot of
   output, perhaps relevant when testing.

2. Configure a Postfix instance.

   ```console
   $ postconf -e 'smtpd_milters = inet:127.0.0.1:9000'
   ```
