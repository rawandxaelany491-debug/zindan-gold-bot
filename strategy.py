from dataclasses import dataclass


@dataclass
class ChartData:
    trend: str
    support: str
    resistance: str
    breakout: str
    pullback: str
    sideway: str
    structure: str


class ZendanStrategy:

    def __init__(self):
        self.name = "Zendan Strategy"


    def analyze(self, data: ChartData):

        if data.sideway.lower() == "yes":
            return {
                "signal": "NO TRADE",
                "reason": "Market is sideways"
            }


        if (
            data.trend.lower() == "up"
            and data.breakout.lower() == "yes"
            and data.pullback.lower() == "yes"
        ):
            return {
                "signal": "BUY",
                "reason": (
                    "Uptrend + Breakout + Pullback confirmation"
                )
            }


        if (
            data.trend.lower() == "down"
            and data.breakout.lower() == "yes"
            and data.pullback.lower() == "yes"
        ):
            return {
                "signal": "SELL",
                "reason": (
                    "Downtrend + Breakout + Pullback confirmation"
                )
            }


        return {
            "signal": "NO TRADE",
            "reason": "Conditions not completed"
        }
            def check_breakout_confirmation(self, candle_close_percent: float):

        if candle_close_percent >= 75:
            return True

        return False


    def check_inversion(self, old_level: str, new_level: str):

        if (
            old_level == "resistance"
            and new_level == "support"
        ):
            return True

        if (
            old_level == "support"
            and new_level == "resistance"
        ):
            return True

        return False


    def get_full_signal(
        self,
        trend,
        breakout_confirmed,
        pullback_confirmed,
        sideway
    ):

        if sideway:
            return {
                "signal": "NO TRADE",
                "reason": "Sideway market"
            }


        if (
            trend == "up"
            and breakout_confirmed
            and pullback_confirmed
        ):
            return {
                "signal": "BUY",
                "reason": "Zendan rules confirmed"
            }


        if (
            trend == "down"
            and breakout_confirmed
            and pullback_confirmed
        ):
            return {
                "signal": "SELL",
                "reason": "Zendan rules confirmed"
            }


        return {
            "signal": "NO TRADE",
            "reason": "Waiting for confirmation"
        }
        def normalize_value(value: str):

    if not value:
        return "unknown"

    return (
        value
        .strip()
        .lower()
        .replace(" ", "")
    )


def create_chart_data(
    trend,
    support,
    resistance,
    breakout,
    pullback,
    sideway,
    structure
):

    return ChartData(
        trend=normalize_value(trend),
        support=normalize_value(support),
        resistance=normalize_value(resistance),
        breakout=normalize_value(breakout),
        pullback=normalize_value(pullback),
        sideway=normalize_value(sideway),
        structure=normalize_value(structure)
    )


def run_zendan_strategy(chart_info):

    strategy = ZendanStrategy()

    result = strategy.analyze(
        chart_info
    )

    return result
    def format_signal(result):

    signal = result.get(
        "signal",
        "NO TRADE"
    )

    reason = result.get(
        "reason",
        "No reason provided"
    )


    if signal == "BUY":

        return (
            "🟢 SIGNAL: BUY\n\n"
            f"Reason: {reason}"
        )


    if signal == "SELL":

        return (
            "🔴 SIGNAL: SELL\n\n"
            f"Reason: {reason}"
        )


    return (
        "⚪ SIGNAL: NO TRADE\n\n"
        f"Reason: {reason}"
    )
    def test_strategy():

    sample_data = create_chart_data(
        trend="up",
        support="confirmed",
        resistance="broken",
        breakout="yes",
        pullback="yes",
        sideway="no",
        structure="higher highs"
    )

    result = run_zendan_strategy(
        sample_data
    )

    return format_signal(result)
    
        
