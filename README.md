# zuul_secrets

How to deal with secrets in zuul

## Requirements before starting

1. Install the [zuul-client](https://zuul-ci.org/docs/zuul-client/installation.html#via-the-python-package-index-pypi)
2. If you haven't done it already, configure authentication on your zuul server.
   E.g. place this code snippet in your _zuul.conf_ file, while adopting the values:

```ini
[auth zuul_operator]
driver=HS256
allow_authz_override=true
realm=zuul.example.com
client_id=zuul.example.com
issuer_id=zuul_operator
secret=some_long_random_string
```

## Using the script

1. Have a close look at the _config.yaml.example_ file.
   It contains all required variables with comments.
   Copy it to _config.yaml_ before proceeding.
2. Run the script: `python3 script.py`
3. Place the generated output yaml code inside the respective zuul files in your repository where you need the secret. The output might look like this:

```yaml
- secret:
    name: zuul_secrets
    data:
      some_password: !encrypted/pkcs1-oaep
        - XGRgRxKQpPd6SfrFstFr4hnoxzN3r4EJjKqtZ69OhoJ90uI7jhnw176JiUJUlyh5Xu6ow
          GLtK2zG2pyEmWVZeYkkV+BwPHCjvXQg3unTDxl5khLAsl8Vug6AV9iwpm6qN6J5Z6Iql+
          a+zabygsX6TSlPUzx4OLSea29K1+ob7YxHvMOgEXTuytm+hZ8/dnZY5d9sLX+2DGbfNjG
          IvJNzXw82aysVtM/mkQjQu/JErycuf6xoB6DBizMArh+Qo67hOo9s48S02KXaNYj6ob0e
          u4yqwYzMjjIGFwfAvn84V3BOusE/WC0Bm//Xz9wbg+dBF5/K/otLePtC5ZhHKLA8GnQIA
          8SkMoImaCz56WaxObKOkcUkDIl9on7h72cSmizOjdJRb8tHMjnwkz6iV+ejkDRSB0ymFd
          p9BzBJK4gGZ1RfIF+tEmj1jc5w8+VPg17rSsnuB0qlgA/88e/k55AgkYmGk6kn889HhVJ
          jOHUrYL3eKlv7fCT6kkK5vIecu3tLxcMQS0MnZETJNszlrcIQWRBarf2K0viw83YfZgTJ
          SSJvtasw5aXgeMnz9gwCDSXr1S4VvAtqlo1ijGGp1m80cV5FZBNTHqoQWjg+9R1hLaTOS
          X/gusGlyK5ZcjOqNSDhW7MrzqhoD/OH0EzBeKNJdUyVINTUhhOFTFA8TFrpcsY=
```

## Caveats

Secrets must not be longer than 3760 bits. Have a look [here](https://zuul-ci.org/docs/zuul/latest/project-config.html#encryption) if your secrets exceeds 3760 bits of length.
