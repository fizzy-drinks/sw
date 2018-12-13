# sw

sw is a super simple SSH wallet for your servers!

## Installation

Simply install `sw-cli` from the PyPI.

```bash
pip install sw-cli
```

## Usage

You can add however many ssh servers to your wallet you like. To this, simply run

```bash
sw add production user@12.345.67.89
```

And then connect to `production` with

```bash
sw connect production
```

### Listing registered servers

```bash
sw list
```

### Removing servers

To remove a server, run `sw remove SERVER_LABEL` like:

```bash
sw remove production
```

### Renaming servers

To rename a server, run `sw rename OLD_NAME NEW_NAME`:

```bash
sw rename production prod
sw connect prod # success!
```

### Exporting your wallet

Export your wallet to JSON and share it with co-workers, store it in cloud, etc.

```bash
sw export > wallet.json
```

### Importing a wallet

Importing a wallet adds the keys from an exported JSON file to your current wallet.

**Important:**  if both wallets have definitions for a given server name, the old
one is going to be overridden!

```bash
sw import wallet.json
```
