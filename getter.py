import xtract_python_getter as xpg

get = xpg.Getter(owner='edeng23', repo='binance-trade-bot')
get.direc='tests/test_files/binance_trade_bot/'
get.token='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'

last_commit_sha = get.get_last_commit_sha()
if not isinstance(last_commit_sha, dict):
    exit
python_paths = get.get_all_python_files(last_commit_sha)
get.get_content(python_paths)
