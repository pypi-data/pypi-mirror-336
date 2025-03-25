
import os
import pathlib
import numpy as np
import windrose as wr
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from multiprocessing import Pool
from metpy.calc import wind_speed, wind_direction
from datetime import datetime
from typing import Literal, Optional
from collections.abc import Iterable

from ..queryreport import print_text
from ..utilities import nice_round_up
from .met import NetcdfMet

iVector = Iterable[list[int]]
fVector = Iterable[list[float]]
sVector = Iterable[list[str]]

seasonDict = dict[str,iVector]
seasonList = list[seasonDict]

_ENSEMBLE_TYPES = Literal["randomize", "sequential"]

class MetRepo:
    """
    A class to access a repository of netcdf met data.
    The repository is assumed to be a directory containing netcdf files in the form
    YYYYMM.nc
    with each file containing met data on pressure levels over days, hours, latitude and longitude

    """
    _lat = float
    _lon = float

    _dirc = str
    _filetype = str
    _files = sVector
    _years = iVector
    _months = iVector
    _days = iVector
    _hours = iVector

    _seasons = seasonList
    _seasons_combine = str

    def __init__(self, dirc: str, lat: float, lon: float, filetype: Literal["nc","grib"]="nc"):
        """
        Initialize a MetRepo instance

        :param dirc: path to met data repository
        :type dirc: str
        :param lat: latitude 
        :type lat: float
        :param lon: _description_
        :type lon: float
        :param filetype: _description_, defaults to "nc"
        :type filetype: Literal[&quot;nc&quot;,&quot;grib&quot;], optional
        :raises RuntimeError: if dirc is not a directory or is not found
        """

        if not os.path.isdir(dirc):
            raise RuntimeError('{dirc} is not a directory or not found')
        
        self._lat = lat
        self._lon = lon

        self._dirc = dirc
        self._filetype = filetype

        self._files = [file.stem for file in sorted(pathlib.Path(self.dirc).glob(f"*.{filetype}"))]

        self._years = []
        self._months = []
        self._days = []
        self._hours = []

        self._seasons = []
        self._seasons_combine = 'first'

    @property
    def latitude(self):
        return self._lat
    
    @property
    def longitude(self):
        return self._lon
    
    @property
    def years_available(self) -> set[int]:
        return set(sorted([int(f[:4]) for f in self._files]))
    
    @property
    def months_available(self) -> set[int]:
        return set(sorted([int(f[4:6]) for f in self._files]))

    @property
    def dirc(self):
        return self._dirc
    
    @property
    def years(self):
        return self._years

    @years.setter
    def years(self, yr: list[int]):
        self._years = yr

    @property
    def months(self):
        return self._months
    
    @months.setter
    def months(self, mnths: list[int]):
        self._months = mnths

    @property
    def days(self):
        return self._days
    
    @days.setter
    def days(self, d):
        self._days = d

    @property
    def hours(self):
        return self._hours
    
    @hours.setter
    def hours(self, hrs: list[int]):
        self._hours = hrs

    @property
    def seasons(self):
        return self._seasons
    
    @seasons.setter
    def seasons(self, season_list: list[dict[str,list[int]]], combine='first'):
        self._seasons = season_list
        self._seasons_combine = combine

    def add_season(self, name: str, months: list[int]):
        self._seasons.append(
            {'name':name,
             'months': sorted(months)}
        )

    @property
    def season_names(self):
        return [s['name'] for s in self.seasons]

    @property
    def dataframe(self):
        return self._dataframe

    def retrieve(self, N: int, method: _ENSEMBLE_TYPES='randomize', processes=1):

        if not self.years:
            years = list(self.years_available)
        else:
            years = [y for y in self.years if y in self.years_available]
            skipped_years = [y for y in self.years if y not in years]
            if skipped_years:
                print_text(f"skipping years {[print(y) for y in skipped_years]}")
        
        if not self.months:
            months = list(self.months_available)
        else:
            months = [m for m in self.months if m in self.months_available]
            skipped_months = [m for m in self.months if m not in months]
            if skipped_months:
                print_text(f"skipping months {[print(m) for m in skipped_months]}")

        if not self.days: # No days are set
            self.days = [d for d in range(1,32)]

        if not self.hours:
            self.hours = [0]

        datetimes = []
        for j in range(N):
            match method:
                case 'randomize':
                    year = random.choice(years)
                    month = random.choice(months)
                    if month==2:
                        day = random.choice(self.days[:28])
                    elif month in [4,6,9,11]:
                        day = random.choice(self.days[:-2])
                    else:
                        day = random.choice(self.days)
                    hour = random.choice(self.hours)
                case 'sequential':
                    year = years
            datetimes.append(datetime.fromisoformat(f"{year:04d}{month:02d}{day:02d} {hour:02d}00"))

        out = []
        pool = Pool(processes=processes)
        out = pool.map(self._build_met_list, datetimes)
        out = [x for sublist in out for x in sublist]

        met_data = pd.concat(out, ignore_index=True)

        self._apply_seasons_to_dataframe(met_data)

        return met_data


    def _apply_seasons_to_dataframe(self, df):        
        if len(self._seasons)>0:
            df['season'] = df.apply(lambda x: self._get_seasons(x), axis=1)
        return df
    
    def _get_seasons(self, x: pd.core.series.Series, method: Literal['combine','first']='combine'):
        xx = [s['name'] for s in self.seasons if x['month'] in s['months']]
        if xx:
            if method=='combine':
                return ' & '.join(xx)
            else:
                return xx[0]
        else:
            return 'other'
    

    def _build_met_list(self, dt: datetime) -> list[pd.DataFrame]:
        out = []
        this_met = self._get_met_as_df(dt)
        out.append(this_met)
        return out


    def _get_met_as_df(self, dt: datetime) -> pd.DataFrame:
        filename = f"{dt.year:04d}{dt.month:02d}.{self._filetype}"
        met = NetcdfMet(os.path.join(self._dirc,filename))
        met.extract(self.latitude, self.longitude, dt, convention="to")
        met_df = pd.DataFrame(columns=(
            'year',
            'month',
            'day',
            'hour',
            'altitude',
            'pressure',
            'temperature',
            'relative_humidity',
            'density',
            'wind_u',
            'wind_v',
            'wind_speed',
            'wind_direction'))
        met_df.loc[0,'year'] = dt.year
        met_df.loc[0,'month'] = dt.month
        met_df.loc[0,'day'] = dt.day
        met_df.loc[0,'hour'] = dt.hour
        met_df.loc[0,'altitude'] = met.altitude
        met_df.loc[0,'pressure'] = met.pressure
        met_df.loc[0,'temperature'] = met.temperature
        met_df.loc[0,'relative_humidity'] = met.relhum
        met_df.loc[0,'density'] = met.density
        met_df.loc[0,'wind_u'] = met.wind_U
        met_df.loc[0,'wind_v'] = met.wind_V
        met_df.loc[0,'wind_speed'] = met.wind_speed
        met_df.loc[0,'wind_direction'] = met.wind_direction
        met.close()
        return met_df


def _plot_windrose_subplots(data, *, direction, var, color=None, **kwargs):
    """wrapper function to create subplots per axis"""
    ax = plt.gca()
    ax = wr.WindroseAxes.from_ax(ax=ax)
    wr.plot_windrose(direction_or_df=data[direction], var=data[var], ax=ax, **kwargs)



def plot_windroses(data: MetRepo | pd.DataFrame, altitudes: list[float], 
                   N: int=1000, 
                   title: Optional[str]=None,
                   row: Optional[str]='altitude',
                   col: Optional[int]=None,
                   col_order: Optional[list[str]]=None,
                   include_all: bool=True,
                   method: _ENSEMBLE_TYPES='randomize', 
                   isblowto: bool=True,
                   processes=1):

    if isinstance(data, MetRepo):
        dataset = data.retrieve(N, method=method, processes=processes)
    elif isinstance(data, pd.DataFrame):
        dataset = data.copy()
    else:
        raise ValueError('plot_windroses data should be either MetRepo or pandas.DataFrame')
    
    df = pd.DataFrame(columns=('altitude','speed','direction'))
    for alt in altitudes:

        dataset[f'wind speed at {alt} m'] = dataset.apply(lambda x: np.interp(alt,x['altitude'],x['wind_speed']), axis=1)
        dataset[f'wind direction at {alt} m'] = dataset.apply(lambda x: np.interp(alt,x['altitude'],x['wind_direction']), axis=1)

        this_df = pd.DataFrame(columns=('altitude','speed','direction'))
        this_df['speed'] = dataset[f'wind speed at {alt} m']
        this_df['direction'] = dataset[f'wind direction at {alt} m']
        this_df['altitude'] = alt
        if col is not None:
            this_df[col] = dataset[col]

        if len(df)==0:
            df = this_df.copy()
        else:
            df = pd.concat([df, this_df], ignore_index=True)

    if include_all:
        df1 = df.copy()
        df1[col] = 'all'

        df = pd.concat([df,df1])

    max_spd = df.apply(lambda x: np.max(x['speed']), axis=1).max()
    spd_bins = [0.1] + np.linspace(1,max_spd,5).tolist()

    g = sns.FacetGrid(
        data=df,
        row=row,
        col=col,
        col_order=col_order,
        subplot_kws={"projection":"windrose"},
        sharex=False,
        sharey=False,
        despine=False,
        height=3.5,
    )

    g.map_dataframe(
        _plot_windrose_subplots,
        direction="direction",
        var="speed",
        normed=True,
        calm_limit=0.1,
        kind="bar",
        opening=1.0,
        bins=spd_bins,
        blowto=not isblowto,
        # edgecolor='k',
    )

    rows = df[row].unique()
    if col_order is not None:
        cols = col_order
    else:
        cols = df[col].unique()

    g.set_titles(template='')

    if col is not None:
        for ax, c in zip(g.axes[0], cols):
            c_title = f"{col}: {c}"
            ax.annotate(c_title, xy=(0.5,1), 
                        xytext=(0,5), 
                        xycoords='axes fraction', 
                        textcoords='offset points', 
                        ha='center', 
                        va='baseline',
                        size='large')

    for ax, r in zip(g.axes[:,0], rows):
        if row=='altitude':
            r_title = f"{row} = {r} m"
        else:
            r_title = f"{row}: {r}"
        ax.annotate(r_title, xy=(0,0.5), 
                    xytext=(-ax.yaxis.labelpad - 5,0), 
                    xycoords=ax.yaxis.label, 
                    textcoords='offset points', 
                    ha='right',
                    va='center',
                    size='large',
                    rotation=90)


    # if row is not None:
    #     if col=='altitude':
    #         g.set_titles(template="{col_name} m")
    #     elif row=='altitude':
    #         g.set_titles(template="{row_name} m")
    g.set_xticklabels([])
    max_wd_freq = 0 
    for ax in g.axes.flatten():
        table = ax._info["table"]
        wd_freq = np.sum(table, axis=0)
        max_wd_freq = np.maximum(max_wd_freq, np.amax(wd_freq))
    
    freq_ticks = np.linspace(0,np.ceil(max_wd_freq/5)*5,6, dtype=int)
    freq_ticks = freq_ticks[1:]
    for ax in g.axes.flatten():
        # title = ax.get_title()
        # ax.set_title('')
        # ax.set_title(title, loc='left')
        # dirc_label = ax.get_xticklabels()
        ax.set_rgrids(freq_ticks, freq_ticks)
        ax.set(rlabel_position=-90)
        ax.tick_params(axis='both', labelsize=8, pad=0)
        

    g.axes.flatten()[-1].set_legend(ncols=1, bbox_to_anchor=(1.1,1,0.1,0.5), title='Wind speed (m/s)')
    for l in g.axes.flatten()[-1].get_legend().texts:
        lt = l.get_text()
        lt = lt.replace('[','')
        lt = lt.replace(')','')
        lt = lt.replace(':',u'\u2014')
        l.set_text(lt)

    fig = plt.gcf()
    fig.subplots_adjust(right=0.8, wspace=0.1, hspace=0.1)

    return fig, g



