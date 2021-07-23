import xtract_python_getter as xpg

get = xpg.Getter(owner='edeng23', repo='binance-trade-bot')
get.direc = 'tests/test_files/binance_trade_bot/'
get.token='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'

last_commit_sha = get.get_last_commit_sha()
print(last_commit_sha)
# python_paths = get.get_all_python_files(last_commit_sha)
# get.get_content(python_paths)
