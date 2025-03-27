import numpy as np
import pytest
import pandas as pd

from tradingo import backtest

from tradingo.test.utils import close_position


def test_backtest_integration(benchmark, tradingo):

    bt = benchmark(
        backtest.backtest,
        bid="prices/close",
        ask="prices/close",
        dividends="prices/dividend",
        start_date=pd.Timestamp("2018-01-01 00:00:00+00:00"),
        end_date=pd.Timestamp.now("utc"),
        name="model",
        stage="raw.shares",
        config_name="test",
        provider="yfinance",
        universe="etfs",
        dry_run=True,
        arctic=tradingo,
    )


@pytest.mark.parametrize(
    "prices_,portfolio_,unrealised_pnl,realised_pnl",
    [
        (
            pd.DataFrame(
                1 + 0.01,
                index=pd.bdate_range("2020-01-01", periods=260, freq="B"),
                columns=["ABCD"],
            ).cumprod(),
            pd.DataFrame(
                1,
                index=pd.bdate_range("2020-01-01", periods=260, freq="B"),
                columns=["ABCD"],
            ).cumprod(),
            "(prices_*portfolio_).squeeze().diff()",
            "pd.Series(0.0, index=prices_.index)",
        ),
        (
            pd.DataFrame(
                1 + 0.01,
                index=pd.bdate_range("2020-01-01", periods=260, freq="B"),
                columns=["ABCD"],
            ).cumprod(),
            pd.DataFrame(
                range(0, 260),
                index=pd.bdate_range("2020-01-01", periods=260, freq="B"),
                columns=["ABCD"],
            ),
            "pd.Series([np.nan, np.nan, *(prices_.diff()*portfolio_.shift()).squeeze().iloc[2:]], index=prices_.index)",
            "pd.Series(0.0, index=prices_.index)",
        ),
        (
            pd.DataFrame(
                1 + 0.01,
                index=pd.bdate_range("2020-01-01", periods=260, freq="B"),
                columns=["ABCD"],
            ).cumprod(),
            close_position(
                pd.DataFrame(
                    1,
                    index=pd.bdate_range("2020-01-01", periods=260, freq="B"),
                    columns=["ABCD"],
                ).cumprod(),
            ),
            "pd.Series([*(prices_.diff()*portfolio_.shift()).squeeze().iloc[0:-1], np.nan], index=prices_.index)",
            "pd.Series([*(0 for _ in range(0, 259)), 12.280985478055433], index=prices_.index)",
        ),
    ],
)
def test_backtest_smoke(tradingo, prices_, portfolio_, unrealised_pnl, realised_pnl):

    dividends = pd.DataFrame(0, columns=prices_.columns, index=prices_.index)

    bt = backtest.backtest(
        portfolio=portfolio_,
        bid_close=prices_,
        ask_close=prices_,
        dividends=dividends,
        name="test",
        config_name="test",
        dry_run=True,
        start_date=portfolio_.index[0],
        end_date=portfolio_.index[-1],
        stage="raw",
        provider="yfinance",
        universe="etfs",
        arctic=tradingo,
    )

    actual_unrealised = bt["backtest/instrument.unrealised_pnl"].squeeze().diff()
    expected_unrealised = (
        eval(unrealised_pnl) if isinstance(unrealised_pnl, str) else unrealised_pnl
    )

    pd.testing.assert_series_equal(
        actual_unrealised,
        expected_unrealised.astype("float32"),
        check_names=False,
        check_freq=False,
        rtol=1e-4,
    )
    actual_realised = (
        bt["backtest/instrument.realised_pnl"].squeeze().diff().fillna(0.0)
    )
    expected_realised = (
        eval(realised_pnl) if isinstance(realised_pnl, str) else realised_pnl
    )
    pd.testing.assert_series_equal(
        actual_realised,
        expected_realised.astype("float32"),
        check_names=False,
        check_freq=False,
        rtol=1e-4,
    )


@pytest.mark.parametrize(
    "position, prices, unrealised_pnl, realised_pnl, total_pnl",
    (
        (
            pd.DataFrame(
                [0, 1, 1, 1, 0, 0],
                columns=["ABC"],
                index=pd.bdate_range("2024-11-24", periods=6),
            ),
            pd.DataFrame(
                [10, 10, 11, 12, 13, 14],
                columns=["ABC"],
                index=pd.bdate_range("2024-11-24", periods=6),
            ),
            pd.DataFrame(
                [np.nan, 0, 1, 2, np.nan, np.nan],
                columns=["ABC"],
                index=pd.bdate_range("2024-11-24", periods=6),
            ),
            pd.DataFrame(
                [0, 0, 0, 0, 3, 3],
                columns=["ABC"],
                index=pd.bdate_range("2024-11-24", periods=6),
            ),
            pd.DataFrame(
                [0, 0, 1, 2, 3, 3],
                columns=["ABC"],
                index=pd.bdate_range("2024-11-24", periods=6),
            ),
        ),
    ),
)
def test_backtest_all_closed(
    position,
    prices,
    unrealised_pnl,
    realised_pnl,
    total_pnl,
):
    bt = backtest.backtest(
        dry_run=True,
        portfolio=position,
        bid_close=prices,
        ask_close=prices,
        dividends=None,
        arctic="None",
    )

    pd.testing.assert_frame_equal(
        bt["backtest/instrument.unrealised_pnl"],
        unrealised_pnl,
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        bt["backtest/instrument.realised_pnl"],
        realised_pnl,
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        bt["backtest/instrument.total_pnl"],
        total_pnl,
        check_dtype=False,
    )


if __name__ == "__main__":
    pytest.main()
