# Discord-Token-Joiner

![preview](preview.png)

Python script that takes a list of Discord account tokens and joins them to a server using an invite link.

## Setup

```bash
git clone git@github.com:NoTinyxd/Discord-Token-Joiner.git
cd Discord-Token-Joiner
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Put your tokens in `Input/tokens.txt`, one per line.
2. Run the script:

```bash
python main.py
```

3. Tokens that work get saved to `valid.txt`.

## Disclaimer

Only use this with accounts you own. Automating user accounts breaks Discord's Terms of Service, so you can get accounts banned. Use at your own risk, I'm not responsible for what happens to your accounts.

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Free for personal and noncommercial use. You can't sell it or use it commercially, and you have to keep the copyright notice.

Required Notice: Copyright (c) 2026 NoTinyxd (https://github.com/NoTinyxd)
