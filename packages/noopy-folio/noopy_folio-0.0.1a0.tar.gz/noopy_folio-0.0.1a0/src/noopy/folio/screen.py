"""Stock Screener

"""
import logging
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import Normalizer, MinMaxScaler
from sklearn.neighbors import LocalOutlierFactor


_LOGGER = logging.getLogger("noofolio")


class Screener(object):
    def __init__(self, data=None, path=None) -> None:
        self._rates = None
        self._data = data
        pass

    def run(self):
        if self._rates:
            return self._rates

        data = self._data
        feature_summary = pd.concat(
            [data.dtypes, data.nunique() / data.notna().sum()],
            axis=1,
            keys=["dtypes", "nunique"],
        )
        feature_summary["nnan"] = data.isna().sum() / data.shape[0]
        feature_summary["numeric?"] = np.where(
            (feature_summary["nunique"] > 0.5)
            & (feature_summary["dtypes"] == "float64"),
            True,
            False,
        )
        # feature_summary.loc["stats_peg", "numeric?"] = True
        feature_summary.loc["stats_roe", "numeric?"] = True
        feature_summary.loc["stats_roa", "numeric?"] = True
        data_cleaned = data.copy()
        # remove delisted firms
        data_cleaned = data_cleaned[data_cleaned["delisted"] == False]

        # remove stats_roe == -99999.99
        data_cleaned[data_cleaned["stats_roe"] == -99999.99] = np.nan
        # remove stats_roe == 0.0
        data_cleaned[data_cleaned["stats_roe"] == 0.0] = np.nan
        # remove stats_roa == 0.0
        data_cleaned[data_cleaned["stats_roa"] == 0.0] = np.nan
        # remove pnl_grossmargin == inf or -inf
        data_cleaned[abs(data_cleaned["pnl_grossmargin"]) == np.inf] = np.nan

        # # only take fundamentals within 360 days asofdate
        # data_cleaned = data_cleaned[
        #     pd.to_datetime(data_cleaned["fundamental_date"]) + dt.timedelta(days=360)
        #     > as_of_date
        # ]

        nonan_data = data_cleaned[
            list(feature_summary[feature_summary["numeric?"] == True].index)
        ].copy()
        nonan_data["ticker"] = data_cleaned["ticker"] + "." + data_cleaned["exchange"]
        nonan_data.dropna(inplace=True)

        # normalizing
        normlizer = Normalizer()
        cf_columns = ["cf_operating", "cf_investing", "cf_financing"]
        cf_transformed = normlizer.fit_transform(nonan_data[cf_columns])
        x_train = nonan_data[
            feature_summary[feature_summary["numeric?"] == True].index
        ].copy()
        x_train[cf_columns] = cf_transformed

        # scaling
        columns_to_scale = [
            c for c in x_train.columns if "bs_" in c or "pnl_" in c or "stats_" in c
        ]
        desc = x_train.describe()
        for c in columns_to_scale:
            mini = desc.loc["min", c]
            maxi = desc.loc["max", c]
            scaler = MinMaxScaler((0.01, maxi - mini + 0.01))
            transformed = scaler.fit_transform(x_train[c].values.reshape(-1, 1))
            x_train.loc[:, c] = transformed
        # x_train["bs_leverage"] = stats.boxcox(x_train["bs_leverage"])[0]
        # x_train["stats_ep"] = stats.boxcox(x_train["stats_ep"])[0]
        # x_train["stats_roe"] = stats.boxcox(x_train["stats_roe"])[0]
        # x_train["stats_bp"] = stats.boxcox(x_train["stats_bp"])[0]
        scaler = MinMaxScaler((0, 1))
        x_train[x_train.columns] = scaler.fit_transform(x_train)

        # outlier detection
        outlier_detector = LocalOutlierFactor()
        y_train_predict = outlier_detector.fit_predict(x_train)

        return list(nonan_data.ticker.iloc[np.where(y_train_predict == -1)])
