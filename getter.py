import xtract_python_getter as xpg

test = xpg.Getter(owner='edeng23', repo='binance-trade-bot', direc='test_files/binance_trade_bot/', token='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')
last_commit_sha = test.get_last_commit_sha()
print(type(last_commit_sha))
# python_paths = test.get_all_python_files(last_commit_sha)
# test.get_content(python_paths)
