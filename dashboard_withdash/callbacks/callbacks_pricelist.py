import sys

from app import application, db, User, TrackStation

from dash.dependencies import Input, Output, State
import pandas as pd


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
        return 'any'

    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime'
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@application.callback(
[
    Output("price_datatable", "data"),
    Output("price_datatable", "columns")
],
[
    Input("interval_updateprices", "n_intervals"),
    Input('price_datatable', "page_current"),
    Input('price_datatable', "page_size"),
    Input('price_datatable', 'sort_by'),
    Input('price_datatable', 'filter_query'),
    State('userlogged', 'data')
]
)
def retrieve_allstations(n, page_current, page_size, sort_by, filter, data):
    username = data['username']
    if not username is None:
        db_none = pd.DataFrame(
        {
        'id': [],
        'ville': [],
        'address': [],
        'zipcode': [],
        'SP95': [],
        'SP98': [],
        'E10': [],
        'E85': [],
        'GPLC': [],
        'GAZOLE': [],
        })
        # id list to track
        liststation_user = User.query.filter_by(name=username).first()
        tracks = TrackStation.query.filter_by(user_id=liststation_user.id).all()
        if tracks is None:
            db_data = None
        else:
            id_list = tuple([track.station_id for track in tracks])
            with db.get_engine().connect() as dbconn, dbconn.begin():
                db_data = pd.read_sql(f'SELECT id, ville, address, zipcode,\
             SP95, SP98, E10, E85, GPLC, GAZOLE FROM station WHERE id IN {id_list}', dbconn)
            db_data.columns = db_none.columns
        if db_data is None:
            db_data = db_none
        else:
            db_data = db_data.astype(dtype={
                'ville': 'string',
                'address': 'string',
                'zipcode': 'string',
                'SP95': 'string',
                'E10': 'string',
                'SP98': 'string',
                'E85': 'string',
                'GPLC': 'string',
                'GAZOLE': 'string'
            })
        filtering_expressions = filter.split(' && ')
        dff = db_data
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):  #and col_name != "recommendation":
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        if len(sort_by):
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        page = page_current
        size = page_size
        classical_columns = [
            'ville',
            'address',
            'zipcode',
            'SP95',
            'E10',
            'SP98',
            'E85',
            'GPLC',
            'GAZOLE'
        ]
        columns = [{
                    'id': c,
                    'name': c,
                    'type': table_type(db_data[c])
                } for c in classical_columns
                ]
        data = dff.iloc[page * size: (page + 1) * size].to_dict('records')
        return data, columns
